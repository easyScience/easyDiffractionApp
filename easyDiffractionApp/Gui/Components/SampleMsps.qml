// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

EaComponents.TableView {
    property int numColumnWidth: EaStyle.Sizes.fontPixelSize * 2.5
    property int labelColumnWidth: EaStyle.Sizes.fontPixelSize * 2.5
    property int typeColumnWidth: EaStyle.Sizes.fontPixelSize * 4.5
    property int numFixedColumn: 3
    property int numFlexColumn: 6
    property int flexColumnWidth: (width -
                                    numColumnWidth -
                                    labelColumnWidth -
                                    typeColumnWidth -
                                    EaStyle.Sizes.tableColumnSpacing * (numFixedColumn + numFlexColumn - 1)) /
                                    numFlexColumn

    // Table model

    model: XmlListModel {
        property int phaseIndex: ExGlobals.Constants.proxy.phase.currentPhaseIndex + 1

        xml: ExGlobals.Constants.proxy.phase.phasesAsXml
        query: `/data/item/atoms/data`

        XmlRole { name: "label"; query: "label/value/string()" }
        XmlRole { name: "mspType"; query: "msp/msp_type/value/string()" }
        XmlRole { name: "mspIso"; query:   "msp/msp_class/chi/value/number()" }
        XmlRole { name: "mspAni11"; query: "msp/msp_class/chi_11/value/number()" }
        XmlRole { name: "mspAni22"; query: "msp/msp_class/chi_22/value/number()" }
        XmlRole { name: "mspAni33"; query: "msp/msp_class/chi_33/value/number()" }
        XmlRole { name: "mspAni12"; query: "msp/msp_class/chi_12/value/number()" }
        XmlRole { name: "mspAni13"; query: "msp/msp_class/chi_13/value/number()" }
        XmlRole { name: "mspAni23"; query: "msp/msp_class/chi_23/value/number()" }

        XmlRole { name: "mspIsoId"; query: "msp/msp_class/chi/__id/string()" }
        XmlRole { name: "mspAniId11"; query: "msp/msp_class/chi_11/__id/string()" }
        XmlRole { name: "mspAniId22"; query: "msp/msp_class/chi_22/__id/string()" }
        XmlRole { name: "mspAniId33"; query: "msp/msp_class/chi_33/__id/string()" }
        XmlRole { name: "mspAniId12"; query: "msp/msp_class/chi_12/__id/string()" }
        XmlRole { name: "mspAniId13"; query: "msp/msp_class/chi_13/__id/string()" }
        XmlRole { name: "mspAniId23"; query: "msp/msp_class/chi_23/__id/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {
        property string modelMspType: model.mspType

        EaComponents.TableViewLabel {
            width: numColumnWidth
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
            horizontalAlignment: Text.AlignLeft
            width: labelColumnWidth
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewComboBox {
            enabled: false
            width: typeColumnWidth
            headerText: "Type"
            model: ["None", "Cani", "Ciso"]
            //currentIndex: model.indexOf(modelMspType)
            Component.onCompleted: {
                currentIndex = model.indexOf(modelMspType)
                if (currentIndex === -1) {
                    currentIndex = 0
                }
            }
        }

        /*
        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "Iso"//"\u03C7Iso"
            text: EaLogic.Utils.toFixed(model.mspIso)
            onEditingFinished: editParameterValue(model.mspIsoId, text)
        }
        */

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "\u03C711"
            text: EaLogic.Utils.toFixed(model.mspAni11)
            onEditingFinished: editParameterValue(model.mspAniId11, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "\u03C722"
            text: EaLogic.Utils.toFixed(model.mspAni22)
            onEditingFinished: editParameterValue(model.mspAniId22, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "\u03C733"
            text: EaLogic.Utils.toFixed(model.mspAni33)
            onEditingFinished: editParameterValue(model.mspAniId33, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "\u03C712"
            text: EaLogic.Utils.toFixed(model.mspAni12)
            onEditingFinished: editParameterValue(model.mspAniId12, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "\u03C713"
            text: EaLogic.Utils.toFixed(model.mspAni13)
            onEditingFinished: editParameterValue(model.mspAniId13, text)
        }

        EaComponents.TableViewTextInput {
            width: flexColumnWidth
            headerText: "\u03C723"
            text: EaLogic.Utils.toFixed(model.mspAni23)
            onEditingFinished: editParameterValue(model.mspAniId23, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }

}

