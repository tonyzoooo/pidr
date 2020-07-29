#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from typing import Iterable, Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.collections import LineCollection
from mayavi import mlab
from neuron import h, nrn
from vtk import vtkObject


def getCoordinates(section):
    """
    Returns 3D coordinates of a given section.
    Args:
        - section:
    Return:
        - array(float), array(float), array(float)
    """
    x, y, z = [], [], []
    nb_points = section.n3d()
    for i in range(nb_points):
        x.append(section.x3d(i))
        y.append(section.y3d(i))
        z.append(section.z3d(i))
    return np.array(x), np.array(y), np.array(z)


def getDiameters(section):
    """
    Returns diameters of a given section.
    Args:
        - section:
    Return:
        - array(float)
    """
    d = []
    nb_points = section.n3d()
    for i in range(nb_points):
        d.append(section.diam3d(i))
    return np.array(d)


def createSegments(array1, array2):
    """
    Returns segments created from 2 arrays. Builds tuples (eg. [[(x1, y1), (x2, y2)], ....])
    Args:
        - array1: array[float]
        - array2: array[float]
    Return:
        - list(list(tuple), ...)
    """
    segments = []
    for i in range(len(array1) - 1):
        start = (array1[i], array2[i])
        end = (array1[i + 1], array2[i + 1])
        segment = [start, end]
        segments.append(segment)
    return segments


def buildTree(sectionlist: Iterable[nrn.Section]):
    """
    Inpired from:https://senselab.med.yale.edu/modeldb/ShowModel?model=153196&file=/FoutzEtAl2012/classes.py#tabs-2
    and https://docs.enthought.com/mayavi/mayavi/auto/example_plotting_many_lines.html#example-plotting-many-lines
    """

    def append_data(section, xyzd, connections, parent_id):
        for i in range(int(h.n3d(sec=section))):
            x = h.x3d(i, sec=section)
            y = h.y3d(i, sec=section)
            z = h.z3d(i, sec=section)
            d = h.diam3d(i, sec=section)
            xyzd.append([x, y, z, d])
            child_id = len(xyzd) - 1
            if len(xyzd) > 1:
                connections.append([child_id, parent_id])
            parent_id = child_id
        return xyzd, connections

    def append_children_data(parent, parent_id, xyzd, connections):
        sref = h.SectionRef(sec=parent)
        if sref.child:
            for child in sref.child:
                xyzd, connections = append_data(child, xyzd, connections, parent_id)
                xyzd, connections = append_children_data(parent=child,
                                                         parent_id=len(xyzd) - 1,
                                                         xyzd=xyzd,
                                                         connections=connections)
        return xyzd, connections

    assert sum(1 for _ in sectionlist) > 0, 'sectionList is empty'
    first_section = next(iter(sectionlist))
    root_section = h.SectionRef(sec=first_section).root
    xyzd = [[h.x3d(0, sec=root_section), h.y3d(0, sec=root_section),
             h.z3d(0, sec=root_section), h.diam3d(0, sec=root_section)]]
    xyzd, connections = append_data(root_section, xyzd, [], 0)
    xyzd, connections = append_children_data(root_section, len(xyzd) - 1, xyzd, connections)
    xyzd = np.array(xyzd)
    connections = np.array(connections)
    return xyzd, connections


def plot2DCell(sectionlist: Iterable[nrn.Section], stimpoint: Tuple[int, ...] = None):
    """
    Plots a 2D view of a cell, specified as a NEURON SectionList
    or any iterable of ``nrn.Section`` objects

    :param sectionlist:     iterable of nrn.Section
    :param stimpoint:       stimulation (x, y) or (x, y, z) point (optionnal)
    """
    window = tk.Tk()
    fig = plt.figure()
    window.wm_title("Cell visualisation (2D)")
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    ax = fig.add_subplot(111)

    colormap = plt.get_cmap('jet')
    N = sum(1 for s in sectionlist)
    i = 0
    for section in sectionlist:
        x, y, z = getCoordinates(section)
        d = getDiameters(section)

        # XY face
        segments = createSegments(x, y)
        lc = LineCollection(segments, linewidths=d, color=colormap(i / N))
        ax.add_collection(lc)
        ax.axis('equal')
        ax.margins(0.05)
        ax.set_xlabel('X (µm)')
        ax.set_ylabel('Y (µm)')
        ax.set_title('XY plan')
        ax.grid(True)
        i += 1

    if stimpoint is not None:
        x = stimpoint[0]
        y = stimpoint[1]
        ax.plot(x, y, 'ro')

    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    plt.close(fig)
    window.eval('tk::PlaceWindow %s center' % window.winfo_pathname(window.winfo_id()))
    window.mainloop()


