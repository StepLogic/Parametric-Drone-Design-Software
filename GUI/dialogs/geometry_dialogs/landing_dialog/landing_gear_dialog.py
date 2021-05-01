from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.tabs.geometry_tabs_.landing_gear.landing_gear_tab import landing_gear_tab


class landing_gear_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.tab = landing_gear_tab()
        self.layout = QFormLayout(self)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.layout.addRow(self.tab)
        self.layout.addRow(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
