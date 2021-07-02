import json

from PySide2.QtCore import QObject, Signal

from easyDiffractionApp.Logic.Background import BackgroundLogic
from easyDiffractionApp.Logic.Experiment import ExperimentLogic
from easyDiffractionApp.Logic.Fitting import FittingLogic
from easyDiffractionApp.Logic.Parameters import ParametersLogic
from easyDiffractionApp.Logic.Phase import PhaseLogic
from easyDiffractionApp.Logic.Plotting1d import Plotting1dLogic
from easyDiffractionApp.Logic.Plotting3d import Plotting3dLogic
from easyDiffractionApp.Logic.Project import ProjectLogic
from easyDiffractionApp.Logic.Stack import StackLogic
from easyDiffractionApp.Logic.State import StateLogic
from easyDiffractionLib.interface import InterfaceFactory


class LogicController(QObject):
    parametersChanged = Signal()

    def __init__(self, parent):
        super().__init__(parent)
        self.proxy = parent
        self.interface = InterfaceFactory()

        # Screen recorder
        self._screen_recorder = self.recorder()

        # instantiate logics
        self.initializeLogics()

        # define signal forwarders
        self.setupSignals()

    def initializeLogics(self):
        self.l_state = StateLogic(self, interface=self.interface)
        self.l_parameters = ParametersLogic(self, interface=self.interface)
        self.l_experiment = ExperimentLogic(self)
        self.l_phase = PhaseLogic(self, interface=self.interface)
        self.l_fitting = FittingLogic(self, interface=self.interface)
        self.l_plotting1d = Plotting1dLogic(self)
        self.l_plotting3d = Plotting3dLogic(self)
        self.l_background = BackgroundLogic(self)
        self.l_project = ProjectLogic(self, interface=self.interface)
        # stack logic
        no_history = [self.parametersChanged]
        with_history = [self.l_phase.phaseAdded, self.parametersChanged]
        self.l_stack = StackLogic(self, self.proxy,
                                  callbacks_no_history=no_history,
                                  callbacks_with_history=with_history)

    def setupSignals(self):
        self.l_background.asObjChanged.connect(self.l_parameters.parametersChanged)
        self.l_background.asObjChanged.connect(self.l_phase._sample.set_background)
        self.l_background.asObjChanged.connect(self.l_parameters._updateCalculatedData)

        self.l_fitting.fitFinished.connect(self.parametersChanged)
        self.l_fitting.fitFinished.connect(self.l_parameters.parametersChanged)
        self.l_fitting.currentCalculatorChanged.connect(self.proxy.currentCalculatorChanged)

        self.l_project.reset.connect(self.resetState)
        self.l_project.phasesEnabled.connect(self.l_phase.phasesEnabled)
        self.l_project.phasesAsObjChanged.connect(self.l_phase.phasesAsObjChanged)
        self.l_project.experimentDataAdded.connect(self.l_experiment._onExperimentDataAdded)
        self.l_project.structureParametersChanged.connect(self.l_phase.structureParametersChanged)
        self.l_project.removePhaseSignal.connect(self.removePhase)
        self.l_project.experimentLoadedChanged.connect(self.l_experiment.experimentLoadedChanged)

        self.parametersChanged.connect(self.l_parameters._updateCalculatedData)
        self.parametersChanged.connect(self.l_phase.structureParametersChanged)
        self.parametersChanged.connect(self.l_experiment._onPatternParametersChanged)
        self.parametersChanged.connect(self.l_parameters.instrumentParametersChanged)
        self.parametersChanged.connect(self.l_background.onAsObjChanged)
        self.parametersChanged.connect(self.l_stack.undoRedoChanged)

        self.l_parameters.parametersValuesChanged.connect(self.parametersChanged)
        self.l_parameters.plotCalculatedDataSignal.connect(self.plotCalculatedData)
        self.l_parameters.plotBraggDataSignal.connect(self.plotBraggData)
        self.l_parameters.undoRedoChanged.connect(self.l_stack.undoRedoChanged)

        self.l_phase.updateProjectInfo.connect(self.l_project.updateProjectInfo)

    def resetFactory(self):
        self.interface = InterfaceFactory()

    def plotCalculatedData(self, data):
        self.l_plotting1d.setCalculatedData(data[0], data[1])

    def plotBraggData(self, data):
        self.l_plotting1d.setBraggData(data[0], data[1], data[2], data[3])  # noqa: E501

    def initializeBorg(self):
        self.l_stack.initializeBorg()

    def resetState(self):
        self.l_plotting1d.clearBackendState()
        self.l_plotting1d.clearFrontendState()
        self.l_stack.resetUndoRedoStack()
        self.l_stack.undoRedoChanged.emit()

    def removePhase(self, phase_name: str):
        if self.l_phase.removePhase(phase_name):
            self.l_phase.structureParametersChanged.emit()
            self.l_phase.phasesEnabled.emit()

    def statusModelAsObj(self):
        engine_name = self.l_fitting.fitter.current_engine.name
        minimizer_name = self.l_fitting._current_minimizer_method_name
        return self.l_state.statusModelAsObj(engine_name, minimizer_name)

    def statusModelAsXml(self):
        engine_name = self.l_fitting.fitter.current_engine.name
        minimizer_name = self.l_fitting._current_minimizer_method_name
        return self.l_state.statusModelAsXml(engine_name, minimizer_name)

    def recorder(self):
        rec = None
        try:
            from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder
            rec = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        return rec
