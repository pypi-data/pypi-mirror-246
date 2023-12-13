"""
Script for estimating the h-Q relationship 
from a given profile (according to GMS). 

The object 'Profile' stores the hydraulic data as 
a pandas.DataFrame and creates a complete diagram 
with the .plot() method.

Run script along with the following files to test:
    - profile.csv
    - closedProfile.csv
It will plot two diagrams with :
    - Limits enclosing the problem
    - The water_depth-discharge relation
    - The water_depth-critical_discharge relation
"""
from typing import Iterable, Tuple
from pathlib import Path
from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import pandas as pd
import numpy as np


g = 9.81


def GMS(K: float, Rh: float, i: float) -> float:
    """
    The Manning-Strickler equation

    Q = K * S * Rh^(2/3) * sqrt(i)

    Parameters
    ----------
    K : float
        The Manning-Strickler coefficient
    Rh : float
        The hydraulic radius, area/perimeter or width
    Js : float
        The slope of the riverbed

    Return
    ------
    float
        The discharge according to Gauckler-Manning-Strickler
    """
    return K * Rh**(2/3) * i**0.5


def twin_points(x_arr: Iterable, z_arr: Iterable) -> Tuple[np.ndarray]:
    """
    Duplicate an elevation to every crossing of its level and the (x, z) curve.
    This will make for straight water tables when filtering like this :
    >>> z_masked = z[z <= z[sx]]  # array with z[ix] at its borders
    Thus, making the cross-section properties (S, P, B) easily computable.

    /|     _____              ////
    /|    //////\            /////
    /+~~~+~~~~~~~o~~~~~~~~~~+/////
    /|__//////////\        ///////
    ///////////////\______////////
    //////////////////////////////
    Legend:
         _
        //\ : ground
        ~ : water table
        o : a certain point given by some pair of (x, z)
        + : the new points created by this function

    Parameters
    ----------
    x : Iterable
        the horizontal coordinates array
    y : Iterable
        the vertical coordinates array

    Return
    ------
    np.ndarray
        the enhanced x-array
    np.ndarray
        the enhanced y-array
    """
    x_arr = np.asarray(x_arr)
    z_arr = np.asarray(z_arr)
    points = np.vstack((x_arr, z_arr)).T

    # to avoid looping over a dynamic array
    new_x = np.array([])
    new_z = np.array([])
    new_i = np.array([], dtype=np.int32)

    for i, ((x1, z1), (x2, z2)) in enumerate(
        zip(points[:-1], points[1:]),
        start=1
    ):

        add_z = np.sort(z_arr[(min(z1, z2) < z_arr) & (z_arr < max(z1, z2))])
        if z2 < z1:
            add_z = add_z[::-1]  # if descending, reverse order
        add_i = np.full_like(add_z, i, dtype=np.int32)
        add_x = x1 + (x2 - x1) * (add_z - z1)/(z2 - z1)  # interpolation

        new_x = np.hstack((new_x, add_x))
        new_z = np.hstack((new_z, add_z))
        new_i = np.hstack((new_i, add_i))

    x = np.insert(x_arr, new_i, new_x)
    z = np.insert(z_arr, new_i, new_z)

    return x, z


def strip_outside_world(x: Iterable, z: Iterable) -> Tuple[np.ndarray]:
    """
    Return the same arrays without the excess borders
    (where the flow section width is unknown).

    If this is not done, the flow section could extend
    to the sides and mess up the polygon.

    Example of undefined profile:

             _
            //\~~~~~~~~~~~~~~~~~~  <- Who knows where this water table ends ?
           ////\          _
    ______//////\        //\_____
    /////////////\______/////////
    /////////////////////////////
    Legend:
         _
        //\ : ground
        ~ : water table

    Parameters
    ----------
    x : Iterable
        Position array from left to right
    z : Iterable
        Elevation array

    Return
    ------
    np.ndarray (1D)
        the stripped x
    np.ndarray(1D)
        the stripped y
    """
    x = np.asarray(x)  # so that indexing works properly
    z = np.asarray(z)
    ix = np.arange(x.size)  # indexes array
    argmin = z.argmin()  # index for the minimum elevation
    left = ix <= argmin  # boolean array inidcatinf left of the bottom
    right = argmin <= ix  # boolean array indicating right

    # Highest framed elevation (avoiding profiles with undefined borders)
    left_max = z[left].argmax()
    right_max = z[right].argmax() + argmin
    z_max = min(z[left_max], z[right_max])
    left[:left_max] = False
    right[right_max+1:] = False

    # strip to the highest framed elevation
    left = left & (z <= z_max)
    right = right & (z <= z_max)

    return x[left | right], z[left | right]


