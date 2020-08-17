#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Tony Zhou
"""

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
from typing import Callable, Optional, Tuple, Iterable

from src.app.model import AppModel, CellSource, SectionModel
from src.app.number_validation import addIntValidation, addFloatValidation, safeInt, safeFloat


class MorphologyView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for creating or loading a cell morphology

        :param master: parent container
        :param model: app model
        """

        super().__init__(master)
        self.model = model

        pad = {'padx': 8, 'pady': 8}

        # Ball & Stick builder
        self.builderFrame = Frame(self, padding=8)
        self.sectionsView = SectionsView(self.builderFrame, model)
        self.sectionsView.grid(row=0, column=0, rowspan=2, **pad)
        self.configView = ConfigView(self.builderFrame, model)
        self.configView.grid(row=0, column=1, columnspan=2, **pad)
        ballstickButton = Button(self.builderFrame, text='Example', command=self._fillBallStick)
        ballstickButton.grid(row=1, column=1, **pad)
        useFileButton = Button(self.builderFrame, text='Use HOC file', command=self._switchToFile)
        useFileButton.grid(row=1, column=2, **pad)
        self.builderFrame.pack()

        # Hoc file loader
        self.hocFileFrame = Frame(self, padding=8)
        self.openHocView = OpenHocView(self.hocFileFrame, model)
        self.openHocView.grid(row=1, column=0, **pad)
        useBuilderButton = Button(self.hocFileFrame, text='Use builder', command=self._switchToBuilder)
        useBuilderButton.grid(row=2, column=0, **pad)
        self.pack()

        self.sectionsView.beforeSectionSelected(self.configView.saveCurrentSection)
        self.sectionsView.afterSectionSelected(self.configView.refreshView)

    def _fillBallStick(self):
        """
        Creates a ball & stick cell morphology and refreshes the gui
        """
        self.model.fillBallStick()
        self.sectionsView.refreshView()

    def _switchToFile(self):
        """
        Replaces the builder view with the file loader view
        """
        self.builderFrame.pack_forget()
        self.hocFileFrame.pack()
        self.model.cellSource = CellSource.HOC_FILE
        self.openHocView.refreshView()

    def _switchToBuilder(self):
        """
        Replaces the file loader with the builder view
        """
        self.hocFileFrame.pack_forget()
        self.builderFrame.pack()
        self.model.cellSource = CellSource.BUILDER
        self.sectionsView.refreshView()


class SectionsView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for the list of sections

        :param master:  parent container
        :param model:   app model
        """
        super().__init__(master)
        self.model = model
        self._beforeSelectionCallbacks = []
        self._afterSelectionCallbacks = []

        newLabel = Label(self, text='New section')
        newLabel.grid(row=0, column=0, sticky='w')
        newButton = Button(self, text='Create', command=self._addSection, width=8)
        newButton.grid(row=0, column=1, sticky='e')
        self.newEntry = Entry(self)
        self.newEntry.grid(row=1, column=0, columnspan=2, pady=4)
        self.newEntry.bind('<Return>', lambda e: self._addSection())

        sectionLabel = Label(self, text='Sections')
        sectionLabel.grid(row=2, column=0, columnspan=2, sticky='w')
        self.sectionList = Listbox(self)
        self.sectionList.grid(row=3, column=0, columnspan=2, pady=4)
        self.sectionList.bind('<<ListboxSelect>>', lambda e: self._manageSelection())

    def beforeSectionSelected(self, callback: Callable[[], None]):
        """
        Registers a callback which will be called before the selection changes

        :param callback: function with no arguments and no return value
            to be called just before a section is selected
        """
        self._beforeSelectionCallbacks.append(callback)

    def afterSectionSelected(self, callback: Callable[[], None]):
        """
        Registers a callback which will be called after the selection has changed

        :param callback: function with no arguments and no return value
            to be called just after a section has been selected
        """
        self._afterSelectionCallbacks.append(callback)

    def _manageSelection(self):
        """
        Updates the current selected section by looking at which name
        is selected in the list
        """
        for callback in self._beforeSelectionCallbacks:
            callback()
        name = self._getSelectedSectionName()
        if name is None:
            return
        if not self.model.trySelectSection(name):
            print('Error: could not select ' + str(name))
            return
        for callback in self._afterSelectionCallbacks:
            callback()

    def _addSection(self):
        """
        Adds a new section to the model and to the section list
        """
        name = self.newEntry.get().strip()
        if self.model.tryAddSection(name):
            self.sectionList.insert('end', name)
            self.newEntry.delete(0, 'end')
            self.sectionList.selection_clear(0, 'end')
            self.sectionList.selection_set('end')
            self._manageSelection()

    def _getSelectedSectionName(self) -> Optional[str]:
        """
        Gets the name of the selected section in the list, or None
        """
        selected = self.sectionList.curselection()
        if len(selected) == 0:
            return None

        index = selected[0]
        return self.sectionList.get(index)

    def refreshView(self):
        """
        Refreshes the list of sections to reflect the model
        """
        self.sectionList.delete(0, 'end')
        for sec in self.model.cell.sections:
            self.sectionList.insert('end', sec.name)
        if len(self.model.cell.sections) > 0:
            self.sectionList.selection_set(0)
            self._manageSelection()


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


class OpenHocView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for file selection

        :param master: parent container
        :param model: app model
        """
        super().__init__(master)
        self.model = model
        master.grid_columnconfigure(0, weight=1)  # center horizontally

        openHocButton = Button(self, text='Open .hoc', command=self._openFile)
        openHocButton.pack(padx=8)

        self.fileLabel = Label(self, text='No file selected', wraplength=400)
        self.fileLabel.pack(padx=8, pady=8)

    def _openFile(self):
        """
        Prompts the user to select a HOC file and updates the filename in
        the model accordingly
        """
        name = filedialog.askopenfilename(
            initialdir='../../resources',
            title='Select file',
            filetypes=(('hoc files', '*.hoc'), ('all files', '*.*'))
        )
        if name != '':
            self.model.filename = name
        self.refreshView()

    def refreshView(self):
        """
        Refreshes the name of the selected file in the gui
        """
        if self.model.filename:
            text = formatPath(self.model.filename)
        else:
            text = 'No file selected'
        self.fileLabel.configure(text=text)


def formatPath(path: str):
    CHEVRON = '  〉  '
    path = path.replace('/', CHEVRON)
    if path.startswith(CHEVRON):
        path = '/' + path
    return path


def _setComboboxValues(combobox: Combobox, values: Iterable):
    valueBefore = combobox.get()
    combobox['values'] = values
    if valueBefore not in values:
        combobox.current(0)  # select first element
