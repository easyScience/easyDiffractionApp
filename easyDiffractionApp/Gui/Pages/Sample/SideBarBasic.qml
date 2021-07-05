// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.3 as Dialogs1

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents

EaComponents.SideBarColumn {

    EaElements.GroupBox {
        title: qsTr("Structural phases")
        collapsible: false
        enabled: ExGlobals.Constants.proxy.fitting.isFitFinished

        ExComponents.SamplePhasesExplorer {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                enabled: ExGlobals.Constants.proxy.phase.phasesAsObj.length === 0

                fontIcon: "upload"
                text: qsTr("Set new phase from CIF")

                onClicked: loadPhaseFileDialog.open()
            }

            EaElements.SideBarButton {
                enabled: ExGlobals.Constants.proxy.phase.phasesAsObj.length === 0

                fontIcon: "plus-circle"
                text: qsTr("Set new phase manually")

                onClicked: ExGlobals.Constants.proxy.phase.addDefaultPhase()

                Component.onCompleted: ExGlobals.Variables.setNewSampleManuallyButton = this
            }
        }

        Component.onCompleted: ExGlobals.Variables.structuralPhasesGroup = this
    }

    EaElements.GroupBox {
        title: qsTr("Symmetry and cell parameters")
        enabled: ExGlobals.Constants.proxy.phase.samplesPresent

        Column {
            ExComponents.SampleSymmetry {}
            ExComponents.SampleCell { titleText: "Cell parameters" }
        }

        Component.onCompleted: ExGlobals.Variables.symmetryGroup = this
    }

    EaElements.GroupBox {
        id: atomsGroup

        title: qsTr("Atoms, atomic coordinates and occupations")
        enabled: ExGlobals.Constants.proxy.phase.samplesPresent

        ExComponents.SampleAtoms {}

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            EaElements.SideBarButton {
                id: appendNewAtomButton

                fontIcon: "plus-circle"
                text: qsTr("Append new atom")

                onClicked: ExGlobals.Constants.proxy.phase.addDefaultAtom()

                Component.onCompleted: ExGlobals.Variables.appendNewAtomButton = appendNewAtomButton
            }

            EaElements.SideBarButton {
                enabled: false
                fontIcon: "clone"
                text: qsTr("Duplicate selected atom")
            }

        }

        Component.onCompleted: ExGlobals.Variables.atomsGroup = atomsGroup
    }

    EaElements.GroupBox {
        title: qsTr("Atomic displacement parameters")
        last: true
        enabled: ExGlobals.Constants.proxy.phase.samplesPresent

        ExComponents.SampleAdps {}

        Component.onCompleted: ExGlobals.Variables.adpsGroup = this
    }

    // Open phase CIF file dialog

    Dialogs1.FileDialog{
        id: loadPhaseFileDialog
        nameFilters: [ "CIF files (*.cif)"]
        onAccepted: ExGlobals.Constants.proxy.phase.addSampleFromCif(fileUrl)
    }
}
