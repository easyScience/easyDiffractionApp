// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Animations 1.0 as EaAnimations
import easyApp.Gui.Elements 1.0 as EaElements

Rectangle {
    color: EaStyle.Colors.contentBackground
    Behavior on color { EaAnimations.ThemeChange {} }

    EaElements.Label {
        enabled: false
        anchors.centerIn: parent
        font.family: EaStyle.Fonts.secondFontFamily
        font.pixelSize: EaStyle.Sizes.fontPixelSize * 3
        font.weight: Font.ExtraLight
        text: 'Not implemented'
    }
}
