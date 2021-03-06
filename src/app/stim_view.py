#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains view classes related to the 'Stimulation' tab.

@author: Loïc Bertrand
"""

from tkinter import *
from tkinter.ttk import *
from typing import Optional

import LFPy

from src.app.model import AppModel, IdxMode
from src.app.number_validation import addFloatValidation, safeFloat, safeInt


class StimulationView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for stimulation parameters

        :param master: parent container
        :param model: app model
        """
        super().__init__(master, padding=4)
        self.model = model
        # Cache of the last LFPy.Cell object created
        self._cell: Optional[LFPy.Cell] = None

        pad = {'padx': 4, 'pady': 4}
        floatSpinArgs = {'from_': 0, 'to': 1e10, 'increment': 0.1, 'validate': 'focusout'}

        self.idxMode = StringVar(value='closest')
        self.idxMode.trace_add('write', lambda a, b, c: self.saveValues())
        Radiobutton(self, text='closest idx', variable=self.idxMode, value='closest').grid(row=1, **pad)
        Radiobutton(self, text='section idx', variable=self.idxMode, value='section').grid(row=2, **pad)

        self.xCoord, self.yCoord, self.zCoord = DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)
        for col, lbl, var in (1, 'x', self.xCoord), \
                             (2, 'y', self.yCoord), \
                             (3, 'z', self.zCoord):
            Label(self, text=lbl).grid(row=0, column=col)
            spinBox = Spinbox(self, textvariable=var, width=5, **floatSpinArgs)
            spinBox.grid(row=1, column=col, **pad)
            spinBox.bind('<FocusOut>', lambda e: self.saveValues())
            addFloatValidation(spinBox)
        Label(self, text='µm').grid(row=1, column=4, **pad, sticky='w')

        self.section = Combobox(self, state='readonly', width=12)
        self.section.grid(row=2, column=1, columnspan=2, **pad, sticky='ew')
        self.section.bind('<<ComboboxSelected>>', lambda e: self._refreshSegIndices())
        self.segIdx = Combobox(self, state='readonly', width=5)
        self.segIdx.grid(row=2, column=3, **pad)
        self.segIdx.bind('<<ComboboxSelected>>', lambda e: self.saveValues())

        Label(self, text='IClamp point process parameters').grid(row=3, columnspan=5, pady=(16, 4))

        self.amp, self.dur, self.delay = DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)
        for row, lbl, var, unit in (4, 'amp', self.amp, 'nA'), \
                                   (5, 'dur', self.dur, 'ms'), \
                                   (6, 'delay', self.delay, 'ms'):
            Label(self, text=lbl).grid(row=row, **pad, sticky='e')
            spinBox = Spinbox(self, textvariable=var, width=5, **floatSpinArgs)
            spinBox.grid(row=row, column=1, columnspan=3, **pad, sticky='ew')
            spinBox.bind('<FocusOut>', lambda e: self.saveValues())
            Label(self, text=unit).grid(row=row, column=4, **pad, sticky='w')
            addFloatValidation(spinBox)

    def refreshView(self):
        """
        Fills the fields using the values stored in the model
        """
        # Refresh cell-independent fields
        stim = self.model.stim
        self.xCoord.set(stim.closestIdx[0])
        self.yCoord.set(stim.closestIdx[1])
        self.zCoord.set(stim.closestIdx[2])
        self.amp.set(stim.amp)
        self.dur.set(stim.dur)
        self.delay.set(stim.delay)
        self.idxMode.set('closest' if stim.idxMode == IdxMode.CLOSEST else 'section')

        # Create cell from specified morphology each time we switch to this view
        if not self.model.hasMorphology():
            print(f'Warning: no morphology detected from {self.model.cellSource.name}')
            return
        self._cell = self.model.toLFPyCell()
        if self._cell is None:
            return

        # Refresh cell-dependant fields
        names = self._cell.allsecnames
        currentSec = self.section.get()
        if currentSec not in names:
            self.section.set('')
        self.section.configure(values=names)
        self._refreshSegIndices()

    def _refreshSegIndices(self):
        """
        Fills the fields related to the segment selection.
        """
        if self._cell is None or not any(self._cell.allseclist):
            # Recreate an LFPy.Cell object if it was destroyed
            self._cell = self.model.toLFPyCell()
            if self._cell is None:
                return
        section = self.section.get()
        # Get segment indices from the selected section
        indices = list(self._cell.get_idx(section)) if section else []
        currentIdx = safeInt(self.segIdx.get, orElse=-1)
        if currentIdx not in indices:
            self.segIdx.set('')
        self.segIdx.configure(values=indices)

    def saveValues(self):
        """
        Saves the values of the fields into the model
        """
        stim = self.model.stim

        stim.idxMode = IdxMode.CLOSEST if self.idxMode.get() == 'closest' else IdxMode.SECTION
        stim.closestIdx = (safeFloat(self.xCoord.get, orElse=stim.closestIdx[0]),
                           safeFloat(self.yCoord.get, orElse=stim.closestIdx[1]),
                           safeFloat(self.zCoord.get, orElse=stim.closestIdx[2]))

        stim.sectionIdx = safeInt(self.segIdx.get, orElse=stim.sectionIdx)

        stim.amp = safeFloat(self.amp.get, orElse=stim.amp)
        stim.dur = safeFloat(self.dur.get, orElse=stim.dur)
        stim.delay = safeFloat(self.delay.get, orElse=stim.delay)
