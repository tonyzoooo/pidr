from interface import *

import matplotlib.pyplot as plt
import numpy as np
from numpy import pi
from numpy.linalg import norm

import util
from demo_github import getStimulationResult, plotStimulation, plotNeuron
from hhrun import hhrun
from morphofiltd import morphofiltd

# -----------------------------------------------------------
# HH (Hodgkin–Huxley model)
# -----------------------------------------------------------

inmvm = 3000    # index max on Vm in LFPy (3000 for synchronisation)
lVLFPy = 8000   # signal length in LFPy
dt = 10**(-3)   # in ms
Nt = 2**15
D = Nt*dt
t = np.arange(dt, D+dt, dt)-dt
n = len(t)

fe = 1/dt
f = np.arange(0, fe/2, fe/Nt)

I = (
    (np.heaviside(t-1, 1/2)-np.heaviside(t-31, 1/2))
    * 0.044 / (2*pi*12.5*25) * 10**8*10**-3
    # * 5.093 # 0.15/(pi*12.5*12.5*2+2*pi*12.5*25)*10**8
)
icur = 1

# pot membrane, proportional to ion channels electric current
# (http://www.bem.fi/book/03/03.htm, 3.14)
[Vm, m, n, h, INa, IK, Il] = hhrun(I, t)

Im = (INa+IK+Il) * (2*pi*12.5*25) / 10**8 * 10**3
inMVm = np.argmax(Vm)
MVm = Vm[inMVm]

# -----------------------------------------------------------
# BS neuron morphology
# -----------------------------------------------------------

SL = 25     # soma length (cylinder with the same diameter)

LA = 1000   # axon length
DA = 2      # axon diameter

LD = 50     # dendrite length
DD = 2      # dendrite diameter
phi = pi/2  # angle avec Oz
theta = pi  # angle with Ox (phi=pi/2,theta=pi) indicates opposite to the axon

# -----------------------------------------------------------
# load LFPy simulation result
# -----------------------------------------------------------

# data = Path('data/')  # os independent path
# Vlfpy = util.readMatrix(data / f'Vlfpy_BS_LA{LA}_DA{DA}_LD{LD}_DD{DD}demo.txt')
# Vmlfpy = util.readMatrix(data / f'Vm_BS_LA{LA}_DA{DA}_LD{LD}_DD{DD}demo.txt')
# Imlfpy = util.readMatrix(data / f'Im_BS_LA{LA}_DA{DA}_LD{LD}_DD{DD}demo.txt')

root = tk.Tk()
main = App(root)
root.mainloop()


result = getStimulationResult(main.filename)

Vlfpy = result.Vlfpy
Vmlfpy = result.Vmlfpy
Imlfpy = result.Imlfpy

cell = result.cell
timeind = result.timeind
stimulus = result.stimulus
meshgrid_electrodes = result.meshgrid_electrodes

# -----------------------------------------------------------
# figure check
# -----------------------------------------------------------

values = np.arange(inMVm-inmvm, inMVm-inmvm+lVLFPy)

fig = plt.figure('Simulation result')


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

# plt.show()

# -----------------------------------------------------------
# filter parameters
# -----------------------------------------------------------

dk = 10     # axonal spatial sampling(~ nb of segments)

order = int(LA/dk+1)
r0 = np.array([0, 0, 0])           # soma position
r1 = np.array([SL/2, 0, 0])        # axon start position
# axon stop position (start of the last segment)
rN = np.array([SL/2+LA-dk, 0, 0])
rd = norm(r1-r0) * np.array([
    np.sin(phi) * np.cos(theta),
    np.sin(phi) * np.sin(theta),
    np.cos(phi)
])          # dendrite end position, normalized
Cs = 2      # somatic equivalent dipole amplitude
taus = 23   # subsampling of the membrane current dk/taus = speed v)

# -----------------------------------------------------------
# electrodes
# -----------------------------------------------------------

