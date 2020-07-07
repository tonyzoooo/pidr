from typing import Optional, List

import LFPy
from neuron import h, nrn

from src.gui import section_util


class CellModel:
    _instancesCount = 0

    def __init__(self):
        self.sections = []
        self.displayName = f'cell[{CellModel._instancesCount}]'
        CellModel._instancesCount += 1

    def getSection(self, name: str) -> Optional[nrn.Section]:
        for sec in self.sections:
            if section_util.simpleName(sec) == name:
                return sec
        return None

    def tryAddSection(self, name: str) -> bool:
        if self._isInvalidName(name):
            print(f"name '{name}' is invalid")
            return False

        section = h.Section(name=name, cell=self)
        self.sections.append(section)
        return True

    def _isInvalidName(self, name):
        return name == '' or name in self.getSimpleNames() \
               or '(' in name or ')' in name or '.' in name

    def getSimpleNames(self) -> List[str]:
        return [section_util.simpleName(sec) for sec in self.sections]

    def toSectionList(self) -> h.SectionList:
        secList = h.SectionList(self.sections)
        h.define_shape()
        return secList

    def toLFPyCell(self) -> LFPy.Cell:
        sectionList = self.clone().toSectionList()
        cell_parameters = {
            'morphology': sectionList,
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
            'verbose': True
        }
        return LFPy.Cell(**cell_parameters)

    def clone(self) -> 'CellModel':
        copy = CellModel()
        copy.sections = [CellModel._cloneSection(sec, copy) for sec in self.sections]
        # same connections
        for clonedSec, sec in zip(copy.sections, self.sections):
            parentConnection = section_util.getParent(sec)
            if parentConnection is not None:
                childEnd, parent, parentEnd = parentConnection
                clonedParent = CellModel._findSimilarSection(copy.sections, parent)
                section_util.setParent(clonedSec, (childEnd, clonedParent, parentEnd))
        return copy

    @staticmethod
    def _cloneSection(section: nrn.Section, cellName: 'CellModel') -> nrn.Section:
        name = section_util.simpleName(section)
        clone = h.Section(name=name, cell=cellName)
        clone.nseg = section.nseg
        clone.diam = section.diam
        clone.L = section.L
        section_util.setMechanism(clone, section_util.getMechanism(section))
        return clone

    @staticmethod
    def _findSimilarSection(secList: h.SectionList, section: nrn.Section) -> Optional[nrn.Section]:
        for s in secList:
            if section_util.simpleName(s) == section_util.simpleName(section):
                return s
        return None

    def printDebug(self):
        print(f'-----{self.displayName}-----')
        for section in self.sections:
            print('name:', section_util.simpleName(section))
            print('orientation:', section.orientation())
            print('parentseg:', section.parentseg())
            print('nseg:', section.nseg)
            print('diam:', section.diam)
            print('L:', section.L)
            print('mechanism:', section_util.getMechanism(section))
            print('-----')

    def __str__(self):
        return self.displayName
