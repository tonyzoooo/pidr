from tkinter import *
from tkinter.ttk import *
from typing import Iterable, Tuple

from neuron import h
from tkvalidate import float_validate

from model import AppModel


class ConfigView(Frame):

    def __init__(self, root: Tk, model: AppModel):
        """
        Container for the configuration of the selected section
        """
        super().__init__(root)
        self.model = model

        spinArgs = {'from_': 0, 'to': 1000, 'increment': 0.1}

        self.selectedSectionLabel = Label(self, text='<no section>')
        self.selectedSectionLabel.grid(row=0, column=1, columnspan=2)

        self.lengthVar = DoubleVar()
        lengthLabel = Label(self, text='L')
        lengthLabel.grid(row=1, column=0)
        lengthEntry = Spinbox(self, textvariable=self.lengthVar, **spinArgs)
        float_validate(lengthEntry)
        lengthEntry.grid(row=1, column=1, columnspan=2)
        lengthEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.diamVar = DoubleVar()
        dimLabel = Label(self, text='diam')
        dimLabel.grid(row=2, column=0)
        diamEntry = Spinbox(self, textvariable=self.diamVar, **spinArgs)
        float_validate(diamEntry)
        diamEntry.grid(row=2, column=1, columnspan=2)
        diamEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        parentLabel = Label(self, text='parent')
        parentLabel.grid(row=3, column=0)
        self.endMenu = Combobox(self, values=[0, 1], width=1, state="readonly")
        self.endMenu.current(0)
        self.endMenu.grid(row=3, column=1, sticky='ew')
        self.endMenu.bind('<<ComboboxSelected>>', lambda e: self.saveCurrentSection())
        self.parentMenu = Combobox(self, values=[''], width=10, state="readonly")
        self.parentMenu.grid(row=3, column=2, sticky='ew')
        self.parentMenu.bind('<<ComboboxSelected>>', lambda e: self.saveCurrentSection())

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

        self.lengthVar.set(section.L)
        self.diamVar.set(section.diam)

        names = self.model.sectionNames
        values = []
        for n in names:
            # TODO: add only possible parents (end not taken by another section)
            if n != AppModel.simpleName(section):
                values.append(n + ' (0)')
                values.append(n + ' (1)')
        _setComboboxValues(self.parentMenu, values)

        # get parent segment of current section
        parentSeg = section.parentseg()
        if parentSeg is None:
            self.endMenu.set(0)
            self.parentMenu.set('')
        else:
            # refresh end index value
            endIndex = int(section.orientation())
            self.endMenu.set(endIndex)
            # refresh parent value
            parentName = AppModel.simpleName(parentSeg.sec)
            index = int(parentSeg.x)
            self.parentMenu.set(f'{parentName} ({index})')

    def saveCurrentSection(self):
        """
        Saves the current section's data
        """
        section = self.model.selectedSection
        if section is None:
            return

        section.diam = self.diamVar.get()
        section.L = self.lengthVar.get()

        endIndex = int(self.endMenu.get())
        parentOption = self.parentMenu.get()
        if parentOption != '':
            (parent, n) = self._parseParentOption(parentOption)
            if not self.model.trySetParent(section, endIndex, parent, n):
                print(f"Error: trySetParent({section}, {endIndex}, {parent}, {n})")

        h.topology()

    def _parseParentOption(self, option: str) -> Tuple[h.Section, int]:
        [name, number] = option.split(' ')
        section = self.model.getSection(name)
        n = int(number[1:-1])
        return section, n


def _setComboboxValues(combobox: Combobox, values: Iterable):
    valueBefore = combobox.get()
    combobox.option_clear()
    combobox['values'] = values
    if valueBefore not in values:
        combobox.set('')
