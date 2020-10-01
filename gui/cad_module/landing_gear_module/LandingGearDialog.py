from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database


class LandingGearDialog(QDialog):
    def __init__(self, parent=None):
        super(LandingGearDialog, self).__init__(parent)
        scroll = QScrollArea(self)
        layout = QFormLayout(self)

        self.setWindowTitle("Landing Gear Configuration")
        ##########################################################################
        ##################################################################################

        self.landing_gear_type_label = QLabel("Configuration(c or t)")
        self.landing_gear_type = QLineEdit()
        layout.addRow(self.landing_gear_type_label, self.landing_gear_type)
        self.struct_length_main_gear_label = QLabel("Main Gear Struct Length")
        self.struct_length_main_gear = QLineEdit()
        layout.addRow(self.struct_length_main_gear_label, self.struct_length_main_gear)

        self.struct_length_aux_label= QLabel("Aux Gear Struct Length")
        self.struct_length_aux = QLineEdit()
        layout.addRow(self.struct_length_aux_label, self.struct_length_aux)

        self.aux_gear_position_label = QLabel("Auxilliary Gear Position")
        layout.addWidget(self.aux_gear_position_label)
        self.aux_gear_position_x_label = QLabel("X")
        self.aux_gear_position_x_text = QLineEdit()
        layout.addRow(self.aux_gear_position_x_label, self.aux_gear_position_x_text)

        self.aux_gear_position_y_label = QLabel("Y")
        self.aux_gear_position_y_text = QLineEdit()
        layout.addRow(self.aux_gear_position_y_label, self.aux_gear_position_y_text)

        self.aux_gear_position_z_label = QLabel("Z")
        self.aux_gear_position_z_text = QLineEdit()
        layout.addRow(self.aux_gear_position_z_label, self.aux_gear_position_z_text)

        self.rol_gear_position_label = QLabel(" Right And Left Gear Position")
        layout.addWidget(self.rol_gear_position_label)
        self.rol_gear_position_x_label = QLabel("X")
        self.rol_gear_position_x_text = QLineEdit()
        layout.addRow(self.rol_gear_position_x_label, self.rol_gear_position_x_text)

        self.rol_gear_position_y_label = QLabel("Y")
        self.rol_gear_position_y_text = QLineEdit()
        layout.addRow(self.rol_gear_position_y_label, self.rol_gear_position_y_text)

        self.rol_gear_position_z_label = QLabel("Z")
        self.rol_gear_position_z_text = QLineEdit()
        layout.addRow(self.rol_gear_position_z_label, self.rol_gear_position_z_text)

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
        aicraft_specifications = Database.read_aircraft_specifications()
        landing_gear_type, struct_length_main_gear,struct_length_aux, aux_gear_position_x, aux_gear_position_y, aux_gear_position_z, rol_gear_position_x, rol_gear_position_y, rol_gear_position_z = self.read_landing_gear_values(
            values=aicraft_specifications)
        self.show_default_values(landing_gear_type, struct_length_main_gear,struct_length_aux, aux_gear_position_x, aux_gear_position_y,
                                 aux_gear_position_z, rol_gear_position_x, rol_gear_position_y, rol_gear_position_z)

    ############################################################################
    def show_default_values(self, landing_gear_type=0, struct_length_main_gear=0,struct_length_aux=0, aux_gear_position_x=0,
                            aux_gear_position_y=0, aux_gear_position_z=0, rol_gear_position_x=0,
                            rol_gear_position_y=0, rol_gear_position_z=0):
        self.landing_gear_type.setText(str(landing_gear_type))
        self.struct_length_main_gear.setText(str(struct_length_main_gear))
        self.struct_length_aux.setText(str(struct_length_aux))
        self.aux_gear_position_x_text.setText(str(aux_gear_position_x))
        self.aux_gear_position_y_text.setText(str(aux_gear_position_y))
        self.aux_gear_position_z_text.setText(str(aux_gear_position_z))
        self.rol_gear_position_x_text.setText(str(rol_gear_position_x))
        self.rol_gear_position_y_text.setText(str(rol_gear_position_y))
        self.rol_gear_position_z_text.setText(str(rol_gear_position_z))


    def read_landing_gear_values(self, values={}):
        landing_gear_type = values.get("landing_gear_type")
        struct_length_main_gear = values.get("struct_length_main_gear")
        struct_length_aux= values.get("struct_length_aux")
        aux_gear_position_x = values.get("aux_gear_position_x")
        aux_gear_position_y = values.get("aux_gear_position_y")
        aux_gear_position_z = values.get("aux_gear_position_z")
        rol_gear_position_x = values.get("rol_gear_position_x")
        rol_gear_position_y = values.get("rol_gear_position_y")
        rol_gear_position_z = values.get("rol_gear_position_z")
        return landing_gear_type, struct_length_main_gear,struct_length_aux, aux_gear_position_x, aux_gear_position_y, aux_gear_position_z, rol_gear_position_x, rol_gear_position_y, rol_gear_position_z

    def init_action(self):
        if (self.landing_gear_type.text() == "c" or self.landing_gear_type.text() == "t"):
            self.parameters = {
                "landing_gear": {
                    "landing_gear_type": self.landing_gear_type.text(),
                    "struct_length_main_gear": float(self.struct_length_main_gear.text()),
                    "struct_length_aux": float(self.struct_length_aux.text()),
                    "aux_gear_position_x": float(self.aux_gear_position_x_text.text()),
                    "aux_gear_position_y": float(self.aux_gear_position_y_text.text()),
                    "aux_gear_position_z": float(self.aux_gear_position_z_text.text()),
                    "rol_gear_position_x":float( self.rol_gear_position_x_text.text()),
                    "rol_gear_position_y": float(self.rol_gear_position_y_text.text()),
                    "rol_gear_position_z": float(self.rol_gear_position_z_text.text())
                }}
            try:
                Database.update_aircraft_specifications(key="landing_gear", value=self.parameters["landing_gear"])
            except:
                Database.write_aircraft_specification(self.parameters)
            return self.parameters
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)


    @staticmethod
    def get_params(parent=None):
        dialog = LandingGearDialog(parent)
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
