// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13

import Gui.Logic 1.0 as ExLogic
import Gui.Globals 1.0 as ExGlobals

Loader {
    source: {
        if (ExGlobals.Constants.proxy.plotting1d.currentLib === 'qtcharts') {
            return ExLogic.Paths.component('ExperimentDataChartQtCharts.qml')
        } else if (ExGlobals.Constants.proxy.plotting1d.currentLib === 'bokeh') {
            return ExLogic.Paths.component('ExperimentDataChartBokeh.qml')
        }
    }
}
