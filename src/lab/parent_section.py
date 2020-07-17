from neuron import h

cell = 'cell[0]'
axon = h.Section(name='axon', cell=cell)
soma = h.Section(name='soma', cell=cell)

for s in h.allsec():
    print(s)

soma.connect(axon(1), 0)

print('1)', soma.parentseg())

h.disconnect(sec=soma)

print('2)', soma.parentseg())

soma.connect(axon(1), 0)

print('3)', soma.parentseg())
