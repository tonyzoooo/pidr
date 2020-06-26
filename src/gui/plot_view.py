#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:08:39 2020

@author: tonyz
"""

import tkinter as tk
from model import AppModel
from plotting import plot3DCell

class PlotView(tk.Frame):
    
    def __init__(self, root: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, root)
        self.model = model
        self.buttonVar = tk.IntVar()
        optButton0 = tk.Radiobutton(self, text="3D View", variable=self.buttonVar, value=1)
        optButton1 = tk.Radiobutton(self, text="2D View 1", variable=self.buttonVar, value=2)
        optButton2 = tk.Radiobutton(self, text="2D View 2", variable=self.buttonVar, value=3)
        optButton3 = tk.Radiobutton(self, text="2D View 3", variable=self.buttonVar, value=4)
        printButton = tk.Button(self, text="Display", command=lambda:self._refresh())
        optButton0.grid(row=0, column=0)
        optButton1.grid(row=1, column=0)
        optButton2.grid(row=2, column=0)
        optButton3.grid(row=3, column=0)
        printButton.grid(row=4, column=0)
        
    def _refresh(self):
        if self.model.filename != "" :
            value = self.buttonVar.get()
            if value == 1:
                plot3DCell(self.model.hocObj, 1)
            elif value == 2:
                plot3DCell(self.model.hocObj, 2)
            elif value == 3:
                plot3DCell(self.model.hocObj, 3)
            elif value == 4:
                plot3DCell(self.model.hocObj, 4)
        self.buttonVar.set(0)
    