from typing import List, Iterable

from neuron import h, nrn


def clearAllSec():
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


def getCellDimensions(sections: Iterable[nrn.Section]) -> dict:
    """
    Takes an iterable of ``nrn.Section`` objects and returns a dictionary
    containing the dimensions of the soma, axon and dendrite.

    :param sections:    iterable of ``nrn.Section`` (List[Section] or SectionList)
    :return:            dictionary of dimensions
    """
    props = {}
    for sec in sections:
        name: str = sec.hname()
        if name.find('soma') >= 0:
            props['SL'] = sec.L
        elif name.find('axon') >= 0:
            props['AL'] = sec.L
            props['AD'] = sec.diam
        elif name.find('dend') >= 0:
            props['DL'] = sec.L
            props['DD'] = sec.diam
    return props
