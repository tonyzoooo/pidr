from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from model import AppModel


class OpenHocView(Frame):

    def __init__(self, root: Tk, model: AppModel):
        """
        Container for file selection
        """
        super().__init__(root)
        self.model = model
        self.root = root

        titleLabel = Label(self, text='Extracellular potential simulation')
        titleLabel.pack()
        openHocButton = Button(self, text='Open .hoc', command=self._openFile)
        openHocButton.pack()

    def _openFile(self):
        self.model.filename = filedialog.askopenfilename(
            initialdir='../../resources',
            title='Select file',
            filetypes=(('hoc files', '*.hoc'), ('all files', '*.*'))
        )
        if self.model.filename != "":
            print('Opened: ' + self.model.filename)
