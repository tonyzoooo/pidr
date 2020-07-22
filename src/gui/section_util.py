from neuron import h


# ParentConnection = Tuple[int, nrn.Section, int]
#
#
# def getMechanism(section: nrn.Section) -> Optional[str]:
#     firstSegment = next(iter(section))
#     return 'hh' if hasattr(firstSegment, 'hh') \
#         else 'pas' if hasattr(firstSegment, 'pas') \
#         else None
#
#
# def setMechanism(section: nrn.Section, mech: Optional[str]):
#     actual = getMechanism(section)
#     if mech == actual:
#         return
#     if actual is not None:
#         section.uninsert(actual)
#     if mech is not None:
#         section.insert(mech)
#
#
# def setParent(child: nrn.Section, parent: Optional[ParentConnection]):
#     h.disconnect(sec=child)
#     if parent is None:
#         return
#     childEnd, parent, parentEnd = parent
#     child.connect(parent, parentEnd, childEnd)  # May exit(1) if wrong connection
#
#
# def getParent(child: nrn.Section) -> Optional[ParentConnection]:
#     parentSeg = child.parentseg()
#     if parentSeg is None:
#         return None
#     else:
#         childEnd = int(child.orientation())
#         parent = parentSeg.sec
#         parentEnd = int(parentSeg.x)
#         return childEnd, parent, parentEnd


# def simpleName(section: nrn.Section) -> str:
#     return section.hname().split('.')[-1]

def fileSections():
    return [sec for sec in h.allsec() if sec.cell() is None]


def hasFileSections():
    for s in h.allsec():
        if s.cell() is None:
            return True
    return False


def getBSProperties(sections) -> dict:
    props = {}
    for sec in sections:
        name: str = sec.name()
        if name.find('soma') >= 0:
            props['SL'] = sec.L
        elif name.find('axon') >= 0:
            props['AL'] = sec.L
            props['AD'] = sec.diam
        elif name.find('dend') >= 0:
            props['DL'] = sec.L
            props['DD'] = sec.diam
    return props
