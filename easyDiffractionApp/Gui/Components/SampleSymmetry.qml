import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Row {
    spacing: EaStyle.Sizes.fontPixelSize

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Crystal system")
        }

        EaElements.ComboBox {
            id: crystalSystemSelector
            width: EaStyle.Sizes.sideBarContentWidth / 3 - EaStyle.Sizes.fontPixelSize * 2
            model: ExGlobals.Constants.proxy.phase.crystalSystemList
            currentIndex: indexOfValue(ExGlobals.Constants.proxy.phase.currentCrystalSystem)
            onActivated: ExGlobals.Constants.proxy.phase.currentCrystalSystem = currentText
        }
    }

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Space group")
        }

        EaElements.ComboBox {
            width: crystalSystemSelector.width
            model: ExGlobals.Constants.proxy.phase.formattedSpaceGroupList
            currentIndex: ExGlobals.Constants.proxy.phase.currentSpaceGroup
            onActivated: ExGlobals.Constants.proxy.phase.currentSpaceGroup = currentIndex
        }
    }

    Column {
        spacing: EaStyle.Sizes.fontPixelSize * -0.5

        EaElements.Label {
            enabled: false
            text: qsTr("Setting")
        }

        EaElements.ComboBox {
            width: crystalSystemSelector.width + EaStyle.Sizes.fontPixelSize * 4.0
            model: ExGlobals.Constants.proxy.phase.formattedSpaceGroupSettingList
            currentIndex: ExGlobals.Constants.proxy.phase.currentSpaceGroupSetting
            onActivated: ExGlobals.Constants.proxy.phase.currentSpaceGroupSetting = currentIndex
        }
    }
}
