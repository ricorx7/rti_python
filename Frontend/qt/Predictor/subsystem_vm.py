from subsystem_view import Ui_Subsystem
from PyQt5.QtWidgets import QWidget

class SubsystemVM(Ui_Subsystem, QWidget):
    """
    Subsystem settings.
    """

    def __init__(self, parent):
        Ui_Subsystem.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent