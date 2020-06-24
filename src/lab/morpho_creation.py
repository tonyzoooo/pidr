# https://neuron.yale.edu/neuron/docs/ball-and-stick-model-part-1

import matplotlib.pyplot as plt
from neuron import h
from neuron.units import ms, mV

h.load_file('stdrun.hoc')


class BallAndStick:

    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()

    def _setup_morphology(self):
        self.sectionList = h.SectionList()
        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)
        self.sectionList.append(self.soma)
        self.sectionList.append(self.dend)
        # self.sectionList.printnames()
        self.dend.connect(self.soma)
        self.soma.L = self.soma.diam = 12.6157
        self.dend.L = 200
        self.dend.diam = 1

    def _setup_biophysics(self):
        for sec in self.sectionList:
            sec.Ra = 100    # Axial resistance in Ohm * cm
            sec.cm = 1      # Membrane capacitance in micro Farads / cm^2
        self.soma.insert('hh')
        for seg in self.soma:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003    # Leak conductance in S/cm2
            seg.hh.el = -54.3     # Reversal potential in mV
        # Insert passive current in the dendrite
        self.dend.insert('pas')
        for seg in self.dend:
            seg.pas.g = 0.001  # Passive conductance in S/cm2
            seg.pas.e = -65    # Leak reversal potential mV

    def __repr__(self):
        return f'BallAndStick[{self._gid}]'


cell = BallAndStick(0)

# print(cell.soma(0.5).area())
h.topology()

# False to use another graphics engine than the built-in one
ps = h.PlotShape(False)

# only works with NEURON built-in graphics
# ps.show(0)

ps.plot(plt)
plt.show()

