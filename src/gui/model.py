#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""
from typing import List, Optional

import LFPy
from neuron import h, nrn

from src.gui import section_util
from src.gui.cell_model import CellModel


class AppModel:

    def __init__(self):
        self._filename = ''
        self.selectedSection = None
        self.hocObject = None
        self.cell = CellModel()

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
        h.load_file(name)
        self.hocObject = h
        h.define_shape()

    def toSectionList(self) -> h.SectionList:
        return self.cell.toSectionList()

    def toLFPyCell(self) -> LFPy.Cell:
        return self.cell.toLFPyCell()
