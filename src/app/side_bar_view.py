#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains view classes related to the side bar controls.

@author: Loïc Bertrand, Tony Zhou
"""

from tkinter import *
from tkinter.ttk import *

from src.app.model import AppModel


class SideBarView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for side bar controls

        :param master: parent container
        :param model: app model
        """
        super().__init__(master)
        self.model = model

        self.plotView = PlotView(self, model)
        self.plotView.grid(row=0, column=0, padx=8, pady=8)
        simuButton = Button(self, text='Simulation', command=self.model.doSimulation)
        simuButton.grid(row=1, column=0, padx=8, pady=(48, 8))


class PlotView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for selecting desired plot parameters

        :param master: parent container
        :param model: app model
        """
        super().__init__(master)
        self.model = model

        self.buttonVar = StringVar(value='2D')
        radio2D = Radiobutton(self, text="2D View", variable=self.buttonVar, value='2D')
        radio3D = Radiobutton(self, text="3D View", variable=self.buttonVar, value='3D')
        displayBtn = Button(self, text="Display", command=self._display)
        radio2D.grid(row=0, column=0)
        radio3D.grid(row=1, column=0, pady=4)
        displayBtn.grid(row=2, column=0, padx=8)

    def _display(self):
        """
        Plots the selected morphology (from builder or from file), in 2D or 3D,
        depending on the selected mode.
        """
        dimension = self.buttonVar.get()
        self.model.plotCell(dimension)
