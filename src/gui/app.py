#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

from tkinter import *
from tkinter.ttk import *

from ttkthemes import ThemedTk

from src.core import demo
from src.gui.config_view import ConfigView
from src.gui.model import AppModel, CellSource
from src.gui.open_hoc_view import OpenHocView
from src.gui.plot_view import PlotView
from src.gui.sections_view import SectionsView


class App(Frame):

    def __init__(self, root: Tk, model: AppModel):
        super().__init__(root)
        self.root = root
        self.model = model

        root.configure(padx=8, pady=8)
        root.geometry('')  # auto-size
        root.title('Simulator :)')
        root.bind('<Escape>', lambda e: root.destroy())
        root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

        pad = {'padx': 8, 'pady': 8}

        # Multitab holder
        self.tabs = Notebook(root)
        self.tabs.grid(row=0, column=0, rowspan=2)

        # Ball & Stick builder tab
        builderTab = Frame(self.tabs, padding=8)
        self.sectionsView = SectionsView(builderTab, model)
        self.sectionsView.grid(row=0, column=0, rowspan=2, **pad)
        self.configView = ConfigView(builderTab, model)
        self.configView.grid(row=0, column=1, **pad)
        ballstickButton = Button(builderTab, text='Create ball & stick', command=self.fillBallStick)
        ballstickButton.grid(row=1, column=1, **pad)
        self.tabs.add(builderTab, text='Cell builder')

        # Hoc file loader tab
        hocFileTab = Frame(self.tabs, padding=8)
        self.openHocView = OpenHocView(hocFileTab, model)
        self.openHocView.grid(row=1, column=0, **pad)
        self.tabs.add(hocFileTab, text='HOC loader')

        # Plotting and simulation controls
        self.plotView = PlotView(root, model)
        self.plotView.grid(row=0, column=1, **pad)
        simuButton = Button(root, text='Simulation', command=self.model.doSimulation)
        simuButton.grid(row=1, column=1, **pad)

        # Event handlers
        self.sectionsView.beforeSelection(self.configView.saveCurrentSection)
        self.sectionsView.afterSelection(self.configView.refreshView)
        self.tabs.bind('<<NotebookTabChanged>>', self.onTabChanged)

    def onTabChanged(self, _):
        index = self.tabs.index(self.tabs.select())
        if index == 0:
            self.model.cellSource = CellSource.BUILDER
        elif index == 1:
            self.model.cellSource = CellSource.HOC_FILE

    def fillBallStick(self):
        self.model.tryAddSection('soma')
        self.model.tryAddSection('axon')
        self.model.tryAddSection('dend')
        soma = self.model.getSection('soma')
        axon = self.model.getSection('axon')
        dend = self.model.getSection('dend')
        soma.nseg = 1
        soma.L = 25
        soma.diam = 25
        soma.insert('hh')
        axon.nseg = 100
        axon.L = 1000
        axon.diam = 2
        axon.insert('hh')
        dend.nseg = 5
        dend.L = 50
        dend.diam = 2
        dend.insert('pas')
        axon.connect(soma(1), 0)
        dend.connect(soma(0), 1)
        self.sectionsView.refreshView()

    @staticmethod
    def launch():
        root = ThemedTk(background=True)
        if 'plastik' in root.get_themes():
            root.set_theme('plastik')  # plastik / arc
        # style = Style()
        # if 'clam' in style.theme_names():
        #     style.theme_use('clam')
        model = AppModel()
        App(root, model)
        root.mainloop()
        return model


if __name__ == '__main__':
    App.launch()