def polygon_properties(
    x_arr: Iterable,
    z_arr: Iterable,
    z: float
) -> Tuple[float]:
    """
    Return the polygon perimeter and area of the formed polygons.

    Parameters
    ----------
    x : Iterable
        x-coordinates
    y : Iterable
        y-coordinates
    z : float
        The z threshold (water table elevation)

    Return
    ------
    float
        Permimeter of the polygon
    float
        Surface area of the polygon
    float
        Length of the water table
    """
    x_arr = np.asarray(x_arr)
    z_arr = np.asarray(z_arr)

    mask = (z_arr[1:] <= z) & (z_arr[:-1] <= z)
    zm = (z_arr[:-1] + z_arr[1:])[mask]/2
    dz = np.diff(z_arr)[mask]
    dx = np.diff(x_arr)[mask]

    length = np.sqrt(dx**2 + dz**2).sum()
    surface = np.abs(((z - zm) * dx).sum())
    width = np.abs(dx.sum())

    return length, surface, width


def hydraulic_data(x: Iterable, z: Iterable) -> pd.DataFrame:
    """
    Derive relation between water depth and discharge (Manning-Strickler)

    Parameters
    ----------
    x : Iterable
        x (transversal) coordinates of the profile. 
        These values will be sorted.
    z : Iterable
        z (elevation) coordinates of the profile. 
        It will be sorted according to x.

    Return
    ------
    pandas.DataFrame
        x : x-coordinates
        z : z-coordinates
        P : wet perimeter
        S : wet surface
        B : dry perimeter
        h : water depth
        Qcr : critical discharge
        Q : discharge (if GMS computed)
    """
    # Compute wet section's properties
    P, S, B = np.transpose([polygon_properties(x, z, zi) for zi in z])
    h = z - z.min()
    mask = P != 0
    Rh = np.full_like(P, None)
    Rh[mask] = S[mask] / P[mask]
    # Compute h_cr-Qcr
    Qcr = np.full_like(B, None)
    mask = B != 0
    Qcr[mask] = np.sqrt(g*S[mask]**3/B[mask])

    return pd.DataFrame.from_dict(dict(
        h=h, P=P, S=S, Rh=Rh, B=B, Qcr=Qcr
    ))


