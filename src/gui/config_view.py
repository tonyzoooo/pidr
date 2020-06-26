import tkinter as tk
from functools import partial
from typing import Iterable, Tuple

from neuron import h
from tkvalidate import float_validate

from model import AppModel


class ConfigView(tk.Frame):

    def __init__(self, root: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, root)
        self.model = model

        """
        Container for the configuration of the selected section
        """
        spinArgs = {'from_': 0, 'to': 1000, 'increment': 0.1}

        self.selectedSectionLabel = tk.Label(self, text='<no section selected>')
        self.selectedSectionLabel.grid(row=0, column=1)

        self.lengthVar = tk.DoubleVar()
        lengthLabel = tk.Label(self, text='L')
        lengthLabel.grid(row=1, column=0)
        lengthEntry = tk.Spinbox(self, textvariable=self.lengthVar, **spinArgs)
        float_validate(lengthEntry)
        lengthEntry.grid(row=1, column=1)
        lengthEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.diamVar = tk.DoubleVar()
        dimLabel = tk.Label(self, text='diam')
        dimLabel.grid(row=2, column=0)
        diamEntry = tk.Spinbox(self, textvariable=self.diamVar, **spinArgs)
        float_validate(diamEntry)
        diamEntry.grid(row=2, column=1)
        diamEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.end0Var = tk.StringVar()
        self.end0Var.trace_add('write', lambda a, b, c: self.saveCurrentSection())
        end0Label = tk.Label(self, text='end (0)')
        end0Label.grid(row=3, column=0)
        self.end0Menu = tk.OptionMenu(self, self.end0Var, '')
        self.end0Menu.grid(row=3, column=1, sticky='nsew')

        self.end1Var = tk.StringVar()
        self.end1Var.trace_add('write', lambda a, b, c: self.saveCurrentSection())
        end1Label = tk.Label(self, text='end (1)')
        end1Label.grid(row=4, column=0)
        self.end1Menu = tk.OptionMenu(self, self.end1Var, '')
        self.end1Menu.grid(row=4, column=1, sticky='nsew')

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
        print(f"{section}'s parent: {AppModel.getParent(section)}")
        print('-----------------')

        names = self.model.sectionNames
        options = []
        for n in names:
            if n != AppModel.simpleName(section):
                options.append(n + ' (0)')
                options.append(n + ' (1)')

        self._changeMenuOptions(self.end0Menu, self.end0Var, options)
        self._changeMenuOptions(self.end1Menu, self.end1Var, options)

    def saveCurrentSection(self):
        """
        Saves the current section's data
        """
        section = self.model.selectedSection
        if section is None:
            return

        section.diam = self.diamVar.get()
        section.L = self.lengthVar.get()

        # self.model.disconnect(section)

        end0 = self.end0Var.get()
        if end0 != '':
            (parent, n) = self._parseMenuOption(end0)
            if not self.model.tryConnect(parent, n, section, 0):
                print("Error: couldn't connect end 0")

        end1 = self.end1Var.get()
        if end1 != '':
            (parent, n) = self._parseMenuOption(end1)
            if not self.model.tryConnect(parent, n, section, 1):
                print("Error: couldn't connect end 1")

        print('---saveCurrentSection---')
        h.topology()
        print(f"{section}'s connections: {self.model.getConnections(section)}")
        print('------------------------')

    def _parseMenuOption(self, option: str) -> Tuple[h.Section, int]:
        [name, number] = option.split(' ')
        section = self.model.getSection(name)
        n = int(number[1:-1])
        return section, n

    def _changeMenuOptions(self, optionMenu: tk.OptionMenu, var: tk.Variable, options: Iterable[str]):
        valueBefore = var.get()
        menu = optionMenu['menu']
        menu.delete(0, 'end')

        menu.add_command(label='', command=partial(var.set, ''))
        for name in options:
            menu.add_command(label=name, command=partial(var.set, name))
        var.set(valueBefore if (valueBefore in options) else '')
