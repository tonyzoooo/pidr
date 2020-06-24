#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""

from neuron import h


class AppModel:

    def __init__(self):
        self.filename = ''
        # self.sectionNames = ['soma', 'dend']  # temporary
        self.sections = h.SectionList()

    def tryAddSection(self, name: str) -> bool: 
        if (name == '' or name in self.sectionNames):
            print('Invalid section name')
            return False

        section = h.Section(name=name, cell='CurrentCell')
        print('newly created ' + str(section))
        self.sections.append(section)
        return True

    @property
    def sectionNames(self):
        """
        Does not work at the moment, needs debugging
        """
        names = []
        for sec in self.sections:
            print('section' + str(sec))
            names.append(sec.name)
        return names
