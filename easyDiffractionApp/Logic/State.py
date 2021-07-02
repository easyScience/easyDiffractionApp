# noqa: E501
from dicttoxml import dicttoxml

from PySide2.QtCore import Signal, QObject

from easyCore import np


class StateLogic(QObject):
    """
    """
    def __init__(self, parent=None, interface=None):
        super().__init__(parent)
        self.parent = parent
        self._interface = interface
        self._interface_name = interface.current_interface_name

        self._parameters = None
        self._instrument_parameters = None
        self._status_model = None
        self._state_changed = False

    ####################################################################################################################
    ####################################################################################################################
    # STATUS
    ####################################################################################################################
    ####################################################################################################################

    def statusModelAsObj(self, current_engine, current_minimizer):
        obj = {
            "calculation":  self._interface.current_interface_name,
            "minimization": f'{current_engine} ({current_minimizer})'  # noqa: E501
        }
        self._status_model = obj
        return obj

    def statusModelAsXml(self, current_engine, current_minimizer):
        model = [
            {"label": "Calculation", "value": self._interface.current_interface_name},  # noqa: E501
            {"label": "Minimization",
             "value": f'{current_engine} ({current_minimizer})'}  # noqa: E501
        ]
        xml = dicttoxml(model, attr_type=False)
        xml = xml.decode()
        return xml

