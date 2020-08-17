#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""

from tkinter import *
from tkinter.ttk import *
from typing import Iterable, Tuple

from src.app.model import AppModel, SectionModel
from src.app.number_validation import safeFloat, addFloatValidation, addIntValidation, safeInt


class ConfigView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for the configuration of the selected section

        :param master: parent container
        :param model: app model
        """
        super().__init__(master)
        self.model = model

        self.selectedSectionLabel = Label(self, text='<no section>')
        self.selectedSectionLabel.grid(row=0, column=1, columnspan=2)

        intSpinArgs = {'from_': 1, 'to': 1e10, 'increment': 1, 'validate': 'focusout'}
        floatSpinArgs = {'from_': 0, 'to': 1e10, 'increment': 0.1, 'validate': 'focusout'}
        labelArgs = {'sticky': 'e', 'padx': 4, 'pady': 4}
        entryArgs = {'sticky': 'ew', 'padx': 4, 'pady': 4}

        Label(self, text='nseg').grid(row=1, **labelArgs)
        self.nsegVar = IntVar(value=1)
        nsegEntry = Spinbox(self, textvariable=self.nsegVar, **intSpinArgs)
        nsegEntry.grid(row=1, column=1, columnspan=2, **entryArgs)
        nsegEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addIntValidation(nsegEntry, from_=1, to=32767)

        self.lengthVar, self.diamVar = (DoubleVar(value=1.0) for _ in [1, 2])
        for row, lbl, var in (2, 'L', self.lengthVar), (3, 'diam', self.diamVar):
            Label(self, text=lbl).grid(row=row, **labelArgs)
            spinBox = Spinbox(self, textvariable=var, **floatSpinArgs)
            spinBox.grid(row=row, column=1, columnspan=2, **entryArgs)
            spinBox.bind('<FocusOut>', lambda e: self.saveCurrentSection())
            Label(self, text='µm').grid(row=row, column=3, padx=4, pady=4, sticky='w')
            addFloatValidation(spinBox, from_=1e-9)

        Label(self, text='parent').grid(row=4, **labelArgs)
        self.endMenu = Combobox(self, values=[0, 1], width=1, state="readonly")
        self.endMenu.current(0)
        self.endMenu.grid(row=4, column=1, **entryArgs)
        self.endMenu.bind('<<ComboboxSelected>>', lambda e: self.saveCurrentSection())
        self.parentMenu = Combobox(self, values=[''], width=10, state="readonly")
        self.parentMenu.grid(row=4, column=2, **entryArgs)
        self.parentMenu.bind('<<ComboboxSelected>>', lambda e: self.saveCurrentSection())

        Label(self, text='mechanism').grid(row=5, **labelArgs)
        self.mechMenu = Combobox(self, values=['', 'hh', 'pas'], state="readonly")
        self.mechMenu.grid(row=5, column=1, columnspan=2, **entryArgs)

    def refreshView(self):
        """
        Refreshes the section configuration view using:
        - the currently selected section in self.sectionList
        - the data of the corresponding section in the model (self.model)
        """
        name = self.model.selectedSectionName
        self.selectedSectionLabel.configure(text=name)
        section = self.model.selectedSection
        if section is None:
            return

        self.nsegVar.set(section.nseg)
        self.lengthVar.set(section.L)
        self.diamVar.set(section.diam)

        values = ['']
        for (parent, end) in self.model.getPossibleConnections(section):
            name = parent.name
            values.append(f'{name}({end})')
        _setComboboxValues(self.parentMenu, values)

        if section.parentSec is None:
            self.endMenu.current(0)  # sets first (default) index
            self.parentMenu.set('')
        else:
            parentName = section.parentSec.name
            parentEnd = section.parentEnd
            self.endMenu.set(section.childEnd)
            self.parentMenu.set(f'{parentName}({parentEnd})')

        self.mechMenu.set(section.mechanism or '')

    def saveCurrentSection(self):
        """
        Saves the current section's data into the model
        """
        section = self.model.selectedSection
        if section is None:
            return

        section.nseg = safeInt(self.nsegVar.get, orElse=section.nseg, from_=1, to=32766)
        section.diam = safeFloat(self.diamVar.get, orElse=section.diam, from_=1e-9)
        section.L = safeFloat(self.lengthVar.get, orElse=section.L, from_=1e-9)

        parentOption = self.parentMenu.get()
        if parentOption == '':
            section.parentSec = None
        else:
            childEnd = int(self.endMenu.get())
            parent, parentEnd = self._parseParentValue(parentOption)
            section.connect(parent, parentEnd, childEnd)

        section.mechanism = self.mechMenu.get() or None

    def _parseParentValue(self, option: str) -> Tuple[SectionModel, int]:
        [name, number] = option.split('(')
        section = self.model.getSection(name)
        n = int(number[0:-1])
        return section, n


def _setComboboxValues(combobox: Combobox, values: Iterable):
    valueBefore = combobox.get()
    combobox['values'] = values
    if valueBefore not in values:
        combobox.current(0)  # select first element
