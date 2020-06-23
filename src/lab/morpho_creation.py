from neuron import h
from neuron.units import ms, mV

h.load_file('stdrun.hoc')


class BallAndStick:

    def __init__(self, gid):
        self._gid = gid
        self.soma = h.Section(name='soma', cell=self)
        self.dend = h.Section(name='dend', cell=self)

    def __repr__(self):
        return f'BallAndStick[{self._gid}]'


cell0 = BallAndStick(0)
cell1 = BallAndStick(1)

h.topology()
