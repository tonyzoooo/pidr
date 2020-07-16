from tkinter import IntVar
from tkinter.ttk import *

from src.gui.model import AppModel


class StimView(Frame):

    def __init__(self, master, model: AppModel):
        super().__init__(master, padding=4)
        self.model = model

        pad = {'padx': 4, 'pady': 4}

        Label(self, text='x').grid(row=0, column=1)
        Label(self, text='y').grid(row=0, column=2)
        Label(self, text='z').grid(row=0, column=3)

        self.idxMode = IntVar(value=1)
        self.idxMode.trace_variable('w', lambda a, b, c: print(self.idxMode.get()))
        Radiobutton(self, text='closest idx', variable=self.idxMode, value=1).grid(row=1, column=0, **pad)
        Radiobutton(self, text='section idx', variable=self.idxMode, value=2).grid(row=2, column=0, **pad)
        self.xCoord = Spinbox(self, width=5)
        self.xCoord.grid(row=1, column=1, **pad)
        self.yCoord = Spinbox(self, width=5)
        self.yCoord.grid(row=1, column=2, **pad)
        self.zCoord = Spinbox(self, width=5)
        self.zCoord.grid(row=1, column=3, **pad)
        self.section = Combobox(self, values=['soma', 'dend', 'axon'], state='readonly', width=12)
        self.section.grid(row=2, column=1, columnspan=2, **pad, sticky='ew')
        self.segIdx = Spinbox(self, width=5)
        self.segIdx.grid(row=2, column=3, **pad)

        Label(self, text='amp').grid(row=3, column=0, **pad, sticky='e')
        self.amp = Spinbox(self)
        self.amp.grid(row=3, column=1, columnspan=3, **pad, sticky='ew')
        Label(self, text='dur').grid(row=4, column=0, **pad, sticky='e')
        self.dur = Spinbox(self)
        self.dur.grid(row=4, column=1, columnspan=3, **pad, sticky='ew')
        Label(self, text='delay').grid(row=5, column=0, **pad, sticky='e')
        self.delay = Spinbox(self)
        self.delay.grid(row=5, column=1, columnspan=3, **pad, sticky='ew')