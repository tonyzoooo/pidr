import tkinter as tk
from tkinter import filedialog

from model import AppModel


class OpenHocView(tk.Frame):

    def __init__(self, root: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, root)
        self.model = model
        self.root = root

        """
        Container for file selection
        """
        titleLabel = tk.Label(self, text='Extracellular potential simulation')
        titleLabel.pack()
        openHocButton = tk.Button(self, text='Open .hoc', command=self._openFile)
        openHocButton.pack()

    def _openFile(self):
        self.model.filename = filedialog.askopenfilename(
            initialdir='../../resources',
            title='Select file',
            filetypes=(('hoc files', '*.hoc'), ('all files', '*.*'))
        )
        if self.model.filename != "":
            print('Opened: ' + self.model.filename)
