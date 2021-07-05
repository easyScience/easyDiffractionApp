// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents


ExComponents.ApplicationWindow {
    id: window

    appName: ExGlobals.Constants.appName
    appVersion: ExGlobals.Constants.appVersion
    appDate: ExGlobals.Constants.appDate
}