def getSectionData(sectionlist):
    indexes = []
    names = []
    for section in sectionlist:
        names.append(section.name())
        if indexes == []:
            indexes = [0]
        else:
            indexes.append(indexes[-1] + section.n3d())
        names.append(section.name())
    return indexes, names


def plot3DCell(sectionlist: Iterable[nrn.Section], stimpoint: Tuple[int, ...] = None):
    """
    Returns collections of lines for different 2d views of cell.
    Args:
        - sectionList:
    Return:
        - LineCollection, LineCollection, LineCollection
    """
    # hide warnings
    # mlab.options.backend = 'envisage'
    o = vtkObject
    o.GetGlobalWarningDisplay()
    o.SetGlobalWarningDisplay(0)  # Turn it off.

    mlab.figure(1)
    mlab.clf()
    xyzd, connections = buildTree(sectionlist)
    x = xyzd[:, 0]
    y = xyzd[:, 1]
    z = xyzd[:, 2]
    d = xyzd[:, 3]
    connections = np.vstack(connections)

    # Create the points
    points = mlab.pipeline.scalar_scatter(x, y, z, d)

    dataset = points.mlab_source.dataset
    dataset.point_data.get_array(0).name = 'diameter'
    dataset.lines = connections
    dataset.point_data.update()
    src = mlab.pipeline.set_active_attribute(points, point_scalars='diameter')
    stripper = mlab.pipeline.stripper(src)
    tube = mlab.pipeline.tube(stripper, tube_sides=6, tube_radius=1)
    tube.filter.capping = True
    # tube.filter.use_default_normal = False
    tube.filter.vary_radius = 'vary_radius_by_absolute_scalar'
    src2 = mlab.pipeline.set_active_attribute(tube)
    mlab.pipeline.surface(src2, colormap='jet')

    # Connect them

    # src.mlab_source.dataset.lines = connections

    # src.update()

    # The stripper filter cleans up connected lines
    # lines = mlab.pipeline.stripper(src)
    # Finally, display the set of lines
    # mlab.pipeline.surface(lines, colormap='jet', line_width=1, opacity=.4)

    # labels
    #    indexes, names = getSectionData(sectionlist)
    #    for i in range(len(indexes)):
    #        index = indexes[i]
    #        name = names[i]
    #        label = mlab.text(x[index], y[index], name ,z[index],width=0.016 * len(name),
    #                          name=name)
    #        label.property.shadow = True

    if stimpoint is not None:
        mlab.points3d(*stimpoint, mode='sphere', scale_factor=10, color=(.9, .2, .2))

    mlab.show()

# =============================================================================
# Old version with matplolib
# =============================================================================
# from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
# from mpl_toolkits.mplot3d import Axes3D

