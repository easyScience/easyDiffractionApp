// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize * 0.5

    // Zero shift
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Zero shift:")
    }
    EaElements.Parameter {
        width: textFieldWidth()
        units: "deg" //ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift.units
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.zero_shift["@id"], text)
    }

    // Wavelength
    EaComponents.TableViewLabel{
        horizontalAlignment: Text.AlignRight
        width: labelWidth()
        text: qsTr("Wavelength:")
    }
    EaElements.Parameter {
        width: textFieldWidth()
        units: "Å" //ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.wavelength.units
        text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.wavelength.value)
        onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.instrumentParametersAsObj.wavelength["@id"], text)
    }

    // Logic

    function labelWidth() {
        return (EaStyle.Sizes.sideBarContentWidth - spacing * 3 - textFieldWidth() * 2) / 2
    }

    function textFieldWidth() {
        return EaStyle.Sizes.fontPixelSize * 11.0
    }

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}
