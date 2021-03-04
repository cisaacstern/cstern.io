A fundamental aim of the <a href="https://cstern.io/projects/albedo">albedo analysis project</a> is to compare so-called "terrain correction" parameters resulting from a planar regression with those from a high-resolution rasterized method. The name ufunc-correct comes from a simple yet powerful insight: namely, NumPy's universal functions (ufuncs) allow us to implement a single function for both planar and raster correction.

To see this "in action" let's first look at the definition of the terrain correction factor as provided by <a href="https://people.eri.ucsb.edu/~nbair/storage/bair_et_al_2015_frontiers.pdf" target="_blank">Bair et al 2015</a> Eq. 1:

$\enspace \enspace c \space = \space \cfrac{cos\theta}{cos\theta_0}$

...the inputs of which are in turn derived from <a href="http://www2.bren.ucsb.edu/~dozier/Pubs/DozierFrewIEEE1990.pdf" target="_blank">Dozier & Frew 1990</a> Eq. 14:

$\enspace \enspace cos\theta_S \space = \space cos\theta_0 \space cosS \space + \space sin\theta_0 \space sinS \space cos(\phi_0 - A)$


Below is my translation of these formulae into Python code, with theta and phi represented as T and P, respectively. (In the app, the actual implementation of this formula is as an instance method, a design choice which neatly ties it to an instance-specific solar position attribute. That code can be found in <a href="https://github.com/cisaacstern/ufunc-correct/blob/main/correction.py" targe="_blank">the project repo</a>.)

The sort of "all at once" array operation demonstrated here is by no means a unique insight; indeed, it's basic NumPy. Yet in scientific programming the ability to perform a array operation without a loop is a fundamental and, in its own quiet a way, revolutionary notion, which is why I've chosen to feature it here. In the future, I hope to dig deeper into both the NumPy C internals and Linear Algebra principles which make this possible. For now, I just appreciate the fact that it is. 

```{.python .codehilite}
import numpy as np


def calc_terrain_correction(altitude, azimuth, slope, aspect):
    '''
    Parameters
    ----------
    altitude : float
        Solar altitude in radians.
    azimuth : float
        Solar azimuth in radians.
    slope : float or numpy.ndarray
        Single slope in radians or array of radian slopes.
    aspect : float or numpy.ndarray
        Single aspect in radians or array of radian aspects.

    Returns
    -------
    float or numpy.ndarray
        Return type depends on input type of slope & aspect.
    '''

    T0, P0 = altitude, azimuth
    S, A = slope, aspect


    cosT0 = np.cos(T0)
    cosS = np.cos(S)
    sinT0 = np.sin(T0)
    sinS = np.sin(S)
    cosP0A = np.cos(P0 - A)


    cosT = (cosT0*cosS) + (sinT0*sinS*cosP0A)

    return cosT/cosT0
```

**Note**: <a href="https://cstern.io/projects/math+hilite">math+hilite</a> addresses the processes for rendering mathematical notation and syntax-highlighted code, as seen on this page.