# def defCylinder(x0, x1, diam):
#    """
#    Calcule les coordonnées d'un cylindre étant donnés son origine, son sommet 
#    et son diamètre.
#    Utilise un maillage simple. 
#    Inspiré de : https://stackoverflow.com/questions/32317247/how-to-draw-a-cylinder-using-matplotlib-along-length-of-point-x1-y1-and-x2-y2
#    et https://stackoverflow.com/questions/39822480/plotting-a-solid-cylinder-centered-on-a-plane-in-matplotlib#answer-39823124
#    Args:
#        - x0: array(float)
#        - x1: array(float)
#        - diam: float
#    Return:
#        - array(float), array(float), array(float), ...
#    """
#    nseg = 5
#    v = x1 - x0
#    mag = np.linalg.norm(v)
#    v = v / (mag or 1)
#    not_v = np.array([1, 0, 0])
#    if (v == not_v).all():
#        not_v = np.array([0, 1, 0])
#    n1 = np.cross(v, not_v)
#    n1 /= (np.linalg.norm(n1) or 1)
#    n2 = np.cross(v, n1)
#    t = np.linspace(0, mag, nseg)
#    theta = np.linspace(0, 2 * np.pi, 2*nseg)
#    rsample = np.linspace(0, diam/2, nseg)
#    t, theta2 = np.meshgrid(t, theta)
#    rsample,theta = np.meshgrid(rsample, theta)
#    X, Y, Z = [x0[i] + v[i] * t + diam/2 * np.sin(theta2) * n1[i] + diam/2 * np.cos(theta2) *       n2[i] for i in [0, 1, 2]]
#    X2, Y2, Z2 = [x0[i] + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
#    X3, Y3, Z3 = [x0[i] + v[i]*mag + rsample[i] * np.sin(theta) * n1[i] + rsample[i] * np.cos(theta) * n2[i] for i in [0, 1, 2]]
#    return X, Y, Z, X2, Y2, Z2, X3, Y3, Z3
#
#
# def getAllPoints(sectionlist):
#    """
#    Calcule toutes les coordonnées de la cellule pour un maillage simple.
#    Args:
#        - sectionlist: SectionList
#    Return:
#        - array(float), array(float), array(float)
#    """
#    x, y, z = [], [], []
#    for s in sectionlist :
#        d = s.diam3d(0)
#        xseg = s.x3d(1) - s.x3d(0)
#        yseg = s.y3d(1) - s.y3d(0)
#        zseg = s.z3d(1) - s.z3d(0)
#        for i in range(s.nseg):
#            x0 = np.array([s.x3d(0)+i*xseg, s.y3d(0)+i*yseg, s.z3d(0)+i*zseg])
#            x1 = np.array([s.x3d(1)+(i+1)*xseg, s.y3d(1)+(i+1)*yseg, s.z3d(1)+(i+1)*zseg])
#            X, Y, Z, X2, Y2, Z2, X3, Y3, Z3 = defCylinder(x0, x1, d)
#            x.extend(list(X))
#            y.extend(list(Y))
#            z.extend(list(Z))
#    x = np.array(x)
#    y = np.array(y)
#    z = np.array(z)
#    return x, y, z
#
#
#
# def plot2DCell(sectionlist):
#    """
#    Trace des graphes de la cellule étant données sa SectionList.
#    Args:
#         - sectionlist: SectionList
#    Return: 
#        - None
#    """
#    window = tk.Tk()
#    window.wm_title("Cell visualisation (2D)")
#    fig = plt.figure()
#    canvas = FigureCanvasTkAgg(fig, master=window)
#    canvas.draw()
#    axXY = fig.add_subplot(311)
#    axXZ = fig.add_subplot(312)
#    axYZ = fig.add_subplot(313)
#    colormap = plt.get_cmap('jet')
#    x, y, z = getAllPoints(sectionlist)
#    caXY = axXY.contour(x, y, z, np.linspace(z.min(), z.max(), 1000), cmap = colormap)
#    caXZ = axXZ.contourf(x, z, y, np.linspace(y.min(), y.max(), 150), cmap = colormap)
#    caYZ = axYZ.contourf(y, z, x, np.linspace(x.min(), x.max(), 150), cmap = colormap)
#    axXY.set_xlabel("X (µm)")
#    axXY.set_ylabel("Y (µm)")
#    axXY.set_title("XY plan")
#    cbarXY = fig.colorbar(caXY, ax = axXY)
#    cbarXY.set_label("Depth in Z axis (µm)")
#    axXY.grid()
#
#    axXZ.set_xlabel("X (µm)")
#    axXZ.set_ylabel("Z (µm)")
#    axXZ.set_title("XZ plan")
#    cbarXZ = fig.colorbar(caXZ, ax = axXZ)
#    cbarXZ.set_label("Depth in Y axis (µm)")
#    axXZ.grid()
#
#
#    axYZ.set_xlabel("Y (µm)")
#    axYZ.set_ylabel("Z (µm)")
#    axYZ.set_title("YZ plan")
#    cbarYZ = fig.colorbar(caYZ, ax = axYZ)
#    cbarYZ.set_label("Depth in X axis (µm)")
#    axYZ.grid()
#    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#    plt.close(fig)
#    window.mainloop()
#
#
# def plot3DCell(sectionlist):
#    """
#    Dessine une cellule neuronale. Nécessite un objet SectionList.
#    Spécifier la vue souhaitée.
#        - sectionlist: SectionList
#        - view: int
#    Return:
#        - None
#    """
#    window = tk.Tk()
#    window.wm_title("Cell visualisation (3D)")
#    fig = plt.figure()
#    canvas = FigureCanvasTkAgg(fig, master=window)
#    canvas.draw()
#
#    nrn_col = plt.get_cmap('Spectral')
#    ax = Axes3D(fig)  # fig.add_subplot(111, projection='3d')
#    max_range = 0
#    c=0
#    x, y, z = [], [], []
#    N = sum(1 for s in sectionlist)
#    # en attendant de trouver une méthode pour avoir le nombres de sections...
#    for s in sectionlist:
#        xseg = s.x3d(1) - s.x3d(0)
#        yseg = s.y3d(1) - s.y3d(0)
#        zseg = s.z3d(1) - s.z3d(0)
#        d = s.diam3d(0)
#        colour = nrn_col(c/N)
#        new_X, new_Y, new_Z, new_X2, new_Y2, new_Z2, new_X3, new_Y3, new_Z3 = [], [], [], [], [], [], [], [], []
#        for i in range(s.nseg):
#            x0 = np.array([s.x3d(0)+i*xseg, s.y3d(0)+i*yseg, s.z3d(0)+i*zseg])
#            x1 = np.array([s.x3d(1)+(i+1)*xseg, s.y3d(1)+(i+1)*yseg, s.z3d(1)+(i+1)*zseg])
#            X, Y, Z, X2, Y2, Z2, X3, Y3, Z3 = defCylinder(x0, x1, d)
#            new_X.extend(X)
#            new_Y.extend(Y)
#            new_Z.extend(Z)
#            new_X2.extend(X2)
#            new_Y2.extend(Y2)
#            new_Z2.extend(Z2)
#            new_X3.extend(X3)
#            new_Y3.extend(Y3)
#            new_Z3.extend(Z3)
#
#        new_X = np.array(new_X)
#        new_Y = np.array(new_Y)
#        new_Z = np.array(new_Z)
#        new_X2 = np.array(new_X2)
#        new_Y2 = np.array(new_Y2)
#        new_Z2 = np.array(new_Z2)
#        new_X3 = np.array(new_X3)
#        new_Y3 = np.array(new_Y3)
#        new_Z3 = np.array(new_Z3)
#        cyl = ax.plot_surface(new_X, new_Y, new_Z, color =colour, label = s.name())
#            # fix for 3d colors
#        cyl._facecolors2d=cyl._facecolors3d
#        cyl._edgecolors2d=cyl._edgecolors3d
#        face1 = ax.plot_surface(new_X2, new_Y2, new_Z2, color =colour)
#        face1._facecolors2d=face1._facecolors3d
#        face1._edgecolors2d=face1._edgecolors3d
#        face2 = ax.plot_surface(new_X3, new_Y3, new_Z3, color =colour)
#        face2._facecolors2d=face2._facecolors3d
#        face2._edgecolors2d=face2._edgecolors3d
#        max_range = np.array([new_X.max()-new_X.min(), new_Y.max()-new_Y.min(), new_Z.max()-new_Z.min(), max_range]).max()
#        x.extend(list(new_X))
#        y.extend(list(new_Y))
#        z.extend(list(new_Z))
#        c+=1
#
#
#
#
#    x = np.array(x)
#    y = np.array(y)
#    z = np.array(z)
#    # equal scaling for all axes
#    # https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to
#    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(x.max()+x.min())
#    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(y.max()+y.min())
#    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(z.max()+z.min())
#
#    ax.set_xlabel("X (µm)")
#    ax.set_ylabel("Y (µm)")
#    ax.set_zlabel("Z (µm)")
#    ax.set_title("Model of 3D cell")
#
#    for xb, yb, zb in zip(Xb, Yb, Zb):
#        ax.plot([xb], [yb], [zb], 'w')
#
#
#    # make the panes transparent
#    #ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
#    #ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
#    #ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
#    # make the grid lines transparent
#    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
#    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
#    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
#    ax.legend()
#
#    toolbar = NavigationToolbar2Tk(canvas, window)
#    toolbar.update()
#    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#    plt.close(fig)
#    window.mainloop()
#
#
