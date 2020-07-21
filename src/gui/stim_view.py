from tkinter import *
from tkinter.ttk import *

from src.gui import section_util
from src.gui.model import AppModel, IdxMode
from src.gui.number_validation import addFloatValidation, addIntValidation, safeFloat


class StimView(Frame):

    def __init__(self, master, model: AppModel):
        super().__init__(master, padding=4)
        self.model = model

        pad = {'padx': 4, 'pady': 4}

        self.idxMode = IntVar(value=1)
        self.idxMode.trace_add('write', lambda a, b, c: self.saveStim())
        Radiobutton(self, text='closest idx', variable=self.idxMode, value=1).grid(row=1, column=0, **pad)
        Radiobutton(self, text='section idx', variable=self.idxMode, value=2).grid(row=2, column=0, **pad)

        self.xCoord, self.yCoord, self.zCoord = DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)
        for col, lbl, var in (1, 'x', self.xCoord), \
                             (2, 'y', self.yCoord), \
                             (3, 'z', self.zCoord):
            Label(self, text=lbl).grid(row=0, column=col)
            spinBox = Spinbox(self, textvariable=var, width=5)
            spinBox.grid(row=1, column=col, **pad)
            spinBox.bind('<FocusOut>', lambda e: self.saveStim())
            addFloatValidation(spinBox)

        self.section = Combobox(self, values=['soma', 'dend', 'axon'], state='readonly', width=12)
        self.section.grid(row=2, column=1, columnspan=2, **pad, sticky='ew')
        self.segIdx = Spinbox(self, width=5)
        self.segIdx.grid(row=2, column=3, **pad)
        addIntValidation(self.segIdx)

        self.amp, self.dur, self.delay = DoubleVar(value=0), DoubleVar(value=0), DoubleVar(value=0)
        for row, lbl, var in (3, 'amp', self.amp), \
                             (4, 'dur', self.dur), \
                             (5, 'delay', self.delay):
            Label(self, text=lbl).grid(row=row, column=0, **pad, sticky='e')
            spinBox = Spinbox(self, textvariable=var)
            spinBox.grid(row=row, column=1, columnspan=3, **pad, sticky='ew')
            spinBox.bind('<FocusOut>', lambda e: self.saveStim())
            addFloatValidation(spinBox)

    def refreshView(self):
        # Should be trigered each time we switch to the stimulation tab
        # Fills the entries depending on the morphology
        cell = self.model.toLFPyCell()
        stim = self.model.stim
        names = self.model.sectionNames

        self.section.configure(values=names)

    def saveStim(self):
        cell = self.model.toLFPyCell()
        stim = self.model.stim

        stim.idxMode = IdxMode.CLOSEST if self.idxMode.get() == 1 else IdxMode.SECTION
        stim.closestIdx = (safeFloat(self.xCoord.get, orElse=stim.closestIdx[0]),
                           safeFloat(self.yCoord.get, orElse=stim.closestIdx[1]),
                           safeFloat(self.zCoord.get, orElse=stim.closestIdx[2]))

        stim.amp = safeFloat(self.amp.get, orElse=stim.amp)
        stim.dur = safeFloat(self.dur.get, orElse=stim.dur)
        stim.delay = safeFloat(self.delay.get, orElse=stim.delay)

        print(stim)
