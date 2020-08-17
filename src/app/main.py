#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Tony Zhou
"""

from tkinter import *
from tkinter.ttk import *

from ttkthemes import ThemedTk

from src.app.morpho_view import MorphologyView
from src.app.model import AppModel
from src.app.plot_view import PlotView
from src.app.stim_view import StimulationView


class App(Frame):

    def __init__(self, root: Tk, model: AppModel):
        """
        Application's main panel

        :param root:    ``Tk`` root
        :param model:   application model reference
        """
        super().__init__(root)
        self.root = root
        self.model = model

        root.configure(padx=8, pady=8)
        root.geometry('')  # adjust window size to fit content
        root.title('Simulation comparator')
        root.bind('<Escape>', lambda e: root.destroy())
        root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

        pad = {'padx': 8, 'pady': 8}

        # Multitab holder
        self.tabs = Notebook(root, width=500, height=300)
        self.tabs.grid(row=0, column=0, rowspan=2)
        self.tabs.bind('<<NotebookTabChanged>>', lambda e: self._onTabChanged())

        # Tab 1: Morphology builder/loader
        morphoTab = Frame(self.tabs)
        self.morphoView = MorphologyView(morphoTab, model)
        self.morphoView.place(anchor="c", relx=.5, rely=.5)
        morphoTab.pack()
        self.tabs.add(morphoTab, text='Morphology')

        # Tab 2: Stimulation parameters
        stimTab = Frame(self.tabs)
        self.stimView = StimulationView(stimTab, model)
        self.stimView.place(anchor="c", relx=.5, rely=.5)
        stimTab.pack()
        self.tabs.add(stimTab, text='Stimulation')

        # Side bar: Plotting and simulation controls
        self.plotView = PlotView(root, model)
        self.plotView.grid(row=0, column=1, **pad)
        simuButton = Button(root, text='Simulation', command=self.model.doSimulation)
        simuButton.grid(row=1, column=1, **pad)

    def _onTabChanged(self):
        tabName = self.tabs.tab(self.tabs.select(), 'text')
        if tabName == 'Stimulation':
            self.stimView.refreshView()

    @staticmethod
    def launch():
        root = ThemedTk(background=True)
        if 'plastik' in root.get_themes():
            root.set_theme('plastik')
        model = AppModel()
        App(root, model)
        root.mainloop()
        return model


if __name__ == '__main__':
    App.launch()
