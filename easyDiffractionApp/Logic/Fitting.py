# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import Signal, QObject, QThread

from threading import Thread

from easyCore.Fitting.Fitting import Fitter as CoreFitter
from easyCore.Fitting.Constraints import ObjConstraint, NumericConstraint

from dicttoxml import dicttoxml
from distutils.util import strtobool


def _defaultFitResults():
    return {
        "success": None,
        "nvarys":  None,
        "GOF":     None,
        "redchi2": None
    }


class FittingLogic(QObject):
    """
    Logic related to the fitter setup
    """
    fitFinished = Signal()
    fitStarted = Signal()
    currentMinimizerChanged = Signal()
    currentMinimizerMethodChanged = Signal()
    currentCalculatorChanged = Signal()
    finished = Signal(dict)
    failed = Signal(str)

    def __init__(self, parent=None, interface=None):
        super().__init__(parent)

        self.parent = parent
        self.interface = interface
        self.fitter = CoreFitter(self.parent.l_phase._sample, self.interface.fit_func)

        # Multithreading
        # self._fitter_thread = None
        self._fit_finished = True
        self._fit_results = _defaultFitResults()
        self.data = None
        self.is_fitting_now = False
        self._current_minimizer_method_index = 0
        self._current_minimizer_method_name = self.fitter.available_methods()[0]  # noqa: E501
        self.currentMinimizerChanged.connect(self.onCurrentMinimizerChanged)

        self.fit_thread = Thread(target=self.fit_threading)
        self.finished.connect(self.onSuccess)
        self.failed.connect(self.onFailed)

    def fit_threading(self):
        data = self.data
        method = self._current_minimizer_method_name

        self._fit_finished = False
        self.fitStarted.emit()
        exp_data = data.experiments[0]

        x = exp_data.x
        y = exp_data.y
        weights = 1 / exp_data.e

        try:
            res = self.fitter.fit(x, y, weights=weights, method=method)
        except Exception as ex:
            self.failed.emit(str(ex))
            return
        self.finished.emit(res)

    def _defaultFitResults(self):
        return {
            "success": None,
            "nvarys":  None,
            "GOF":     None,
            "redchi2": None
        }

    def onSuccess(self, res):
        if self.fit_thread.is_alive():
            self.fit_thread.join()
        self._fit_results = {
            "success": res.success,
            "nvarys":  res.n_pars,
            "GOF":     float(res.goodness_of_fit),
            "redchi2": float(res.reduced_chi)
        }
        self.setFitResults()

    def onFailed(self, ex):
        if self.fit_thread.is_alive():
            self.fit_thread.join()
        print("**** onFailed: fit FAILED with:\n {}".format(str(ex)))
        self._fit_results = self._defaultFitResults()
        self._fit_results['success'] = 'Failure'  # not None but a string
        self.setFitResults()

    def setFitResults(self):
        self._fit_finished = True
        self.fitFinished.emit()
        # must reinstantiate the thread object
        self.fit_thread = Thread(target=self.fit_threading)

    # def fit(self, data):
    def fit(self):
        self.data = self.parent.l_parameters._data
        if not self.fit_thread.is_alive():
            self.is_fitting_now = True
            self.fit_thread.start()

    def currentMinimizerIndex(self):
        current_name = self.fitter.current_engine.name
        index = self.fitter.available_engines.index(current_name)
        return index

    def setCurrentMinimizerIndex(self, new_index: int):
        if self.currentMinimizerIndex() == new_index:
            return
        new_name = self.fitter.available_engines[new_index]
        self.fitter.switch_engine(new_name)
        self.currentMinimizerChanged.emit()

    def onCurrentMinimizerChanged(self):
        idx = 0
        minimizer_name = self.fitter.current_engine.name
        if minimizer_name == 'lmfit':
            idx = self.minimizerMethodNames().index('leastsq')
        elif minimizer_name == 'bumps':
            idx = self.minimizerMethodNames().index('lm')
        if -1 < idx != self._current_minimizer_method_index:
            # Bypass the property as it would be added to the stack.
            self._current_minimizer_method_index = idx
            self._current_minimizer_method_name = self.minimizerMethodNames()[idx]  # noqa: E501
            self.currentMinimizerMethodChanged.emit()
        return

    def minimizerMethodNames(self):
        current_minimizer = self.fitter.available_engines[self.currentMinimizerIndex()]  # noqa: E501
        tested_methods = {
            'lmfit': ['leastsq', 'powell', 'cobyla'],
            'bumps': ['newton', 'lm'],
            'DFO_LS': ['leastsq']
        }
        return tested_methods[current_minimizer]

    def currentMinimizerMethodIndex(self, new_index: int):
        if self._current_minimizer_method_index == new_index:
            return

        self._current_minimizer_method_index = new_index
        self._current_minimizer_method_name = self.minimizerMethodNames()[new_index]  # noqa: E501
        self.currentMinimizerMethodChanged.emit()

    ####################################################################################################################
    # Calculator
    ####################################################################################################################

    def calculatorNames(self):
        return self.interface.available_interfaces

    def currentCalculatorIndex(self):
        return self.interface.available_interfaces.index(self.interface.current_interface_name)

    def setCurrentCalculatorIndex(self, new_index: int):
        if self.currentCalculatorIndex == new_index:
            return
        new_name = self.interface.available_interfaces[new_index]
        self.interface.switch(new_name)
        self.currentCalculatorChanged.emit()
        print("***** _onCurrentCalculatorChanged")
        self._onCurrentCalculatorChanged()
        self.parent.l_parameters._updateCalculatedData()

    def _onCurrentCalculatorChanged(self):
        data = self.parent.l_parameters._data.simulations
        data = data[0]
        data.name = f'{self.interface.current_interface_name} engine'

    # Constraints
    def addConstraint(self, dependent_par_idx, relational_operator,
                      value, arithmetic_operator, independent_par_idx):
        if dependent_par_idx == -1 or value == "":
            print("Failed to add constraint: Unsupported type")
            return
        # if independent_par_idx == -1:
        #    print(f"Add constraint: {self.fitablesList()[dependent_par_idx]['label']}{relational_operator}{value}")
        # else:
        #    print(f"Add constraint: {self.fitablesList()[dependent_par_idx]['label']}{relational_operator}{value}{arithmetic_operator}{self.fitablesList()[independent_par_idx]['label']}")
        pars = [par for par in self.fitter.fit_object.get_parameters() if par.enabled]
        if arithmetic_operator != "" and independent_par_idx > -1:
            c = ObjConstraint(pars[dependent_par_idx],
                              str(float(value)) + arithmetic_operator,
                              pars[independent_par_idx])
        elif arithmetic_operator == "" and independent_par_idx == -1:
            c = NumericConstraint(pars[dependent_par_idx],
                                  relational_operator.replace("=", "=="),
                                  float(value))
        else:
            print("Failed to add constraint: Unsupported type")
            return
        # print(c)
        c()
        self.fitter.add_fit_constraint(c)

    def constraintsList(self):
        constraint_list = []
        for index, constraint in enumerate(self.fitter.fit_constraints()):
            if type(constraint) is ObjConstraint:
                independent_name = constraint.get_obj(constraint.independent_obj_ids).name
                relational_operator = "="
                value = float(constraint.operator[:-1])
                arithmetic_operator = constraint.operator[-1]
            elif type(constraint) is NumericConstraint:
                independent_name = ""
                relational_operator = constraint.operator.replace("==", "=")
                value = constraint.value
                arithmetic_operator = ""
            else:
                print(f"Failed to get constraint: Unsupported type {type(constraint)}")
                return
            number = index + 1
            dependent_name = constraint.get_obj(constraint.dependent_obj_ids).name
            enabled = int(constraint.enabled)
            constraint_list.append(
                {"number": number,
                 "dependentName": dependent_name,
                 "relationalOperator": relational_operator,
                 "value": value,
                 "arithmeticOperator": arithmetic_operator,
                 "independentName": independent_name,
                 "enabled": enabled}
            )
        return constraint_list

    def constraintsAsXml(self):
        xml = dicttoxml(self.constraintsList(), attr_type=False)
        xml = xml.decode()
        return xml

    def removeConstraintByIndex(self, index: int):
        self.fitter.remove_fit_constraint(index)

    def toggleConstraintByIndex(self, index, enabled):
        constraint = self.fitter.fit_constraints()[index]
        constraint.enabled = bool(strtobool(enabled))


class Fitter(QThread):
    """
    Simple wrapper for calling a function in separate thread
    """
    failed = Signal(str)
    finished = Signal(dict)

    def __init__(self, parent, obj, method_name, *args, **kwargs):
        QThread.__init__(self, parent)
        self._obj = obj
        self.method_name = method_name
        self.args = args
        self.kwargs = kwargs

    def run(self):
        res = {}
        if hasattr(self._obj, self.method_name):
            func = getattr(self._obj, self.method_name)
            try:
                res = func(*self.args, **self.kwargs)
            except Exception as ex:
                self.failed.emit(str(ex))
                return str(ex)
            self.finished.emit(res)
        return res

    def stop(self):
        self.terminate()
        self.wait()  # to assure proper termination
