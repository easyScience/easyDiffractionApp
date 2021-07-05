# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from dicttoxml import dicttoxml

from PySide2.QtCore import Signal, QObject

from easyCore import np, borg
from easyDiffractionLib import Phases, Phase, Lattice, Site, SpaceGroup
from easyCore.Symmetry.tools import SpacegroupInfo
from easyApp.Logic.Utils.Utils import generalizePath
from easyDiffractionLib.sample import Sample
from easyDiffractionLib.Elements.Experiments.Experiment import Pars1D
from easyDiffractionLib.Elements.Experiments.Pattern import Pattern1D


class PhaseLogic(QObject):
    """
    """
    phaseAdded = Signal()
    updateProjectInfo = Signal(tuple)
    structureParametersChanged = Signal()
    phasesEnabled = Signal()  # from other logics
    phasesAsObjChanged = Signal()

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self.state = parent.l_parameters
        self.phases = None
        self._phases_as_obj = []
        self._phases_as_xml = ""
        self._phases_as_cif = ""
        self._sample = self._defaultSample()
        self._current_phase_index = 0

    ####################################################################################################################
    ####################################################################################################################
    # phases
    ####################################################################################################################
    ####################################################################################################################

    def currentPhaseIndex(self, new_index: int):
        if self._current_phase_index == new_index or new_index == -1:
            return False
        self._current_phase_index = new_index
        return True

    def removePhase(self, phase_name: str):
        if phase_name in self._sample.phases.phase_names:
            del self._sample.phases[phase_name]
            return True
        return False

    def addDefaultPhase(self):
        borg.stack.enabled = False
        self._sample.phases.append(self._defaultPhase())
        borg.stack.enabled = True

    def _defaultPhase(self):
        space_group = SpaceGroup.from_pars('P 42/n c m')
        cell = Lattice.from_pars(8.56, 8.56, 6.12, 90, 90, 90)
        atom = Site.from_pars(label='Cl1', specie='Cl', fract_x=0.125, fract_y=0.167, fract_z=0.107)  # noqa: E501
        atom.add_adp('Uiso', Uiso=0.0)
        phase = Phase('Dichlorine', spacegroup=space_group, cell=cell)
        phase.add_atom(atom)
        return phase

    def _onPhaseAdded(self):
        if self._interface.current_interface_name != 'CrysPy':
            self._interface.generate_sample_binding("filename", self._sample)
        self._sample.phases.name = 'Phases'
        name = self._sample.phases[self._current_phase_index].name
        self.updateProjectInfo.emit(('samples', name))

    def currentCrystalSystem(self):
        phases = self._sample.phases
        if not phases:
            return ''

        current_system = phases[self._current_phase_index].spacegroup.crystal_system  # noqa: E501
        current_system = current_system.capitalize()
        return current_system

    def setCurrentCrystalSystem(self, new_system: str):
        new_system = new_system.lower()
        space_group_numbers = SpacegroupInfo.get_ints_from_system(new_system)
        top_space_group_number = space_group_numbers[0]
        top_space_group_name = SpacegroupInfo.get_symbol_from_int_number(top_space_group_number)  # noqa: E501
        self._setCurrentSpaceGroup(top_space_group_name)

    def phasesAsExtendedCif(self):
        if len(self._sample.phases) == 0:
            return

        symm_ops = self._sample.phases[0].spacegroup.symmetry_opts
        symm_ops_cif_loop = "loop_\n _symmetry_equiv_pos_as_xyz\n"
        for symm_op in symm_ops:
            symm_ops_cif_loop += f' {symm_op.as_xyz_string()}\n'
        return self._phases_as_cif + symm_ops_cif_loop

    def phasesAsCif(self, phases_as_cif):
        if self._phases_as_cif == phases_as_cif:
            return
        self._sample.phases = Phases.from_cif_str(phases_as_cif)

    def _setPhasesAsObj(self):
        self._phases_as_obj = self._sample.phases.as_dict(skip=['interface'])['data']

    def _setPhasesAsXml(self):
        self._phases_as_xml = dicttoxml(self._phases_as_obj, attr_type=True).decode()  # noqa: E501

    def _setPhasesAsCif(self):
        self._phases_as_cif = str(self._sample.phases.cif)

    def _setCurrentSpaceGroup(self, new_name: str):
        phases = self._sample.phases
        if phases[self._current_phase_index].spacegroup.space_group_HM_name == new_name:  # noqa: E501
            return
        phases[self._current_phase_index].spacegroup.space_group_HM_name = new_name  # noqa: E501

    def _spaceGroupSettingList(self):
        phases = self._sample.phases
        if not phases:
            return []

        current_number = self._currentSpaceGroupNumber()
        settings = SpacegroupInfo.get_compatible_HM_from_int(current_number)
        return settings

    def _spaceGroupNumbers(self):
        current_system = self.currentCrystalSystem().lower()
        numbers = SpacegroupInfo.get_ints_from_system(current_system)
        return numbers

    def _currentSpaceGroupNumber(self):
        phases = self._sample.phases
        current_number = phases[self._current_phase_index].spacegroup.int_number  # noqa: E501
        return current_number

    def getCurrentSpaceGroup(self):
        def space_group_index(number, numbers):
            if number in numbers:
                return numbers.index(number)
            return 0

        phases = self._sample.phases
        if not phases:
            return -1

        space_group_numbers = self._spaceGroupNumbers()
        current_number = self._currentSpaceGroupNumber()
        current_idx = space_group_index(current_number, space_group_numbers)
        return current_idx

    def currentSpaceGroup(self, new_idx: int):
        space_group_numbers = self._spaceGroupNumbers()
        space_group_number = space_group_numbers[new_idx]
        space_group_name = SpacegroupInfo.get_symbol_from_int_number(space_group_number)  # noqa: E501
        self._setCurrentSpaceGroup(space_group_name)

    def formattedSpaceGroupList(self):
        def format_display(num):
            name = SpacegroupInfo.get_symbol_from_int_number(num)
            return f"<font color='#999'>{num}</font> {name}"

        space_group_numbers = self._spaceGroupNumbers()
        display_list = [format_display(num) for num in space_group_numbers]
        return display_list

    def crystalSystemList(self):
        systems = [system.capitalize() for system in SpacegroupInfo.get_all_systems()]  # noqa: E501
        return systems

    def formattedSpaceGroupSettingList(self):
        def format_display(num, name):
            return f"<font color='#999'>{num}</font> {name}"

        raw_list = self._spaceGroupSettingList()
        formatted_list = [format_display(i + 1, name) for i, name in enumerate(raw_list)]  # noqa: E501
        return formatted_list

    def currentSpaceGroupSetting(self):
        phases = self._sample.phases
        if not phases:
            return 0

        settings = self._spaceGroupSettingList()
        # current_setting = phases[self._current_phase_index].spacegroup.space_group_HM_name.raw_value  # noqa: E501
        current_setting = phases[self._current_phase_index].spacegroup.hermann_mauguin  # noqa: E501
        current_number = settings.index(current_setting)
        return current_number

    def setCurrentSpaceGroupSetting(self, new_number: int):
        settings = self._spaceGroupSettingList()
        name = settings[new_number]
        self._setCurrentSpaceGroup(name)

    ####################################################################################################################
    # Phase: Atoms
    ####################################################################################################################
    def addDefaultAtom(self):
        index = len(self._sample.phases[0].atoms.atom_labels) + 1
        label = f'Label{index}'
        atom = Site.from_pars(label=label,
                              specie='O',
                              fract_x=0.05,
                              fract_y=0.05,
                              fract_z=0.05)
        atom.add_adp('Uiso', Uiso=0.0)
        self._sample.phases[self._current_phase_index].add_atom(atom)

    def removeAtom(self, atom_label: str):
        self._sample.phases[self._current_phase_index].remove_atom(atom_label)

    def setCurrentExperimentDatasetName(self, name):
        if self.parent.l_parameters._data.experiments[0].name == name:
            return
        self.parent.l_parameters._data.experiments[0].name = name
        self.updateProjectInfo.emit(('experiments', name))

    ####################################################################################################################
    ####################################################################################################################
    # SAMPLE
    ####################################################################################################################
    ####################################################################################################################

    def _defaultSample(self):
        sample = Sample(parameters=Pars1D.default(),
                        pattern=Pattern1D.default(),
                        interface=self._interface)
        sample.pattern.zero_shift = 0.0
        sample.pattern.scale = 100.0
        sample.parameters.wavelength = 1.912
        sample.parameters.resolution_u = 0.1447
        sample.parameters.resolution_v = -0.4252
        sample.parameters.resolution_w = 0.3864
        sample.parameters.resolution_x = 0.0
        sample.parameters.resolution_y = 0.0  # 0.0961
        return sample

    def addSampleFromCif(self, cif_url):
        cif_path = generalizePath(cif_url)
        borg.stack.enabled = False
        self._sample.phases = Phases.from_cif_file(cif_path)
        borg.stack.enabled = True

    def setCurrentPhaseName(self, name):
        if self._sample.phases[self._current_phase_index].name == name:
            return
        self._sample.phases[self._current_phase_index].name = name
        # self._project_info['samples'] = name
        self.updateProjectInfo.emit(('samples', name))

    def samplesPresent(self):
        result = len(self._sample.phases) > 0
        return result

    def _updateCalculatedData(self):
        self.state._updateCalculatedData()
