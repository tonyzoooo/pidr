#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  5 21:54:28 2020

@author: tonyz
"""

import tkinter as tk

from config_view import ConfigView
from open_hoc_view import OpenHocView
from sections_view import SectionsView
from model import AppModel


class App(tk.Frame):

    def __init__(self, root: tk.Tk, model: AppModel):
        tk.Frame.__init__(self, root)
        self.root = root
        self.model = model

        root.geometry('500x400')
        root.title('Simulator :)')
        root.bind('<Escape>', lambda e: exit())
        root.protocol("WM_DELETE_WINDOW", lambda: exit())

        pad = {'padx': 10, 'pady': 10}

        self.configView = ConfigView(root, model)
        self.configView.grid(row=0, column=1, **pad)

        self.sectionsView = SectionsView(root, model)
        self.sectionsView.grid(row=0, column=0, **pad)
        self.sectionsView.beforeSelection(self.configView.saveCurrentSection)
        self.sectionsView.afterSelection(self.configView.refreshView)

        self.openHocView = OpenHocView(root, model)
        self.openHocView.grid(row=1, column=0, columnspan=2, **pad)

    @staticmethod
    def launch():
        root = tk.Tk()
        model = AppModel()
        App(root, model)
        root.mainloop()
        return model


if __name__ == '__main__':
    App.launch()