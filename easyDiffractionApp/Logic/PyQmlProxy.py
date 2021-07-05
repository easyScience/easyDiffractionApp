# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

# noqa: E501
from PySide2.QtCore import QObject, Signal, Property

from easyDiffractionApp.Logic.LogicController import LogicController
from easyDiffractionApp.Logic.Proxies.Background import BackgroundProxy
from easyDiffractionApp.Logic.Proxies.Experiment import ExperimentProxy
from easyDiffractionApp.Logic.Proxies.Fitting import FittingProxy
from easyDiffractionApp.Logic.Proxies.Parameters import ParametersProxy
from easyDiffractionApp.Logic.Proxies.Phase import PhaseProxy
from easyDiffractionApp.Logic.Proxies.Plotting1d import Plotting1dProxy
from easyDiffractionApp.Logic.Proxies.Plotting3d import Plotting3dProxy
from easyDiffractionApp.Logic.Proxies.Project import ProjectProxy
from easyDiffractionApp.Logic.Proxies.Stack import StackProxy


class PyQmlProxy(QObject):
    # SIGNALS
    currentCalculatorChanged = Signal()

    # Status info
    statusInfoChanged = Signal()

    # Misc
    dummySignal = Signal()

    # METHODS

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize logics
        self.lc = LogicController(self)

        ################## proxies #################
        self._fitting_proxy = FittingProxy(self, self.lc)
        self._plotting_1d_proxy = Plotting1dProxy(logic=self.lc)
        self._plotting_3d_proxy = Plotting3dProxy(logic=self.lc)
        self._background_proxy = BackgroundProxy(self, logic=self.lc)
        self._stack_proxy = StackProxy(self, logic=self.lc)
        self._parameters_proxy = ParametersProxy(self, logic=self.lc)
        self._project_proxy = ProjectProxy(self, logic=self.lc)
        self._experiment_proxy = ExperimentProxy(self, logic=self.lc)
        self._phase_proxy = PhaseProxy(self, logic=self.lc)

        ################## signals from other proxies #################
        self.currentCalculatorChanged.connect(self.statusInfoChanged)
        self._fitting_proxy.currentMinimizerChanged.connect(self.statusInfoChanged)
        self._fitting_proxy.currentMinimizerMethodChanged.connect(self.statusInfoChanged)
        # Constraints
        self._fitting_proxy.constraintsChanged.connect(self._parameters_proxy._setParametersAsObj)
        self._fitting_proxy.constraintsChanged.connect(self._parameters_proxy._setParametersAsXml)
        self._fitting_proxy.constraintsChanged.connect(self._parameters_proxy._onSimulationParametersChanged)

        # start the undo/redo stack
        self.lc.initializeBorg()

    ####################################################################################################################
    ####################################################################################################################
    # Proxies
    ####################################################################################################################
    ####################################################################################################################

    # 1d plotting
    @Property('QVariant', notify=dummySignal)
    def plotting1d(self):
        return self._plotting_1d_proxy

    # 3d plotting
    @Property('QVariant', notify=dummySignal)
    def plotting3d(self):
        return self._plotting_3d_proxy

    # background
    @Property('QVariant', notify=dummySignal)
    def background(self):
        return self._background_proxy

    # experiment
    @Property('QVariant', notify=dummySignal)
    def experiment(self):
        return self._experiment_proxy

    # fitting
    @Property('QVariant', notify=dummySignal)
    def fitting(self):
        return self._fitting_proxy

    # project
    @Property('QVariant', notify=dummySignal)
    def project(self):
        return self._project_proxy

    # stack
    @Property('QVariant', notify=dummySignal)
    def stack(self):
        return self._stack_proxy

    # phase
    @Property('QVariant', notify=dummySignal)
    def phase(self):
        return self._phase_proxy

    # parameters
    @Property('QVariant', notify=dummySignal)
    def parameters(self):
        return self._parameters_proxy

    # status
    @Property('QVariant', notify=statusInfoChanged)
    def statusModelAsObj(self):
        return self.lc.statusModelAsObj()

    @Property(str, notify=statusInfoChanged)
    def statusModelAsXml(self):
        return self.lc.statusModelAsXml()

    # screen recorder
    @Property('QVariant', notify=dummySignal)
    def screenRecorder(self):
        return self.lc._screen_recorder
