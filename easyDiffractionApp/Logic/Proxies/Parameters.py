# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import timeit
from typing import Union

from PySide2.QtCore import QObject, Signal, Slot, Property

class ParametersProxy(QObject):

    dummySignal = Signal()
    stateChanged = Signal(bool)
    # Fitables
    parametersAsObjChanged = Signal()
    parametersAsXmlChanged = Signal()

    # Experiment
    patternParametersAsObjChanged = Signal()

    instrumentParametersAsObjChanged = Signal()
    instrumentParametersAsXmlChanged = Signal()

    # Analysis
    simulationParametersChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_parameters

        self.logic.instrumentParametersChanged.connect(self._onInstrumentParametersChanged)
        self.logic.parametersChanged.connect(self._onParametersChanged)
        # Analysis
        self.simulationParametersChanged.connect(self._onSimulationParametersChanged)
        self.simulationParametersChanged.connect(self.parent._stack_proxy.undoRedoChanged)

    ####################################################################################################################
    # Simulation parameters
    ####################################################################################################################

    @Property('QVariant', notify=simulationParametersChanged)
    def simulationParametersAsObj(self):
        return self.logic._simulation_parameters_as_obj

    @simulationParametersAsObj.setter
    def simulationParametersAsObj(self, json_str):
        self.logic.simulationParametersAsObj(json_str)
        self.simulationParametersChanged.emit()

    def _onSimulationParametersChanged(self):
        print("***** _onSimulationParametersChanged")
        self.logic._updateCalculatedData()

    ####################################################################################################################
    # Pattern parameters (scale, zero_shift, backgrounds)
    ####################################################################################################################

    @Property('QVariant', notify=patternParametersAsObjChanged)
    def patternParametersAsObj(self):
        return self.logic._pattern_parameters_as_obj

    ####################################################################################################################
    # Instrument parameters (wavelength, resolution_u, ..., resolution_y)
    ####################################################################################################################

    @Property('QVariant', notify=instrumentParametersAsObjChanged)
    def instrumentParametersAsObj(self):
        return self.logic._instrument_parameters_as_obj

    @Property(str, notify=instrumentParametersAsXmlChanged)
    def instrumentParametersAsXml(self):
        return self.logic._instrument_parameters_as_xml

    def _setInstrumentParametersAsObj(self):
        start_time = timeit.default_timer()
        self.logic._setInstrumentParametersAsObj()
        print("+ _setInstrumentParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsObjChanged.emit()

    def _setInstrumentParametersAsXml(self):
        start_time = timeit.default_timer()
        self.logic._setInstrumentParametersAsXml()
        print("+ _setInstrumentParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.instrumentParametersAsXmlChanged.emit()

    def _onInstrumentParametersChanged(self):
        print("***** _onInstrumentParametersChanged")
        self._setInstrumentParametersAsObj()
        self._setInstrumentParametersAsXml()

   ####################################################################################################################
    # Fitables (parameters table from analysis tab & ...)
    ####################################################################################################################

    @Property('QVariant', notify=parametersAsObjChanged)
    def parametersAsObj(self):
        return self.logic._parameters_as_obj

    @Property(str, notify=parametersAsXmlChanged)
    def parametersAsXml(self):
        return self.logic._parameters_as_xml

    def _setParametersAsObj(self):
        start_time = timeit.default_timer()

        self.logic._setParametersAsObj()
        print("+ _setParametersAsObj: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsObjChanged.emit()

    def _setParametersAsXml(self):
        start_time = timeit.default_timer()
        self.logic._setParametersAsXml()
        print("+ _setParametersAsXml: {0:.3f} s".format(timeit.default_timer() - start_time))
        self.parametersAsXmlChanged.emit()

    def _onParametersChanged(self):
        print("***** _onParametersChanged")
        self._setParametersAsObj()
        self._setParametersAsXml()
        self.parent.project.stateChanged.emit(True)

    # Filtering
    @Slot(str)
    def setParametersFilterCriteria(self, new_criteria):
        self.logic.setParametersFilterCriteria(new_criteria)
        self._onParametersChanged()

    ####################################################################################################################
    # Any parameter
    ####################################################################################################################

    @Slot(str, 'QVariant')
    def editParameter(self, obj_id: str, new_value: Union[bool, float, str]):
        self.logic.editParameter(obj_id, new_value)

