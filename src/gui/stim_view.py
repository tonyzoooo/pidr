from tkinter import IntVar
from tkinter.ttk import *

from src.gui.model import AppModel
from src.gui.number_validation import addFloatValidation


class StimView(Frame):

    def __init__(self, master, model: AppModel):
        super().__init__(master, padding=4)
        self.model = model

        pad = {'padx': 4, 'pady': 4}

        self.idxMode = IntVar(value=1)
        self.idxMode.trace_variable('w', lambda a, b, c: ...)
        Radiobutton(self, text='closest idx', variable=self.idxMode, value=1).grid(row=1, column=0, **pad)
        Radiobutton(self, text='section idx', variable=self.idxMode, value=2).grid(row=2, column=0, **pad)

        self.xCoord, self.yCoord, self.zCoord = (Spinbox(self, width=5) for _ in [1, 2, 3])
        for col, lbl, spinBox in (1, 'x', self.xCoord), \
                                 (2, 'y', self.yCoord), \
                                 (3, 'z', self.zCoord):
            Label(self, text=lbl).grid(row=0, column=col)
            spinBox.grid(row=1, column=col, **pad)
            addFloatValidation(spinBox)

        self.section = Combobox(self, values=['soma', 'dend', 'axon'], state='readonly', width=12)
        self.section.grid(row=2, column=1, columnspan=2, **pad, sticky='ew')
        self.segIdx = Spinbox(self, width=5)
        self.segIdx.grid(row=2, column=3, **pad)

        self.amp, self.dur, self.delay = (Spinbox(self) for _ in [1, 2, 3])
        for row, lbl, spinBox in (3, 'amp', self.amp), \
                                 (4, 'dur', self.dur), \
                                 (5, 'delay', self.delay):
            Label(self, text=lbl).grid(row=row, column=0, **pad, sticky='e')
            spinBox.grid(row=row, column=1, columnspan=3, **pad, sticky='ew')

    def refreshView(self):
        pass
