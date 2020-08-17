#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Tony Zhou
"""

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

from src.app.model import AppModel


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
        text = self.model.filename or 'No file selected'
        self.fileLabel.configure(text=text)
