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

    def tryAddSection(self, name: str) -> bool:
        if name == '' or name in self.sectionNames:
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

    def trySetParent(self, child: h.Section, cEnd: int, parent: h.Section, pEnd: int) -> bool:
        if (cEnd not in [0, 1]) or (pEnd not in [0, 1]):
            print(f'Error: wrong indices: cEnd={cEnd}, pEnd={pEnd}')
            return False
        if child is None or parent is None:
            print(f'Error: child={child}, parent={parent}')
            return False
        # TODO: Disconnect actual parent (if present) before connecting another
        child.connect(parent(pEnd), cEnd)  # May exit(1) if wrong connection
        return True
    
    def disconnect(self, section: h.Section):
        if section is not None:
            h.disconnect(section)

    @staticmethod
    def getParent(section: h.Section) -> Optional[h.Section]:
        # par = section.parentseg()
        # 'area', 'cm', 'diam', 'node_index', 'point_processes', 'ri', 'sec', 'v', 'volume', 'x'
        parentSegment = section.parentseg()
        if parentSegment is None:
            return None
        return parentSegment.sec

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
         

