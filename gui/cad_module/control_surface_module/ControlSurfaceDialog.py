import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database


class ControlSurfaceDialog(QDialog):
    def __init__(self, parent=None,part=""):
        super(ControlSurfaceDialog, self).__init__(parent)
        self.part = part
        layout = QFormLayout(self)
        self.setWindowTitle("Control Surface Info")

        ##########################################################################
        ##################################################################################

        ##########################################################################
        ##################################################################################
        self.span_label = QLabel("Span")
        self.span_text = QLineEdit()
        layout.addRow(self.span_label, self.span_text)

        ##################################################################################
        ##############################################################################
        self.chord_length_label = QLabel("Chord Length")
        self.chord_length_text = QLineEdit()
        layout.addRow(self.chord_length_label, self.chord_length_text)




        self.Wing_postion_tlabel = QLabel("Position")
        layout.addWidget(self.Wing_postion_tlabel)

        self.Wing_postion_x_label = QLabel("X")
        self.vtp_position_x_text = QLineEdit()
        layout.addRow(self.Wing_postion_x_label, self.vtp_position_x_text)

        self.Wing_postion_y_label = QLabel("Y")
        self.vtp_position_y_text = QLineEdit()
        layout.addRow(self.Wing_postion_y_label, self.vtp_position_y_text)

        self.Wing_postion_z_label = QLabel("Z")
        self.Wing_postion_z_text = QLineEdit()
        layout.addRow(self.Wing_postion_z_label, self.Wing_postion_z_text)

        self.toolbox_ = QHBoxLayout()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)

        try:
            aicraft_specifications = Database.read_aircraft_specifications()
            root_location_x, root_location_y, root_location_z, span, chord = self.read_vals(
                part=self.part, values=aicraft_specifications)
            print(aicraft_specifications)
            self.show_default_values(root_location_x, root_location_y, root_location_z,
                                     span, chord)
        except(Exception):
            self.show_default_values()

        self.setLayout(layout)

    ############################################################################
    def show_default_values(self, root_location_x=0, root_location_y=0, root_location_z=0, span=0, chord=0):
        self.span_text.setText(str(span))

        self.chord_length_text.setText(str(chord))

        self.vtp_position_x_text.setText(str(root_location_x))

        self.vtp_position_y_text.setText(str(root_location_y))

        self.Wing_postion_z_text.setText(str(root_location_z))

    def read_vals(self, part="", values=None):
        if values is None:
            values = {}
        root_location_x = values.get(part + "_root_position_x")
        root_location_y = values.get(part + "_root_position_y")
        root_location_z = values.get(part + "_root_position_z")
        chord = values.get(part + "_chord")
        span = values.get(part + "_span")
        return root_location_x, root_location_y, root_location_z, span,chord

    def init_action(self):
        self.parameters = {
            self.part: {
                self.part+"_root_position_x": float(self.vtp_position_x_text.text()),
                self.part+"_root_position_y": float(self.vtp_position_y_text.text()),
                self.part+"_root_position_z": float(self.Wing_postion_z_text.text()),
                self.part + "_span": float(self.span_text.text()),
                self.part+"_chord": float(self.chord_length_text.text()),
            }}
        try:
            Database.update_aircraft_specifications(key=self.part, value=self.parameters[self.part])
        except:
            Database.write_aircraft_specification(self.parameters)
        return self.parameters

    @staticmethod
    def get_params(parent=None,part=""):
        dialog = ControlSurfaceDialog(parent,part=part)
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
