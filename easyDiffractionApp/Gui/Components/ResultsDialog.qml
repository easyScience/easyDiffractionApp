import QtQuick 2.13
import QtQuick.Controls 2.13

import easyApp.Gui.Globals 1.0 as EaGlobals
import easyApp.Gui.Style 1.0 as EaStyle
import easyApp.Gui.Elements 1.0 as EaElements

import Gui.Globals 1.0 as ExGlobals

EaElements.Dialog {
    id: dialog

    property bool gotResults: typeof ExGlobals.Constants.proxy.fitting.fitResults.nvarys !== 'undefined' &&
                              ExGlobals.Constants.proxy.fitting.isFitFinished

    title: qsTr("Refinement Results")

    standardButtons: Dialog.Ok

    Component.onCompleted: setPreferencesOkButton()

    Column {
        EaElements.Label {
            text: gotResults
                  ? `Success: ${ExGlobals.Constants.proxy.fitting.fitResults.success}`
                  : `Fitting cancelled`
        }

        EaElements.Label {
            enabled: gotResults
            text: gotResults
                  ? `Num. refined parameters: ${ExGlobals.Constants.proxy.fitting.fitResults.nvarys}`
                  : ""
        }

        EaElements.Label {
            enabled: gotResults
            text: gotResults
                  ? `Goodness-of-fit (reduced \u03c7\u00b2): ${ExGlobals.Constants.proxy.fitting.fitResults.redchi2.toFixed(2)}`
                  : ""
        }
    }

    // Logic

    function setPreferencesOkButton() {
        const buttons = dialog.footer.contentModel.children
        for (let i in buttons) {
            const button = buttons[i]
            if (button.text === 'OK') {
                ExGlobals.Variables.refinementResultsOkButton = button
                return
            }
        }
    }
}

