import math
import os

import LFPy
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from matplotlib.collections import PolyCollection
#import scipy
#from scipy.signal import butter, lfilter
#import matplotlib.animation as animation
from neuron import h


def PolyArea(x, y):
    return 0.5*np.abs(np.dot(x, np.roll(y, 1))-np.dot(y, np.roll(x, 1)))


def plotNeuron(cell, electrode, fig):
    '''plotting'''
    #fig = plt.figure(2)
    #fig.canvas.set_window_title('Neuron Morphology')
    # plt.plot(electrode.x, electrode.y, '.',  marker='o',
    #          markersize=3, color='r', zorder=0)
    #    rotation = {'x' : 0, 'y' : math.pi, 'z' : 0} #-math.pi/9 # Mainen
    #    cell.set_rotation(**rotation)
    # Plot neuron morphology
    zips = []
    for x, y in cell.get_idx_polygons(projection=('x', 'y')):
        # PATCH Radu do not plot big boxes
        #        tmp=list(zip(x,y))
        #        if not 250 in tmp[1]:
        if PolyArea(x, y) < 10000:
            zips.append(list(zip(x, y)))
        # END PATCH
    polycol = PolyCollection(zips, edgecolors='#999999', facecolors='#666666', linewidths=1.7)
    ax = fig.add_subplot(111)
    ax.patch.set_visible(False)
    ax.axis('off')
    ax.add_collection(polycol)
    ax.axis(ax.axis('equal'))

    #plt.xlabel(r'Distance $\mu$m - (Ox)')
    #plt.ylabel(r'Distance $\mu$m - (0y) ')
    #plt.grid(True)
    #plt.title(r'$Neuron$ $Morphology$')
    return fig  

def getStimulationResult(filename):
    # =============================================================================
    # ================================= MORPHOLOGY ================================
    # =============================================================================

    LA = "1000"
    DA = "2"
    LD = "50" 
    DD = "2"

    st = 1/1000

    # filename = f'../resources/BSR_LA{LA}_DA{DA}_LD{LD}_DD{DD}_demo.hoc'
    # filename = '../resources/BSR_LA1000_DA2_LD50_DD2_demo.hoc'
    # filename = '../resources/stel_Mainen_ax200.hoc'
    cell_parameters = {
        'morphology': filename,
        'v_init': -65,
        'passive': True,
        'passive_parameters': {'g_pas': 1./30000, 'e_pas': -65},
        'cm': 1.0,
        'Ra': 150,
        'dt': st,
        'tstart': 0.,
        'tstop': 20.,
        'nsegs_method': 'lambda_f',  # spatial discretization method
        'lambda_f': 100.,  # frequency where length constants are computed
    }
    cell = LFPy.Cell(**cell_parameters)

    # =============================================================================
    # ================================= stimulation parameters================================
    # =============================================================================

    amp = 0.2
    dur = 10
    delay = 1
    #                if cell_parameters["passive"]==False:
    #                    amp=1.95**(int(ida)/1.95)/30+1.6*int(ila)/10000+int(ild)/5000*int(idd)*1.5
    #                else:
    #                    amp=1.65**(int(ida)/1.95)/30+0.805*int(ila)/10000+int(ild)/5000*int(idd)*1.1 #-0.4 for Mainen equivalent

    stim = {
        'idx': cell.get_closest_idx(x=0, y=0, z=0),
        'record_current': True,
        'pptype': 'IClamp',
        'amp': amp,
        'dur': dur,  # 0.01
        'delay': delay,  # 5
    }


    stimulus = LFPy.StimIntElectrode(cell, **stim)


    # =============================================================================
    # ================================= SIMULATION  ===============================
    # =============================================================================


    cell.simulate(rec_imem=True)
    # cell.imem[np.isnan(cell.imem)]=0.0


    # =============================================================================
    # ================================= electrodes ================================
    # =============================================================================

    hstep = np.array(range(-250, 1251, 125))
    vstep = np.array(range(250, 49, -50))
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


    # =============================================================================
    # ================================= plot and save  ===============================
    # =============================================================================

    timeind = (cell.tvec > np.argmax(cell.somav)*st -
            3) & (cell.tvec <= np.argmax(cell.somav)*st+5)


    # fileout="Vlfpy_BS"+"_LA"+LA+"_DA"+DA+"_LD"+LD+"_DD"+DD+"demo.txt"
    # np.savetxt(fileout,meshgrid_electrodes.LFP.T[timeind])
    Vlfpy = meshgrid_electrodes.LFP.T[timeind]

    # fileout2="Vm_BS"+"_LA"+LA+"_DA"+DA+"_LD"+LD+"_DD"+DD+"demo.txt"
    # np.savetxt(fileout2,cell.somav[timeind])
    Vmlfpy = cell.somav[timeind]

    # fileout3="Im_BS"+"_LA"+LA+"_DA"+DA+"_LD"+LD+"_DD"+DD+"demo.txt"
    # np.savetxt(fileout3,cell.imem[0,timeind])
    Imlfpy = cell.imem[0,timeind]

    # elpos=(x_elec,y_elec,z_elec)
    # np.savetxt("elpos_demo",elpos)
    res = StimulationResult()
    res.Vlfpy = Vlfpy
    res.Vmlfpy = Vmlfpy
    res.Imlfpy = Imlfpy
    res.cell = cell
    res.timeind = timeind
    res.stimulus = stimulus
    res.meshgrid_electrodes = meshgrid_electrodes
    return res

class StimulationResult:
    Vlfpy = None
    Vmlfpy = None
    Imlfpy = None
    cell = None
    timeind = None
    stimulus = None
    meshgrid_electrodes = None

def plotStimulation(cell, timeind, stimulus, meshgrid_electrodes):
    fig = plt.figure('Stimulation')

    # ================= STIMULATION PLOT ==========================================
    plt.subplot(411)
    pl.plot(cell.tvec[timeind], stimulus.i[timeind])
    plt.axis('tight')
    plt.ylabel(r'$I_s$ (nA)', va='center')
    plt.grid(True)
    # ================= SOMA PLOT =================================================
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

    # ================= ELECTRODE LFP  ============================================
    plt.subplot(414)
    # ,label='x='+str(elec_parameters["x"])+' - y='+str(elec_parameters["y"]))
    plt.plot(cell.tvec[timeind], meshgrid_electrodes.LFP.T[timeind], lw=1)
    plt.ylabel(r'$V_e$ (mV)', va='center')
    plt.xlabel('time (ms)')
    plt.grid(True)
    return fig
