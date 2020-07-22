from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *

from src.gui.model import AppModel


class OpenHocView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for file selection
        """
        super().__init__(master)
        self.model = model
        master.grid_columnconfigure(0, weight=1)  # center horizontally

        openHocButton = Button(self, text='Open .hoc', command=self._openFile)
        openHocButton.pack(padx=8, pady=(64, 8))

        self.fileLabel = Label(self, text='No file selected', wraplength=400)
        self.fileLabel.pack(padx=8, pady=8)

    def _openFile(self):
        name = filedialog.askopenfilename(
            initialdir='../../resources',
            title='Select file',
            filetypes=(('hoc files', '*.hoc'), ('all files', '*.*'))
        )
        self.model.filename = name if name != '' else None
        self.refreshView()

    def refreshView(self):
        text = self.model.filename or 'No file selected'
        self.fileLabel.configure(text=text)
