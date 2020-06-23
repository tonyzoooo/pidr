import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import norm


def plotCylinder(p0: np.ndarray, p1: np.ndarray, diam: float, **kwargs):
    R = diam / 2

    v = p1 - p0     # vector in direction of axis
    mag = norm(v)   # find magnitude of vector
    v = v / mag     # unit vector in direction of axis

    # make some vector not in the same direction as v
    not_v = np.array([1, 0, 0])
    if (v == not_v).all():
        not_v = np.array([0, 1, 0])

    n1 = np.cross(v, not_v)  # make vector perpendicular to v
    n1 /= norm(n1)           # normalize n1
    n2 = np.cross(v, n1)     # make unit vector perpendicular to v and n1

    # surface ranges over t from 0 to length of axis and 0 to 2*pi
    t = np.linspace(0, mag, 2)
    theta = np.linspace(0, 2 * np.pi, 10)
    t, theta = np.meshgrid(t, theta)  # use meshgrid to make 2d arrays

    # generate coordinates for surface
    X, Y, Z = [p0[i]
               + v[i] * t
               + R * np.sin(theta) * n1[i]
               + R * np.cos(theta) * n2[i] for i in [0, 1, 2]]

    ax = plt.gca()
    ax.plot_surface(X, Y, Z, **kwargs)


if __name__ == '__main__':

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    p0 = np.array([1, 3, 2])
    p1 = np.array([8, 5, 9])

    plotCylinder(p0, p1, diam=0.8, color='red')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_zlim(0, 10)
    plt.show()
