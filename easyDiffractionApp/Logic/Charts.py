# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from easyDiffractionApp.Logic.Proxies.Plotting1d import Plotting1dProxy


class ChartsLogic():
    def __init__(self, parent):

        self.parent = parent
        # Plotting 1D
        self._plotting_1d_proxy = Plotting1dProxy()

        # Plotting 3D
        self._3d_plotting_libs = ['chemdoodle']
        self._current_3d_plotting_lib = self._3d_plotting_libs[0]

        self._show_bonds = True
        self._bonds_max_distance = 2.0

    def plotting1d(self):
        return self._plotting_1d_proxy

    # 3d plotting

    def plotting3dLibs(self):
        return self._3d_plotting_libs

    def current3dPlottingLib(self):
        return self._current_3d_plotting_lib

    def onCurrent3dPlottingLibChanged(self):
        pass

    # Structure view

    # def _onStructureViewChanged(self):
    #     print("***** _onStructureViewChanged")

    def showBonds(self):
        return self._show_bonds

    def setShowBonds(self, show_bonds: bool):
        if self._show_bonds == show_bonds:
            return
        self._show_bonds = show_bonds

    def bondsMaxDistance(self):
        return self._bonds_max_distance

    def setBondsMaxDistance(self, max_distance: float):
        if self._bonds_max_distance == max_distance:
            return
        self._bonds_max_distance = max_distance
