#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""
from typing import List, Optional

import LFPy
from neuron import h


class AppModel:

    def __init__(self):
        self._filename = ''
        self.sections = []
        self.selectedSection = None
        self.hocObject = None

    @property
    def selectedSectionName(self):
        if self.selectedSection is None:
            return None
        return AppModel.simpleName(self.selectedSection)

    def trySelectSection(self, name: str) -> bool:
        section = self.getSection(name)
        if section is None:
            return False
        self.selectedSection = section
        return True

    def _isInvalidName(self, name):
        return name == '' or name in self.sectionNames \
               or '(' in name or ')' in name or '.' in name

    def tryAddSection(self, name: str) -> bool:
        if self._isInvalidName(name):
            print(f"name '{name}' is invalid")
            return False

        section = h.Section(name=name, cell='cell')
        self.sections.append(section)
        return True

    def getSection(self, name: str) -> Optional[h.Section]:
        for sec in self.sections:
            if name == AppModel.simpleName(sec):
                return sec
        return None

    def setParent(self, child: h.Section, cEnd: int, parent: h.Section, pEnd: int):
        # TODO: Disconnect actual parent (if present) before connecting another
        h.disconnect(child)
        print(f"connect({child}, {cEnd}, {parent}, {pEnd})")
        child.connect(parent(pEnd), cEnd)  # May exit(1) if wrong connection

    def getPossibleConnections(self, section: h.Section):
        result = []
        for sec in self.sections:
            if sec != section:
                if sec.parentseg() is None or sec.orientation() != 0:
                    result.append((sec, 0))
                if sec.parentseg() is None or sec.orientation() != 1:
                    result.append((sec, 1))
        return result

    def hasSections(self):
        return len(self.sections) != 0

    @property
    def sectionNames(self) -> List[str]:
        return [AppModel.simpleName(s) for s in self.sections]

    @staticmethod
    def simpleName(section: h.Section) -> str:
        return section.name().split('.')[-1]

    @staticmethod
    def getMechanism(section: h.Section) -> Optional[str]:
        firstSegment = next(iter(section))
        return 'hh' if hasattr(firstSegment, 'hh') \
            else 'pas' if hasattr(firstSegment, 'pas') \
            else None

    @staticmethod
    def setMechanism(section: h.Section, mech: Optional[str]):
        actual = AppModel.getMechanism(section)
        if mech == actual:
            return
        if actual is not None:
            section.uninsert(actual)
        if mech is not None:
            section.insert(mech)

    def printSections(self):
        for section in self.sections:
            print('----------------')
            print('name:', AppModel.simpleName(section))
            print('orientation:', section.orientation())
            print('parentseg:', section.parentseg())
        print('----------------')

    # another getter for plotting
    def allsec(self):
        return self.sections

    @property
    def filename(self) -> str:
        """
        Returns name of file.
        """
        return self._filename

    @filename.setter
    def filename(self, name):
        self._filename = name
        h.load_file(name)
        self.hocObject = h
        h.define_shape()

    def toSectionList(self) -> h.SectionList:
        sectionList = h.SectionList()
        for s in self.sections:
            sectionList.append(s)
        h.define_shape()
        return sectionList

    def toLFPyCell(self) -> LFPy.Cell:
        sectionList = self.toSectionList()
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
            # 'verbose': True
        }
        return LFPy.Cell(**cell_parameters)
