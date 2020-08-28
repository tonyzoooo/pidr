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
    Tries to convert the value supplied by the ``getter`` to an int or to a float,
    contained in the (optionally) given range or returns the ``orElse`` default
    value if any error occurred.

    :param getter:  callable returning a string
    :param orElse:  fallback value
    :param from_:   minimum value (optional)
    :param to:      maximum value (optional)
    :return:        a valid ``float`` value

    Examples
    --------
    >>> safeFloat(lambda: '0.2', orElse=12)
    0.2
    >>> safeFloat(lambda: '', orElse=42)
    42
    >>> safeFloat(lambda: '0', orElse=100.0, from_=10)
    100.0
    """
    try:
        value = getter()
    except (TclError, RuntimeError):
        return orElse

    if type(value) not in [int, float]:
        try:
            value = int(value)
        except (ValueError, RuntimeError):
            try:
                value = float(value)
            except (ValueError, RuntimeError):
                return orElse

    return value if from_ <= value <= to else orElse


def safeInt(getter: Callable[[], str], orElse: int, from_=-sys.maxsize, to=sys.maxsize) -> int:
    """
    Tries to convert the value supplied by the ``getter`` to an int, contained
    in the (optionally) given range or returns the ``orElse`` default value if
    any error occurred.

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
