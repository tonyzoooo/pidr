from pathlib import Path

from matplotlib.pyplot import figure, plot, show, subplot
from numpy import (arange, array, convolve, cos, fix, heaviside, linspace,
                   meshgrid, ndarray, pi, sin, size, zeros)
from numpy.linalg import norm

from hhrun import hhrun
from morphofiltd import morphofiltd
from util import readMatrix, upsample, reshapeMeshgrid

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
X = arange(-250, 1250+125, 125).transpose()
Y = arange(250, 50-50, -50).transpose()
Z = 0

elpos = reshapeMeshgrid(meshgrid(Y, X, Z)).transpose()

# simulation
w = morphofiltd(elpos, order, r0, r1, rN, rd, Cs)

# w is of the correct size (65x101)

# but value at [0, 0] is 3.410289076352674e-05
# but should be -3.4103e-05

# and value at [19, 19] is 5.045248610418316e-05
# but should be -1.5023e-05


wup = upsample(w.transpose(), taus).transpose()  # wup pas bon ><

Vel = zeros((len(w), len(Im)))

for iel in range(len(w)):
    Vel[iel] = convolve(Im, wup[iel], 'same')

# cut
commonPart = inMVm - inmvm - fix(wup.shape[1]/2)
rangeStart = commonPart + 1
rangeEnd = commonPart + lVLFPy
intervVm = arange(rangeStart, rangeEnd + 1)
# intervVm should be a vector of 8000 values :
# values : [4930, 4931, ..., 12928, 12929]

Vel2 = Vel[:][intervVm]
# normalize
elsync = 56
Vel2 = Vel2 / norm(Vel2[elsync][:]) * norm(Vlfpy[:][elsync])
# plot grid
cc = zeros(1, size(elpos, 1))
t = arange(dt, dt*size(Vel2, 2) + dt, dt)

"""
figure
cmap = colormap
for ifil = 1:
    size(elpos, 1),
    subplot(5, 13, ifil)
    plot(t, Vel2(ifil, :)-Vel2(ifil, 1), 'LineWidth', 2)
    hold on
    plot(t, Vlfpy(:, ifil)-Vlfpy(1, ifil), 'LineWidth', 2)
    cc(ifil) = corr(Vel2(ifil, :)', Vlfpy(: , ifil))
    scatter(4, -2*10**-3, 100, cmap(1+fix(size(cmap, 1)*cc(ifil)), : ), 'filled')
    ylim([-5 5]*10**-3)
    if ifil > 52
    text(2, -12*10**-3, [num2str((ifil-53)*125-250), '\mu', 'm'])
    end
    if rem(ifil, 13) == 1,
    text(-8, 0*10**-3, [num2str(-fix(ifil/13)*50+250), '\mu', 'm'])
    end
    axis off
end
colorbar('Position', [0.93 0.3 0.007 0.6], 'FontSize', 14)

fprintf('\n Mean correlation = %1.2f \n Min correlation = %1.2f  \n Max correlation = %1.2f \n',
        mean(cc), min(cc), max(cc))
"""
