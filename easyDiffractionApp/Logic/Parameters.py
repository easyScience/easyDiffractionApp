# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501
from typing import Union

from dicttoxml import dicttoxml
import json

from PySide2.QtCore import Signal, QObject

from easyCore import np, borg

from easyCore.Utils.classTools import generatePath

from easyDiffractionApp.Logic.DataStore import DataSet1D, DataStore


class ParametersLogic(QObject):
    """
    """
    instrumentParametersChanged = Signal()
    simulationParametersChanged = Signal()
    parametersChanged = Signal()
    parametersValuesChanged = Signal()
    undoRedoChanged = Signal()
    plotCalculatedDataSignal = Signal(tuple)
    plotBraggDataSignal = Signal(tuple)

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._interface_name = interface.current_interface_name

        self._parameters = None
        self._instrument_parameters = None
        self._status_model = None

        # Experiment
        self._pattern_parameters_as_obj = self._defaultPatternParameters()
        self._instrument_parameters_as_obj = self._defaultInstrumentParameters()  # noqa: E501
        self._instrument_parameters_as_xml = ""
        # Parameters
        self._parameters_as_obj = []
        self._parameters_as_xml = []
        self._parameters_filter_criteria = ""

        self._data = self._defaultData()
        self._simulation_parameters_as_obj = self._defaultSimulationParameters()  # noqa: E501

    ####################################################################################################################
    ####################################################################################################################
    # data
    ####################################################################################################################
    ####################################################################################################################

    def _defaultData(self):
        x_min = self._defaultSimulationParameters()['x_min']
        x_max = self._defaultSimulationParameters()['x_max']
        x_step = self._defaultSimulationParameters()['x_step']
        num_points = int((x_max - x_min) / x_step + 1)
        x_data = np.linspace(x_min, x_max, num_points)

        data = DataStore()

        data.append(
            DataSet1D(
                name='PND',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='experiment'
            )
        )
        data.append(
            DataSet1D(
                name='{:s} engine'.format(self._interface_name),
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Intensity',
                data_type='simulation'
            )
        )
        data.append(
            DataSet1D(
                name='Difference',
                x=x_data, y=np.zeros_like(x_data),
                x_label='2theta (deg)', y_label='Difference',
                data_type='simulation'
            )
        )
        return data

    def _defaultSimulationParameters(self):
        return {
            "x_min": 10.0,
            "x_max": 120.0,
            "x_step": 0.1
        }

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    def simulationParametersAsObj(self, json_str):
        if self._simulation_parameters_as_obj == json.loads(json_str):
            return

        self._simulation_parameters_as_obj = json.loads(json_str)
        self.simulationParametersChanged.emit()

    def _defaultPatternParameters(self):
        return {
            "scale":      1.0,
            "zero_shift": 0.0
        }

    def _setPatternParametersAsObj(self):
        parameters = self.parent.l_phase._sample.pattern.as_dict(skip=['interface'])
        self._pattern_parameters_as_obj = parameters

    ####################################################################################################################
    # Instrument parameters (wavelength, resolution_u, ..., resolution_y)
    ####################################################################################################################

    def _defaultInstrumentParameters(self):
        return {
            "wavelength":   1.0,
            "resolution_u": 0.01,
            "resolution_v": -0.01,
            "resolution_w": 0.01,
            "resolution_x": 0.0,
            "resolution_y": 0.0
        }

    def _setInstrumentParametersAsObj(self):
        # parameters = self._sample.parameters.as_dict()
        parameters = self.parent.l_phase._sample.parameters.as_dict(skip=['interface'])
        self._instrument_parameters_as_obj = parameters

    def _setInstrumentParametersAsXml(self):
        parameters = [self._instrument_parameters_as_obj]
        self._instrument_parameters_as_xml = dicttoxml(parameters, attr_type=True).decode()  # noqa: E501

    ####################################################################################################################
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    def _setIconifiedLabels(self):
        for index in range(len(self._parameters_as_obj)):
            label = self._parameters_as_obj[index]["label"]
            previousLabel = self._parameters_as_obj[index - 1]["label"] if index > 0 else ""

            separator = '&nbsp;&nbsp;'
            textColor = '$TEXT_COLOR'
            iconColor = '$ICON_COLOR'
            iconsFamily = '$ICONS_FAMILY'

            # Modify current label
            label = label.replace(".background.", ".")
            label = label.replace("Uiso.Uiso", "Uiso")
            label = label.replace("fract_", "fract.")
            label = label.replace("length_", "length.")
            label = label.replace("angle_", "angle.")
            label = label.replace("resolution_", "resolution.")

            # Modify previous label
            previousLabel = previousLabel.replace(".background.", ".")
            previousLabel = previousLabel.replace("Uiso.Uiso", "Uiso")
            previousLabel = previousLabel.replace("fract_", "fract.")
            previousLabel = previousLabel.replace("length_", "length.")
            previousLabel = previousLabel.replace("angle_", "angle.")
            previousLabel = previousLabel.replace("resolution_", "resolution.")

            # Labels to lists
            list = label.split(".")
            previousList = previousLabel.split(".")

            # First element formatting
            if list[0] == previousList[0]:
                list[0] = f'<font color="{iconColor}" face="{iconsFamily}">{list[0]}</font>'
                list[0] = list[0]\
                    .replace("Phases", "gem")\
                    .replace("Instrument", "microscope")
            else:
                list[0] = f"<font face='{iconsFamily}'>{list[0]}</font>"
                list[0] = list[0]\
                    .replace("Phases", f"<font face='{iconsFamily}'>gem</font>")\
                    .replace("Instrument", f"<font face='{iconsFamily}'>microscope</font>")

            # Intermediate elements formatting (excluding first and last)
            for i in range(1, len(list) - 1):
                if previousLabel and len(list) == len(previousList) and list[i] == previousList[i]:
                    list[i] = f"<font color='{textColor}'>{list[i]}</font>"
                    list[i] = list[i].replace("lattice", f'<font color={iconColor} face="{iconsFamily}">cube</font>')
                    list[i] = list[i].replace("length", f'<font color={iconColor} face="{iconsFamily}">ruler</font>')
                    list[i] = list[i].replace("angle", f'<font color={iconColor} face="{iconsFamily}">less-than</font>')
                    list[i] = list[i].replace("atoms", f'<font color={iconColor} face="{iconsFamily}">atom</font>')
                    list[i] = list[i].replace("adp", f'<font color={iconColor} face="{iconsFamily}">arrows-alt</font>')
                    list[i] = list[i].replace("fract", f'<font color={iconColor} face="{iconsFamily}">map-marker-alt</font>')
                    list[i] = list[i].replace("resolution", f'<font color={iconColor} face="{iconsFamily}">grip-lines-vertical</font>')
                    list[i] = list[i].replace("point_background", f'<font color={iconColor} face="{iconsFamily}">wave-square</font>')
                else:
                    list[i] = list[i].replace("lattice", f'<font face="{iconsFamily}">cube</font>')
                    list[i] = list[i].replace("length", f'<font face="{iconsFamily}">ruler</font>')
                    list[i] = list[i].replace("angle", 'f<font face="{iconsFamily}">less-than</font>')
                    list[i] = list[i].replace("atoms", f'<font face="{iconsFamily}">atom</font>')
                    list[i] = list[i].replace("adp", f'<font face="{iconsFamily}">arrows-alt</font>')
                    list[i] = list[i].replace("fract", f'<font face="{iconsFamily}">map-marker-alt</font>')
                    list[i] = list[i].replace("resolution", f'<font face="{iconsFamily}">grip-lines-vertical</font>')
                    list[i] = list[i].replace("point_background", f'<font face="{iconsFamily}">wave-square</font>')

            # Back to string
            label = separator.join(list)

            # 180,0_deg to 180.0°
            label = label.replace(",", ".").replace("_deg", "°")

            # Add formatted label
            self._parameters_as_obj[index]["iconified_label"] = label

            # Add formatted label
            number = self._parameters_as_obj[index]["number"]
            self._parameters_as_obj[index]["iconified_label_with_index"] = f'{number}{separator}{label}'

    def _setParametersAsObj(self):
        self._parameters_as_obj.clear()

        par_ids, par_paths = generatePath(self.parent.l_phase._sample, True)
        par_index = 0

        for par_id, par_path in zip(par_ids, par_paths):
            # par_id = par_ids[par_index]
            par = borg.map.get_item_by_key(par_id)

            if not par.enabled:
                continue

            # add experimental dataset name
            par_path = par_path.replace('Pars1D.', f'Instrument.{self.parent.l_experiment.experimentDataAsObj()[0]["name"]}.')
            par_path = par_path.replace('Pattern1D.', f'Instrument.{self.parent.l_experiment.experimentDataAsObj()[0]["name"]}.')
            # par_path = par_path.replace('Instrument.', f'Instrument.{self.parent.l_experiment.experimentDataAsObj()[0]["name"]}.')

            if self._parameters_filter_criteria.lower() not in par_path.lower():  # noqa: E501
                continue

            self._parameters_as_obj.append({
                "id":     str(par_id),
                "number": par_index + 1,
                "label":  par_path,
                "label_with_index": f"{par_index + 1} {par_path}",
                "value":  par.raw_value,
                "unit":   '{:~P}'.format(par.unit),
                "error":  float(par.error),
                "fit":    int(not par.fixed)
            })

            par_index += 1

        self._setIconifiedLabels()

    def _setParametersAsXml(self):
        self._parameters_as_xml = dicttoxml(self._parameters_as_obj, attr_type=False).decode()  # noqa: E501

    def setParametersFilterCriteria(self, new_criteria):
        if self._parameters_filter_criteria == new_criteria:
            return
        self._parameters_filter_criteria = new_criteria

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):  # noqa: E501
        if not obj_id:
            return

        obj = self._parameterObj(obj_id)
        if obj is None:
            return

        if isinstance(new_value, bool):
            if obj.fixed == (not new_value):
                return

            obj.fixed = not new_value
            self.parametersChanged.emit()
            self.undoRedoChanged.emit()

        else:
            if obj.raw_value == new_value:
                return

            obj.value = new_value
            self.parametersValuesChanged.emit()
            self.parametersChanged.emit()

    def _parameterObj(self, obj_id: str):
        if not obj_id:
            return
        obj_id = int(obj_id)
        obj = borg.map.get_item_by_key(obj_id)
        return obj

    ####################################################################################################################
    # Calculated data
    ####################################################################################################################
    def _updateCalculatedData(self):
        if not self.parent.l_experiment._experiment_loaded and not self.parent.l_experiment._experiment_skipped:
            return
        self.parent.l_phase._sample.output_index = self.parent.l_phase._current_phase_index

        #  THIS IS WHERE WE WOULD LOOK UP CURRENT EXP INDEX
        sim = self._data.simulations[0]

        if self.parent.l_experiment._experiment_loaded:
            exp = self._data.experiments[0]
            sim.x = exp.x

        elif self.parent.l_experiment._experiment_skipped:
            x_min = float(self._simulation_parameters_as_obj['x_min'])
            x_max = float(self._simulation_parameters_as_obj['x_max'])
            x_step = float(self._simulation_parameters_as_obj['x_step'])
            num_points = int((x_max - x_min) / x_step + 1)
            sim.x = np.linspace(x_min, x_max, num_points)

        sim.y = self._interface.fit_func(sim.x)
        hkl = self._interface.get_hkl()

        self.plotCalculatedDataSignal.emit((sim.x, sim.y))
        self.plotBraggDataSignal.emit((hkl['ttheta'], hkl['h'], hkl['k'], hkl['l']))  # noqa: E501
