
from DPS_gui._tabs.specifications_tabs_.specification_tab import specification_tab
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class specification_dialog(QDialog):
        def __init__(self):
            super().__init__()
            specification_tab_ = specification_tab()
            self.layout = specification_tab_.create_widget()
            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            self.layout.addWidget(self.buttons)
            self.setLayout(self.layout)
            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

