#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""
from enum import Enum
from typing import List, Optional

import LFPy
from neuron import h, nrn

from src.core import demo
from src.gui import section_util
from src.gui.cell_model import CellModel


class AppModel:

    def __init__(self):
        self._filename = None
        self.selectedSection = None
        self.hocObject = None
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

    def tryAddSection(self, name: str) -> bool:
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

    # another getter for plotting
    def allsec(self) -> List[nrn.Section]:
        return self.cell.sections

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
        self._filename = name
        if name:
            h.load_file(name)
            self.hocObject = h
            h.define_shape()

    def toSectionList(self) -> h.SectionList:
        return self.cell.toSectionList()

    def toLFPyCell(self) -> LFPy.Cell:
        return self.cell.toLFPyCell()

    def doSimulation(self):
        source = self.cellSource
        if source is CellSource.BUILDER:
            if self.hasSections():
                cell = self.toLFPyCell()
                demo.executeDemo(cell)
        elif source is CellSource.HOC_FILE:
            if self.hasHocFile():
                demo.executeDemo(self.filename)


class CellSource(Enum):
    BUILDER = 1
    HOC_FILE = 2
