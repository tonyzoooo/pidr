#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from neuron import h
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
            
def plotCylinder(x0, x1, diam, ax, colour, name):
    """
    Dessine un cylindre étant donnés son origine, son sommet et son diamètre.
    Décrit son nom et sa couleur.
    Utilise un maillage simple. 
    Nécessite un subplot.
    Inspiré de : https://stackoverflow.com/questions/32317247/how-to-draw-a-cylinder-using-matplotlib-along-length-of-point-x1-y1-and-x2-y2
    et https://stackoverflow.com/questions/39822480/plotting-a-solid-cylinder-centered-on-a-plane-in-matplotlib#answer-39823124
    Args:
        - x0: array(float)
        - x1: array(float)
        - diam: float
        - ax: plt.subplot
    Return:
        - array(float), array(float), array(float)
    """
    v = x1 - x0
    mag = np.linalg.norm(v)
    v = v/mag
    not_v = np.array([1, 0, 0])
    if (v == not_v).all():
        not_v = np.array([0, 1, 0])
    n1 = np.cross(v, not_v)
    n1 /= np.linalg.norm(n1)
    n2 = np.cross(v, n1)
    t = np.linspace(0, mag, 5)
    theta = np.linspace(0, 2 * np.pi, 10)
    rsample = np.linspace(0, diam/2, 5)
    t, theta2 = np.meshgrid(t, theta)
    rsample,theta = np.meshgrid(rsample, theta)
    X, Y, Z = [x0[i] + v[i] * t + diam/2 * np.sin(theta2) * n1[i] + diam/2 * np.cos(theta2) *       n2[i] for i in [0, 1, 2]]
    X2, Y2, Z2 = [x0[i] + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
    X3, Y3, Z3 = [x0[i] + v[i]*mag + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
    cyl = ax.plot_surface(X, Y, Z, color =colour, label = name)
    # fix for 3d colors
    cyl._facecolors2d=cyl._facecolors3d
    cyl._edgecolors2d=cyl._edgecolors3d
    face1 = ax.plot_surface(X2, Y2, Z2, color =colour)
    face1._facecolors2d=face1._facecolors3d
    face1._edgecolors2d=face1._edgecolors3d
    face2 = ax.plot_surface(X3, Y3, Z3, color =colour)
    face2._facecolors2d=face2._facecolors3d
    face2._edgecolors2d=face2._edgecolors3d
    return X, Y, Z
    
    

def plot3DCell(cell):
    """
    Dessine une cellule neuronale en 3D. Nécessite un objet hoc.
        - cell: hoc
    Return:
        - None
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    h.define_shape()
    max_range = 0
    cmap = plt.get_cmap('Spectral')
    i = 0
    N = sum(1 for s in cell.allsec())
    # en attendant de trouver une méthode pour avoir le nombres de sections...
    for s in cell.allsec() :
        x0 = np.array([s.x3d(0), s.y3d(0), s.z3d(0)])
        x1 = np.array([s.x3d(1), s.y3d(1), s.z3d(1)])
        d = s.diam3d(0)
        colour = cmap(i/N)
        X, Y, Z = plotCylinder(x0, x1, d, ax, colour, s.name())
        max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min(), max_range]).max()
        i+=1
        
    # equal scaling for all axes
    # https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())

    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')
            
    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")
    ax.set_zlabel("Z (µm)")
    plt.title("Model of 3D cell")
    plt.grid()
    plt.legend()
    plt.show()