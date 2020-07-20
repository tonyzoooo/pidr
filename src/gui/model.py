#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""
from enum import Enum
from typing import List, Optional, Tuple

import LFPy
from neuron import h, nrn

from src.gui import section_util


class CellSource(Enum):
    BUILDER = 1
    HOC_FILE = 2


class AppModel:

    def __init__(self):
        self._filename = None
        self.selectedSection = None
        self.cell = CellModel()
        # Cell to use for plotting and simulation
        self.cellSource = CellSource.BUILDER

    @property
    def selectedSectionName(self):
        if self.selectedSection is None:
            return None
        return section_util.simpleName(self.selectedSection)

    def trySelectSection(self, name: str) -> bool:
        section = self.cell.getSection(name)
        if section is None:
            return False
        self.selectedSection = section
        return True

    def tryAddSection(self, name: str) -> Optional[nrn.Section]:
        return self.cell.tryAddSection(name)

    def getSection(self, name: str) -> Optional[nrn.Section]:
        return self.cell.getSection(name)

    def getPossibleConnections(self, section: nrn.Section):
        result = []
        for sec in self.cell.sections:
            if sec != section:
                if sec.parentseg() is None or sec.orientation() != 0:
                    result.append((sec, 0))
                if sec.parentseg() is None or sec.orientation() != 1:
                    result.append((sec, 1))
        return result

    def hasSections(self):
        return len(self.cell.sections) != 0

    def hasHocFile(self):
        return self.filename is not None

    @property
    def sectionNames(self) -> List[str]:
        return self.cell.getSimpleNames()

    @property
    def sections(self) -> List[nrn.Section]:
        return self.cell.sections

    @property
    def filename(self) -> str:
        """
        Returns name of file.
        """
        return self._filename

    @filename.setter
    def filename(self, name):
        # Remove existing file sections if present
        for sec in h.allsec():
            if sec.cell() is None:
                h.delete_section(sec=sec)

        self._filename = name
        if name:
            print('loading file', name)
            try:
                h.load_file(1, name)
            except RuntimeError as e:
                print('load_file:', e)
            try:
                h.define_shape()
            except RuntimeError as e:
                print('define_shape:', e)

    def toSectionList(self) -> h.SectionList:
        return self.cell.toSectionList()

    def toLFPyCell(self) -> LFPy.Cell:
        return self.cell.toLFPyCell()

    def doSimulation(self):
        from src.core import demo
        source = self.cellSource
        if source is CellSource.BUILDER:
            if self.hasSections():
                cell = self.toLFPyCell()
                props = section_util.getBSProperties(self.cell.sections)
                demo.executeDemo(morphology=cell, props=props)
        elif source is CellSource.HOC_FILE:
            if self.hasHocFile():
                props = section_util.getBSProperties(section_util.fileSections())
                demo.executeDemo(morphology=self.filename, props=props)


class CellModel:
    _instancesCount = 0
    _lastInstanceCreated: Optional['CellModel'] = None

    def __init__(self):
        self.sections = []
        self.displayName = f'cell[{CellModel._instancesCount}]'
        CellModel._instancesCount += 1
        CellModel._lastInstanceCreated = self

    def getSection(self, name: str) -> Optional[nrn.Section]:
        for sec in self.sections:
            if section_util.simpleName(sec) == name:
                return sec
        return None

    def tryAddSection(self, name: str) -> Optional[nrn.Section]:
        if self._isInvalidName(name):
            print(f"name '{name}' is invalid")
            return None

        section = h.Section(name=name, cell=self)
        self.sections.append(section)
        return section

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
            # 'verbose': True
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


class IdxMode(Enum):
    CLOSEST = 1
    EXACT = 2


class StimModel:

    def __init__(self):
        # Cell segment index where the stimulation electrode is placed
        self.idxMode = IdxMode.CLOSEST
        self.closestIdx: Tuple[int, int, int] = (0, 0, 0)
        self.exactIdx: int = 0
        # Type of point process:
        # - ICLamp: Single pulse current clamp point process
        # - VClamp: Two electrode voltage clamp with three levels
        # - SEClamp: Single electrode voltage clamp with three levels
        self.pptype = 'IClamp'
        self.amp = 0
        self.dur = 0
        self.delay = 0

    def toLFPyStimIntElectrode(self, cell: LFPy.Cell) -> LFPy.StimIntElectrode:
        stim = {
            'idx': self._getIdx(cell),
            'record_current': True,
            'pptype': self.pptype,
            'amp': self.amp,
            'dur': self.dur,
            'delay': self.delay,
        }
        return LFPy.StimIntElectrode(cell, **stim)

    def _getIdx(self, cell: LFPy.Cell) -> int:
        if self.idxMode is IdxMode.CLOSEST:
            return cell.get_closest_idx(*self.closestIdx)
        elif self.idxMode is IdxMode.EXACT:
            return self.exactIdx
