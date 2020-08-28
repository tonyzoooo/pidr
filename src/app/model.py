#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains classes related to the storing of the application's state.
This includes the cell morphology created with the builder, the filename of the
selected HOC file and the stimulation parameters. This also provides methods
related to the features of the application.

@author: Loïc Bertrand, Tony Zhou
"""
from enum import Enum
from typing import List, Optional, Tuple, Literal

import LFPy
from neuron import h, nrn

from src.app import plotting, section_util, config
from src.core import util, lfpy_simulation
from src.core.util import auto_str


class CellSource(Enum):
    """
    Enumeration to specify which source to use to create a morphology
    which will be used to plot the cell and to make the simulation.
    """
    BUILDER = 1  # Use morphology created with the builder
    HOC_FILE = 2  # Use morphology from selected HOC file


class AppModel:
    """
    Class to store and manage the application's state and data
    """

    def __init__(self):
        self.filename = ''
        self.selectedSection: Optional[SectionModel] = None
        self.cellSource = CellSource.BUILDER
        self.cell = CellModel()
        self.stim = StimModel()
        self.elecGrid = ElecGridModel()
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
        return bool(self.filename)

    @staticmethod
    def _loadFileIntoMemory(name):
        """
        Load an HOC file into the HOC interpreter's memory. This will clear
        any pre-existing section from the HOC interpreter's memory.

        :param name:    an HOC file path
        """
        section_util.clearNeuronSections()
        if name:
            print('Loading file', name, 'manually (CellModel::_loadFileIntoMemory)')
            try:
                h.load_file(1, name)
            except RuntimeError as e:
                print('load_file:', e)
            try:
                h.define_shape()
            except RuntimeError as e:
                print('define_shape:', e)

    def toSectionList(self) -> h.SectionList:
        """
        Converts this model into a NEURON ``SectionList``. This will clear
        any pre-existing section from the HOC interpreter's memory.

        :return:    a NEURON ``SectionList``
        """
        if self.cellSource is CellSource.BUILDER:
            return self.cell.toSectionList()
        else:  # CellSource.HOC_FILE
            AppModel._loadFileIntoMemory(self.filename)
            return h.allsec()

    def hasMorphology(self) -> bool:
        """
        :return:    ``True`` if any section is present in the selected ``CellSource``
        """
        source = self.cellSource
        return (source is CellSource.BUILDER and self.hasSections()
                or source is CellSource.HOC_FILE and self.hasHocFile())

    def toLFPyCell(self) -> Optional[LFPy.Cell]:
        """
        Converts this model into an ``LFPy.Cell`` using the selected ``CellSource``.
        This will clear any pre-existing section from the HOC interpreter's memory.

        :return:    an ``LFPy.Cell`` object or None is the model has no morphology
        """
        section_util.clearNeuronSections()

        if not self.hasMorphology():
            return None
        if self.cellSource is CellSource.BUILDER:
            return self.cell.toLFPyCell()
        else:  # CellSource.HOC_FILE
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
            try:
                return LFPy.Cell(**cell_parameters)
            except RuntimeError:
                print(f'Error during LFPy.Cell creation using file {self.filename} (AppModel::toLFPyCell)')
                return None

    def plotCell(self, dimension: Literal['2D', '3D']):
        """
        Plots the selected morphology (from builder or from file), in 2D or 3D,
        depending on the selected mode. Tries to create an ``LFPy.Cell`` and an
        LFPy Electrode object to plot the exact position of the stimulation. If
        the creation fails, it creates a simple ``h.SectionList`` and does not
        plot the electrode position.
        
        :param dimension: dimension for the plot ('2D' or '3D')
        """
        if not self.hasMorphology():
            return

        cell = self.toLFPyCell()
        if cell is not None:
            sections = cell.allseclist
            stim, _ = self.stim.toLFPyStimIntElectrode(cell)
            stimpoint = (stim.x, stim.y, stim.z)
        else:
            # Cell construction failed => no stim point plot possible
            sections = self.toSectionList()
            stimpoint = None

        if dimension == '3D':
            plotting.plot3DCell(sections, stimpoint)
        elif dimension == '2D':
            plotting.plot2DCell(sections, stimpoint)

    def doSimulation(self):
        """
        Launches the simulation using the selected ``CellSource`` and stimulation parameters
        """
        from src.core import demo
        if self.hasMorphology():
            cell = self.toLFPyCell()
            if cell is not None:
                stim, stimParams = self.stim.toLFPyStimIntElectrode(cell)
                elecGrid = self.elecGrid.toNumpyRanges()
                demo.executeDemo(cell, stim, stimParams, elecGrid)

    def fillBallStick(self):
        """
        Creates a ball & stick cell morphology
        """
        self.cell.sections.clear()
        soma = self.tryAddSection('soma')
        axon = self.tryAddSection('axon')
        dend = self.tryAddSection('dend')
        soma.nseg = 1
        soma.L = 25
        soma.diam = 25
        soma.insert('hh')
        axon.nseg = 100
        axon.L = 1000
        axon.diam = 2
        axon.insert('hh')
        dend.nseg = 5
        dend.L = 50
        dend.diam = 2
        dend.insert('pas')
        axon.connect(soma, 1, 0)
        dend.connect(soma, 0, 1)


class SectionModel:
    """
    Class to record all the information of a section and its connections with other sections.
    This class has been created to decouple the application model from NEURON objects, since
    NEURON objects do not act like typical objects (they become unusable if we remove
    ``nrn.Section`` references via ``h.delete_section(sec=sec)``.
    """

    def __init__(self, name):
        self.name = name
        self.nseg = 1
        self.L = 1  # µm
        self.diam = 1  # µm
        self.mechanism: Optional[str] = None
        self.parentSec: Optional['SectionModel'] = None
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
        if self.mechanism:
            sec.insert(self.mechanism)
        return sec


class CellModel:
    _instancesCount = 0

    def __init__(self):
        self.sections: List[SectionModel] = []
        self.displayName = f'cell[{CellModel._instancesCount}]'
        CellModel._instancesCount += 1
        self._nrnSectionsCache = []  # important, see CellModel::toSectionList

    def getSection(self, name: str) -> Optional[SectionModel]:
        for sec in self.sections:
            if sec.name == name:
                return sec
        return None

    def tryAddSection(self, name: str) -> Optional[SectionModel]:
        if self._isInvalidName(name):
            print(f"Section name '{name}' is invalid (AppModel::tryAddSection)")
            return None

        section = SectionModel(name)
        self.sections.append(section)
        return section

    def _isInvalidName(self, name):
        return name == '' or name in self.getNames() \
               or '(' in name or ')' in name

    def getNames(self) -> List[str]:
        return [sec.name for sec in self.sections]

    def toSectionList(self) -> h.SectionList:
        """
        Creates a ``h.SectionList`` object from this model. All ``nrn.Section``
        objects created are stored in ``self._nrnSectionsCache`` to avoid them
        being garbage collected and freed from NEURON's memory. (see
        https://github.com/neuronsimulator/nrn/issues/632 for a more detailed
        explanation)

        :return:    a ``h.SectionList`` object corresponding to this cell model
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
        section_util.clearNeuronSections()
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

    def toHocFormat(self) -> str:
        # Create sections
        res = f"create {', '.join(s.name for s in self.sections)}\n"
        # Connections
        for s in self.sections:
            if s.parentSec:
                res += f'connect {s.name}({s.childEnd}), {s.parentSec.name}({s.parentEnd})\n'
        res += '\n'
        # Section parameters
        for s in self.sections:
            res += (f'{s.name} {{\n'
                    f'    nseg = {s.nseg}\n'
                    f'    L = {s.L}\n'
                    f'    diam = {s.diam}\n')
            if s.mechanism:
                res += f'    insert {s.mechanism}\n'
            res += '}\n'
        return res

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
    """
    Class to store information about the stimulation.
    """

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
        """
        Converts this StimModel into an ``LFPy.StimIntElectrode`` object and also
        returns the parameters used for it's construction

        :param cell:    the ``LFPy.Cell`` object associated with this
            stimulation electrode
        :return:        a tuple consisting of the stimulation object
            and the dictionary of parameters used for it's construction
        """
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
            'pptype': self.pptype,  # Type of point process: VClamp / SEClamp / ICLamp.
            # These parameters depend on the type of point process:
            'amp': self.amp,  # Na
            'dur': self.dur,  # ms
            'delay': self.delay,  # ms
        }


class ElecGridModel:
    """
    Class to store recording electrode positions as a grid
    """

    def __init__(self):
        # Electrode positions are defined on a grid
        # by two closed ranges (start, stop, step)
        # try:
        self.xs = config.electrode_grid['xs']
        self.ys = config.electrode_grid['ys']
        # except (AttributeError, KeyError) as e:
        #     print(f'{type(e).__name__}: {e}')
        #     self.xs = (-250, 1250, 125)
        #     self.ys = (250, 50, -50)

    def toNumpyRanges(self) -> lfpy_simulation.ElectrodeRanges:
        """
        Converts this grid specification to numpy ranges.

        :return:    electrode grid as numpy arrays
        """
        xs = util.closedRange(*self.xs)
        xy = util.closedRange(*self.ys)
        return lfpy_simulation.ElectrodeRanges(xs, xy)
