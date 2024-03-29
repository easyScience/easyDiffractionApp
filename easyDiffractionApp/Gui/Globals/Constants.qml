// SPDX-FileCopyrightText: 2023 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021-2022 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

pragma Singleton

import QtQuick 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import Gui.Logic 1.0 as ExLogic

QtObject {
    readonly property var proxy: typeof _pyQmlProxyObj !== "undefined" && _pyQmlProxyObj !== null ? _pyQmlProxyObj : new ExLogic.PyQmlProxy.PyQmlProxy()
    readonly property bool remote: typeof EaGlobals.Variables.projectConfig.ci.app.info !== 'undefined'

    readonly property string appName: EaGlobals.Variables.projectConfig.release.app_name
    readonly property string appPrefixName: "Easy"
    readonly property string appSuffixName: appName.replace(appPrefixName, "")
    readonly property string appPrefixNameLogo: appPrefixName.toLowerCase()
    readonly property string appSuffixNameLogo: appSuffixName.toLowerCase()

    readonly property string appLogo: logo('App.svg')
    readonly property string appUrl: EaGlobals.Variables.projectConfig.tool.poetry.homepage

    readonly property string appVersion: EaGlobals.Variables.projectConfig.tool.poetry.version
    readonly property string appDate: remote ?
                                          EaGlobals.Variables.projectConfig.ci.app.info.build_date :
                                          new Date().toISOString().slice(0,10)

    readonly property string commit: remote ?
                                         EaGlobals.Variables.projectConfig.ci.app.info.commit_sha_short :
                                         ''
    readonly property string commitUrl: remote ?
                                            EaGlobals.Variables.projectConfig.ci.app.info.commit_url :
                                            ''

    readonly property string branch: remote ?
                                         EaGlobals.Variables.projectConfig.ci.app.info.branch_name
                                       : ''
    readonly property string branchUrl: remote ?
                                            EaGlobals.Variables.projectConfig.ci.app.info.branch_url :
                                            ''

    readonly property string eulaUrl: githubRawContent(branch, 'LICENSE.md')
    readonly property string oslUrl: githubRawContent(branch, 'DEPENDENCIES.md')

    readonly property string description:
`${appName} is a scientific software for
modelling and analysis of neutron diffraction data.

${appName} is built by ESS DMSC in
Copenhagen, Denmark.`

    readonly property string essLogo: logo('ESSlogo.png')

    // Logic

    function logo(file) {
        return Qt.resolvedUrl(`../Resources/Logo/${file}`)
    }

    function githubRawContent(branch, file) {
        return `https://raw.githubusercontent.com/easyScience/easyDiffractionApp/${branch}/${file}`
    }
}
