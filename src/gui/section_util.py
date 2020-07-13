from typing import Optional, Tuple

from neuron import nrn, h

ParentConnection = Tuple[int, nrn.Section, int]


def getMechanism(section: nrn.Section) -> Optional[str]:
    firstSegment = next(iter(section))
    return 'hh' if hasattr(firstSegment, 'hh') \
        else 'pas' if hasattr(firstSegment, 'pas') \
        else None


def setMechanism(section: nrn.Section, mech: Optional[str]):
    actual = getMechanism(section)
    if mech == actual:
        return
    if actual is not None:
        section.uninsert(actual)
    if mech is not None:
        section.insert(mech)


def setParent(child: nrn.Section, parent: Optional[ParentConnection]):
    h.disconnect(child)
    if parent is None:
        return
    childEnd, parent, parentEnd = parent
    child.connect(parent, parentEnd, childEnd)  # May exit(1) if wrong connection


def getParent(child: nrn.Section) -> Optional[ParentConnection]:
    parentSeg = child.parentseg()
    if parentSeg is None:
        return None
    else:
        childEnd = int(child.orientation())
        parent = parentSeg.sec
        parentEnd = int(parentSeg.x)
        return childEnd, parent, parentEnd


def simpleName(section: nrn.Section) -> str:
    return section.hname().split('.')[-1]
