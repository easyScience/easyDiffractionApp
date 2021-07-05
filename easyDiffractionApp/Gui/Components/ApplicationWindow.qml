// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQuick.Dialogs 1.3 as Dialogs1
import QtQuick.XmlListModel 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals
import Gui.Components 1.0 as ExComponents
import Gui.Pages.Home 1.0 as ExHomePage
import Gui.Pages.Project 1.0 as ExProjectPage
import Gui.Pages.Sample 1.0 as ExSamplePage
import Gui.Pages.Experiment 1.0 as ExExperimentPage
import Gui.Pages.Analysis 1.0 as ExAnalysisPage
import Gui.Pages.Summary 1.0 as ExSummaryPage

EaComponents.ApplicationWindow {

    title: ' ' //`${ExGlobals.Constants.appName} ${ExGlobals.Constants.appVersion}`

    ///////////////////
    // APPLICATION BAR
    ///////////////////

    // Left group of application bar tool buttons
    appBarLeftButtons: [

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.project.stateHasChanged &&
                     ExGlobals.Constants.proxy.project.currentProjectPath !== '--- EXAMPLE ---'
            highlighted: true
            fontIcon: "save"
            ToolTip.text: qsTr("Save current state of the project")
            onClicked:  ExGlobals.Constants.proxy.project.saveProject()
        },

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.stack.canUndo
            fontIcon: "undo"
            ToolTip.text: qsTr("Undo " + ExGlobals.Constants.proxy.stack.undoText)
            onClicked: ExGlobals.Constants.proxy.stack.undo()
        },

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.stack.canRedo
            fontIcon: "redo"
            ToolTip.text: qsTr("Redo " + ExGlobals.Constants.proxy.stack.redoText)
            onClicked: ExGlobals.Constants.proxy.stack.redo()
        },

        EaElements.ToolButton {
            enabled: ExGlobals.Constants.proxy.project.projectCreated ||
                     ExGlobals.Constants.proxy.phase.samplesPresent ||
                     ExGlobals.Constants.proxy.experiment.experimentSkipped ||
                     ExGlobals.Constants.proxy.experiment.experimentLoaded
            fontIcon: "backspace"
            ToolTip.text: qsTr("Reset to initial state without project, phases and data")
            onClicked: resetStateDialog.open()
            Component.onCompleted: ExGlobals.Variables.resetStateButton = this
        }

    ]

    // Right group of application bar tool buttons
    appBarRightButtons: [

        EaElements.ToolButton {
            fontIcon: "cog"
            ToolTip.text: qsTr("Application preferences")
            onClicked: EaGlobals.Variables.showAppPreferencesDialog = true
            Component.onCompleted: ExGlobals.Variables.preferencesButton = this
        },

        EaElements.ToolButton {
            enabled: false
            fontIcon: "question-circle"
            ToolTip.text: qsTr("Get online help")
            onClicked: Qt.openUrlExternally(ExGlobals.Constants.appUrl)
        },

        EaElements.ToolButton {
            fontIcon: "bug"
            ToolTip.text: qsTr("Report a bug or issue")
            onClicked: Qt.openUrlExternally(`${ExGlobals.Constants.appUrl}/index.html#contact`)
        }

    ]

    // Central group of application bar tab buttons (workflow tabs)
    // Tab buttons for the pages described below
    appBarCentralTabs.contentData: [

        // Home tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.homePageEnabled
            fontIcon: "home"
            text: qsTr("Home")
            ToolTip.text: qsTr("Home page")
            Component.onCompleted: ExGlobals.Variables.homeTabButton = this
        },

        // Project tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.projectPageEnabled
            fontIcon: "archive"
            text: qsTr("Project")
            ToolTip.text: qsTr("Project description page")
            Component.onCompleted: ExGlobals.Variables.projectTabButton = this
        },

        // Sample tab
        EaElements.AppBarTabButton {
            enabled: ExGlobals.Variables.samplePageEnabled
            fontIcon: "gem"
            text: qsTr("Sample")
            ToolTip.text: qsTr("Sample model description page")
            Component.onCompleted: ExGlobals.Variables.sampleTabButton = this
        },

        // Experiment tab
        EaElements.AppBarTabButton {
            id: experimentTabButton
            enabled: ExGlobals.Constants.proxy.phase.samplesPresent
            fontIcon: "microscope"
            text: qsTr("Experiment")
            ToolTip.text: qsTr("Experimental settings and data page")
            Component.onCompleted: ExGlobals.Variables.experimentTabButton = this
        },

        // Analysis tab
        EaElements.AppBarTabButton {
            id: analysisTabButton
            enabled: ExGlobals.Constants.proxy.phase.samplesPresent &&
                     (ExGlobals.Constants.proxy.experiment.experimentSkipped ||
                      ExGlobals.Constants.proxy.experiment.experimentLoaded)
            fontIcon: "calculator"
            text: qsTr("Analysis")
            ToolTip.text: qsTr("Simulation and fitting page")
            Component.onCompleted: ExGlobals.Variables.analysisTabButton = analysisTabButton
        },

        // Summary tab
        EaElements.AppBarTabButton {
            id: summaryTabButton
            enabled: ExGlobals.Constants.proxy.phase.samplesPresent &&
                     (ExGlobals.Constants.proxy.experiment.experimentSkipped ||
                      ExGlobals.Constants.proxy.experiment.experimentLoaded)
            fontIcon: "clipboard-list"
            text: qsTr("Summary")
            ToolTip.text: qsTr("Summary of the work done")
            Component.onCompleted: ExGlobals.Variables.summaryTabButton = summaryTabButton
        }

    ]

    /////////////////////////
    // MAIN CONTENT + SIDEBAR
    /////////////////////////

    // Pages for the tab buttons described above
    contentArea: [

        // Home page
        ExHomePage.MainContent {},

        // Project page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Constants.proxy.project.projectCreated ?
                             "" :
                             qsTr("No Project Created/Opened")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Description") },
                    EaElements.TabButton { text: qsTr("Text View") + " (CIF)" }
                ]

                items: [
                    ExProjectPage.MainContentDescription {},
                    ExProjectPage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.projectPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
                ]

                items: [
                    ExProjectPage.SideBarBasic {},
                    ExProjectPage.SideBarAdvanced {}
                ]
            }
        },

        // Sample page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Constants.proxy.phase.samplesPresent ? "" : qsTr("No Samples Added/Loaded")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Structure view") },
                    EaElements.TabButton {
                        /*
                        text: typeof ExGlobals.Constants.proxy.phase.phasesAsObj[ExGlobals.Constants.proxy.phase.currentPhaseIndex] !== 'undefined' && ExGlobals.Constants.proxy.phase.phasesAsObj.length > 0
                              ? ExGlobals.Constants.proxy.phase.phasesAsObj[ExGlobals.Constants.proxy.phase.currentPhaseIndex].name + '.cif'
                              : 'Unknown'
                              */
                        text: qsTr("Text View") + " (CIF)"
                        Component.onCompleted: ExGlobals.Variables.phaseCifTab = this
                    }
                ]

                items: [
                    ExSamplePage.MainContentStructureView {},
                    ExSamplePage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.samplePageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
                ]

                items: [
                    ExSamplePage.SideBarBasic {},
                    ExSamplePage.SideBarAdvanced {}
                ]
            }
        },

        // Experiment page
        EaComponents.ContentPage {
            defaultInfo: ExGlobals.Constants.proxy.experiment.experimentLoaded ? "" : qsTr("No Experiments Loaded")

            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Plot view") },
                    EaElements.TabButton { enabled: false; text: qsTr("Table view"); Component.onCompleted: ExGlobals.Variables.experimentTableTab = this },
                    EaElements.TabButton { enabled: false; text: qsTr("Text View") + " (CIF)"; Component.onCompleted: ExGlobals.Variables.experimentCifTab = this }
                ]

                items: [
                    ExExperimentPage.MainContentPlotView {},
                    ExExperimentPage.MainContentTableView {},
                    ExExperimentPage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.experimentPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
                ]

                items: [
                    ExExperimentPage.SideBarBasic {},
                    ExExperimentPage.SideBarAdvanced {}
                ]
            }
        },

        // Analysis page
        EaComponents.ContentPage {
            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton {
                        text: ExGlobals.Constants.proxy.experiment.experimentLoaded ? qsTr("Fitting") : qsTr("Simulation")
                    },
                    EaElements.TabButton {
                        visible: ExGlobals.Constants.proxy.experiment.experimentLoaded
                        enabled: false
                        text: 'calculations.cif' //ExGlobals.Constants.proxy.projectInfoAsJson.calculations
                        Component.onCompleted: ExGlobals.Variables.calculationCifTab = this
                    }
                ]

                items: [
                    ExAnalysisPage.MainContentFitting {},
                    ExAnalysisPage.MainContentTextView {}
                ]

                Component.onCompleted: ExGlobals.Variables.analysisPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton {
                        text: qsTr("Basic controls")
                        Component.onCompleted: ExGlobals.Variables.analysisBasicControlsTabButton = this
                    },
                    EaElements.TabButton {
                        text: qsTr("Advanced controls")
                        Component.onCompleted: ExGlobals.Variables.analysisAdvancedControlsTabButton = this
                    }
                ]

                items: [
                    ExAnalysisPage.SideBarBasic {},
                    ExAnalysisPage.SideBarAdvanced {}
                ]
            }
        },

        // Summary page
        EaComponents.ContentPage {
            mainContent: EaComponents.MainContent {
                tabs: [
                    EaElements.TabButton { text: qsTr("Report") }
                ]

                items: [
                    ExSummaryPage.MainContentReport {}
                ]

                Component.onCompleted: ExGlobals.Variables.summaryPageMainContent = this
            }

            sideBar: EaComponents.SideBar {
                tabs: [
                    EaElements.TabButton { text: qsTr("Basic controls") },
                    EaElements.TabButton { enabled: false; text: qsTr("Advanced controls") }
                ]

                items: [
                    ExSummaryPage.SideBarBasic {},
                    ExSummaryPage.SideBarAdvanced {}
                ]
            }
        }
    ]

    /////////////
    // STATUS BAR
    /////////////

    statusBar: EaElements.StatusBar {
        visible: EaGlobals.Variables.appBarCurrentIndex !== 0

        model: XmlListModel {
            xml: ExGlobals.Constants.proxy.statusModelAsXml
            query: "/root/item"

            XmlRole { name: "label"; query: "label/string()" }
            XmlRole { name: "value"; query: "value/string()" }
        }
    }

    ///////////////
    // Init dialogs
    ///////////////

    // Application dialogs (invisible at the beginning)
    ExProjectPage.ProjectDescriptionDialog {
        onAccepted: {
            ExGlobals.Constants.proxy.project.projectCreated = true
            ExGlobals.Variables.samplePageEnabled = true
        }
    }

    ExComponents.CloseDialog {
        id: closeDialog
    }

    EaElements.Dialog {
        id: resetStateDialog

        title: qsTr("Reset state")

        EaElements.Label {
            horizontalAlignment: Text.AlignHCenter
            text: qsTr("Are you sure you want to reset the application to its\noriginal state without project, phases and data?\n\nThis operation cannot be undone.")
        }

        footer: EaElements.DialogButtonBox {
            EaElements.Button {
                text: qsTr("Cancel")
                onClicked: resetStateDialog.close()
            }

            EaElements.Button {
                text: qsTr("OK")
                onClicked: {
                    EaGlobals.Variables.appBarCurrentIndex = 0
                    ExGlobals.Variables.projectPageEnabled = false
                    ExGlobals.Variables.samplePageEnabled = false
                    ExGlobals.Constants.proxy.project.resetState()
                    resetStateDialog.close()
                }
                Component.onCompleted: ExGlobals.Variables.resetStateOkButton = this
            }
        }
    }

    ///////////////////
    // Init user guides
    ///////////////////

    ExComponents.UserGuides {}

    ////////
    // Misc
    ////////

    onClosing: {
       closeDialog.visible = ExGlobals.Constants.proxy.project.stateHasChanged
       close.accepted = !ExGlobals.Constants.proxy.project.stateHasChanged
       if (close.accepted) {
           close.accepted = false
           window.quit()
       }
    }

    Component.onCompleted: {
        ExGlobals.Variables.appBarCentralTabs = appBarCentralTabs
    }

}
