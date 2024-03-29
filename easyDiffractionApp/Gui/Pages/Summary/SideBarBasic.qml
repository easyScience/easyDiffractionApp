// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Dialogs 1.3 as QtQuickDialogs1
import Qt.labs.settings 1.0
import QtWebEngine 1.10

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals
import Gui.Pages.Summary 1.0 as ExSummaryPage

EaComponents.SideBarColumn {

    // TEMPORARILY DISABLED
    // EaElements.GroupBox {
    //     title: qsTr("Create report")
    //     // enabled: !ExGlobals.Constants.proxy.project.readOnly
    //     enabled: true
    //     collapsible: false
    //     last: true

    //     // Create button
    //     EaElements.SideBarButton {
    //         wide: true
    //         fontIcon: "flask"
    //         text: qsTr("Create")

    //         onClicked: {
    //             ExGlobals.Constants.proxy.project.requestReport()
    //         }

    //         Component.onCompleted: ExGlobals.Variables.exportReportButton = this
    //     }
    // }

    EaElements.GroupBox {
        title: qsTr("Export report")
        // enabled: !ExGlobals.Constants.proxy.project.readOnly
        enabled: true
        collapsible: false
        last: true

        // Name-Format
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 1.5

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    enabled: false
                    width: locationLabel.width
                    anchors.verticalCenter: parent.verticalCenter
                    horizontalAlignment: TextInput.AlignRight
                    text: qsTr("Name")
                }

                EaElements.TextField {
                    id: reportNameField

                    width: EaStyle.Sizes.sideBarContentWidth - locationLabel.width - formatLabel.width - reportFormatField.width - EaStyle.Sizes.fontPixelSize * 2.5
                    horizontalAlignment: TextInput.AlignLeft
                    placeholderText: qsTr("Enter report file name here")

                    Component.onCompleted: text = 'report'
                }
            }

            Row {
                spacing: EaStyle.Sizes.fontPixelSize * 0.5

                EaElements.Label {
                    id: formatLabel
                    enabled: false
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Format")
                }

                EaElements.ComboBox {
                    id: reportFormatField

                    topInset: 0
                    bottomInset: 0
                    width: EaStyle.Sizes.fontPixelSize * 10

                    textRole: "text"
                    valueRole: "value"
                    model: [
                        { value: 'html', text: qsTr("Interactive HTML") },
                        { value: 'pdf', text: qsTr("Static PDF") }                    ]
                }
            }

        }

        // Location
        Row {
            spacing: EaStyle.Sizes.fontPixelSize * 0.5

            EaElements.Label {
                id: locationLabel

                enabled: false
                anchors.verticalCenter: parent.verticalCenter
                text: qsTr("Location")
            }

            EaElements.TextField {
                id: reportLocationField

                width: EaStyle.Sizes.sideBarContentWidth - locationLabel.width - EaStyle.Sizes.fontPixelSize * 0.5
                rightPadding: chooseButton.width
                horizontalAlignment: TextInput.AlignLeft

                placeholderText: qsTr("Enter report location here")
                text: ExGlobals.Constants.proxy.project.projectCreated ?
                          EaLogic.Utils.urlToLocalFile(reportParentDirDialog.folder + '/' + reportNameField.text + '.' + reportFormatField.currentValue) :
                          ''

                EaElements.ToolButton {
                    id: chooseButton

                    anchors.right: parent.right

                    showBackground: false
                    fontIcon: "folder-open"
                    ToolTip.text: qsTr("Choose report parent directory")

                    onClicked: reportParentDirDialog.open()
                }
            }
        }

        // Export button
        EaElements.SideBarButton {
            wide: true
            fontIcon: "download"
            text: qsTr("Export")

            onClicked: {
                if (reportFormatField.currentValue === 'html') {
                    ExGlobals.Constants.proxy.project.saveReport(reportLocationField.text)
                } else if (reportFormatField.currentValue === 'pdf') {
                    ExGlobals.Variables.reportWebView.printToPdf(reportLocationField.text)
                }
            }

            Component.onCompleted: ExGlobals.Variables.exportReportButton = this
        }

        Component.onCompleted: ExGlobals.Variables.exportReportGroup = this
    }

    // Directory dialog
    QtQuickDialogs1.FileDialog {
        id: reportParentDirDialog

        title: qsTr("Choose report parent directory")
        selectFolder: true
        selectMultiple: false

        folder: ExGlobals.Constants.proxy.project.currentProjectPath
    }

}
