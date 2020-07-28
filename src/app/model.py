from enum import Enum
from typing import List, Optional, Tuple

import LFPy
from neuron import h, nrn

from src.core.util import auto_str
from src.app import section_util


class CellSource(Enum):
    """
    Enumeration to specify which source to use to create a morphology
    which will be used to plot the cell and to make the simulation.
    """
    BUILDER = 1  # Use moprhology created with the builder
    HOC_FILE = 2  # Use morphology from selected HOC file


class AppModel:

    def __init__(self):
        self.filename = None
        self.selectedSection: Optional[SectionModel] = None
        self.cell = CellModel()
        self.cellSource = CellSource.BUILDER
        self.stim = StimModel()
        h.load_file('stdlib.hoc')

    @property
    def selectedSectionName(self) -> Optional[str]:
        if self.selectedSection is None:
            return None
        return self.selectedSection.name

    def trySelectSection(self, name: str) -> bool:
        section = self.cell.getSection(name)
        if section is None:
            return False
        self.selectedSection = section
        return True

    def tryAddSection(self, name: str) -> Optional['SectionModel']:
        return self.cell.tryAddSection(name)

    def getSection(self, name: str) -> Optional['SectionModel']:
        return self.cell.getSection(name)

    def getPossibleConnections(self, section: 'SectionModel') -> List[Tuple['SectionModel', int]]:
        result = []
        for sec in self.cell.sections:
            if sec != section:
                if sec.parentSec is None or sec.childEnd != 0:
                    result.append((sec, 0))
                if sec.parentSec is None or sec.childEnd != 1:
                    result.append((sec, 1))
        return result

    def hasSections(self):
        return len(self.cell.sections) != 0

    def hasHocFile(self):
        return self.filename is not None

    @staticmethod
    def _loadFileIntoMemory(name):
        section_util.clearAllSec()
        if name:
            print('loading file', name)
            try:
                h.load_file(1, name)
            except RuntimeError as e:
                print('load_file:', e)
            try:
                h.define_shape()
            except RuntimeError as e:
                print('define_shape:', e)

    @property
    def sectionNames(self) -> List[str]:
        source = self.cellSource
        if source is CellSource.BUILDER:
            return self.cell.getNames()

    def toSectionList(self) -> h.SectionList:
        if self.cellSource is CellSource.BUILDER:
            return self.cell.toSectionList()
        else:
            AppModel._loadFileIntoMemory(self.filename)
            return h.allsec()

    def hasMorphology(self) -> bool:
        source = self.cellSource
        return (source is CellSource.BUILDER and self.hasSections()
                or source is CellSource.HOC_FILE and self.hasHocFile())

    def toLFPyCell(self) -> Optional[LFPy.Cell]:
        if not self.hasMorphology():
            return None
        if self.cellSource is CellSource.BUILDER:
            return self.cell.toLFPyCell()
        else:
            cell_parameters = {
                'morphology': self.filename,
                'v_init': -65,  # Initial membrane potential. Defaults to -70 mV
                'passive': True,  # Passive mechanisms are initialized if True
                'passive_parameters': {'g_pas': 1. / 30000, 'e_pas': -65},
                'cm': 1.0,  # Membrane capacitance
                'Ra': 150,  # Axial resistance
                'dt': 1 / 1000,  # simulation timestep
                'tstart': 0.,  # Initialization time for simulation <= 0 ms
                'tstop': 20.,  # Stop time for simulation > 0 ms
                'nsegs_method': 'lambda_f',  # spatial discretization method
                'lambda_f': 100.,  # frequency where length constants are computed
                'delete_sections': False,
            }
            return LFPy.Cell(**cell_parameters)

    def doSimulation(self):
        from src.core import demo
        if self.hasMorphology():
            cell = self.toLFPyCell()
            dims = section_util.getCellDimensions(cell.allseclist)
            stim, stimParams = self.stim.toLFPyStimIntElectrode(cell)
            demo.executeDemo(cell, stim, stimParams, dims)


class SectionModel:

    def __init__(self, name):
        self.name = name
        self.nseg = 1
        self.L = 1  # µm
        self.diam = 1  # µm
        self.mechanism = None
        self.parentSec = None
        self.childEnd = 0  # orientation
        self.parentEnd = 0

    def connect(self, parent: 'SectionModel', parentEnd: int, childEnd: int):
        self.parentSec = parent
        self.parentEnd = parentEnd
        self.childEnd = childEnd

    def insert(self, mechanism: str):
        self.mechanism = mechanism

    def toNrnSection(self) -> nrn.Section:
        sec = h.Section(name=self.name)
        sec.nseg = self.nseg
        sec.L = self.L
        sec.diam = self.diam
        sec.insert(self.mechanism)
        return sec


