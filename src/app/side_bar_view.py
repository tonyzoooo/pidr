#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains view classes related to the side bar controls.

@author: Loïc Bertrand, Tony Zhou
"""

from tkinter import *
from tkinter.ttk import *

from src.app.model import AppModel
from src.app.plotting import plot3DCell, plot2DCell


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

        self.buttonVar = StringVar(value='3D')
        self.figures = []
        optButton0 = Radiobutton(self, text="3D View", variable=self.buttonVar, value='3D')
        optButton1 = Radiobutton(self, text="2D View", variable=self.buttonVar, value='2D')
        printButton = Button(self, text="Display", command=self._display)
        optButton0.grid(row=0, column=0)
        optButton1.grid(row=1, column=0, pady=4)
        printButton.grid(row=2, column=0, padx=8)

    def _display(self):
        """
        Plots the selected morphology (from builder or from file), in 2D or 3D,
        depending on the selected mode. Tries to create an ``LFPy.Cell`` and an
        LFPy Electrode object to plot the exact position of the stimulation. If
        the creation fails, it creates a simple ``h.SectionList`` and does not
        plot the electrode position.
        """
        if not self.model.hasMorphology():
            return

        cell = self.model.toLFPyCell()
        if cell is not None:
            sections = cell.allseclist
            stim, _ = self.model.stim.toLFPyStimIntElectrode(cell)
            stimpoint = (stim.x, stim.y, stim.z)
        else:
            # Cell construction failed => no stim point plot possible
            sections = self.model.toSectionList()
            stimpoint = None

        dim = self.buttonVar.get()
        if dim == '3D':
            plot3DCell(sections, stimpoint)
        elif dim == '2D':
            plot2DCell(sections, stimpoint)
