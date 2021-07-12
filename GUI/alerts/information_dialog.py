from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Utils.database.geometry.control_surface_database import read_control_surface_objects


class information_dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.selection_ = None
        self.layout = QFormLayout(self)

        self.layout.addRow(QLabel("Click Yes\n"
                                  +"If you have correctly modelled and enter all important parameters e.g check settings in aerodynamics and performa a simulation\n"+
                                  "If not you crash this App at your own will.Developers are not liable.\n"+
                                  "Close the console should it crash and open an issue with the developers"))
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)


