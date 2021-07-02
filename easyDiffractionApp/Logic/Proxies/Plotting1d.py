__author__ = 'github.com/andrewsazonov'
__version__ = '0.0.1'

from PySide2.QtCore import QObject, Signal, Slot, Property
from easyDiffractionApp.Logic.Plotting1d import Plotting1dLogic


class Plotting1dProxy(QObject):
    """
    A proxy class to interact between the QML plot and Python datasets.
    """

    dummySignal = Signal()

    # Lib
    currentLibChanged = Signal()

    # Ranges
    experimentPlotRangesObjChanged = Signal()
    analysisPlotRangesObjChanged = Signal()

    # Data containers
    bokehMeasuredDataObjChanged = Signal()
    bokehCalculatedDataObjChanged = Signal()
    bokehDifferenceDataObjChanged = Signal()
    bokehBraggDataObjChanged = Signal()
    bokehBackgroundDataObjChanged = Signal()

    qtchartsMeasuredDataObjChanged = Signal()
    qtchartsCalculatedDataObjChanged = Signal()
    qtchartsDifferenceDataObjChanged = Signal()
    qtchartsBraggDataObjChanged = Signal()
    qtchartsBackgroundDataObjChanged = Signal()

    def __init__(self, parent=None, logic=None):
        super().__init__(parent)
        # self.logic = Plotting1dLogic(self)
        self.logic = logic.l_plotting1d
        # connect logic signal to proxy signal
        self.logic.currentLibChanged.connect(self.currentLibChanged)

        # Ranges
        self.logic.experimentPlotRangesObjChanged.connect(self.experimentPlotRangesObjChanged)
        self.logic.analysisPlotRangesObjChanged.connect(self.analysisPlotRangesObjChanged)

        # Data containers
        self.logic.bokehMeasuredDataObjChanged.connect(self.bokehMeasuredDataObjChanged)
        self.logic.bokehCalculatedDataObjChanged.connect(self.bokehCalculatedDataObjChanged)
        self.logic.bokehDifferenceDataObjChanged.connect(self.bokehDifferenceDataObjChanged)
        self.logic.bokehBraggDataObjChanged.connect(self.bokehBraggDataObjChanged)
        self.logic.bokehBackgroundDataObjChanged.connect(self.bokehBackgroundDataObjChanged)

        self.logic.qtchartsMeasuredDataObjChanged.connect(self.qtchartsMeasuredDataObjChanged)
        self.logic.qtchartsCalculatedDataObjChanged.connect(self.qtchartsCalculatedDataObjChanged)
        self.logic.qtchartsDifferenceDataObjChanged.connect(self.qtchartsDifferenceDataObjChanged)
        self.logic.qtchartsBraggDataObjChanged.connect(self.qtchartsBraggDataObjChanged)
        self.logic.qtchartsBackgroundDataObjChanged.connect(self.qtchartsBackgroundDataObjChanged)

    # Libs for GUI
    @Property('QVariant', notify=dummySignal)
    def libs(self):
        return self.logic._libs

    @Property(str, notify=currentLibChanged)
    def currentLib(self):
        return self.logic._current_lib

    @currentLib.setter
    def currentLib(self, lib):
        self.logic.currentLib(lib)

    # Ranges for GUI
    @Property('QVariant', notify=experimentPlotRangesObjChanged)
    def experimentPlotRangesObj(self):
        return self.logic._experiment_plot_ranges_obj

    @Property('QVariant', notify=analysisPlotRangesObjChanged)
    def analysisPlotRangesObj(self):
        return self.logic._analysis_plot_ranges_obj

    # Data containers for GUI
    @Property('QVariant', notify=bokehMeasuredDataObjChanged)
    def bokehMeasuredDataObj(self):
        return self.logic._bokeh_measured_data_obj

    @Property('QVariant', notify=bokehCalculatedDataObjChanged)
    def bokehCalculatedDataObj(self):
        return self.logic._bokeh_calculated_data_obj

    @Property('QVariant', notify=bokehDifferenceDataObjChanged)
    def bokehDifferenceDataObj(self):
        return self.logic._bokeh_difference_data_obj

    @Property('QVariant', notify=bokehBraggDataObjChanged)
    def bokehBraggDataObj(self):
        return self.logic._bokeh_bragg_data_obj

    @Property('QVariant', notify=bokehBackgroundDataObjChanged)
    def bokehBackgroundDataObj(self):
        return self.logic._bokeh_background_data_obj

    @Property('QVariant', notify=qtchartsMeasuredDataObjChanged)
    def qtchartsMeasuredDataObj(self):
        return self.logic._qtcharts_measured_data_obj

    @Property('QVariant', notify=qtchartsCalculatedDataObjChanged)
    def qtchartsCalculatedDataObj(self):
        return self.logic._qtcharts_calculated_data_obj

    @Property('QVariant', notify=qtchartsDifferenceDataObjChanged)
    def qtchartsDifferenceDataObj(self):
        return self.logic._qtcharts_difference_data_obj

    @Property('QVariant', notify=qtchartsBraggDataObjChanged)
    def qtchartsBraggDataObj(self):
        return self.logic._qtcharts_bragg_data_obj

    @Property('QVariant', notify=qtchartsBackgroundDataObjChanged)
    def qtchartsBackgroundDataObj(self):
        return self.logic._qtcharts_background_data_obj

    # QtCharts for GUI
    @Slot('QVariant', 'QVariant')
    def lineSeriesCustomReplace(self, line_series, points):
        self.logic.lineSeriesCustomReplace(line_series, points)

    @Slot(int, str, result='QBrush')
    def verticalLine(self, size, color):
        return self.logic.verticalLine(size, color)
