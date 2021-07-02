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
    //id: phasesTable

    defaultInfoText: qsTr("No Associated Phases")

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.phase.phasesAsXml
        query: "/root/item"

        XmlRole { name: "label"; query: "name/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewLabel {
            id: numColumn
            width: EaStyle.Sizes.fontPixelSize * 2.5
            headerText: "No."
            text: model.index + 1
        }

        EaComponents.TableViewLabel {
        //EaComponents.TableViewTextInput {
            horizontalAlignment: Text.AlignLeft
            width: EaStyle.Sizes.sideBarContentWidth
                   - numColumn.width
                   - scaleColumn.width
                   - useColumn.width
                   - deleteRowColumn.width
                   - EaStyle.Sizes.tableColumnSpacing * 4
                   - EaStyle.Sizes.borderThickness * 2
            headerText: "Label"
            text: model.label
        }

        EaComponents.TableViewTextInput {
            id: scaleColumn
            headerText: "Scale"
            text: EaLogic.Utils.toFixed(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.scale.value)
            onEditingFinished: editParameterValue(ExGlobals.Constants.proxy.parameters.patternParametersAsObj.scale["@id"], text)
        }

        EaComponents.TableViewCheckBox {
            id: useColumn
            enabled: false
            width: EaStyle.Sizes.fontPixelSize * 4
            headerText: "Use"
            checked: true
        }

        EaComponents.TableViewButton {
            id: deleteRowColumn
            enabled: false
            headerText: "Del."
            fontIcon: "minus-circle"
            ToolTip.text: qsTr("Remove this phase")
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }
}
