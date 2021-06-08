import json

from PySide2.QtCore import QObject, Signal

# from easyDiffractionLib.interface import InterfaceFactory

# from easyDiffractionApp.Logic.State import StateLogic
# from easyDiffractionApp.Logic.Fitter import FitterLogic as FitterLogic
from easyDiffractionApp.Logic.Stack import StackLogic
from easyDiffractionApp.Logic.Plotting3d import Plotting3dLogic


class LogicController(QObject):
    parametersChanged = Signal()
    phaseAdded = Signal()

    def __init__(self, parent, state=None, interface=None):
        super().__init__(parent)
        self.proxy = parent
        self._fit_results = ""
        # self._interface = InterfaceFactory()
        # temporary kludge
        self.state = state
        self._interface = interface

        self.initialize()
        self.mapSignals()

    def initialize(self):
        # initialize various logic components

        # main logic
        #self.state = StateLogic(self,
        #                        interface=self._interface)

        # chart logic
        self.plotting3d = Plotting3dLogic(self)

        # stack logic
        no_history = [self.parametersChanged]
        with_history = [self.phaseAdded, self.parametersChanged]
        self.stackLogic = StackLogic(self.proxy,
                                     callbacks_no_history=no_history,
                                     callbacks_with_history=with_history)

        # fitter logic
        #####################################################
        #self.fitLogic = FittingLogic(self, self.state._sample,
        #                            self._interface.fit_func)
        self._fitting_proxy = self.proxy._fitting_proxy
        # self._fit_results = self.fitLogic._defaultFitResults()
        # communication between logic and proxy notifiers
        self._fitting_proxy.fitResultsChanged.connect(self.onFitFinished)
        # self.fitLogic.fitStarted.connect(self.onFitStarted)

        # background logic
        self._background_proxy = self.proxy._background_proxy
        self._background_proxy.logic.asObjChanged.connect(self.proxy._onParametersChanged)
        self._background_proxy.logic.asObjChanged.connect(self.state._sample.set_background)
        self._background_proxy.logic.asObjChanged.connect(self.state._updateCalculatedData)
        self._background_proxy.asXmlChanged.connect(self.updateChartBackground)

        # parameters slots
        self.parametersChanged.connect(self.proxy._onParametersChanged)
        self.parametersChanged.connect(self.state._updateCalculatedData)
        # self.parametersChanged.connect(self.chartsLogic._onStructureViewChanged)
        self.parametersChanged.connect(self.proxy._onStructureParametersChanged)
        self.parametersChanged.connect(self.proxy._onPatternParametersChanged)
        self.parametersChanged.connect(self.proxy._onInstrumentParametersChanged)
        self.parametersChanged.connect(self._background_proxy.logic.onAsObjChanged)
        self.parametersChanged.connect(self.proxy.undoRedoChanged)

        # Screen recorder
        self._screen_recorder = self.recorder()

    def mapSignals(self):
        """
        Map signals from logics to proxy
        Needed so logics don't call emit directly on proxy signals
        """
        self.state.projectCreatedChanged.connect(self.proxy.projectCreatedChanged)
        self.state.undoRedoChanged.connect(self.proxy.undoRedoChanged)
        self.state.parametersChanged.connect(self.proxy._onParametersChanged)
        self.state.experimentLoadedChanged.connect(self.proxy.experimentLoadedChanged)
        self.state.experimentSkippedChanged.connect(self.proxy.experimentSkippedChanged)
        self.state.phasesEnabled.connect(self.proxy.phasesEnabled)
        self.state.phasesAsObjChanged.connect(self.proxy.phasesAsObjChanged)
        self.state.structureParametersChanged.connect(self.proxy.structureParametersChanged)
        self.state.projectInfoChanged.connect(self.proxy.projectInfoChanged)
        self.state.experimentDataAdded.connect(self._onExperimentDataAdded)
        self.state.undoRedoChanged.connect(self.proxy.undoRedoChanged)
        self.state.resetUndoRedoStack.connect(self.proxy.resetUndoRedoStack)
        self.state.removePhaseSignal.connect(self.removePhase)
        self.state.currentMinimizerIndex.connect(self._fitting_proxy.logic.setCurrentMinimizerIndex)
        self.state.currentMinimizerMethodIndex.connect(self._fitting_proxy.logic.currentMinimizerMethodIndex)

        # self._fitting_proxy.logic.currentMinimizerChanged.connect(self.proxy.currentMinimizerChanged)
        self.state.plotCalculatedDataSignal.connect(self.plotCalculatedData)
        self.state.plotBraggDataSignal.connect(self.plotBraggData)


    def initializeBorg(self):
        self.stackLogic.initializeBorg()

