#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:08:39 2020

@author: tonyz
"""

from tkinter import *
from tkinter.ttk import *

from src.gui.model import AppModel, CellSource
from src.gui.plotting import plot2DCell, plot3DCell


class PlotView(Frame):

    def __init__(self, master, model: AppModel):
        super().__init__(master)
        self.model = model

        self.buttonVar = IntVar(value=1)
        self.figures = []
        optButton0 = Radiobutton(self, text="3D View", variable=self.buttonVar, value=1)
        optButton1 = Radiobutton(self, text="2D View", variable=self.buttonVar, value=2)
        printButton = Button(self, text="Display", command=self._refresh)
        optButton0.grid(row=0, column=0)
        optButton1.grid(row=1, column=0, pady=4)
        printButton.grid(row=2, column=0, padx=8)

    def _refresh(self):
        source = self.model.cellSource
        if source is CellSource.HOC_FILE:
            if self.model.filename != '':
                self._displayCell(self.model.hocObject.allsec())
        elif source is CellSource.BUILDER:
            if self.model.hasSections():
                sectionList = self.model.toSectionList()
                self._displayCell(sectionList)

    def _displayCell(self, sections):
        value = self.buttonVar.get()
        if value == 1:
            plot3DCell(sections)
        elif value == 2:
            plot2DCell(sections)
