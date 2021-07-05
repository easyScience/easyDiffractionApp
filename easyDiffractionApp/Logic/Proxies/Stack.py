# SPDX-FileCopyrightText: 2021 easyDiffraction contributors <support@easydiffraction.org>
# SPDX-License-Identifier: BSD-3-Clause
# © 2021 Contributors to the easyDiffraction project <https://github.com/easyScience/easyDiffractionApp>

from PySide2.QtCore import QObject, Property, Signal, Slot


class StackProxy(QObject):

    undoRedoChanged = Signal()
    dummySignal = Signal()

    def __init__(self, parent, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_stack
        self.logic.undoRedoChanged.connect(self.undoRedoChanged)

    @Property(bool, notify=undoRedoChanged)
    def canUndo(self) -> bool:
        return self.logic.canUndo()

    @Property(bool, notify=undoRedoChanged)
    def canRedo(self) -> bool:
        return self.logic.canRedo()

    @Slot()
    def undo(self):
        self.logic.undo()

    @Slot()
    def redo(self):
        self.logic.redo()

    @Property(str, notify=undoRedoChanged)
    def undoText(self):
        return self.logic.undoText()

    @Property(str, notify=undoRedoChanged)
    def redoText(self):
        return self.logic.redoText()

    @Slot()
    def resetUndoRedoStack(self):
        self.logic.resetUndoRedoStack()
        self.undoRedoChanged.emit()
