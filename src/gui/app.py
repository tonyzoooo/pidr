#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

from tkinter import *
from tkinter.ttk import *

import matplotlib.pyplot as plt
from ttkthemes import ThemedTk

import lfpy_simulation
from config_view import ConfigView
from model import AppModel
from open_hoc_view import OpenHocView
from plot_view import PlotView
from sections_view import SectionsView


class App(Frame):

    def __init__(self, root: Tk, model: AppModel):
        super().__init__(root)
        self.root = root
        self.model = model

        root.geometry('600x400')
        root.title('Simulator :)')
        root.bind('<Escape>', lambda e: root.destroy())
        root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

        pad = {'padx': (12, 0), 'pady': (12, 0)}

        self.configView = ConfigView(root, model)
        self.configView.grid(row=0, column=1, **pad)

        self.sectionsView = SectionsView(root, model)
        self.sectionsView.grid(row=0, column=0, **pad)
        self.sectionsView.beforeSelection(self.configView.saveCurrentSection)
        self.sectionsView.afterSelection(self.configView.refreshView)

        self.plotView = PlotView(root, model)
        self.plotView.grid(row=0, column=2, **pad)

        self.openHocView = OpenHocView(root, model)
        self.openHocView.grid(row=1, column=0, **pad)

        ballstickButton = Button(root, text='fill ball & stick', command=self.fillBallStick)
        ballstickButton.grid(row=1, column=1, **pad)

        cellButton = Button(root, text='create LFPy Cell', command=self.createCell)
        cellButton.grid(row=1, column=2, **pad)

    def createCell(self):
        cell = self.model.createLFPyCell()
        fig = plt.figure('Cell')
        lfpy_simulation.plotNeuron(cell=cell, fig=fig, electrode=None)
        plt.show()

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
