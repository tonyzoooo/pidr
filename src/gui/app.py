#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *

from ttkthemes import ThemedTk

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
        self.tabs = Notebook(root, width=500, height=300)
        self.tabs.grid(row=0, column=0, rowspan=2)

        # Tab 1: Morphology
        self.morphoTab = Frame(self.tabs)
        # - Ball & Stick builder
        self.builderFrame = Frame(self.morphoTab, padding=8)
        self.sectionsView = SectionsView(self.builderFrame, model)
        self.sectionsView.grid(row=0, column=0, rowspan=2, **pad)
        self.configView = ConfigView(self.builderFrame, model)
        self.configView.grid(row=0, column=1, columnspan=2, **pad)
        ballstickButton = Button(self.builderFrame, text='Create ball & stick', command=self.fillBallStick)
        ballstickButton.grid(row=1, column=1, **pad)
        useFileButton = Button(self.builderFrame, text='Use HOC file', command=self.switchToFile)
        useFileButton.grid(row=1, column=2, **pad)
        self.builderFrame.pack()
        # - Hoc file loader
        self.hocFileFrame = Frame(self.morphoTab, padding=8)
        self.openHocView = OpenHocView(self.hocFileFrame, model)
        self.openHocView.grid(row=1, column=0, **pad)
        useBuilderButton = Button(self.hocFileFrame, text='Use builder', command=self.switchToBuilder)
        useBuilderButton.grid(row=2, column=0, **pad)
        self.morphoTab.pack()
        self.tabs.add(self.morphoTab, text='Morphology')

        # Tab 2: Stimulation
        stimTab = Frame(self.tabs)
        stimLabel = Label(stimTab, text='<Stimulation parameters>')
        stimLabel.pack(pady=(100, 0))
        stimTab.pack()
        self.tabs.add(stimTab, text='Stimulation')

        # Plotting and simulation controls
        self.plotView = PlotView(root, model)
        self.plotView.grid(row=0, column=1, **pad)
        simuButton = Button(root, text='Simulation', command=self.model.doSimulation)
        simuButton.grid(row=1, column=1, **pad)

        # Event handlers
        self.sectionsView.beforeSelection(self.configView.saveCurrentSection)
        self.sectionsView.afterSelection(self.configView.refreshView)
        self.tabs.bind('<<NotebookTabChanged>>', self.onTabChanged)

    def switchToFile(self):
        if self.model.hasSections():
            if not messagebox.askokcancel("Warning", "Do you really want to clear the builder?"):
                return
        self.builderFrame.pack_forget()
        self.hocFileFrame.pack()
        self.model.cellSource = CellSource.HOC_FILE
        self.openHocView.refreshView()

    def switchToBuilder(self):
        self.hocFileFrame.pack_forget()
        self.builderFrame.pack()
        self.model.cellSource = CellSource.BUILDER
        self.sectionsView.refreshView()

    def onTabChanged(self, _):
        index = self.tabs.index(self.tabs.select())

    def fillBallStick(self):
        self.model.cell.sections.clear()
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
