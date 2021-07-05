# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501

from dicttoxml import dicttoxml
import pathlib
import json

from PySide2.QtCore import Signal, QObject

from easyCore import np

from easyApp.Logic.Utils.Utils import generalizePath


class ExperimentLogic(QObject):
    """
    """
    experimentLoadedChanged = Signal()
    experimentSkippedChanged = Signal()
    experimentDataChanged = Signal()
    patternParametersAsObjChanged = Signal()
    clearFrontendState = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.state = parent.l_parameters

        self._experiment_parameters = None
        self._experiment_data_as_xml = ""
        self.experiment_data = None
        self._experiment_data = None
        self._experiment_loaded = False
        self._experiment_skipped = False
        self.experiments = self._defaultExperiments()
        self.clearFrontendState.connect(self.onClearFrontendState)

    def _defaultExperiment(self):
        return {
            "label": "D1A@ILL",
            "color": "#00a3e3"
        }

    def _loadExperimentData(self, file_url):
        print("+ _loadExperimentData")
        file_path = generalizePath(file_url)
        data = self.state._data.experiments[0]
        data.x, data.y, data.e = np.loadtxt(file_path, unpack=True)
        return data

    def _experimentDataParameters(self, data):
        x_min = data.x[0]
        x_max = data.x[-1]
        x_step = (x_max - x_min) / (len(data.x) - 1)
        parameters = {
            "x_min":  x_min,
            "x_max":  x_max,
            "x_step": x_step
        }
        return parameters

    def experimentDataXYZ(self):
        return (self._experiment_data.x, self._experiment_data.y, self._experiment_data.e)  # noqa: E501

    def _defaultExperiments(self):
        return []

    def experimentLoaded(self, loaded: bool):
        if self._experiment_loaded == loaded:
            return
        self._experiment_loaded = loaded
        self.experimentLoadedChanged.emit()

    def experimentSkipped(self, skipped: bool):
        if self._experiment_skipped == skipped:
            return
        self._experiment_skipped = skipped
        self.experimentSkippedChanged.emit()

    def experimentDataAsObj(self):
        return [{'name': experiment.name} for experiment in self.state._data.experiments]

    def _setExperimentDataAsXml(self):
        self._experiment_data_as_xml = dicttoxml(self.experiments, attr_type=True).decode()  # noqa: E501

    def addExperimentDataFromXye(self, file_url):
        self._experiment_data = self._loadExperimentData(file_url)
        self.state._data.experiments[0].name = pathlib.Path(file_url).stem
        self.experiments = [{'name': experiment.name} for experiment in self.state._data.experiments]
        self.experimentLoaded(True)
        self.experimentSkipped(False)

    def removeExperiment(self):
        self.experiments.clear()
        self.experimentLoaded(False)
        self.experimentSkipped(False)

    def _onExperimentSkippedChanged(self):
        self.state._updateCalculatedData()

    def _onExperimentLoadedChanged(self):
        self.state._onPatternParametersChanged()

    def setCurrentExperimentDatasetName(self, name):
        self.parent.l_phase.setCurrentExperimentDatasetName(name)

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.parent.l_plotting1d.setMeasuredData(
                                          self._experiment_data.x,
                                          self._experiment_data.y,
                                          self._experiment_data.e)
        self._experiment_parameters = \
            self._experimentDataParameters(self._experiment_data)

        # non-kosher connection to foreign proxy. Ewwww :(
        self.parent.proxy.parameters.simulationParametersAsObj = \
            json.dumps(self._experiment_parameters)

        if len(self.parent.l_phase._sample.pattern.backgrounds) == 0:
            self.parent.l_background.initializeContainer()

        self.experimentDataChanged.emit()
        self.parent.l_project._project_info['experiments'] = \
            self.parent.l_parameters._data.experiments[0].name

        self.parent.l_project.projectInfoChanged.emit()

    def _onPatternParametersChanged(self):
        self.state._setPatternParametersAsObj()
        self.patternParametersAsObjChanged.emit()

    def onClearFrontendState(self):
        self.parent.l_plotting1d.clearFrontendState()