#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 16:03:18 2020

@author: tonyz
"""

import matplotlib.pyplot as plt
from neuron import h
import numpy as np

            
def plotCylinder(x0, x1, nb_pts, diam, ax):
    """
    Dessine un cylindre étant donnés son origine, son sommet et son diamètre. 
    Utilise un maillage simple (nombre de points à spécifier). 
    Nécessite un subplot.
    Inspiré de : https://stackoverflow.com/questions/32317247/how-to-draw-a-cylinder-using-matplotlib-along-length-of-point-x1-y1-and-x2-y2
    et https://stackoverflow.com/questions/39822480/plotting-a-solid-cylinder-centered-on-a-plane-in-matplotlib#answer-39823124
    Args:
        - x0: array(float)
        - x1: array(float)
        - nb_pts: int
        - diam: float
        - ax: plt.subplot
    Return:
        - None
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
    t = np.linspace(0, mag, nb_pts)
    theta = np.linspace(0, 2 * np.pi, nb_pts)
    rsample = np.linspace(0, diam/2, nb_pts)
    t, theta2 = np.meshgrid(t, theta)
    rsample,theta = np.meshgrid(rsample, theta)
    X, Y, Z = [x0[i] + v[i] * t + diam/2 * np.sin(theta2) * n1[i] + diam/2 * np.cos(theta2) *       n2[i] for i in [0, 1, 2]]
    X2, Y2, Z2 = [x0[i] + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
    X3, Y3, Z3 = [x0[i] + v[i]*mag + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
    ax.plot_surface(X, Y, Z, color='pink')
    ax.plot_surface(X2, Y2, Z2, color='pink')
    ax.plot_surface(X3, Y3, Z3, color='pink')

    

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
    for s in cell.allsec():
        for i in range(s.n3d()-1):
            x0 = np.array([s.x3d(i), s.y3d(i), s.z3d(i)])
            x1 = np.array([s.x3d(i+1), s.y3d(i+1), s.z3d(i+1)])
            d = s.diam3d(i)
            plotCylinder(x0, x1, 10, d, ax)
    ax.set_xlabel("X (µm)")
    ax.set_ylabel("Y (µm)")
    ax.set_zlabel("Z (µm)")
    plt.title("Model of 3D cell")
    plt.show()