# SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021-2023 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import timeit

from PySide2.QtCore import QObject, Signal, Slot, Property
from easyCore.Utils.UndoRedo import property_stack_deco


class PhaseProxy(QObject):

    dummySignal = Signal()

    phasesAsObjChanged = Signal()
    phasesAsXmlChanged = Signal()
    phasesAsCifChanged = Signal()
    currentPhaseChanged = Signal()
    phasesEnabled = Signal()
    structureParametersChanged = Signal()
    structureViewChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_phase

        self.structureParametersChanged.connect(self._onStructureParametersChanged)
        # logics sending signal
        self.logic.structureParametersChanged.connect(self.structureParametersChanged)

        self.logic.phaseAdded.connect(self._onPhaseAdded)
        self.logic.phasesEnabled.connect(self.phasesEnabled)
        self.logic.phasesAsObjChanged.connect(self.phasesAsObjChanged)
        self.logic.phasesAsObjChanged.connect(self.structureViewChanged)

        self.currentPhaseChanged.connect(self._onCurrentPhaseChanged)

    ####################################################################################################################
    # Phase models (list, xml, cif)
    ####################################################################################################################

    @Property('QVariant', notify=phasesAsObjChanged)
    def phasesAsObj(self):
        return self.logic._phases_as_obj

    @Property(str, notify=phasesAsXmlChanged)
    def phasesAsXml(self):
        return self.logic._phases_as_xml

    @Property(str, notify=phasesAsCifChanged)
    def phasesAsCif(self):
        return self.logic._phases_as_cif

    @Property(str, notify=structureViewChanged)
    def currentPhaseAsExtendedCif(self):
        return self.logic.currentPhaseAsExtendedCif()

    @phasesAsCif.setter
    @property_stack_deco
    def phasesAsCif(self, phases_as_cif):
        self.logic.phasesAsCif(phases_as_cif)

    def _setPhasesAsObj(self):
        start_time = timeit.default_timer()
        self.logic._setPhasesAsObj()
        print("+ _setPhasesAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsObjChanged.emit()
        self.structureViewChanged.emit()

    def _setPhasesAsXml(self):
        start_time = timeit.default_timer()
        self.logic._setPhasesAsXml()
        print("+ _setPhasesAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsXmlChanged.emit()

    def _setPhasesAsCif(self):
        start_time = timeit.default_timer()
        self.logic._setPhasesAsCif()
        print("+ _setPhasesAsCif: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.phasesAsCifChanged.emit()

    def _onStructureParametersChanged(self):
        print("***** _onStructureParametersChanged")
        self._setPhasesAsObj()
        self._setPhasesAsXml()
        self._setPhasesAsCif()
        self.parent._project_proxy.stateChanged.emit(True)

    ####################################################################################################################
    # Phase: Add / Remove
    ####################################################################################################################

    @Slot(str)
    def addSampleFromCif(self, cif_url):
        self.logic.addSampleFromCif(cif_url)
        self._onPhaseAdded()
        self.currentPhaseIndex = 0
        self.structureViewChanged.emit()

    @Slot()
    def addDefaultPhase(self):
        print("+ addDefaultPhase")
        self.logic.addDefaultPhase()
        self._onPhaseAdded()
        self.currentPhaseIndex = 0
        self.structureViewChanged.emit()

    @Slot(str)
    def removePhase(self, phase_name: str):
        if self.logic.removePhase(phase_name):
            self.currentPhaseIndex = 0
            self.structureParametersChanged.emit()
            self.phasesEnabled.emit()

    def _onPhaseAdded(self):
        print("***** _onPhaseAdded")
        self.logic._onPhaseAdded()
        self.phasesEnabled.emit()
        self.phasesAsObjChanged.emit()
        self.structureParametersChanged.emit()
        self.parent._project_proxy.projectInfoChanged.emit()

    @Property(bool, notify=phasesEnabled)
    def samplesPresent(self) -> bool:
        return self.logic.samplesPresent()

    ####################################################################################################################
    # Phase: Symmetry
    ####################################################################################################################

    # Crystal system

    @Property('QVariant', notify=structureParametersChanged)
    def crystalSystemList(self):
        return self.logic.crystalSystemList()

    @Property(str, notify=structureParametersChanged)
    def currentCrystalSystem(self):
        return self.logic.currentCrystalSystem()

    @currentCrystalSystem.setter
    def currentCrystalSystem(self, new_system: str):
        self.logic.setCurrentCrystalSystem(new_system)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupList(self):
        return self.logic.formattedSpaceGroupList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroup(self):
        return self.logic.getCurrentSpaceGroup()

    @currentSpaceGroup.setter
    def currentSpaceGroup(self, new_idx: int):
        self.logic.currentSpaceGroup(new_idx)
        self.structureParametersChanged.emit()

    @Property('QVariant', notify=structureParametersChanged)
    def formattedSpaceGroupSettingList(self):
        return self.logic.formattedSpaceGroupSettingList()

    @Property(int, notify=structureParametersChanged)
    def currentSpaceGroupSetting(self):
        return self.logic.currentSpaceGroupSetting()

    @currentSpaceGroupSetting.setter
    def currentSpaceGroupSetting(self, new_number: int):
        self.logic.setCurrentSpaceGroupSetting(new_number)
        self.structureParametersChanged.emit()

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################

    @Slot()
    def addDefaultAtom(self):
        try:
            self.logic.addDefaultAtom()
        except AttributeError:
            print("Error: failed to add atom")

    @Slot(str)
    def removeAtom(self, atom_label: str):
        self.logic.removeAtom(atom_label)

    @Property(bool, notify=currentPhaseChanged)
    def hasMsp(self):
        return self.logic.hasMsp()

    ####################################################################################################################
    # Current phase
    ####################################################################################################################

    @Property(int, notify=currentPhaseChanged)
    def currentPhaseIndex(self):
        return self.logic._current_phase_index

    @currentPhaseIndex.setter
    def currentPhaseIndex(self, new_index: int):
        if self.logic.currentPhaseIndex(new_index):
            self.currentPhaseChanged.emit()

    def _onCurrentPhaseChanged(self):
        print("***** _onCurrentPhaseChanged")
        self.structureViewChanged.emit()
        self.structureParametersChanged.emit()

    @Slot(str)
    def setCurrentPhaseName(self, name):
        if self.logic.getCurrentPhaseName() == name:
            return
        self.logic.setCurrentPhaseName(name)
        self.structureParametersChanged.emit()
        self.parent._project_proxy.projectInfoChanged.emit()

