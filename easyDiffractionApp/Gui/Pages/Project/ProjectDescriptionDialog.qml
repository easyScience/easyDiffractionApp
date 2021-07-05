import QtQuick 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Components 1.0 as EaComponents

// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import Gui.Globals 1.0 as ExGlobals

EaComponents.ProjectDescriptionDialog {
    visible: EaGlobals.Variables.showProjectDescriptionDialog
    onClosed: EaGlobals.Variables.showProjectDescriptionDialog = false

    onProjectNameChanged: ExGlobals.Constants.proxy.project.editProjectInfo("name", projectName)
    onProjectShortDescriptionChanged: ExGlobals.Constants.proxy.project.editProjectInfo("short_description", projectShortDescription)
    //onProjectLocationChanged: ExGlobals.Constants.proxy.project.editProjectInfo("location", projectLocation)
    onProjectLocationChanged: ExGlobals.Constants.proxy.project.currentProjectPath = projectLocation

    onAccepted: {
        ExGlobals.Constants.proxy.project.currentProjectPath = projectLocation
        ExGlobals.Constants.proxy.project.createProject()
    }

    Component.onCompleted: {
        projectName = ExGlobals.Constants.proxy.project.projectInfoAsJson.name
        projectShortDescription = ExGlobals.Constants.proxy.project.projectInfoAsJson.short_description
        projectLocation = ExGlobals.Constants.proxy.project.currentProjectPath
    }
}


