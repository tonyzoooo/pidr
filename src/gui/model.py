#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""
from typing import List, Optional, Tuple

from neuron import h

class AppModel:

    def __init__(self):
        self._filename = ''
        self.sections = []  # h.SectionList()
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
               or '(' in name or ')' in name

    def tryAddSection(self, name: str) -> bool:
        if self._isInvalidName(name):
            print(f"name '{name}' is invalid")
            return False

        section = h.Section(name=name, cell='CurrentCell')
        self.sections.append(section)
        return True

    def getSection(self, name: str) -> h.Section:
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

    @property
    def sectionNames(self) -> List[str]:
        """
        Returns the section names in a list
        """
        names = []
        for sec in self.sections:
            names.append(AppModel.simpleName(sec))
        return names

    @staticmethod
    def simpleName(section: h.Section) -> str:
        return section.name().split('.')[1]

    def printSections(self):
        for section in self.sections:
            print('----------------')
            print('name:', AppModel.simpleName(section))
            print('orientation:', section.orientation())
            print('parentseg:', section.parentseg())
        print('----------------')

    #another getter for plotting
    def allsec(self):
        return self.sections
    
    @property
    def filename(self) -> str:
        """
        Returns name of filename.
        """
       
        return self._filename
    
    @filename.setter
    def filename(self, name):
        self._filename = name
        h.load_file(name)
        self.hocObject = h
        h.define_shape()
         

