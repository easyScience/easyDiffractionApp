__author__ = 'github.com/AndrewSazonov'
__version__ = '0.0.1'

from PySide2.QtCore import QObject, Property, Signal, Slot


class BackgroundProxy(QObject):

    asXmlChanged = Signal()
    dummySignal = Signal()

    def __init__(self, parent, logic=None):
        super().__init__(parent)
        self.parent = parent
        self.logic = logic.l_background
        self.logic.asXmlChanged.connect(self.asXmlChanged)

    @Property('QVariant', notify=dummySignal)
    def asObj(self):
        return self.logic._background_as_obj

    @Property(str, notify=asXmlChanged)
    def asXml(self):
        return self.logic._background_as_xml

    @Slot()
    def setDefaultPoints(self):
        self.logic.setDefaultPoints()

    @Slot()
    def addPoint(self):
        self.logic.addPoint()

    @Slot(str)
    def removePoint(self, point_name: str):
        self.logic.removePoint(point_name)
