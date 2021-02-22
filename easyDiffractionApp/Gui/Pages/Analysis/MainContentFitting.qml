import QtQuick 2.13

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Loader {
    source: ExGlobals.Constants.proxy.current1dPlottingLib === 'matplotlib' ?
                ExLogic.Paths.component('AnalysisDataChartMatplotlib.qml') :
                ExLogic.Paths.component('AnalysisDataChartQtCharts.qml')
}