###############################################################################
#  MULTI-STATE UTILITY METHODS
###############################################################################

    def recorder(self):
        rec = None
        try:
            from easyDiffractionApp.Logic.ScreenRecorder import ScreenRecorder
            rec = ScreenRecorder()
        except (ImportError, ModuleNotFoundError):
            print('Screen recording disabled')
        return rec

    @property
    def _background_obj(self):
        bgs = self.state._sample.pattern.backgrounds
        itm = None
        if len(bgs) > 0:
            itm = bgs[0]
        return itm

    def updateChartBackground(self):
        if self._background_proxy.asObj is None:
            return
        self.proxy._plotting_1d_proxy.logic.setBackgroundData(
                                self._background_proxy.asObj.x_sorted_points,
                                self._background_proxy.asObj.y_sorted_points)

    # def onFitStarted(self):
    #     self.proxy.fitFinishedNotify.emit()

    def onFitFinished(self):
    #     self.proxy.fitResultsChanged.emit()
    #     self.proxy.fitFinishedNotify.emit()
        self.parametersChanged.emit()

    def _onExperimentDataAdded(self):
        print("***** _onExperimentDataAdded")
        self.proxy._plotting_1d_proxy.logic.setMeasuredData(
                                            self.state._experiment_data.x,
                                            self.state._experiment_data.y,
                                            self.state._experiment_data.e)
        self.state._experiment_parameters = \
            self.state._experimentDataParameters(self.state._experiment_data)

        self.proxy.simulationParametersAsObj = \
            json.dumps(self.state._experiment_parameters)

        # self.state.simulationParametersAsObj(json.dumps(self.state._experiment_parameters))

        if len(self.state._sample.pattern.backgrounds) == 0:
            self._background_proxy.logic.initializeContainer()

        self.proxy.experimentDataChanged.emit()
        self.proxy.projectInfoAsJson['experiments'] = \
            self.state._data.experiments[0].name
        self.proxy.projectInfoChanged.emit()

    def _onPhaseAdded(self):
        self.state._onPhaseAdded(self._background_proxy.asObj)

    def removePhase(self, phase_name: str):
        if self.state.removePhase(phase_name):
            self.proxy.structureParametersChanged.emit()
            self.proxy.phasesEnabled.emit()

    def samplesPresent(self):
        return len(self.state._sample.phases) > 0

    # def minimizerNames(self):
    #     return self._fitting_proxy.logic.fitter.available_engines

    # def minimizerMethodNames(self):
    #     return self._fitting_proxy.logic.minimizerMethodNames()

    def currentCalculatorIndex(self):
        return self._interface.available_interfaces.index(self._interface.current_interface_name)

    def currentMinimizerMethodIndex(self, new_index: int):
        self._fitting_proxy.logic.currentMinimizerMethodIndex(new_index)
        self.proxy._fitting_proxy.currentMinimizerMethodChanged.emit()

    def setCurrentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return False
        new_name = self._interface.available_interfaces[new_index]
        self._interface.switch(new_name)
        return True

    def currentMinimizerMethodName(self):
        return self._fitting_proxy.logic._current_minimizer_method_name

    def statusModelAsObj(self):
        engine_name = self._fitting_proxy.logic.fitter.current_engine.name
        minimizer_name = self._fitting_proxy.logic._current_minimizer_method_name
        return self.state.statusModelAsObj(engine_name, minimizer_name)

    def statusModelAsXml(self):
        engine_name = self._fitting_proxy.logic.fitter.current_engine.name
        minimizer_name = self._fitting_proxy.logic._current_minimizer_method_name
        return self.state.statusModelAsXml(engine_name, minimizer_name)

    def plotCalculatedData(self, data):
        self.proxy._plotting_1d_proxy.logic.setCalculatedData(data[0], data[1])

    def plotBraggData(self, data):
        self.proxy._plotting_1d_proxy.logic.setBraggData(data[0], data[1], data[2], data[3])  # noqa: E501
