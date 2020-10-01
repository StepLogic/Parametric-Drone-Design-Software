from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database




class StructureDialog(QDialog):
    def __init__(self, parent=None, part="wing", rib_number=3, spar_number=3):
        super(StructureDialog, self).__init__(parent)
        scroll = QScrollArea(self)
        layout = QFormLayout(self)
        self.setWindowTitle("Structure Info")
        self.part = part
        ##########################################################################
        ##################################################################################

        self.rib_number_label = QLabel("Rib Number=   {}".format(rib_number))
        layout.addRow(self.rib_number_label)

        self.rib_mass_label = QLabel("Rib Mass[({}-{})grams])".format(0.3, 0.4))
        self.rib_mass_text = QLineEdit()
        layout.addRow(self.rib_mass_label, self.rib_mass_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.spar_mass_label = QLabel("Spar Mass[({}-{})grams])".format(0.3, 0.4))
        self.spar_mass_text = QLineEdit()
        layout.addRow(self.spar_mass_label, self.spar_mass_text)

        ##################################################################################

        ##############################################################################
        self.spar_number_label = QLabel("Spar Number=     {}".format(spar_number))
        layout.addRow(self.spar_number_label)

        self.spar_1_position_x_label = QLabel("Spar_1_position(X)")
        self.spar_1_position_text = QLineEdit()
        layout.addRow(self.spar_1_position_x_label, self.spar_1_position_text)

        self.spar_2_position_x_label = QLabel("Spar_2_position(X)")
        self.spar_2_position_text = QLineEdit()
        layout.addRow(self.spar_2_position_x_label, self.spar_2_position_text)

        self.spar_3_position_x_label = QLabel("Spar_2_position(X)")
        self.spar_3_position_text = QLineEdit()
        layout.addRow(self.spar_3_position_x_label, self.spar_3_position_text)

        ##########################################################################################

        self.toolbox_ = QHBoxLayout()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget = QWidget(self)
        widget.setLayout(layout)
        scroll.setWidget(widget)
        temp_layout = QVBoxLayout(self)
        temp_layout.addWidget(scroll)
        self.setLayout(temp_layout)
        try:
            structure_specifications = Database.read_structures_specifications()
            spar_mass, rib_mass, spar_1_position, spar_2_position, spar_3_position= self.read_values(
                values=structure_specifications)

            self.show_default_values(spar_mass, rib_mass, spar_1_position, spar_2_position, spar_3_position)
        except(Exception):
            self.show_default_values()

    ############################################################################
    def show_default_values(self, rib_mass=0, spar_mass=0,
                            spar_1_position=0, spar_2_position=0,
                            spar_3_position=0):

        self.rib_mass_text.setText(str(rib_mass))
        self.spar_mass_text.setText(str(spar_mass))
        self.spar_1_position_text.setText(str(spar_1_position))
        self.spar_2_position_text.setText(str(spar_2_position))
        self.spar_3_position_text.setText(str(spar_3_position))

    def read_values(self, values={}):
        rib_mass = values[self.part + "_structure"]["rib_mass"]
        spar_mass = values[self.part + "_structure"]["spar_mass"]
        spar_1_position = values[self.part + "_structure"]["spar_1_position"]
        spar_2_position = values[self.part + "_structure"]["spar_2_position"]
        spar_3_position = values[self.part + "_structure"]["spar_3_position"]

        return spar_mass, rib_mass, spar_1_position, spar_2_position, spar_3_position

    def init_action(self):
        self.parameters = {
            self.part + "_structure": {
                "rib_mass": float(self.rib_mass_text.text()),
                "spar_mass": float(self.spar_mass_text.text()),
                "spar_1_position": float(self.spar_1_position_text.text()),
                "spar_2_position": float(self.spar_2_position_text.text()),
                "spar_3_position": float(self.spar_3_position_text.text()),

            }}
        try:
            Database.update_structure_specifications(key=self.part + "_structure", value=self.parameters[self.part + "_structure"])
        except:
            Database.update_structure_specifications(key="", value=self.parameters)
        return self.parameters


    @staticmethod
    def get_params(parent=None, part=""):
        dialog = StructureDialog(parent, part)
        result = dialog.exec_()
        if (result == 1):
            try:
                params = dialog.init_action()
                return (params, QDialog.Accepted)
            except(Exception):
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Critical)
                dialog.setText("Incorrect or No Values Entered")
                dialog.addButton(QMessageBox.Ok)
                dialog.exec()
                return ([], QDialog.Rejected)
        else:
            return ([], QDialog.Rejected)
