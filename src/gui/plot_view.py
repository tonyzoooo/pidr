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
<<<<<<< Updated upstream
        self.buttonVar = IntVar()
        optButton0 = Radiobutton(self, text="3D View", variable=self.buttonVar, value=1)
        optButton1 = Radiobutton(self, text="2D View 1", variable=self.buttonVar, value=2)
        optButton2 = Radiobutton(self, text="2D View 2", variable=self.buttonVar, value=3)
        optButton3 = Radiobutton(self, text="2D View 3", variable=self.buttonVar, value=4)
        printButton = Button(self, text="Display", command=lambda: self._refresh())
||||||| constructed merge base
        self.buttonVar = tk.IntVar()
        optButton0 = tk.Radiobutton(self, text="3D View", variable=self.buttonVar, value=1)
        optButton1 = tk.Radiobutton(self, text="2D View 1", variable=self.buttonVar, value=2)
        optButton2 = tk.Radiobutton(self, text="2D View 2", variable=self.buttonVar, value=3)
        optButton3 = tk.Radiobutton(self, text="2D View 3", variable=self.buttonVar, value=4)
        printButton = tk.Button(self, text="Display", command=lambda:self._refresh())
=======
        self.buttonVar = tk.IntVar()
        self.figures = []
        optButton0 = tk.Radiobutton(self, text="3D View", variable=self.buttonVar, value=1)
        optButton1 = tk.Radiobutton(self, text="2D View", variable=self.buttonVar, value=2)
        printButton = tk.Button(self, text="Display", command=lambda:self._refresh())
>>>>>>> Stashed changes
        optButton0.grid(row=0, column=0)
        optButton1.grid(row=1, column=0)
<<<<<<< Updated upstream
        optButton2.grid(row=2, column=0)
        optButton3.grid(row=3, column=0)
        printButton.grid(row=4, column=0)

||||||| constructed merge base
        optButton2.grid(row=2, column=0)
        optButton3.grid(row=3, column=0)
        printButton.grid(row=4, column=0)
        
=======
        printButton.grid(row=2, column=0)
        
>>>>>>> Stashed changes
    def _refresh(self):
<<<<<<< Updated upstream
        if self.model.filename != "":
||||||| constructed merge base
        if self.model.filename != "" :
=======
        if self.model.filename != '':
>>>>>>> Stashed changes
            value = self.buttonVar.get()
            if value == 1:
                plot3DCell(self.model.hocObject.allsec())
            elif value == 2:
                plot2DCell(self.model.hocObject.allsec())
        self.buttonVar.set(0)
