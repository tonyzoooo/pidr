from tkinter import *
from tkinter.ttk import *
from typing import Optional

from model import AppModel


class SectionsView(Frame):

    def __init__(self, root: Tk, model: AppModel):
        """
        self for the list of sections
        """
        super().__init__(root)
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

    def beforeSelection(self, callback):
        """
        Registers a callback which will be called before the selection changes
        """
        self._beforeSelectionCallbacks.append(callback)

    def afterSelection(self, callback):
        """
        Registers a callback which will be called after the selection changes
        """
        self._afterSelectionCallbacks.append(callback)

    def _manageSelection(self):
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
        if len(self.model.sections) == 0:
            return None

        selected = self.sectionList.curselection()
        if len(selected) == 0:
            return None

        index = selected[0]
        return self.sectionList.get(index)
