#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains view classes related to the 'Stimulation' tab.

@author: Loïc Bertrand
"""

from tkinter import *
from tkinter.ttk import *

from src.app.model import AppModel
from src.app.number_validation import addFloatValidation, safeFloat


class ElecGridView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for recording electrodes parameters

        :param master: parent container
        :param model: app model
        """
        super().__init__(master, padding=4)
        self.model = model

        pad = {'padx': 4, 'pady': 4}
        floatSpinArgs = {'increment': 0.1, 'validate': 'focusout'}

        Label(self, text='Electrode grid parameters').grid(row=0, column=1, columnspan=3, pady=(0, 12))

        for col, lbl in (1, 'start'), (2, 'stop'), (3, 'step'):
            Label(self, text=lbl).grid(row=1, column=col, **pad)

        Label(self, text='xs').grid(row=2, column=0, **pad)
        Label(self, text='ys').grid(row=3, column=0, **pad)

        self.xStart, self.xStop, self.xStep = DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)
        self.yStart, self.yStop, self.yStep = DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)
        for row, col, var in (2, 1, self.xStart), (2, 2, self.xStop), (2, 3, self.xStep), \
                             (3, 1, self.yStart), (3, 2, self.yStop), (3, 3, self.yStep):
            spinBox = Spinbox(self, textvariable=var, width=10, **floatSpinArgs)
            spinBox.grid(row=row, column=col, **pad)
            spinBox.bind('<FocusOut>', lambda e: self.saveValues())
            addFloatValidation(spinBox)

        Label(self, text='µm').grid(row=2, column=4, **pad, sticky='w')
        Label(self, text='µm').grid(row=3, column=4, **pad, sticky='w')

        self.refreshView()

    def refreshView(self):
        """
        Fills the fields using the values stored in the model
        """
        self.xStart.set(self.model.elecGrid.xs[0])
        self.xStop.set(self.model.elecGrid.xs[1])
        self.xStep.set(self.model.elecGrid.xs[2])

        self.yStart.set(self.model.elecGrid.ys[0])
        self.yStop.set(self.model.elecGrid.ys[1])
        self.yStep.set(self.model.elecGrid.ys[2])

    def saveValues(self):
        """
        Saves the values of the fields into the model
        """
        grid = self.model.elecGrid

        grid.xs = (
            safeFloat(self.xStart.get, orElse=grid.xs[0]),
            safeFloat(self.xStop.get, orElse=grid.xs[1]),
            safeFloat(self.xStep.get, orElse=grid.xs[2]),
        )
        grid.ys = (
            safeFloat(self.yStart.get, orElse=grid.ys[0]),
            safeFloat(self.yStop.get, orElse=grid.ys[1]),
            safeFloat(self.yStep.get, orElse=grid.ys[2]),
        )