class CellModel:
    _instancesCount = 0

    def __init__(self):
        self.sections: List[SectionModel] = []
        self.displayName = f'cell[{CellModel._instancesCount}]'
        CellModel._instancesCount += 1
        self._nrnSectionsCache = []  # important, see self.toSectionList

    def getSection(self, name: str) -> Optional[SectionModel]:
        for sec in self.sections:
            if sec.name == name:
                return sec
        return None

    def tryAddSection(self, name: str) -> Optional[SectionModel]:
        if self._isInvalidName(name):
            print(f"name '{name}' is invalid")
            return None

        section = SectionModel(name)
        self.sections.append(section)
        return section

    def _isInvalidName(self, name):
        return name == '' or name in self.getNames() \
               or '(' in name or ')' in name or '.' in name

    def getNames(self) -> List[str]:
        return [sec.name for sec in self.sections]

    def toSectionList(self) -> h.SectionList:
        """
        Creates a ``h.SectionList`` object from this model. All ``nrn.Section``
        objects created are stored in ``self._nrnSectionsCache`` to avoid them
        being garbage collected and freed from NEURON's memory. (see
        https://github.com/neuronsimulator/nrn/issues/632 for a more detailed
        explanation)

        :return: a ``h.SectionList`` object corresponding to this cell model
        """
        nrnSections = [sec.toNrnSection() for sec in self.sections]
        secList = h.SectionList(nrnSections)
        # Same connections
        for nrnSec, sec in zip(nrnSections, self.sections):
            if sec.parentSec is not None:
                nrnParent = CellModel._findSimilarSection(nrnSections, sec.parentSec)
                nrnSec.connect(nrnParent, sec.parentEnd, sec.childEnd)
        h.define_shape()
        self._nrnSectionsCache = nrnSections
        return secList

    @staticmethod
    def _findSimilarSection(secList: List[nrn.Section], section: SectionModel) -> Optional[nrn.Section]:
        for s in secList:
            if s.hname() == section.name:
                return s
        return None

    def toLFPyCell(self) -> LFPy.Cell:
        sectionList = self.toSectionList()
        cell_parameters = {
            'morphology': sectionList,
            'v_init': -65,  # Initial membrane potential. Defaults to -70 mV
            'passive': True,  # Passive mechanisms are initialized if True
            'passive_parameters': {'g_pas': 1. / 30000, 'e_pas': -65},
            'cm': 1.0,  # Membrane capacitance
            'Ra': 150,  # Axial resistance
            'dt': 1 / 1000,  # simulation timestep
            'tstart': 0.,  # Initialization time for simulation <= 0 ms
            'tstop': 20.,  # Stop time for simulation > 0 ms
            'nsegs_method': 'lambda_f',  # spatial discretization method
            'lambda_f': 100.,  # frequency where length constants are computed
            'delete_sections': False,
            # 'verbose': True
        }
        return LFPy.Cell(**cell_parameters)

    def __str__(self):
        return self.displayName


class IdxMode(Enum):
    """
    Enumeration to specify the way to select a segment to be the
    source of a stimulation.
    """
    CLOSEST = 1  # Segment closest to a point in 3D space
    SECTION = 2  # Specific segment of a given section


@auto_str
class StimModel:

    def __init__(self):
        # Cell segment index where the stimulation electrode is placed
        self.idxMode = IdxMode.CLOSEST
        self.closestIdx = (0.0, 0.0, 0.0)
        self.sectionIdx = 0
        # Type of point process:
        # - ICLamp: Single pulse current clamp point process
        # - VClamp: Two electrode voltage clamp with three levels
        # - SEClamp: Single electrode voltage clamp with three levels
        self.pptype = 'IClamp'
        self.amp = 0.2  # nA
        self.dur = 10.0  # ms
        self.delay = 1.0  # ms

    def toLFPyStimIntElectrode(self, cell: LFPy.Cell) -> (LFPy.StimIntElectrode, dict):
        stim_parameters = self.getParams(cell)
        stim = LFPy.StimIntElectrode(cell, **stim_parameters)
        return stim, stim_parameters

    def _getIdx(self, cell: LFPy.Cell) -> int:
        if self.idxMode is IdxMode.CLOSEST:
            return cell.get_closest_idx(*self.closestIdx)
        elif self.idxMode is IdxMode.SECTION:
            return self.sectionIdx

    def getParams(self, cell: LFPy.Cell):
        return {
            'idx': self._getIdx(cell),
            'record_current': True,
            'pptype': self.pptype,
            'amp': self.amp,
            'dur': self.dur,
            'delay': self.delay,
        }