def profile_diagram(
    x: Iterable,
    z: Iterable,
    h: Iterable,
    Q: Iterable,
    Qcr: Iterable,
    fig=None,
    axes=None
) -> Tuple[Figure, Tuple[plt.Axes, plt.Axes]]:
    """
    Plot riverbed cross section and Q(h) in a sigle figure

    Parameters
    ----------
    h : float
        Water depth of stream cross section to fill
    show : bool
        wether to show figure or not
    fig, (ax0, ax1)
        figure and axes on which to draw (ax0: riverberd, ax1: Q(h))

    Returns
    -------
    pyplot figure
        figure containing plots
    pyplot axis
        profile coordinates transversal position vs. elevation
    pyplot axis
        discharge vs. water depth
    """
    if fig is None:
        fig = plt.figure()
    if axes is None:
        ax1 = fig.add_subplot()
        ax0 = fig.add_subplot()
        ax0.patch.set_visible(False)

    x = np.array(x)
    z = np.array(z)
    h = np.array(h)
    Q = np.array(Q)
    Qcr = np.array(Qcr)

    l1, = ax0.plot(x, z, '-ok',
                   mfc='w', lw=3, ms=5, mew=1,
                   label='Profil en travers utile')

    ax0.set_xlabel('Distance profil [m]')
    ax0.set_ylabel('Altitude [m.s.m.]')

    # positionning axis labels on right and top
    ax0.xaxis.tick_top()
    ax0.xaxis.set_label_position('top')
    ax0.yaxis.tick_right()
    ax0.yaxis.set_label_position('right')

    # plotting water depths
    ix = h.argsort()  # simply a sorting index
    l2, = ax1.plot(Q[ix], h[ix], '--b', label="$y_0$ (hauteur d'eau)")
    l3, = ax1.plot(Qcr[ix], h[ix], '-.', label='$y_{cr}$ (hauteur critique)')
    ax1.set_xlabel('Débit [m$^3$/s]')
    ax1.set_ylabel("Hauteur d'eau [m]")
    ax0.grid(False)

    # plotting 'RG' & 'RD'
    ztxt = z.mean()
    ax0.text(x.min(), ztxt, 'RG')
    ax0.text(x.max(), ztxt, 'RD', ha='right')

    # match height and altitude ylims
    ax1.set_ylim(ax0.get_ylim() - z.min())

    # common legend for both axes
    lines = (l1, l2, l3)
    labels = [line.get_label() for line in lines]
    ax0.legend(lines, labels)

    return fig, (ax0, ax1)


class Profile(pd.DataFrame):
    """
    An :func:`~pandas.DataFrame` object.

    Attributes
    ----------
    x : pd.Series
        x-coordinates 
        (horizontal distance from origin)
    z : pd.Series
        z-coordinates (altitudes)
    h : pd.Series
        Water depths
    P : pd.Series
        Wtted perimeter
    S : pd.Series
        Wetted area
    Rh : pd.Series
        Hydraulic radius
    Q : pd.Series
        Discharge (GMS)
    Q : pd.Series
        Critical discharge
    K : float
        Manning-Strickler coefficient
    Js : float
        bed's slope

    Methods
    -------
    plot(h: float = None)
        Plots a matplotlib diagram with the profile,
        the Q-h & Q-h_critical curves and a bonus surface from h
    interp_Q(h: Iterable)
        Returns an quadratic interpolation of the discharge (GMS)
    """

    def __init__(
        self,
        x: Iterable,  # position array from left to right river bank
        z: Iterable,  # altitude array from left to right river bank
        K: float = None,  # The manning-strickler coefficient
        Js: float = None  # The riverbed's slope
    ) -> None:
        """Initialize :func:`~hydraulic_data(x, z, K, Js)` and set K and Js"""

        x, z = twin_points(x, z)
        x, z = strip_outside_world(x, z)
        hd = hydraulic_data(x, z)
        hd["x"] = x
        hd["z"] = z

        super().__init__(hd)

        if K is not None and Js is not None:
            self["v"] = GMS(K, self.Rh, Js)
            self["Q"] = self.S * self.v
            self.K = K
            self.Js = Js

    def interp_B(self, h_array: Iterable) -> np.ndarray:
        return interp1d(self.h, self.B)(h_array)

    def interp_P(self, h_array: Iterable) -> np.ndarray:
        return interp1d(self.h, self.P)(h_array)

    def interp_S(self, h_array: Iterable) -> np.ndarray:
        """
        Quadratic interpolation of the surface. 
        dS = dh*dB/2 where B is the surface width

        Parameters
        ----------
        h_array : Iterable
            Array of water depths

        Returns
        -------
        np.ndarray
            The corresponding surface area
        """

        h, B, S = self[
            ["h", "B", "S"]
        ].sort_values("h").drop_duplicates("h").to_numpy().T

        s = np.zeros_like(h_array)
        for i, h_interp in enumerate(h_array):
            # Checking if h_interp is within range
            mask = h >= h_interp
            if mask.all():
                s[i] = 0
                continue
            if not mask.any():
                s[i] = S[-1]

            # Find lower and upper bounds
            argsup = mask.argmax()
            arginf = argsup - 1
            # interpolate
            r = (h_interp - h[arginf]) / (h[argsup] - h[arginf])
            Bi = r * (B[argsup] - B[arginf]) + B[arginf]
            ds = (h_interp - h[arginf]) * (Bi + B[arginf])/2
            s[i] = S[arginf] + ds

        return s

    def interp_Q(self, h_array: Iterable) -> np.ndarray:
        """
        Interpolate discharge from water depth with
        the quadratic interpolation of S.

        Parameters
        ----------
        h_array : Iterable
            The water depths array.

        Return
        ------
        np.ndarray
            The corresponding discharges
        """
        h = np.asarray(h_array)
        S = self.interp_S(h)
        P = self.interp_P(h)
        Q = np.zeros_like(h)
        mask = ~np.isclose(P, 0)
        Q[mask] = S[mask] * GMS(self.K, S[mask]/P[mask], self.Js)
        return Q

    def interp_Qcr(self, h_array: Iterable) -> np.ndarray:
        """
        Interpolate critical discharge from water depth.

        Parameters
        ----------
        h_array : Iterable
            The water depths array.

        Return
        ------
        np.ndarray
            The corresponding critical discharge
        """
        Qcr = np.full_like(h_array, None)
        B = self.interp_B(h_array)
        S = self.interp_S(h_array)
        mask = B != 0
        Qcr[mask] = np.sqrt(g*S[mask]**3/B[mask])
        return Qcr

    def plot(self, interp_num=1000, *args, **kwargs) -> Tuple[Figure, Tuple[plt.Axes]]:
        """Call :func:`~profile_diagram(self.x, self.z,  self.h, self.Q, self.Qcr)` 
        and update the lines with the interpolated data."""
        fig, (ax1, ax2) = profile_diagram(
            self.x, self.z, self.h, self.Q, self.Qcr,
            *args, **kwargs
        )

        l1, l2 = ax2.get_lines()
        h = np.linspace(self.h.min(), self.h.max(), interp_num)
        l1.set_data(self.interp_Q(h), h)
        l2.set_data(self.interp_Qcr(h), h)

        return fig, (ax1, ax2)


