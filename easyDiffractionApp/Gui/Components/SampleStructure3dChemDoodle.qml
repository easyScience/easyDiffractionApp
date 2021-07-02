import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Charts 1.0 as EaCharts

import Gui.Globals 1.0 as ExGlobals

EaCharts.BaseChemDoodle {
    cifStr: JSON.stringify(ExGlobals.Constants.proxy.phase.phasesAsExtendedCif)
}
