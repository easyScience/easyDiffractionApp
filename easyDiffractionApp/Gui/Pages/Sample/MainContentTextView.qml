import QtQuick 2.13
import QtQuick.Controls 2.13

// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Logic 1.0 as ExLogic

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            font.family: EaStyle.Fonts.monoFontFamily
            textFormat: TextEdit.RichText
            text: ExLogic.Helpers.highlightCifSyntax(ExGlobals.Constants.proxy.phase.phasesAsCif)
            onEditingFinished: ExGlobals.Constants.proxy.phase.phasesAsCif = ExLogic.Helpers.removeCifSyntaxHighlighting(text)
        }
    }

    ///////////////
    // Tool buttons
    ///////////////

    Row {
        anchors.top: parent.top
        anchors.right: parent.right

        anchors.topMargin: EaStyle.Sizes.fontPixelSize
        anchors.rightMargin: EaStyle.Sizes.fontPixelSize

        spacing: 0.25 * EaStyle.Sizes.fontPixelSize

        EaElements.TabButton {
            checkable: false
            autoExclusive: false
            height: EaStyle.Sizes.toolButtonHeight
            width: EaStyle.Sizes.toolButtonHeight
            borderColor: EaStyle.Colors.chartAxis
            fontIcon: "clipboard-check"
            ToolTip.text: qsTr("Accept changes")
            onClicked: forceActiveFocus()
        }
    }

}
