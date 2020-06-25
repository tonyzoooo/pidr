import tkinter as tk
from typing import Optional

from model import AppModel


class SectionsView(tk.Frame):

    def __init__(self, root: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, root)
        self.model = model
        self._beforeSelectionCallbacks = []
        self._afterSelectionCallbacks = []

        """
        self for the list of sections
        """
        newLabel = tk.Label(self, text='New section', justify='left')
        newLabel.grid(row=0, column=0)
        newButton = tk.Button(self, text='Create', command=self._addSection)
        newButton.grid(row=0, column=1, sticky='nsew')
        self.newEntry = tk.Entry(self)
        self.newEntry.grid(row=1, column=0, columnspan=2)
        self.newEntry.bind('<Return>', lambda e: self._addSection())

        sectionLabel = tk.Label(self, text='Sections:', justify='left')
        sectionLabel.grid(row=2, column=0, columnspan=2)
        self.sectionList = tk.Listbox(self)
        self.sectionList.grid(row=3, column=0, columnspan=2)
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
