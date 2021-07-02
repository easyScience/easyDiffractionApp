class Plotting3dLogic():
    def __init__(self, parent):

        self.parent = parent

        # Plotting 3D
        self._3d_plotting_libs = ['chemdoodle', 'qtdatavisualization']
        self._current_3d_plotting_lib = self._3d_plotting_libs[0]

        self._show_bonds = True
        self._bonds_max_distance = 2.0

    def plotting3dLibs(self):
        return self._3d_plotting_libs

    def current3dPlottingLib(self):
        return self._current_3d_plotting_lib

    def onCurrent3dPlottingLibChanged(self):
        pass

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
