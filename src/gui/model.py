#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""
from typing import List

from neuron import h


class AppModel:

    def __init__(self):
        self.filename = ''
        self.sections = []  # h.SectionList()
        self.selectedSection = None

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

    @staticmethod
    def tryConnect(child: h.Section, cEnd: int, parent: h.Section, pEnd: int) -> bool:
        if (cEnd not in [0, 1]) or (pEnd not in [0, 1]):
            print(f'Error: wrong indices: cEnd={cEnd}, pEnd={pEnd}')
            return False
        if child is None or parent is None:
            print(f'Error: child={child}, parent={parent}')
            return False
        child.connect(parent(pEnd), cEnd)  # May exit(1) if wrong connection
        print('connected')
        return True
    
    @staticmethod
    def disconnect(section: h.Section):
        if section is not None:
            h.disconnect(section)

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