X = np.arange(-250, 1250+125, 125)
Y = np.arange(250, 50-50, -50)
Z = 0

elpos = util.reshapeMeshgrid(np.meshgrid(X, Y, Z)).transpose()

# -----------------------------------------------------------
# simulation
# -----------------------------------------------------------

w = morphofiltd(elpos, order, r0, r1, rN, rd, Cs)
wup = util.upsample(w.transpose(), taus).transpose()

Vel = np.zeros((len(w), len(Im)))

for iel in range(len(w)):
    Vel[iel] = np.convolve(Im, wup[iel], 'same')

# cut
commonPart = inMVm - inmvm - int(np.fix(wup.shape[1]/2))
rangeStart = commonPart + 1
rangeEnd = commonPart + lVLFPy
intervVm = np.arange(rangeStart, rangeEnd + 1)
Vel2 = Vel[:, intervVm]

# normalize
elsync = 55
Vel2 = Vel2 / norm(Vel2[elsync, :]) * norm(Vlfpy[:, elsync])

# -----------------------------------------------------------
# plot grid
# -----------------------------------------------------------

cc = np.zeros((1, elpos.shape[0]))
t = np.arange(0, dt * Vel2.shape[1], dt)

fig = plt.figure('Simulation & Neuron Morphology')
# plt.title('Simulation & Neuron Morphology')
gs = fig.add_gridspec(5,  13)

plotNeuron(cell, meshgrid_electrodes, fig)

cmap = plt.cm.get_cmap('jet')
line_labels = ["Cell", "Tran", "LFPy"]
line_obj = []
ifil = 0
for i in range(5):
    for j in range(13):
        ax = fig.add_subplot(gs[i, j])
        ax.axis('off')
        l1 = ax.plot(t, Vel2[ifil]-Vel2[ifil, 0], linewidth=2)[0]
        l2 = ax.plot(t, Vlfpy[:, ifil]-Vlfpy[0, ifil], linewidth=2)[0]
        if len(line_obj) < 2:
            line_obj.append(l1)
            line_obj.append(l2)
        cc[0, ifil] = np.corrcoef(Vel2[ifil].transpose(), Vlfpy[:, ifil])[0][1]
        rgba = cmap(cc[0, ifil])
        color = np.array([[rgba[n] for n in range(3)]])
        plt.scatter(4, -2e-3, 50, color, 'o', cmap)
        plt.ylim(np.array([-5, 5]) * 1e-3)
        if i == 0:
            plt.text(1, 6e-3, str(j*125-250) + r'$\mu$m')
        if j == 0:
            plt.text(-10, -2e-3, str(-i*50+250) + r'$\mu$m')
        ifil += 1

fig.legend(
    line_obj,                   # The line objects
    labels=line_labels,         # The labels for each line
    loc="lower left",           # Position of legend
    bbox_to_anchor=(0.1, 0.05), # Anchor
    borderaxespad=0.1,          # Small spacing around legend box
    title="Legend"              # Title for the legend
)

# plt.subplots_adjust(right=0.82)
# pos = fig.add_axes([0.88, 0.1, 0.02, 0.75])
# plt.colorbar(plt.cm.ScalarMappable(cmap=cmap), cax = pos, orientation='vertical')
plt.subplots_adjust(top=0.90, bottom=0.32)
pos = fig.add_axes([0.75, 0.1, 0.15, 0.03])
plt.colorbar(plt.cm.ScalarMappable(cmap=cmap),
             cax=pos, orientation='horizontal')


# plt.show()

print('Mean correlation = ' + '{0:.2f}'.format(np.mean(cc)))
print('Min correlation = ' + '{0:.2f}'.format(np.min(cc)))
print('Max correlation = ' + '{0:.2f}'.format(np.max(cc)))

# -----------------------------------------------------------
# plot stimulation
# -----------------------------------------------------------

plotStimulation(cell, timeind, stimulus, meshgrid_electrodes)

plt.show()
