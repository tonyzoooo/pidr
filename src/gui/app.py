#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

from tkinter import *
from tkinter.ttk import *

from config_view import ConfigView
from open_hoc_view import OpenHocView
from sections_view import SectionsView
from plot_view import PlotView
from model import AppModel


class App(Frame):

    def __init__(self, root: Tk, model: AppModel):
        super().__init__(root)
        self.root = root
        self.model = model

        root.geometry('600x400')
        root.title('Simulator :)')
        root.bind('<Escape>', lambda e: root.destroy())
        root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

        pad = {'padx': 10, 'pady': 10}

        self.configView = ConfigView(root, model)
        self.configView.grid(row=0, column=1, **pad)

        self.sectionsView = SectionsView(root, model)
        self.sectionsView.grid(row=0, column=0, **pad)
        self.sectionsView.beforeSelection(self.configView.saveCurrentSection)
        self.sectionsView.afterSelection(self.configView.refreshView)

        self.plotView = PlotView(root, model)
        self.plotView.grid(row=0, column=2, **pad)

        self.openHocView = OpenHocView(root, model)
        self.openHocView.grid(row=1, column=0, columnspan=2, **pad)

        debugButton = Button(root, text='debug', command=self.debugCommand)
        debugButton.grid(row=1, column=2, **pad)

    def debugCommand(self):
        print('debug')
        cell = self.model.createLFPyCell()
        print(cell)
        pass

    @staticmethod
    def launch():
        root = Tk()
        style = Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        model = AppModel()
        App(root, model)
        root.mainloop()
        return model


if __name__ == '__main__':
    App.launch()
