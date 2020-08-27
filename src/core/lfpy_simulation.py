#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Steven Le Cam, Radu Ranta, Tony Zhou
"""
from typing import Dict

import LFPy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PolyCollection


def polyArea(x: np.ndarray, y: np.ndarray):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


def plotNeuron(cell: LFPy.Cell, fig: plt.Figure, electrodeRanges: Dict[str, np.ndarray]):
    Y = electrodeRanges['y']
    X = electrodeRanges['x']

    # plt.plot(electrode.x, electrode.y, '.',  marker='o',
    #          markersize=3, color='r', zorder=0)
    # rotation = {'x' : 0, 'y' : math.pi, 'z' : 0} #-math.pi/9 # Mainen
    # cell.set_rotation(**rotation)
    zips = []
    for x, y in cell.get_idx_polygons(projection=('x', 'y')):
        # PATCH Radu do not plot big boxes
        #        tmp=list(zip(x,y))
        #        if not 250 in tmp[1]:
        if polyArea(x, y) < 10000:
            zips.append(list(zip(x, y)))
        # END PATCH
    polycol = PolyCollection(zips, edgecolors='#999999',
                             facecolors='#666666', linewidths=1.7)
    polycol.set_clip_on(False)  # draw outside of axes
    ax = fig.add_axes([0.15, 0.35, 0.725, 0.48])
    # align axes to grid :
    ax.set_xlim(X[0], X[-1])  # (-250, 1250)
    ax.set_ylim(Y[-1], Y[0])  # (50, 250)

    ax.axis('off')
    ax.add_collection(polycol)
    plt.xlabel('Distance μm - (Ox)')
    plt.ylabel('Distance μm - (Oy)')

    return fig


def runLfpySimulation(cell: LFPy.Cell,
                      electrodeRanges: Dict[str, np.ndarray] = None):
    """
    Executes a simulation with LFPy using the given cell and electrode positions

    :param cell:
    :param electrodeRanges:
    :return:
    """

    # -----------------------------------------------------------
    # stimulation parameters
    # -----------------------------------------------------------

    # if cell_parameters["passive"]==False:
    #     amp=1.95**(int(ida)/1.95)/30+1.6*int(ila)/10000+int(ild)/5000*int(idd)*1.5
    # else:
    #     amp=1.65**(int(ida)/1.95)/30+0.805*int(ila)/10000+int(ild)/5000*int(idd)*1.1 #-0.4 for Mainen equivalent

    # -----------------------------------------------------------
    # Simulation
    # -----------------------------------------------------------

    # The constructor of LFPy.StimIntElectrode objects takes the LFPy.Cell
    # as an argument. This has the effect to bind this electrode to the
    # cell. That's why we don't need to parameterize the stimulation here.

    cell.simulate(rec_imem=True)
    # cell.imem[np.isnan(cell.imem)]=0.0

    # -----------------------------------------------------------
    # Electrodes
    # -----------------------------------------------------------

    hstep = electrodeRanges['x']
    vstep = electrodeRanges['y']
    N = vstep.shape
    Ny = hstep.shape

    x_elec = np.tile(hstep, N)
    y_elec = np.sort(np.tile(vstep, Ny))[::-1]
    z_elec = np.zeros(x_elec.shape)

    meshgrid = {
        'sigma': 0.33,
        'x': x_elec,
        'y': y_elec,
        'z': z_elec,
    }

    # Electrodes initialization
    meshgrid_electrodes = LFPy.RecExtElectrode(cell, **meshgrid)
    meshgrid_electrodes.calc_lfp()

    # -----------------------------------------------------------
    # Plot and save
    # -----------------------------------------------------------

    st = cell.dt  # simulation timestep
    timeind = (cell.tvec > np.argmax(cell.somav) * st -
               3) & (cell.tvec <= np.argmax(cell.somav) * st + 5)

    # fileout="Vlfpy_BS"+"_LA"+LA+"_DA"+DA+"_LD"+LD+"_DD"+DD+"demo.txt"
    # np.savetxt(fileout,meshgrid_electrodes.LFP.T[timeind])
    Vlfpy = meshgrid_electrodes.LFP.T[timeind]

    # fileout2="Vm_BS"+"_LA"+LA+"_DA"+DA+"_LD"+LD+"_DD"+DD+"demo.txt"
    # np.savetxt(fileout2,cell.somav[timeind])
    Vmlfpy = cell.somav[timeind]

    # fileout3="Im_BS"+"_LA"+LA+"_DA"+DA+"_LD"+LD+"_DD"+DD+"demo.txt"
    # np.savetxt(fileout3,cell.imem[0,timeind])
    Imlfpy = cell.imem[0, timeind]

    # elpos=(x_elec,y_elec,z_elec)
    # np.savetxt("elpos_demo",elpos)
    res = StimulationResult()
    res.Vlfpy = Vlfpy
    res.Vmlfpy = Vmlfpy
    res.Imlfpy = Imlfpy
    res.timeind = timeind
    res.meshgrid_electrodes = meshgrid_electrodes
    return res


class StimulationResult:
    Vlfpy: np.ndarray = None
    Vmlfpy: np.ndarray = None
    Imlfpy: np.ndarray = None
    timeind: float = None
    meshgrid_electrodes: LFPy.RecExtElectrode = None


def plotStimulation(cell: LFPy.Cell,
                    timeind: int,
                    stimulus: LFPy.StimIntElectrode,
                    meshgrid_electrodes: LFPy.RecExtElectrode):
    fig = plt.figure('Stimulation')

    # ================= STIMULATION PLOT =================================
    plt.subplot(411)
    plt.plot(cell.tvec[timeind], stimulus.i[timeind])
    plt.axis('tight')
    plt.ylabel(r'$I_s$ (nA)', va='center')
    plt.grid(True)
    # ================= SOMA PLOT ========================================
    plt.subplot(412)
    plt.plot(cell.tvec[timeind], cell.somav[timeind], lw=1)
    plt.axis('tight')
    plt.ylabel(r'$V_m$ (mV)', va='center')
    plt.grid(True)

    # ================= Imem  ============================================
    plt.subplot(413)
    # ,label='x='+str(elec_parameters["x"])+' - y='+str(elec_parameters["y"]))
    plt.plot(cell.tvec[timeind], cell.imem[0, timeind], lw=1)
    plt.axis('tight')
    plt.ylabel(r'$I_m$ (nA)', va='center')
    plt.grid(True)

    # ================= ELECTRODE LFP  ===================================
    plt.subplot(414)
    # ,label='x='+str(elec_parameters["x"])+' - y='+str(elec_parameters["y"]))
    plt.plot(cell.tvec[timeind], meshgrid_electrodes.LFP.T[timeind], lw=1)
    plt.ylabel(r'$V_e$ (mV)', va='center')
    plt.xlabel('time (ms)')
    plt.grid(True)

    return fig
