from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Utils.database.geometry.control_surface_database import read_control_surface_objects


class control_surface_delete_dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.selection_ = None
        self.layout = QFormLayout(self)

        self.itemsComboBox = QComboBox()
        self.itemsComboBox.addItems(read_control_surface_objects())
        self.itemsComboBox.currentIndexChanged.connect(self.selectionChanged)
        self.layout.addRow(self.itemsComboBox)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)

    def selectionChanged(self, i):
        self.selection_ = read_control_surface_objects()[i]

    def accept_inputs(self):
        if self.selection_ is None:
            self.selection_ = read_control_surface_objects()[self.itemsComboBox.currentIndex()]
        return (self.selection_)
