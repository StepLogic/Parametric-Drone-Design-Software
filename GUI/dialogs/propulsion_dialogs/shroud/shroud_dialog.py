from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.tabs.propulsion_tab.shroud_tab import shroud_tab


class shroud_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.tab=shroud_tab()
        self.layout =self.tab.create_widget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.layout.addRow(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.setLayout(self.layout)
