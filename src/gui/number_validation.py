import sys
from math import ceil
from tkinter import TclError
from typing import Callable


def safeFloat(getter: Callable[[], str], orElse: float = 1.0, _from=-sys.maxsize, to=sys.maxsize) -> float:
    try:
        floatValue = float(getter())
    except (TclError, ValueError):
        return orElse
    return floatValue if _from <= floatValue <= to else orElse


def safeInt(getter: Callable[[], str], orElse: int = 1.0, _from=-sys.maxsize, to=sys.maxsize) -> int:
    try:
        intValue = int(getter())
    except (TclError, ValueError):
        try:
            intValue = ceil(float(getter()))
        except (TclError, ValueError):
            return orElse
    return intValue if _from <= intValue <= to else orElse


def addFloatValidation(spinBox, _from=-sys.maxsize, to=sys.maxsize):
    _addNumberValidation(spinBox, safeFloat, _from=_from, to=to)


def addIntValidation(spinBox, _from=-sys.maxsize, to=sys.maxsize):
    _addNumberValidation(spinBox, safeInt, _from=_from, to=to)


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
