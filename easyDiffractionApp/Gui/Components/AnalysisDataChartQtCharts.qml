import QtQuick 2.13

import easyAppGui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseQtCharts {
    measuredData: ExGlobals.Constants.proxy.plotting1d.qtchartsMeasuredDataObj
    calculatedData: ExGlobals.Constants.proxy.plotting1d.qtchartsCalculatedDataObj
    braggData: ExGlobals.Constants.proxy.plotting1d.qtchartsBraggDataObj
    differenceData: ExGlobals.Constants.proxy.plotting1d.qtchartsDifferenceDataObj

    plotRanges: ExGlobals.Constants.proxy.plotting1d.analysisPlotRangesObj

    xAxisTitle: qsTr("2theta (deg)")
    yMainAxisTitle: qsTr("Intensity")
    yDifferenceAxisTitle: qsTr("Difference")

    Component.onCompleted: ExGlobals.Variables.analysisChart = this
}