DIR = Path(__file__).parent


def test_Section():

    df = pd.read_csv(DIR / 'profile.csv')
    profile = Profile(
        df['Dist. cumulée [m]'],
        df['Altitude [m s.m.]'],
        33,
        0.12/100
    )

    with plt.style.context('ggplot'):
        fig, (ax1, ax2) = profile.plot()
        ax1.plot(df['Dist. cumulée [m]'],
                 df['Altitude [m s.m.]'],
                 '-o', ms=8, c='gray', zorder=0,
                 lw=3, label="Profil complet")
        ax2.dataLim.x1 = profile.Q.max()
        ax2.autoscale_view()
        fig.show()


def test_ClosedSection():

    df = pd.read_csv(DIR / 'closedProfile.csv')
    r = 10
    K = 33
    i = 0.12/100
    profile = Profile(
        (df.x+1)*r, (df.z+1)*r,
        K, i
    )

    with plt.style.context('ggplot'):
        fig, (ax1, ax2) = profile.plot()
        ax2.dataLim.x1 = profile.Q.max()
        ax2.autoscale_view()

        # Analytical solution
        theta = np.linspace(1e-10, np.pi)
        S = theta*r**2 - r**2*np.cos(theta)*np.sin(theta)
        P = 2*theta*r
        Q = K*(S/P)**(2/3)*S*(i)**0.5
        h = r * (1-np.cos(theta))
        ax2.plot(Q, h, alpha=0.5, label="$y_0$ (analytique)")

        ax1.legend(loc="upper left").remove()
        ax2.legend(loc=(0.2, 0.6)).get_frame().set_alpha(1)
        fig.show()


if __name__ == "__main__":
    test_Section()
    test_ClosedSection()
    plt.show()
