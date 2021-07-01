from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.tabs.aerodynamic_tabs_.aerodynamic_settings_tab import aerodynamic_settings_tab


class settings_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.tab = aerodynamic_settings_tab()
        self.layout = QFormLayout(self)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.layout.addRow(self.tab)
        self.layout.addRow(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
