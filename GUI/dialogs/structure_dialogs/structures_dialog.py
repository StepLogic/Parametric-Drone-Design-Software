from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.tabs.structures.structures_tab import structures_tab


class structures_dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.layout =QFormLayout()
        self.tab=structures_tab()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.layout.addWidget(self.tab)
        self.layout.addWidget(self.buttons)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.setLayout(self.layout)
