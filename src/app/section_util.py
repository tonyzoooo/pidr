#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains utility functions related to ``nrn.Section`` objects.

@author: Loïc Bertrand
"""

from typing import List, Iterable, Optional

from neuron import h, nrn


def clearNeuronSections():
    """
    Deletes all sections from the HOC interpreter's memory.
    If ``nrn.Section`` objects have a Python reference somewhere, they
    become unusable (``<deleted section>``).
    """
    for sec in h.allsec():
        h.delete_section(sec=sec)


def fileSections() -> List[nrn.Section]:
    """
    Returns a list of the ``nrn.Section`` objects which are in the HOC
    interpreter's memory and which are not associated to a cell.
    These sections have probably been loaded from a HOC file.

    :return:    list of sections loaded from a file
    """
    return [sec for sec in h.allsec() if sec.cell() is None]


def computeDimensions(sections: Iterable[nrn.Section]) -> dict:
    """
    Takes an iterable of ``nrn.Section`` objects and returns a dictionary
    containing the dimensions of the soma, axon and dendrite.

    :param sections:    iterable of ``nrn.Section`` (List[Section] or SectionList)
    :return:            dictionary of dimensions
    """
    props = {}
    for sec in sections:
        dendLens = []
        dendDiams = []
        name: str = sec.hname()
        if name.find('soma') >= 0:
            props['SL'] = sec.L
        elif name.find('axon') >= 0:
            props['AL'] = sec.L
            props['AD'] = sec.diam
        elif name.find('dend') >= 0:
            # props['DL'] = sec.L
            # props['DD'] = sec.diam
            dendLens.append(sec.L)
            dendDiams.append(sec.diam)
        avgLen = avg(dendLens)
        if avgLen is not None:
            props['DL'] = avgLen
        avgDiam = avg(dendDiams)
        if avgDiam is not None:
            props['DD'] = avgDiam
    return props


def avg(numbers: List[float]) -> Optional[float]:
    if not numbers:
        return None
    return sum(numbers) / len(numbers)
