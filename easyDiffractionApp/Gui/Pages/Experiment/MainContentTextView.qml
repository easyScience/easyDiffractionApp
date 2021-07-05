// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            ///text: EaLogic.Utils.prettyXml(ExGlobals.Constants.proxy.fitablesListAsXml)
            //text: prettyJson(ExGlobals.Constants.proxy.fitting.fitablesDict)
            //text: prettyJson(ExGlobals.Constants.proxy.fitting.fitablesList)
        }
    }

}
