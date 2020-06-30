import sys
from math import ceil
from tkinter import TclError
from typing import Callable


def safeFloat(getter: Callable[[], str], orElse: float = 1.0, from_=-sys.maxsize, to=sys.maxsize) -> float:
    try:
        floatValue = float(getter())
    except (TclError, ValueError):
        return orElse
    return floatValue if from_ <= floatValue <= to else orElse


def safeInt(getter: Callable[[], str], orElse: int = 1.0, from_=-sys.maxsize, to=sys.maxsize) -> int:
    try:
        intValue = int(getter())
    except (TclError, ValueError):
        try:
            intValue = ceil(float(getter()))
        except (TclError, ValueError):
            return orElse
    return intValue if from_ <= intValue <= to else orElse


def addFloatValidation(spinBox, from_=-sys.maxsize, to=sys.maxsize):
    _addNumberValidation(spinBox, safeFloat, from_=from_, to=to)


def addIntValidation(spinBox, from_=-sys.maxsize, to=sys.maxsize):
    _addNumberValidation(spinBox, safeInt, from_=from_, to=to)


def _addNumberValidation(spinBox, safeConverter, **kwargs):
    oldValue = spinBox.get()

    def onValidation(newValue):
        nonlocal oldValue
        safe = safeConverter(lambda: newValue, orElse=oldValue, **kwargs)
        oldValue = safe
        spinBox.set(safe)
        return newValue == safe

    vcmd = (spinBox.register(onValidation), '%P')
    spinBox.configure(validatecommand=vcmd)
