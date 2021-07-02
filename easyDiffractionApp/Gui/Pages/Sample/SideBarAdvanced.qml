import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements
import easyApp.Gui.Components 1.0 as EaComponents

import Gui.Globals 1.0 as ExGlobals

EaComponents.SideBarColumn {

    /*
    EaElements.GroupBox {
        title: qsTr("Bonds")
        enabled: ExGlobals.Constants.proxy.phase.samplesPresent

        Row {
            spacing: EaStyle.Sizes.fontPixelSize

            // Show bonds
            EaElements.CheckBox {
                text: qsTr("Show bonds")
                onCheckedChanged: ExGlobals.Constants.proxy.plotting3d.showBonds = checked
                Component.onCompleted: checked = ExGlobals.Constants.proxy.plotting3d.showBonds
            }

            // Spacer
            EaElements.Label {
                width: EaStyle.Sizes.fontPixelSize * 2.5
            }

            // Min distance
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                text: qsTr("Min distance:")
            }
            EaElements.Parameter {
                enabled: false
                anchors.verticalCenter: parent.verticalCenter
                width: 75
                Component.onCompleted: text = 0
            }

            // Spacer
            EaElements.Label {
                width: EaStyle.Sizes.fontPixelSize * 3.0
            }

            // Max distance
            EaComponents.TableViewLabel{
                horizontalAlignment: Text.AlignRight
                text: qsTr("Max distance:")
            }
            EaElements.Parameter {
                anchors.verticalCenter: parent.verticalCenter
                width: 75
                onEditingFinished: ExGlobals.Constants.proxy.plotting3d.bondsMaxDistance = text
                Component.onCompleted: text = ExGlobals.Constants.proxy.plotting3d.bondsMaxDistance
            }

        }

    }
    */

}
