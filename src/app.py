#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class App(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg='blue')
        self.master = master
        master.style = ttk.Style()
        master.style.theme_use("clam")
        master.geometry("300x150")
        master.title("Simulator :)")
        self.container = tk.Frame(self)
        self.label = tk.Label(text="Simulation de potentiels extracellulaires")
        self.button = tk.Button(text="Ouvrir .hoc", command=self.openFile)
        self.filename = ""
        self.label.pack()
        self.button.pack()
        master.bind("<Escape>", lambda e: master.destroy())

    @staticmethod
    def launch():
        root = tk.Tk()
        mainApp = App(root)
        root.mainloop()
        return mainApp

    def openFile(self):
        self.filename = filedialog.askopenfilename(
            initialdir="../resources",
            title="Select file",
            filetypes=(("hoc files", "*.hoc"), ("all files", "*.*"))
        )
        print("Opened: " + self.filename)
        self.master.destroy()


# if __name__ == "__main__":
#     root = tk.Tk()
#     mainApp = App(root)
#     root.mainloop()
