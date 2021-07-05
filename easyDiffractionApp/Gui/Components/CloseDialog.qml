import QtQuick 2.14
import QtQuick.Controls 2.14

import easyApp.Gui.Elements 1.0 as EaElements

// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    visible: false

    title: qsTr("Save Changes")

    EaElements.Label {
        anchors.horizontalCenter: parent.horizontalCenter
        text: qsTr("The project has not been saved. Do you want to exit?")
    }

    footer: EaElements.DialogButtonBox {
        EaElements.Button {
            text: qsTr("Save and exit")
            onClicked: {
                ExGlobals.Constants.proxy.project.saveProject()
                window.quit()
            }
        }

        EaElements.Button {
            text: qsTr("Exit without saving")
            onClicked: window.quit()
        }
    }
}

