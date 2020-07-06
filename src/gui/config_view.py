from tkinter import *
from tkinter.ttk import *
from typing import Iterable, Tuple

from neuron import nrn

from src.gui.model import AppModel
from src.gui.number_validation import safeFloat, addFloatValidation, addIntValidation, safeInt


class ConfigView(Frame):

    def __init__(self, root: Tk, model: AppModel):
        """
        Container for the configuration of the selected section
        """
        super().__init__(root)
        self.root = root
        self.model = model

        self.selectedSectionLabel = Label(self, text='<no section>')
        self.selectedSectionLabel.grid(row=0, column=1, columnspan=2)

        intSpinArgs = {'from_': 1, 'to': 1e10, 'increment': 1, 'validate': 'focusout'}
        floatSpinArgs = {'from_': 0, 'to': 1e10, 'increment': 0.1, 'validate': 'focusout'}
        labelArgs = {'sticky': 'e', 'padx': (0, 8)}
        entryArgs = {'sticky': 'ew', 'pady': 4}

        Label(self, text='nseg').grid(row=1, **labelArgs)
        self.nsegVar = IntVar(value=1)
        nsegEntry = Spinbox(self, textvariable=self.nsegVar, **intSpinArgs)
        nsegEntry.grid(row=1, column=1, columnspan=2, **entryArgs)
        nsegEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addIntValidation(nsegEntry, from_=1, to=32767)

        Label(self, text='L').grid(row=2, **labelArgs)
        self.lengthVar = DoubleVar(value=1.0)
        lengthEntry = Spinbox(self, textvariable=self.lengthVar, **floatSpinArgs)
        lengthEntry.grid(row=2, column=1, columnspan=2, **entryArgs)
        lengthEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addFloatValidation(lengthEntry, from_=1e-9)

        Label(self, text='diam').grid(row=3, **labelArgs)
        self.diamVar = DoubleVar(value=1.0)
        diamEntry = Spinbox(self, textvariable=self.diamVar, **floatSpinArgs)
        diamEntry.grid(row=3, column=1, columnspan=2, **entryArgs)
        diamEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addFloatValidation(diamEntry, from_=1e-9)

        Label(self, text='parent').grid(row=4, **labelArgs)
        self.endMenu = Combobox(self, values=[0, 1], width=1, state="readonly")
        self.endMenu.current(0)
        self.endMenu.grid(row=4, column=1, padx=(0, 8), **entryArgs)
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
            name = AppModel.simpleName(parent)
            values.append(f'{name}({end})')
        _setComboboxValues(self.parentMenu, values)

        parentConnection = AppModel.getParent(section)
        if parentConnection is None:
            self.endMenu.current(0)  # sets first (default) index
            self.parentMenu.set('')
        else:
            childEnd, parent, parentEnd = parentConnection
            parentName = AppModel.simpleName(parent)
            self.endMenu.set(childEnd)
            self.parentMenu.set(f'{parentName}({parentEnd})')

        self.mechMenu.set(AppModel.getMechanism(section) or '')

    def saveCurrentSection(self):
        """
        Saves the current section's data
        """
        section = self.model.selectedSection
        if section is None:
            return

        section.nseg = safeInt(self.nsegVar.get, orElse=section.nseg, from_=1, to=32766)
        section.diam = safeFloat(self.diamVar.get, orElse=section.diam, from_=1e-9)
        section.L = safeFloat(self.lengthVar.get, orElse=section.L, from_=1e-9)

        parentOption = self.parentMenu.get()
        if parentOption == '':
            AppModel.setParent(section, None)
        else:
            childEnd = int(self.endMenu.get())
            parent, parentEnd = self._parseParentValue(parentOption)
            AppModel.setParent(section, (childEnd, parent, parentEnd))

        AppModel.setMechanism(section, self.mechMenu.get() or None)

    def _parseParentValue(self, option: str) -> Tuple[nrn.Section, int]:
        [name, number] = option.split('(')
        section = self.model.getSection(name)
        n = int(number[0:-1])
        return section, n


def _setComboboxValues(combobox: Combobox, values: Iterable):
    valueBefore = combobox.get()
    combobox['values'] = values
    if valueBefore not in values:
        combobox.set('')
