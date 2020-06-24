#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

import tkinter as tk
from tkinter import filedialog

from app_model import AppModel


class App(tk.Frame):

    def __init__(self, master: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, master)
        self.master = master
        self.model = model

        master.geometry('500x400')
        master.title('Simulator :)')
        master.bind('<Escape>', lambda e: master.destroy())

        pad = {'padx': 10, 'pady': 10}

        self._createSectionsContainer().grid(row=0, column=0, **pad)
        self._createConfigContainer().grid(row=0, column=1, **pad)
        self._createOpenHocFileContainer().grid(row=1, column=0, columnspan=2, **pad)

    def _createSectionsContainer(self):
        """
        Container for the list of sections
        """
        container = tk.Frame(self.master)

        newLabel = tk.Label(container, text='New section', justify='left')
        newLabel.grid(row=0, column=0)
        newButton = tk.Button(container, text='Create',
                              command=self._addSection)
        newButton.grid(row=0, column=1)
        self.newEntry = tk.Entry(container)
        self.newEntry.grid(row=1, column=0, columnspan=2)
        self.newEntry.bind('<Return>', lambda e: self._addSection())

        sectionLabel = tk.Label(container, text='Sections:', justify='left')
        sectionLabel.grid(row=2, column=0, columnspan=2)
        self.sectionList = tk.Listbox(container)
        for name in self.model.sectionNames:
            self.sectionList.insert('end', name)
        self.sectionList.grid(row=3, column=0, columnspan=2)

        return container

    def _addSection(self):
        """
        Event handler: adds a new section to the model and to the section list
        """
        name = self.newEntry.get()
        if (self.model.tryAddSection(name)):
            self.sectionList.insert('end', name)
            self.newEntry.delete(0, 'end')
            self._refreshConfigView()
            print(self.model.sectionNames)

    def _refreshConfigView(self):
        """
        Refreshes the section configuration view using:
        - the currently selected section in self.sectionList
        - the data of the corresponding section in the model (self.model)
        """
        pass

    def _createConfigContainer(self):
        """
        Container for the configuration of the selected section
        """
        spinArgs = {'from_': 0, 'to': 1000, 'increment': 0.1}

        container = tk.Frame(self.master)
        lengthLabel = tk.Label(container, text='L')
        lengthLabel.grid(row=0, column=0)
        lengthEntry = tk.Spinbox(container, **spinArgs)
        lengthEntry.grid(row=0, column=1)

        dimLabel = tk.Label(container, text='diam')
        dimLabel.grid(row=1, column=0)
        dimEntry = tk.Spinbox(container, **spinArgs)
        dimEntry.grid(row=1, column=1)

        self.end0Value = tk.StringVar()
        end0Label = tk.Label(container, text='end 0')
        end0Label.grid(row=2, column=0)
        end0Entry = tk.OptionMenu(
            container, self.end0Value, '', *self.model.sectionNames)
        end0Entry.grid(row=2, column=1)

        self.end1Value = tk.StringVar()
        end1Label = tk.Label(container, text='end 1')
        end1Label.grid(row=3, column=0)
        end1Entry = tk.OptionMenu(
            container, self.end1Value, '', *self.model.sectionNames)
        end1Entry.grid(row=3, column=1)

        return container

    def _createOpenHocFileContainer(self):
        """
        Container for file selection
        """
        container = tk.Frame(self.master)
        titleLabel = tk.Label(
            container, text='Simulation de potentiels extracellulaires')
        titleLabel.pack()
        openHocButton = tk.Button(
            container, text='Ouvrir .hoc', command=self._openFile)
        openHocButton.pack()
        return container

    def _openFile(self):
        self.model.filename = filedialog.askopenfilename(
            initialdir='resources',
            title='Select file',
            filetypes=(('hoc files', '*.hoc'), ('all files', '*.*'))
        )
        print('Opened: ' + self.model.filename)
        self.master.destroy()

    @staticmethod
    def launch():
        root = tk.Tk()
        model = AppModel()
        app = App(root, model)
        root.mainloop()
        return model


if __name__ == '__main__':
    App.launch()
