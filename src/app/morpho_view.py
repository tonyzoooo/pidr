#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand
"""

from tkinter import *
from tkinter.ttk import *

from src.app.config_view import ConfigView
from src.app.model import AppModel, CellSource
from src.app.open_hoc_view import OpenHocView
from src.app.sections_view import SectionsView


class MorphologyView(Frame):

    def __init__(self, master, model: AppModel):
        """
        Container for creating or loading a cell morphology

        :param master: parent container
        :param model: app model
        """

        super().__init__(master)
        self.model = model

        pad = {'padx': 8, 'pady': 8}

        # Ball & Stick builder
        self.builderFrame = Frame(self, padding=8)
        self.sectionsView = SectionsView(self.builderFrame, model)
        self.sectionsView.grid(row=0, column=0, rowspan=2, **pad)
        self.configView = ConfigView(self.builderFrame, model)
        self.configView.grid(row=0, column=1, columnspan=2, **pad)
        ballstickButton = Button(self.builderFrame, text='Example', command=self._fillBallStick)
        ballstickButton.grid(row=1, column=1, **pad)
        useFileButton = Button(self.builderFrame, text='Use HOC file', command=self._switchToFile)
        useFileButton.grid(row=1, column=2, **pad)
        self.builderFrame.pack()

        # Hoc file loader
        self.hocFileFrame = Frame(self, padding=8)
        self.openHocView = OpenHocView(self.hocFileFrame, model)
        self.openHocView.grid(row=1, column=0, **pad)
        useBuilderButton = Button(self.hocFileFrame, text='Use builder', command=self._switchToBuilder)
        useBuilderButton.grid(row=2, column=0, **pad)
        self.pack()

        self.sectionsView.beforeSectionSelected(self.configView.saveCurrentSection)
        self.sectionsView.afterSectionSelected(self.configView.refreshView)

    def _fillBallStick(self):
        """
        Creates a ball & stick cell morphology and refreshes the gui
        """
        self.model.fillBallStick()
        self.sectionsView.refreshView()

    def _switchToFile(self):
        """
        Replaces the builder view with the file loader view
        """
        self.builderFrame.pack_forget()
        self.hocFileFrame.pack()
        self.model.cellSource = CellSource.HOC_FILE
        self.openHocView.refreshView()

    def _switchToBuilder(self):
        """
        Replaces the file loader with the builder view
        """
        self.hocFileFrame.pack_forget()
        self.builderFrame.pack()
        self.model.cellSource = CellSource.BUILDER
        self.sectionsView.refreshView()
