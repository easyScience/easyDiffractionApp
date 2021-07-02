from PySide2.QtCore import Signal, QObject

from easyCore import borg
from easyCore.Objects.Groups import BaseCollection
from easyCore.Objects.Base import BaseObj
from easyDiffractionLib import Phases, Phase


class StackLogic(QObject):
    """
    Logic for Undo/Redo stack-related operations.
    """
    undoRedoChanged = Signal()

    def __init__(self, parent, proxy,
                 callbacks_no_history=None,
                 callbacks_with_history=None):
        super().__init__(parent)
        self.parent = parent
        self.proxy = proxy
        self.callbacks_no_history = callbacks_no_history
        self.callbacks_with_history = callbacks_with_history

    def initializeBorg(self):
        # Start the undo/redo stack
        borg.stack.enabled = True
        borg.stack.clear()

    def canUndo(self) -> bool:
        return borg.stack.canUndo()

    def canRedo(self) -> bool:
        return borg.stack.canRedo()

    def callbacks(self, frame=None):
        """
        """
        callback = self.callbacks_no_history
        if len(frame) > 1:
            callback = self.callbacks_with_history
        else:
            element = frame.current._parent
            if isinstance(element, (BaseObj, BaseCollection)):
                if isinstance(element, (Phase, Phases)):
                    callback = self.callbacks_with_history
                else:
                    callback = self.callbacks_no_history
            elif element is self.proxy:
                # This is a property of the proxy.
                # I.e. minimizer, minimizer method, name or something boring.
                # Signals should be sent by triggering the set method.
                callback = []
            else:
                print(f'Unknown undo thing: {element}')
        return callback

    def undo(self):
        if self.canUndo:
            callback = self.callbacks(borg.stack.history[0])
            borg.stack.undo()
            _ = [call.emit() for call in callback]

    def redo(self):
        if self.canRedo:
            callback = self.callbacks(borg.stack.future[0])
            borg.stack.redo()
            _ = [call.emit() for call in callback]

    def undoText(self):
        return borg.stack.undoText()

    def redoText(self):
        return borg.stack.redoText()

    def resetUndoRedoStack(self):
        if borg.stack.enabled:
            borg.stack.clear()
