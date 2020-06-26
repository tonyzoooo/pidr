import tkinter as tk
from functools import partial
from typing import Iterable, Tuple

from neuron import h
from tkvalidate import float_validate

from model import AppModel


class ConfigView(tk.Frame):

    def __init__(self, root: tk.Tk, model: AppModel):
        """
        Container for the configuration of the selected section
        """
        super().__init__(root)
        self.model = model

        spinArgs = {'from_': 0, 'to': 1000, 'increment': 0.1}

        self.selectedSectionLabel = tk.Label(self, text='<no section>')
        self.selectedSectionLabel.grid(row=0, column=1, columnspan=2)

        self.lengthVar = tk.DoubleVar()
        lengthLabel = tk.Label(self, text='L')
        lengthLabel.grid(row=1, column=0)
        lengthEntry = tk.Spinbox(self, textvariable=self.lengthVar, **spinArgs)
        float_validate(lengthEntry)
        lengthEntry.grid(row=1, column=1, columnspan=2)
        lengthEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.diamVar = tk.DoubleVar()
        dimLabel = tk.Label(self, text='diam')
        dimLabel.grid(row=2, column=0)
        diamEntry = tk.Spinbox(self, textvariable=self.diamVar, **spinArgs)
        float_validate(diamEntry)
        diamEntry.grid(row=2, column=1, columnspan=2)
        diamEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.parentVar = tk.StringVar()
        self.parentVar.trace_add('write', lambda a, b, c: self.saveCurrentSection())
        self.endVar = tk.IntVar(0)
        self.endVar.trace_add('write', lambda a, b, c: self.saveCurrentSection())
        parentLabel = tk.Label(self, text='parent')
        parentLabel.grid(row=3, column=0)
        endMenu = tk.OptionMenu(self, self.endVar, 0, 1)
        endMenu.grid(row=3, column=1, sticky='ew')
        self.parentMenu = tk.OptionMenu(self, self.parentVar, '')
        self.parentMenu.grid(row=3, column=2, sticky='ew')

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

        print('---refreshView---')
        h.topology()
        print('-----------------')

        names = self.model.sectionNames
        options = []
        for n in names:
            # TODO: add only possible parents (end not taken by another section)
            if n != AppModel.simpleName(section):
                options.append(n + ' (0)')
                options.append(n + ' (1)')
        self._setMenuOptions(self.parentMenu, self.parentVar, options)

        # get parent segment of current section
        parentSeg = section.parentseg()
        if parentSeg is None:
            self.parentVar.set('')
        else:
            # refresh end index value
            endIndex = int(section.orientation())
            self.endVar.set(endIndex)
            # refresh parent value
            parentName = AppModel.simpleName(parentSeg.sec)
            index = int(parentSeg.x)
            self.parentVar.set(f'{parentName} ({index})')


    def saveCurrentSection(self):
        """
        Saves the current section's data
        """
        section = self.model.selectedSection
        if section is None:
            return

        section.diam = self.diamVar.get()
        section.L = self.lengthVar.get()

        endIndex = self.endVar.get()
        parentOption = self.parentVar.get()
        if parentOption != '':
            (parent, n) = self._parseParentOption(parentOption)
            if not self.model.trySetParent(section, endIndex, parent, n):
                print(f"Error: trySetParent({section}, {endIndex}, {parent}, {n})")

        print('---saveCurrentSection---')
        h.topology()
        print(f"{section}'s connections: {self.model.getConnections(section)}")
        print('------------------------')

    def _parseParentOption(self, option: str) -> Tuple[h.Section, int]:
        [name, number] = option.split(' ')
        section = self.model.getSection(name)
        n = int(number[1:-1])
        return section, n

    def _setMenuOptions(self, optionMenu: tk.OptionMenu, var: tk.Variable, options: Iterable[str]):
        valueBefore = var.get()
        menu = optionMenu['menu']
        menu.delete(0, 'end')

        menu.add_command(label='', command=partial(var.set, ''))
        for name in options:
            menu.add_command(label=name, command=partial(var.set, name))

        if valueBefore not in options:
            var.set('')
