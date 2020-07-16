from neuron import h

from model import CellModel


def sectionsFromCell(cell: CellModel):
    return [s for s in h.allsec() if s.cell() is cell]


def sectionsFromFile():
    return [s for s in h.allsec() if s.cell() is None]


def test():
    cell = CellModel()
    cell.tryAddSection('soma')
    cell.tryAddSection('axon')
    cell.tryAddSection('dend')
    soma = cell.getSection('soma')
    axon = cell.getSection('axon')
    dend = cell.getSection('dend')
    soma.nseg = 1
    soma.L = 25
    soma.diam = 25
    soma.insert('hh')
    axon.nseg = 100
    axon.L = 1000
    axon.diam = 2
    axon.insert('hh')
    dend.nseg = 5
    dend.L = 50
    dend.diam = 2
    dend.insert('pas')
    axon.connect(soma(1), 0)
    dend.connect(soma(0), 1)

    copy = cell.clone()

    h.load_file('../../resources/BSR_LA1000_DA2_LD50_DD2_demo.hoc')

    print('--1--')
    for s in h.allsec():
        print(s)

    print('--2--')
    for s in cell.sections:
        print(s)

    print('--3--')
    for s in sectionsFromFile():
        print(s)

    print('--4--')
    for s in sectionsFromCell(copy):
        print(s)


test()
