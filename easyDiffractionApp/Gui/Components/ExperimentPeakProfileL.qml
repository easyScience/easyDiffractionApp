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
    id: tableView

    width: EaStyle.Sizes.sideBarContentWidth * 2 / 5 - EaStyle.Sizes.fontPixelSize / 2

    // Table model

    model: XmlListModel {
        xml: ExGlobals.Constants.proxy.parameters.instrumentParametersAsXml
        query: `/root/item`

        XmlRole { name: "x"; query: "resolution_x/value/number()" }
        XmlRole { name: "y"; query: "resolution_y/value/number()" }

        XmlRole { name: "xId"; query: "resolution_x/key[4]/string()" }
        XmlRole { name: "yId"; query: "resolution_y/key[4]/string()" }
    }

    // Table rows

    delegate: EaComponents.TableViewDelegate {

        EaComponents.TableViewTextInput {
            width: tableView.width / contentRowData.length
            headerText: "X"
            text: EaLogic.Utils.toFixed(model.x)
            onEditingFinished: editParameterValue(model.xId, text)
        }

        EaComponents.TableViewTextInput {
            width: tableView.width / contentRowData.length
            headerText: "Y"
            text: EaLogic.Utils.toFixed(model.y)
            onEditingFinished: editParameterValue(model.yId, text)
        }

    }

    // Logic

    function editParameterValue(id, value) {
        ExGlobals.Constants.proxy.parameters.editParameter(id, parseFloat(value))
    }

}
