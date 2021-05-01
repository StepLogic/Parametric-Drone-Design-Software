from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.tabs.propulsion_tab.propulsion_tab import propulsion_tab


class propulsion_dialog(QDialog):
    def __init__(self):
        super().__init__()
        tab = propulsion_tab()
        self.layout = tab.create_widget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.setLayout(self.layout)
