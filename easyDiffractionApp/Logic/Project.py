# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501
import os
import datetime

from dicttoxml import dicttoxml
import json

from PySide2.QtCore import Signal, QObject

from easyCore import np, borg

from easyDiffractionLib.sample import Sample
from easyApp.Logic.Utils.Utils import generalizePath


class ProjectLogic(QObject):
    """
    """
    projectCreatedChanged = Signal()
    projectInfoChanged = Signal()
    reset = Signal()
    phasesEnabled = Signal()
    phasesAsObjChanged = Signal()
    structureParametersChanged = Signal()
    removePhaseSignal = Signal(str)
    experimentDataAdded = Signal()
    # parametersChanged = Signal()
    experimentLoadedChanged = Signal()

    def __init__(self, parent=None , interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._interface_name = interface.current_interface_name
        self.project_save_filepath = ""
        self.project_load_filepath = ""
        self._project_info = self._defaultProjectInfo()
        self._project_created = False
        self._state_changed = False

        self._report = ""
        self._currentProjectPath = os.path.expanduser("~")

    ####################################################################################################################
    ####################################################################################################################
    # Reporting
    ####################################################################################################################
    ####################################################################################################################

    def setReport(self, report):
        """
        Keep the QML generated HTML report for saving
        """
        self._report = report

    def saveReport(self, filepath):
        """
        Save the generated report to the specified file
        Currently only html
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self._report)
            success = True
        except IOError:
            success = False
        return success

    def setProjectCreated(self, created: bool):
        if self._project_created == created:
            return
        self._project_created = created
        self.projectCreatedChanged.emit()

    ####################################################################################################################
    ####################################################################################################################
    # project
    ####################################################################################################################
    ####################################################################################################################

    def _defaultProjectInfo(self):
        return dict(
            name="Example Project",
            short_description="diffraction, powder, 1D",
            samples="Not loaded",
            experiments="Not loaded",
            modified=datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        )

    def projectExamplesAsXml(self):
        model = [
            {"name": "PbSO4", "description": "neutrons, powder, 1D, D1A@ILL",
             "path": "../Resources/Examples/PbSO4/project.json"},
            {"name": "Co2SiO4", "description": "neutrons, powder, 1D, D20@ILL",
             "path": "../Resources/Examples/Co2SiO4/project.json"},
            {"name": "Dy3Al5O12", "description": "neutrons, powder, 1D, G41@LLB",
             "path": "../Resources/Examples/Dy3Al5O12/project.json"}
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml

    def projectInfoAsCif(self):
        cif_list = []
        for key, value in self._project_info.items():
            if ' ' in value:
                value = f"'{value}'"
            cif_list.append(f'_{key} {value}')
        cif_str = '\n'.join(cif_list)
        return cif_str

    def projectInfoAsJson(self, json_str):
        self._project_info = json.loads(json_str)

    def editProjectInfo(self, key, value):
        if key == 'location':
            self._currentProjectPath = value
            return
        else:
            if self._project_info[key] == value:
                return
            self._project_info[key] = value

    def currentProjectPath(self, new_path):
        if self._currentProjectPath == new_path:
            return
        self._currentProjectPath = new_path

    def createProject(self):
        projectPath = self._currentProjectPath
        mainCif = os.path.join(projectPath, 'project.cif')
        samplesPath = os.path.join(projectPath, 'samples')
        experimentsPath = os.path.join(projectPath, 'experiments')
        calculationsPath = os.path.join(projectPath, 'calculations')
        if not os.path.exists(projectPath):
            os.makedirs(projectPath)
            os.makedirs(samplesPath)
            os.makedirs(experimentsPath)
            os.makedirs(calculationsPath)
            with open(mainCif, 'w') as file:
                file.write(self.projectInfoAsCif())
        else:
            print(f"ERROR: Directory {projectPath} already exists")

    def stateHasChanged(self, changed: bool):
        if self._state_changed == changed:
            return
        self._state_changed = changed

    def _loadProjectAs(self, filepath):
        """
        """
        self.project_load_filepath = filepath
        print("LoadProjectAs " + filepath)
        self._loadProject()

    def _loadProject(self):
        """
        """
        path = generalizePath(self.project_load_filepath)
        if not os.path.isfile(path):
            print("Failed to find project: '{0}'".format(path))
            return
        with open(path, 'r') as xml_file:
            descr: dict = json.load(xml_file)

        interface_name = descr.get('interface', None)
        if interface_name is not None:
            old_interface_name = self._interface.current_interface_name
            if old_interface_name != interface_name:
                self._interface.switch(interface_name)

        self.parent.l_phase._sample = Sample.from_dict(descr['sample'])
        self.parent.l_phase._sample.interface = self._interface

        # send signal to tell the proxy we changed phases
        self.phasesEnabled.emit()
        self.phasesAsObjChanged.emit()
        self.structureParametersChanged.emit()
        self.parent.l_background._setAsXml()

        # experiment
        if 'experiments' in descr:
            self.parent.l_experiment.experimentLoaded(True)
            self.parent.l_experiment.experimentSkipped(False)
            self.parent.l_parameters._data.experiments[0].x = np.array(descr['experiments'][0])
            self.parent.l_parameters._data.experiments[0].y = np.array(descr['experiments'][1])
            self.parent.l_parameters._data.experiments[0].e = np.array(descr['experiments'][2])
            self.parent.l_experiment._experiment_data = self.parent.l_parameters._data.experiments[0]
            self.parent.l_experiment.experiments = [{'name': descr['project_info']['experiments']}]
            self.parent.l_experiment.setCurrentExperimentDatasetName(descr['project_info']['experiments'])

            # send signal to tell the proxy we changed experiment
            self.experimentDataAdded.emit()
            self.parent.parametersChanged.emit()
            self.experimentLoadedChanged.emit()

        else:
            # delete existing experiment
            self.parent.l_experiment.removeExperiment()
            self.parent.l_experiment.experimentLoaded(False)
            if descr['experiment_skipped']:
                self.parent.l_experiment.experimentSkipped(True)
                self.parent.l_experiment.experimentSkippedChanged.emit()

        # project info
        self._project_info = descr['project_info']

        new_minimizer_settings = descr.get('minimizer', None)
        if new_minimizer_settings is not None:
            new_engine = new_minimizer_settings['engine']
            new_method = new_minimizer_settings['method']

            new_engine_index = self.parent.l_fitting.fitter.available_engines.index(new_engine)
            self.parent.l_fitting.setCurrentMinimizerIndex(new_engine_index)
            new_method_index = self.parent.l_fitting.minimizerMethodNames().index(new_method)
            self.parent.l_fitting.currentMinimizerMethodIndex(new_method_index)

        self.parent.l_fitting.fitter.fit_object = self.parent.l_phase._sample
        self.parent.l_stack.resetUndoRedoStack()
        self.parent.l_stack.undoRedoChanged.emit()
        self.setProjectCreated(True)

    def saveProject(self):
        """
        """
        projectPath = self._currentProjectPath
        project_save_filepath = os.path.join(projectPath, 'project.json')
        descr = {
            'sample': self.parent.l_phase._sample.as_dict(skip=['interface'])
        }
        if self.parent.l_parameters._data.experiments:
            experiments_x = self.parent.l_parameters._data.experiments[0].x
            experiments_y = self.parent.l_parameters._data.experiments[0].y
            experiments_e = self.parent.l_parameters._data.experiments[0].e
            descr['experiments'] = [experiments_x, experiments_y, experiments_e]

        descr['experiment_skipped'] = self.parent.l_experiment._experiment_skipped
        descr['project_info'] = self._project_info

        descr['interface'] = self._interface.current_interface_name

        descr['minimizer'] = {
            'engine': self.parent.l_fitting.fitter.current_engine.name,
            'method': self.parent.l_fitting._current_minimizer_method_name
        }
        content_json = json.dumps(descr, indent=4, default=self.default)
        path = generalizePath(project_save_filepath)
        createFile(path, content_json)

    def default(self, obj):
        if type(obj).__module__ == np.__name__:
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            else:
                return obj.item()
        raise TypeError('Unknown type:', type(obj))

    def resetState(self):
        self._project_info = self._defaultProjectInfo()
        self.setProjectCreated(False)
        self.projectInfoChanged.emit()
        self.project_save_filepath = ""
        self.parent.l_experiment.removeExperiment()
        if self.parent.l_phase.samplesPresent():
            self.removePhaseSignal.emit(self.parent.l_phase._sample.phases[self.parent.l_phase._current_phase_index].name)
        self.reset.emit()

    def updateProjectInfo(self, key_value):
        if len(key_value) == 2:
            self._project_info[key_value[0]] = key_value[1]
            self.projectInfoChanged.emit()


def createFile(path, content):
    if os.path.exists(path):
        print(f'File already exists {path}. Overwriting...')
        os.unlink(path)
    try:
        message = f'create file {path}'
        with open(path, "w") as file:
            file.write(content)
    except Exception as exception:
        print(message, exception)
