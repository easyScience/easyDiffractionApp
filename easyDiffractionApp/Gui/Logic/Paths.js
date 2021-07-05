// SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
// SPDX-License-Identifier: BSD-3-Clause
// © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

function component(fileName)
{
    const dirPath = Qt.resolvedUrl("../Components")
    //const dirPath = "../../Components"
    const filePath = dirPath + "/" + fileName
    return filePath
}
