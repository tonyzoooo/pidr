#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:08:39 2020

@author: tonyz
"""

from tkinter import *
from tkinter.ttk import *
from model import AppModel
from plotting import plot2DCell, plot3DCell



class PlotView(Frame):

    def __init__(self, root: Tk, model: AppModel):
        super().__init__(root)
        self.model = model

        self.buttonVar = IntVar()
        self.figures = []
        optButton0 = Radiobutton(self, text="3D View", variable=self.buttonVar, value=1)
        optButton1 = Radiobutton(self, text="2D View", variable=self.buttonVar, value=2)
        printButton = Button(self, text="Display", command=lambda:self._refresh())
        optButton0.grid(row=0, column=0)
        optButton1.grid(row=1, column=0)
        printButton.grid(row=2, column=0)
        

    def _refresh(self):
        if self.model.filename != '':
            value = self.buttonVar.get()
            if value == 1:
                plot3DCell(self.model.hocObject.allsec())
            elif value == 2:
                plot2DCell(self.model.hocObject.allsec())
        self.buttonVar.set(0)
