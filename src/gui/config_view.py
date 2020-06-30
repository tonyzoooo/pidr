from tkinter import *
from tkinter.ttk import *
from typing import Iterable, Tuple

from neuron import h

from model import AppModel
from number_validation import safeFloat, addFloatValidation, addIntValidation, safeInt


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

        intSpinArgs = {
            'from_': 1, 'to': 1e10, 'increment': 1, 'validate': 'focusout'
        }

        self.nsegVar = IntVar(value=1)
        nsegLabel = Label(self, text='nseg')
        nsegLabel.grid(row=1, column=0)
        nsegEntry = Spinbox(self, textvariable=self.nsegVar, **intSpinArgs)
        nsegEntry.grid(row=1, column=1, columnspan=2)
        nsegEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addIntValidation(nsegEntry, _from=1, to=32767)

        floatSpinArgs = {
            'from_': 0, 'to': 1e10, 'increment': 0.1, 'validate': 'focusout'
        }

        self.lengthVar = DoubleVar(value=1.0)
        lengthLabel = Label(self, text='L')
        lengthLabel.grid(row=2, column=0)
        lengthEntry = Spinbox(self, textvariable=self.lengthVar, **floatSpinArgs)
        lengthEntry.grid(row=2, column=1, columnspan=2)
        lengthEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addFloatValidation(lengthEntry, _from=1e-9)

        self.diamVar = DoubleVar(value=1.0)
        dimLabel = Label(self, text='diam')
        dimLabel.grid(row=3, column=0)
        diamEntry = Spinbox(self, textvariable=self.diamVar, **floatSpinArgs)
        diamEntry.grid(row=3, column=1, columnspan=2)
        diamEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())
        addFloatValidation(diamEntry, _from=1e-9)

        parentLabel = Label(self, text='parent')
        parentLabel.grid(row=4, column=0)
        self.endMenu = Combobox(self, values=[0, 1], width=1, state="readonly")
        self.endMenu.current(0)
        self.endMenu.grid(row=4, column=1, sticky='ew')
        self.endMenu.bind('<<ComboboxSelected>>', lambda e: self.saveCurrentSection())
        self.parentMenu = Combobox(self, values=[''], width=10, state="readonly")
        self.parentMenu.grid(row=4, column=2, sticky='ew')
        self.parentMenu.bind('<<ComboboxSelected>>', lambda e: self.saveCurrentSection())

    def refreshView(self):
        """
        Refreshes the section configuration view using:
        - the currently selected section in self.sectionList
        - the data of the corresponding section in the model (self.model)
        """
        print('refreshView()')
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

        # get parent segment of current section
        parentSeg = section.parentseg()
        if parentSeg is None:
            self.endMenu.current(0)  # sets first (default) index
            self.parentMenu.set('')
        else:
            # refresh end index value
            endIndex = int(section.orientation())
            self.endMenu.set(endIndex)
            # refresh parent value
            parentName = AppModel.simpleName(parentSeg.sec)
            index = int(parentSeg.x)
            self.parentMenu.set(f'{parentName}({index})')

    def saveCurrentSection(self):
        """
        Saves the current section's data
        """
        print('saveCurrentSection()')
        section = self.model.selectedSection
        if section is None:
            return

        section.nseg = safeInt(self.nsegVar.get, orElse=section.nseg, _from=1, to=32766)
        section.diam = safeFloat(self.diamVar.get, orElse=section.diam, _from=1e-9)
        section.L = safeFloat(self.lengthVar.get, orElse=section.L, _from=1e-9)

        endIndex = int(self.endMenu.get())
        parentOption = self.parentMenu.get()
        if parentOption != '':
            (parent, n) = self._parseParentValue(parentOption)
            self.model.setParent(section, endIndex, parent, n)

    def _parseParentValue(self, option: str) -> Tuple[h.Section, int]:
        [name, number] = option.split('(')
        section = self.model.getSection(name)
        n = int(number[0:-1])
        return section, n


def _setComboboxValues(combobox: Combobox, values: Iterable):
    valueBefore = combobox.get()
    combobox['values'] = values
    if valueBefore not in values:
        combobox.set('')
