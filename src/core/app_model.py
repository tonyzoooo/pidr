#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""

from neuron import h


class AppModel:

    def __init__(self):
        self.filename = ''
        self.sections = []  # h.SectionList()

    def tryAddSection(self, name: str) -> bool:
        if (name == '' or name in self.sectionNames):
            print(f"name '{name}' is invalid")
            return False

        section = h.Section(name=name, cell='CurrentCell')
        self.sections.append(section)
        return True

    def getSection(self, name: str) -> h.Section:
        for sec in self.sections:
            simpleName = sec.name().split('.')[1]
            if name == simpleName:
                return sec
        return None

    @property
    def sectionNames(self):
        """
        Returns the section names in a list
        """
        names = []
        for sec in self.sections:
            simpleName = sec.name().split('.')[1]
            names.append(simpleName)
        return names
