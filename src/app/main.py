#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is the entry point of this application.

@author: Loïc Bertrand, Tony Zhou
"""

from tkinter import *
from tkinter.ttk import *

from ttkthemes import ThemedTk

from src.app.model import AppModel
from src.app.morpho_view import MorphologyView
from src.app.side_bar_view import SideBarView
from src.app.stim_view import StimulationView


class App(ThemedTk):

    def __init__(self, model: AppModel):
        """
        Application's root panel

        :param model:   application model reference
        """
        super().__init__(background=True)
        if 'plastik' in self.get_themes():
            self.set_theme('plastik')
        self.model = model

        self.configure(padx=8, pady=8)
        self.geometry('')  # adjust window size to fit content
        self.title('Simulator')
        self.bind('<Escape>', lambda e: self.destroy())
        self.protocol("WM_DELETE_WINDOW", lambda: self.destroy())

        # Multitab holder
        self.notebook = Notebook(self, width=500, height=300)
        self.notebook.bind('<<NotebookTabChanged>>', lambda e: self._onTabChanged())
        self.notebook.grid(row=0, column=0)

        # Tab 1: Morphology builder/loader
        morphoTab = Frame(self.notebook)
        morphoTab.pack()
        self.morphoView = MorphologyView(morphoTab, model)
        self.morphoView.place(anchor="c", relx=.5, rely=.5)
        self.notebook.add(morphoTab, text='Morphology')

        # Tab 2: Stimulation parameters
        stimTab = Frame(self.notebook)
        stimTab.pack()
        self.stimView = StimulationView(stimTab, model)
        self.stimView.place(anchor="c", relx=.5, rely=.5)
        self.notebook.add(stimTab, text='Stimulation')

        # Side bar: Plotting and simulation controls
        sideBar = SideBarView(self, model)
        sideBar.grid(row=0, column=1)

    def _onTabChanged(self):
        tabName = self.notebook.tab(self.notebook.select(), 'text')
        if tabName == 'Stimulation':
            self.stimView.refreshView()

    @staticmethod
    def launch():
        model = AppModel()
        app = App(model)
        app.mainloop()
        return model


if __name__ == '__main__':
    App.launch()
