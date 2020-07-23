from neuron import h


def clearAllSec():
    for sec in h.allsec():
        h.delete_section(sec=sec)


def fileSections():
    return [sec for sec in h.allsec() if sec.cell() is None]


def getBSProperties(sections: h.SectionList) -> dict:
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
