#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains helper functions to validate ``int`` of ``float``
values from a ``ttk.Spinbox`` or any string value.

@author: Loïc Bertrand
"""

import sys
import tkinter.ttk as ttk
from tkinter import TclError
from typing import Callable


def safeFloat(getter: Callable[[], str], orElse: float, from_=-sys.maxsize, to=sys.maxsize) -> float:
    """
    Returns the value provided by the ``getter`` callable, converted to a ``float``.
    If it cannot be converted to a ``float``, if it isn't contained into the given range
    or if the getter throws an exception, the ``orElse`` value is returned instead.

    :param getter:  callable returning a string
    :param orElse:  fallback value
    :param from_:   minimum value (optional)
    :param to:      maximum value (optional)
    :return:        a valid ``float`` value
    """
    try:
        floatValue = float(getter())
    except (TclError, ValueError, RuntimeError):
        return orElse
    return floatValue if from_ <= floatValue <= to else orElse


def safeInt(getter: Callable[[], str], orElse: int, from_=-sys.maxsize, to=sys.maxsize) -> int:
    """
    Returns the value provided by the ``getter`` callable, converted to an ``int``.
    If it cannot be converted to a ``int``, if it isn't contained into the given range
    or if the getter throws an exception, the ``orElse`` value is returned instead.

    :param getter:  callable returning a string
    :param orElse:  fallback value
    :param from_:   minimum value (included, optional)
    :param to:      maximum value (included, optional)
    :return:        a valid ``int`` value
    """
    try:
        intValue = int(getter())
    except (TclError, ValueError):
        try:
            intValue = round(float(getter()))
        except (TclError, ValueError):
            return orElse
    return intValue if from_ <= intValue <= to else orElse


def addFloatValidation(spinBox: ttk.Spinbox, from_=-sys.maxsize, to=sys.maxsize):
    """
    Makes sure that a ttk.Spinbox only accepts valid ``float`` values

    :param spinBox:     a ttk.Spinbox
    :param from_:       minimum value (included, optional)
    :param to:          maximum value (included, optional)
    """
    _addNumberValidation(spinBox, safeFloat, from_=from_, to=to)


def addIntValidation(spinBox: ttk.Spinbox, from_=-sys.maxsize, to=sys.maxsize):
    """
    Makes sure that a ttk.Spinbox only accepts valid ``int`` values

    :param spinBox:     a ttk.Spinbox
    :param from_:       minimum value (included, optional)
    :param to:          maximum value (included, optional)
    """
    _addNumberValidation(spinBox, safeInt, from_=from_, to=to)


def _addNumberValidation(spinBox: ttk.Spinbox, safeConverter, **kwargs):
    oldValue = spinBox.get()

    def onValidation(newValue):
        nonlocal oldValue
        safe = safeConverter(lambda: newValue, oldValue, **kwargs)
        oldValue = safe
        spinBox.set(safe)
        return newValue == safe

    vcmd = (spinBox.register(onValidation), '%P')
    spinBox.configure(validatecommand=vcmd)
