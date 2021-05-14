import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Elements 1.0 as EaElements
import easyApp.Components 1.0 as EaComponents
import easyApp.Logic 1.0 as EaLogic

import Gui.Globals 1.0 as ExGlobals

Item {

    ScrollView {
        anchors.fill: parent

        EaElements.TextArea {
            ///text: EaLogic.Utils.prettyXml(ExGlobals.Constants.proxy.fitablesListAsXml)
            //text: prettyJson(ExGlobals.Constants.proxy.fitablesDict)
            //text: prettyJson(ExGlobals.Constants.proxy.fitablesList)
        }
    }

}
