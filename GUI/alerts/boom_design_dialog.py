from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Utils.data_objects.boom_placeholders import boom_objects_list
from Utils.data_objects.placeholder import design_types


class boom_design_dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.boom_type_= None
        self.design_type_=None
        self.layout = QFormLayout(self)
        self.lineText=QLineEdit()
        self.typeComboBox = QComboBox()
        self.typeComboBox.addItems(boom_objects_list)
        self.typeComboBox.currentIndexChanged.connect(self.selectionChanged)
        self.designComboBox = QComboBox()
        self.designComboBox.addItems(design_types)
        self.designComboBox.currentIndexChanged.connect(self.selectionChanged2)
        self.layout.addRow(self.typeComboBox)
        self.layout.addRow(self.designComboBox)
        self.layout.addRow(self.lineText)
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)

    def selectionChanged(self, i):
        self.boom_type_ = boom_objects_list[i]
    def selectionChanged2(self, i):
        self.design_type_ = design_types[i]

    def accept_inputs(self):
        if self.design_type_ is None:
            self.design_type_ = design_types[self.designComboBox.currentIndex()]
        if self.boom_type_ is None:
            self.boom_type_ = boom_objects_list[self.typeComboBox.currentIndex()]

        return self.lineText.text(), self.boom_type_, self.design_type_