from pathlib import Path

from matplotlib.pyplot import (axis, colorbar, colormaps, figure, plot,
                               scatter, show, subplot, text, ylim, cm, savefig, imshow, subplots)
from numpy import (arange, array, convolve, corrcoef, cos, fix, heaviside,
                   linspace, mean, meshgrid, ndarray, pi, sin, size, zeros, min, max)
from numpy.linalg import norm
from matplotlib.image import imread

from hhrun import hhrun
from morphofiltd import morphofiltd
from util import readMatrix, reshapeMeshgrid, upsample

# Programme principal
# HH
inmvm = 3000    # index max on Vm in LFPy (3000 for synchronisation)
lVLFPy = 8000   # signal length in LFPy
dt = 10**(-3)   # in ms
Nt = 2**15
D = Nt*dt
t = arange(dt, D+dt, dt)-dt
n = len(t)

fe = 1/dt
f = arange(0, fe/2, fe/Nt)

I = (heaviside(t-1, 1/2)-heaviside(t-31, 1/2)) * 0.044 / (2*pi*12.5*25) * \
    10**8*10**-3  # *5.093 # 0.15/(pi*12.5*12.5*2+2*pi*12.5*25)*10**8
icur = 1
# pot membrane, proportionnel au courant des canaux ioniques (http://www.bem.fi/book/03/03.htm, 3.14)
[Vm, m, n, h, INa, IK, Il] = hhrun(I, t)
Im = (INa+IK+Il)*(2*pi*12.5*25)/10**8*10**3

MVm = max(Vm)
inMVm = 0
while Vm[inMVm] != MVm:
    inMVm += 1

# BS neuron morphology

SL = 25     # soma length (cylinder with the same diameter)

LA = 1000   # axon length
DA = 2      # axon diameter

LD = 50     # dendrite length
DD = 2      # dendrite diameter
phi = pi/2  # angle avec Oz
theta = pi  # angle with Ox (phi=pi/2,theta=pi) indicates opposite to the axon

# load LFPy simulation result
data = Path('data/')  # os independent path
Vlfpy = readMatrix(data / f'Vlfpy_BS_LA{LA}_DA{DA}_LD{LD}_DD{DD}demo.txt')
Vmlfpy = readMatrix(data / f'Vm_BS_LA{LA}_DA{DA}_LD{LD}_DD{DD}demo.txt')
Imlfpy = readMatrix(data / f'Im_BS_LA{LA}_DA{DA}_LD{LD}_DD{DD}demo.txt')

# figure check
values = arange(inMVm-inmvm, inMVm-inmvm+lVLFPy)

figure()

subplot(2, 1, 1)
plot(Vm[values])
plot(Vmlfpy)

subplot(2, 1, 2)
plot(Im[values])
plot(Imlfpy)

# show()

# filter parameters
dk = 10
# axonal spatial sampling(~ nb of segments)
order = int(LA/dk+1)
r0 = array([0, 0, 0])
# soma position
r1 = array([SL/2, 0, 0])
# axon start position
rN = array([SL/2+LA-dk, 0, 0])
# axon stop position(start of the last segment)
rd = norm(r1-r0) * array([sin(phi)*cos(theta), sin(phi)*sin(theta), cos(phi)])
# dendrite end position, normalized
Cs = 2
# somatic equivalent dipole amplitude
taus = 23
# subsampling of the membrane current dk/taus = speed v)

# electrodes
X = arange(-250, 1250+125, 125)
Y = arange(250, 50-50, -50)
Z = 0

elpos = reshapeMeshgrid(meshgrid(X, Y, Z)).transpose()

# simulation
w = morphofiltd(elpos, order, r0, r1, rN, rd, Cs)
wup = upsample(w.transpose(), taus).transpose()

Vel = zeros((len(w), len(Im)))

for iel in range(len(w)):
    Vel[iel] = convolve(Im, wup[iel], 'same')

# cut
commonPart = inMVm - inmvm - int(fix(wup.shape[1]/2))
rangeStart = commonPart + 1
rangeEnd = commonPart + lVLFPy
intervVm = arange(rangeStart, rangeEnd + 1)
Vel2 = Vel[:, intervVm]

# normalize
elsync = 55
Vel2 = Vel2 / norm(Vel2[elsync, :]) * norm(Vlfpy[:, elsync])

# plot grid
cc = zeros((1, elpos.shape[0]))
t = arange(0, dt * Vel2.shape[1], dt)


fig, ax = subplots()

cmap = cm.get_cmap('jet')

for ifil in range(elpos.shape[0]):
    subplot(5, 13, ifil+1)
    plot(t, Vel2[ifil]-Vel2[ifil, 0], linewidth=2 )
    plot(t, Vlfpy[:, ifil]-Vlfpy[0, ifil], linewidth=2)
    a= corrcoef(Vel2[ifil].transpose(), Vlfpy[:, ifil])[0][1]
    cc[0, ifil] = corrcoef(Vel2[ifil].transpose(), Vlfpy[:, ifil])[0][1]
    rgba = cmap(cc[0, ifil])
    color = array([[rgba[i] for i in range(3)]])
    scatter(4, -2 * 10**-3, 50, color , 'o', cmap )
    ylim(array([-5, 5]) * 10**-3)
    if ifil > 51:
        text(2, -12*10**-3, str((ifil-53)*125-250+125) + '\u03BCm')
    if ifil % 13 == 0:
        text(-8, 0*10**-3, str(-fix(ifil/13)*50+250) + '\u03BCm')
    axis('off')

fig.savefig('simulation_results.png', bbox_inches='tight')
im = imread('simulation_results.png')

pos = fig.add_axes([0.93,0.1,0.02,0.8]) 


im = ax.imshow(im, cmap = cmap)
fig.colorbar(im, cax=pos, orientation='vertical')

fig.savefig('simulation_results.png', bbox_inches='tight')

print('Mean correlation =' +  '{0:.2f}'.format(mean(cc)))
print('Min correlation =' +  '{0:.2f}'.format(min(cc)))
print('Max correlation =' +  '{0:.2f}'.format(max(cc)))
