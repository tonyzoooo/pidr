#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Steven Le Cam, Radu Ranta, Tony Zhou
"""

import LFPy
import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from numpy.linalg import norm

from src.app import section_util
from src.core import util
from src.core.hhrun import hhrun
from src.core.lfpy_simulation import plotNeuron, plotStimulation, runLfpySimulation
from src.core.morphofiltd import morphofiltd


def executeDemo(cell: LFPy.Cell, stim: LFPy.StimIntElectrode, stimParams: dict):
    """
    Executes the demo comparing LFPy's simulation and Tran's fast simulation
    based on a morphological filtering approximation.

    :param cell:        LFPy.Cell object
    :param stim:        LFPy.StimIntElectrode object
    :param stimParams:  parameters of the stimulation as a dictionary
    """

    # -----------------------------------------------------------
    # run LFPy simulation
    # -----------------------------------------------------------

    result = runLfpySimulation(cell=cell, stim=stim)

    Vlfpy = result.Vlfpy
    Vmlfpy = result.Vmlfpy
    Imlfpy = result.Imlfpy
    timeind = result.timeind
    meshgrid_electrodes = result.meshgrid_electrodes

    # -----------------------------------------------------------
    # HH (Hodgkin–Huxley model)
    # -----------------------------------------------------------

    inmvm = np.argmax(Vmlfpy)  # index max on Vm in LFPy
    lVLFPy = len(Vlfpy)  # signal length in LFPy
    dt = 1 / 1000  # sampling period in ms
    Nt = 2 ** 15
    D = Nt * dt
    t = util.closed_range(dt, D, dt) - dt

    # fe = 1 / dt
    # f = np.arange(0, fe / 2, fe / Nt)

    dur = stimParams.get('dur', 30)
    delay = stimParams.get('delay', 1)
    I = (
            (np.heaviside(t - delay, 1 / 2) - np.heaviside(t - dur - delay, 1 / 2))
            * 0.044 / (2 * pi * 12.5 * 25) * 10 ** 8 * 10 ** -3
        # * 5.093 # 0.15 / (pi * 12.5 * 12.5 * 2 + 2 * pi * 12.5 * 25) * 10 ** 8
    )
    # icur = 1

    # pot membrane, proportional to ion channels electric current
    # (http://www.bem.fi/book/03/03.htm, 3.14)
    Vm, m, n, h, INa, IK, Il = hhrun(I, t)

    Im = (INa + IK + Il) * (2 * pi * 12.5 * 25) / 10 ** 8 * 10 ** 3
    inMVm = np.argmax(Vm)

    # -----------------------------------------------------------
    # Ball & Stick neuron morphology
    # -----------------------------------------------------------

    dims = section_util.computeDimensions(cell.allseclist)
    print('dimensions:', dims)

    SL = dims.get('SL', 25)  # soma length (cylinder with the same diameter)

    AL = dims.get('AL', 1000)  # axon length
    AD = dims.get('AD', 2)  # axon diameter

    LD = dims.get('LD', 200)  # dendrite length
    DD = dims.get('DD', 2)  # dendrite diameter
    phi = pi / 2  # angle with Oz
    theta = pi  # angle with Ox (phi=pi/2,theta=pi) indicates opposite to the axon

    # -----------------------------------------------------------
    # figure check
    # -----------------------------------------------------------

    values = np.arange(inMVm - inmvm, inMVm - inmvm + lVLFPy)

    plt.figure('Simulation result')

    plt.subplot(2, 1, 1)
    plt.plot(Vm[values], label="Tran")
    plt.plot(Vmlfpy, label="LFPy")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane voltage (mV)")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(Im[values], label='Tran')
    plt.plot(Imlfpy, label="LFPy")
    plt.xlabel("Time (ms)")
    plt.ylabel("Current (nA)")
    plt.legend()

    # -----------------------------------------------------------
    # filter parameters
    # -----------------------------------------------------------

    dk = 10  # axonal spatial sampling(~ nb of segments)

    order = int(AL / dk + 1)
    r0 = np.array([0, 0, 0])  # soma position
    r1 = np.array([SL / 2, 0, 0])  # axon start position
    rN = np.array([SL / 2 + AL - dk, 0, 0])  # axon stop position (start of the last segment)
    rd = norm(r1 - r0) * np.array([
        np.sin(phi) * np.cos(theta),
        np.sin(phi) * np.sin(theta),
        np.cos(phi)
    ])  # dendrite end position, normalized
    amp = stimParams.get('amp', 0.2)
    Cs = amp * 10  # somatic equivalent dipole amplitude
    taus = 23  # subsampling of the membrane current dk/taus = speed v)

    """
                     ----
            -rd'----| r0 |r1-----------------------rN-
                     ----
    """

    # -----------------------------------------------------------
    # electrodes
    # -----------------------------------------------------------

    X = util.closed_range(-250, 1250, 125)
    Y = util.closed_range(250, 50, -50)
    Z = 0

    elpos = util.reshapeMeshgrid(np.meshgrid(X, Y, Z))

    # -----------------------------------------------------------
    # simulation
    # -----------------------------------------------------------

    w = morphofiltd(elpos, order, r0, r1, rN, rd, Cs)
    wup = util.upsample(w.T, taus).T

    Vel = np.zeros((len(w), len(Im)))

    for iel in range(len(w)):
        Vel[iel] = np.convolve(Im, wup[iel], 'same')

    # cut
    rangeStart = inMVm - inmvm - int(np.fix(wup.shape[1] / 2))
    intervVm = np.arange(rangeStart, rangeStart + lVLFPy)
    Vel2 = Vel[:, intervVm]

    # normalize
    elsync = 55
    Vel2 = Vel2 / norm(Vel2[elsync, :]) * norm(Vlfpy[:, elsync])

    # -----------------------------------------------------------
    # plot grid
    # -----------------------------------------------------------

    cc = np.zeros((1, elpos.shape[0]))
    t = util.closed_range(dt, dt * Vel2.shape[1], dt)

    fig = plt.figure('Simulation & Neuron Morphology')
    gs = fig.add_gridspec(5, 13)

    plotNeuron(cell, fig)

    cmap = plt.cm.get_cmap('jet')
    line_labels = ["Tran", "LFPy"]
    line_obj = []
    ifil = 0

    for i in range(5):
        for j in range(13):
            ax = fig.add_subplot(gs[i, j])
            ax.axis('off')
            l1 = ax.plot(t, Vel2[ifil, :] - Vel2[ifil, 0], linewidth=2)
            l2 = ax.plot(t, Vlfpy[:, ifil] - Vlfpy[0, ifil], linewidth=2)
            if len(line_obj) < 2:
                line_obj.append(l1[0])
                line_obj.append(l2[0])
            res = np.corrcoef(Vel2[ifil].T, Vlfpy[:, ifil])[0][1]
            cc[0, ifil] = max(0, res)
            rgba = cmap(cc[0, ifil])
            color = np.array([[rgba[n] for n in range(3)]])
            plt.scatter(4, -2e-3, 50, color, 'o', cmap)
            plt.ylim(np.array([-5, 5]) * 1e-3)
            if i == 0:
                plt.text(1, 6e-3, rf'{j * 125 - 250}$\mu$m')
            if j == 0:
                plt.text(-10, -2e-3, rf'{-i * 50 + 250}$\mu$m')
            ifil += 1

    fig.legend(
        handles=line_obj,  # The line objects
        labels=line_labels,  # The labels for each line
        loc="lower left",  # Position of legend
        bbox_to_anchor=(0.1, 0),  # Anchor
        borderaxespad=0.1,  # Small spacing around legend box
    )

    plt.subplots_adjust(top=0.90, bottom=0.32)
    pos = fig.add_axes([0.75, 0.1, 0.15, 0.03])
    plt.colorbar(plt.cm.ScalarMappable(cmap=cmap),
                 cax=pos, orientation='horizontal')

    print('Mean correlation = ' + '{0:.2f}'.format(np.mean(cc)))
    print('Min correlation = ' + '{0:.2f}'.format(np.min(cc)))
    print('Max correlation = ' + '{0:.2f}'.format(np.max(cc)))

    # -----------------------------------------------------------
    # plot stimulation
    # -----------------------------------------------------------

    plotStimulation(cell, timeind, stim, meshgrid_electrodes)

    plt.show()


def main():
    """
    Executes the simulation with the following parameters
    """
    cell_parameters = {
        # 'morphology': 'resources/BSR_LA1000_DA2_LD50_DD2_demo.hoc',
        'morphology': 'resources/L5_Mainen_ax600_phi1.hoc',
        # 'morphology': 'resources/stel_Mainen_ax200.hoc',
        'v_init': -65,  # Initial membrane potential. Defaults to -70 mV
        'passive': True,  # Passive mechanisms are initialized if True
        'passive_parameters': {'g_pas': 1. / 30000, 'e_pas': -65},
        'cm': 1.0,  # Membrane capacitance
        'Ra': 150,  # Axial resistance
        'dt': 1 / 1000,  # simulation timestep
        'tstart': 0.,  # Initialization time for simulation <= 0 ms
        'tstop': 20.,  # Stop time for simulation > 0 ms
        'nsegs_method': 'lambda_f',  # spatial discretization method
        'lambda_f': 100.,  # frequency where length constants are computed
        'delete_sections': False,
    }
    cell = LFPy.Cell(**cell_parameters)

    stim_parameters = {
        'idx': cell.get_closest_idx(x=0, y=0, z=0),
        'record_current': True,
        'pptype': 'IClamp',  # Type of point process: VClamp / SEClamp / ICLamp.
        # These parameters depend on the type of point process:
        'amp': 0.2,  # nA
        'dur': 10,  # ms
        'delay': 1,  # ms
    }
    stim = LFPy.StimIntElectrode(cell, **stim_parameters)

    executeDemo(cell, stim, stim_parameters)


if __name__ == '__main__':
    main()
