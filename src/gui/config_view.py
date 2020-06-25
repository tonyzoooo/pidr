import tkinter as tk

from tkvalidate import float_validate

from model import AppModel


class ConfigView(tk.Frame):

    def __init__(self, root: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, root)
        self.model = model

        """
        Container for the configuration of the selected section
        """
        spinArgs = {'from_': 0, 'to': 1000, 'increment': 0.1}

        self.selectedSectionLabel = tk.Label(self, text='<no section selected>')
        self.selectedSectionLabel.grid(row=0, column=1)

        self.lengthVar = tk.DoubleVar()
        lengthLabel = tk.Label(self, text='L')
        lengthLabel.grid(row=1, column=0)
        lengthEntry = tk.Spinbox(self, textvariable=self.lengthVar, **spinArgs)
        float_validate(lengthEntry)
        lengthEntry.grid(row=1, column=1)
        lengthEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.diamVar = tk.DoubleVar()
        dimLabel = tk.Label(self, text='diam')
        dimLabel.grid(row=2, column=0)
        diamEntry = tk.Spinbox(self, textvariable=self.diamVar, **spinArgs)
        float_validate(diamEntry)
        diamEntry.grid(row=2, column=1)
        diamEntry.bind('<FocusOut>', lambda e: self.saveCurrentSection())

        self.end0Var = tk.StringVar()
        end0Label = tk.Label(self, text='end 0')
        end0Label.grid(row=3, column=0)
        end0Entry = tk.OptionMenu(self, self.end0Var, '', *self.model.sectionNames)
        end0Entry.grid(row=3, column=1, sticky='nsew')

        self.end1Var = tk.StringVar()
        end1Label = tk.Label(self, text='end 1')
        end1Label.grid(row=4, column=0)
        end1Entry = tk.OptionMenu(self, self.end1Var, '', *self.model.sectionNames)
        end1Entry.grid(row=4, column=1, sticky='nsew')

    def refreshView(self):
        """
        Refreshes the section configuration view using:
        - the currently selected section in self.sectionList
        - the data of the corresponding section in the model (self.model)
        """
        name = self.model.selectedSectionName
        self.selectedSectionLabel.configure(text=name)
        section = self.model.selectedSection
        if section is None:
            return

        self.lengthVar.set(section.L)
        self.diamVar.set(section.diam)

    def saveCurrentSection(self):
        """
        Saves the current section's data
        """
        section = self.model.selectedSection
        if section is not None:
            section.diam = self.diamVar.get()
            section.L = self.lengthVar.get()
