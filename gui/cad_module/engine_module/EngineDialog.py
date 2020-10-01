import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database


class EngineDialog(QDialog):
    def __init__(self, parent=None):
        super(EngineDialog, self).__init__(parent)
        scroll = QScrollArea(self)
        layout = QFormLayout(self)
        self.engine_position = ""
        self.setWindowTitle("Engine Parameters")

        ##########################################################################
        ##################################################################################

        self.number_of_engines = QLabel("Number of Engines")
        self.number_of_engines_text = QLineEdit()
        layout.addRow(self.number_of_engines, self.number_of_engines_text)

        self.voltage_rating_label = QLabel("Voltage Rating")
        self.voltage_rating_text = QLineEdit()
        layout.addRow(self.voltage_rating_label, self.voltage_rating_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.current_rating_label = QLabel("Current Rating")
        self.current_rating_text = QLineEdit()
        layout.addRow(self.current_rating_label, self.current_rating_text)

        ##################################################################################

        self.engine_position_label = QLabel("Engine Position")
        self.engine_position_text = QLineEdit()

        layout.addRow(self.engine_position_label, self.engine_position_text)

        self.engine_position_x_label = QLabel("X")
        self.engine_position_x_text = QLineEdit()
        layout.addRow(self.engine_position_x_label, self.engine_position_x_text)

        self.engine_position_y_label = QLabel("Y")
        self.engine_position_y_text = QLineEdit()
        layout.addRow(self.engine_position_y_label, self.engine_position_y_text)

        self.engine_position_z_label = QLabel("Z")
        self.engine_position_z_text = QLineEdit()
        layout.addRow(self.engine_position_z_label, self.engine_position_z_text)
        ##########################################################################################

        ##############################################################################
        self.propeller_diameter_label = QLabel("Propeller Diameter")
        self.propeller_diameter_text = QLineEdit()
        layout.addRow(self.propeller_diameter_label, self.propeller_diameter_text)

        self.propeller_chord_label = QLabel("Propeller Chord")
        self.propeller_chord_text = QLineEdit()
        layout.addRow(self.propeller_chord_label, self.propeller_chord_text)

        self.cover_length_label = QLabel("Cover Length")
        self.cover_length_text = QLineEdit()
        layout.addRow(self.cover_length_label, self.cover_length_text)

        self.cover_radius_label = QLabel("Cover Radius")
        self.cover_radius_text = QLineEdit()
        layout.addRow(self.cover_radius_label, self.cover_radius_text)
        ##############################################################################
        self.maximum_thrust_label = QLabel("Maximum Thrust")
        self.maximum_thrust_text = QLineEdit()
        layout.addRow(self.maximum_thrust_label, self.maximum_thrust_text)

        self.maximum_rpm_label = QLabel("Maximum RPM")
        self.maximum_rpm_text = QLineEdit()
        layout.addRow(self.maximum_rpm_label, self.maximum_rpm_text)

        self.propeller_number_label = QLabel("Number Of Propellers(Max 3)")
        self.propeller_number_text = QLineEdit()
        layout.addRow(self.propeller_number_label, self.propeller_number_text)

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
            aicraft_specifications = Database.read_aircraft_specifications()
            voltage_rating, number_of_engines, current_rating, engine_position, propeller_diameter, propeller_chord, maximum_rpm, cover_length, cover_radius, propeller_number, engine_position_x, engine_position_y, engine_position_z, maximum_thrust = self.read_engine_values(
                values=aicraft_specifications)
            self.show_default_values(voltage_rating=voltage_rating, number_of_engines=number_of_engines
                                     , current_rating=current_rating,
                                     engine_position=engine_position, propeller_diameter=propeller_diameter,
                                     propeller_chord=propeller_chord,
                                     maximum_rpm=maximum_rpm, cover_length=cover_length,
                                     propeller_number=propeller_number,
                                     engine_position_x=engine_position_x,
                                     engine_position_y=engine_position_y,
                                     engine_position_z=engine_position_z, maximum_thrust=maximum_thrust,
                                     cover_radius=cover_radius)
        except(Exception):
            self.show_default_values()

    ############################################################################
    def show_default_values(self, voltage_rating=0, number_of_engines=0, current_rating=0,
                            engine_position=0, propeller_diameter=0, propeller_chord=0, maximum_rpm=0,
                            propeller_number=0,
                            engine_position_x=0, engine_position_y=0, engine_position_z=0, maximum_thrust=0,
                            cover_length=0, cover_radius=0):

        self.number_of_engines_text.setText(str(number_of_engines))
        self.voltage_rating_text.setText(str(voltage_rating))
        self.current_rating_text.setText(str(current_rating))
        self.engine_position_text.setText(str(engine_position))
        self.propeller_diameter_text.setText(str(propeller_diameter))
        self.maximum_rpm_text.setText(str(maximum_rpm))
        self.maximum_thrust_text.setText(str(maximum_thrust))
        self.propeller_chord_text.setText(str(propeller_chord))
        self.cover_length_text.setText(str(cover_length))
        self.cover_radius_text.setText(str(cover_radius))
        self.propeller_number_text.setText(str(propeller_number))
        self.engine_position_x_text.setText(str(engine_position_x))
        self.engine_position_x_text.setText(str(engine_position_x))
        self.engine_position_y_text.setText(str(engine_position_y))
        self.engine_position_z_text.setText(str(engine_position_z))

    def read_engine_values(self, values={}):
        number_of_engines = values.get("number_of_engines")
        voltage_rating = values.get("voltage_rating")
        current_rating = values.get("current_rating")
        engine_position = values.get("engine_position")
        propeller_chord = values.get("propeller_chord")
        propeller_diameter = values.get("propeller_diameter")
        cover_length = values.get("cover_length")
        cover_radius = values.get("cover_radius")
        maximum_thrust = values.get("maximum_thrust")
        maximum_rpm = values.get("maximum_rpm")
        propeller_number = values.get("propeller_number")
        engine_position_x = values.get("engine_position_x")
        engine_position_y = values.get("engine_position_y")
        engine_position_z = values.get("engine_position_z")

        return voltage_rating, number_of_engines, current_rating, engine_position, propeller_diameter, propeller_chord, maximum_rpm, cover_length, cover_radius, propeller_number, engine_position_x, engine_position_y, engine_position_z, maximum_thrust


    def init_action(self):
        self.engine_position = self.engine_position_text.text()
        if (self.engine_position_text.text() == "w" and int(self.number_of_engines_text.text()) >= 2):
            self.parameters = {
                "engine": {
                    "engine_position": self.engine_position,
                    "number_of_engines": int(self.number_of_engines_text.text()),
                    "voltage_rating": float(self.voltage_rating_text.text()),
                    "current_rating": float(self.current_rating_text.text()),
                    "maximum_rpm": float(self.maximum_rpm_text.text()),
                    "maximum_thrust": float(self.maximum_thrust_text.text()),
                    "propeller_diameter": float(self.propeller_diameter_text.text()),
                    "propeller_chord": float(self.propeller_chord_text.text()),
                    "cover_length": float(self.cover_length_text.text()),
                    "cover_radius": float(self.cover_radius_text.text()),
                    "engine_position_x": float(self.engine_position_x_text.text()),
                    "engine_position_y": float(self.engine_position_y_text.text()),
                    "engine_position_z": float(self.engine_position_z_text.text()),
                    "propeller_number": int(self.propeller_number_text.text())
                }
            }
            try:
                Database.update_aircraft_specifications(key="engine", value=self.parameters["engine"])
            except:
                Database.write_aircraft_specification(self.parameters)
            return self.parameters
        elif self.engine_position_text.text() == "n" and int(self.number_of_engines_text.text()) == 1:
            self.parameters = {
                "engine": {
                    "engine_position": self.engine_position,
                    "number_of_engines": int(self.number_of_engines_text.text()),
                    "voltage_rating": float(self.voltage_rating_text.text()),
                    "current_rating": float(self.current_rating_text.text()),
                    "maximum_rpm": float(self.maximum_rpm_text.text()),
                    "maximum_thrust": float(self.maximum_thrust_text.text()),
                    "propeller_diameter": float(self.propeller_diameter_text.text()),
                    "propeller_chord": float(self.propeller_chord_text.text()),
                    "cover_length": float(self.cover_length_text.text()),
                    "cover_radius": float(self.cover_radius_text.text()),
                    "engine_position_x": float(self.engine_position_x_text.text()),
                    "engine_position_y": float(self.engine_position_y_text.text()),
                    "engine_position_z": float(self.engine_position_z_text.text()),
                    "propeller_number": int(self.propeller_number_text.text())
                }
            }
            try:
                Database.update_aircraft_specifications(key="engine", value=self.parameters["engine"])
            except:
                Database.write_aircraft_specification(self.parameters)
            return self.parameters
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)

    @staticmethod
    def get_params(parent=None):
        dialog = EngineDialog(parent)
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
