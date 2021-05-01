from DPS_gui._tabs.perfomance_tabs_.performance_tab import performance_tab
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class performance_dialog(QDialog):
    def __init__(self):
        super().__init__()
        tab = performance_tab()
        self.layout = tab.create_widget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.setLayout(self.layout)
