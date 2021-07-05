# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import QObject, Signal, Property

# from easyDiffractionApp.Logic.Plotting3d import Plotting3dLogic
from easyCore.Utils.UndoRedo import property_stack_deco


class Plotting3dProxy(QObject):
    # Plotting
    current3dPlottingLibChanged = Signal()
    structureViewChanged = Signal()
    dummySignal = Signal()

    def __init__(self, logic=None):
        super().__init__()
        # self.parent = parent
        self.logic = logic.l_plotting3d
        self.current3dPlottingLibChanged.connect(self.onCurrent3dPlottingLibChanged)

    @Property('QVariant', notify=current3dPlottingLibChanged)
    def current3dPlottingLib(self):
        return self.logic.current3dPlottingLib()

    @current3dPlottingLib.setter
    @property_stack_deco('Changing 3D library from {old_value} to {new_value}')
    def current3dPlottingLib(self, plotting_lib):
        self.logic._current_3d_plotting_lib = plotting_lib
        self.current3dPlottingLibChanged.emit()

    def onCurrent3dPlottingLibChanged(self):
        self.logic.onCurrent3dPlottingLibChanged()

    @Property('QVariant', notify=dummySignal)
    def plotting3dLibs(self):
        return self.logic.plotting3dLibs()

    @Property(bool, notify=structureViewChanged)
    def showBonds(self):
        return self.logic.showBonds()

    @showBonds.setter
    def showBonds(self, show_bonds: bool):
        self.logic.setShowBonds(show_bonds)
        self.structureViewChanged.emit()

    @Property(float, notify=structureViewChanged)
    def bondsMaxDistance(self):
        return self.logic.bondsMaxDistance()

    @bondsMaxDistance.setter
    def bondsMaxDistance(self, max_distance: float):
        self.logic.setBondsMaxDistance(max_distance)
        self.structureViewChanged.emit()
