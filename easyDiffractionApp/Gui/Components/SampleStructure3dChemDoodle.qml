// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseChemDoodle {
    cifStr: JSON.stringify(ExGlobals.Constants.proxy.phase.phasesAsExtendedCif)
}
