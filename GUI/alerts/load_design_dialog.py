from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Utils.database.database import read_saved_designs
from Utils.database.geometry.boom_database import read_boom_objects
from Utils.database.settings.workfile_database import read_designs


class load_design_dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.selection_= None
        self.layout = QFormLayout(self)
        self.itemsComboBox = QComboBox()
        self.itemsComboBox.addItems(read_designs())
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
        self.selection_ = read_designs()[i]

    def accept_inputs(self):
        if self.selection_ is None:
            self.selection_ = read_designs()[self.itemsComboBox.currentIndex()]
        return (self.selection_)