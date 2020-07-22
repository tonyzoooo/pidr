#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:08:39 2020

@author: tonyz
"""

from tkinter import *
from tkinter.ttk import *

from src.gui.model import AppModel
from src.gui.plotting import plot2DCell, plot3DCell


class PlotView(Frame):

    def __init__(self, master, model: AppModel):
        super().__init__(master)
        self.model = model

        self.buttonVar = StringVar(value='3D')
        self.figures = []
        optButton0 = Radiobutton(self, text="3D View", variable=self.buttonVar, value='3D')
        optButton1 = Radiobutton(self, text="2D View", variable=self.buttonVar, value='2D')
        printButton = Button(self, text="Display", command=self._display)
        optButton0.grid(row=0, column=0)
        optButton1.grid(row=1, column=0, pady=4)
        printButton.grid(row=2, column=0, padx=8)

    def _display(self):
        if self.model.hasMorphology():
            sectionList = self.model.toSectionList()
            dim = self.buttonVar.get()
            if dim == '3D':
                plot3DCell(sectionList)
            elif dim == '2D':
                plot2DCell(sectionList)
