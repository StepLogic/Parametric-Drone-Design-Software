from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database


class WeightDialog(QDialog):
    def __init__(self,params,parent=None):
        super(WeightDialog, self).__init__(parent)
        layout = QFormLayout(self)
        vlayout = QVBoxLayout()
        scroll = QScrollArea(self)
        self.setWindowTitle("Weight Specification")
        self.toolbox_ = QHBoxLayout()
        self.frame = QFrame()
        vlayout = QVBoxLayout()
        self.params=params
        ##########################################################################
        ##################################################################################

        self.mass_of_battery_label = QLabel("Mass Of Battery")
        self.mass_of_battery_text = QLineEdit()
        layout.addRow(self.mass_of_battery_label, self.mass_of_battery_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.power_plant_weight_label = QLabel("Mass of Powerplant")
        self.power_plant_weight_text = QLineEdit()
        layout.addRow(self.power_plant_weight_label, self.power_plant_weight_text)

        ##################################################################################

        ##############################################################################
        self.mass_of_payload_label = QLabel("Mass Of Payload")
        self.mass_of_payload_text = QLineEdit()
        layout.addRow(self.mass_of_payload_label, self.mass_of_payload_text)



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

    ############################################################################
        try:
            structure_specifications = Database.read_structures_specifications()
            mass_of_battery, mass_of_power_plant,mass_of_payload= self.read_values(
                values=structure_specifications)

            self.show_default_values(mass_of_battery, mass_of_power_plant,mass_of_payload)
        except(Exception):
            self.show_default_values()

    ############################################################################
    def show_default_values(self, mass_of_battery=0, mass_of_power_plant=0,
                            mass_of_payload=0):

        self.mass_of_battery_text.setText(str(mass_of_battery))
        self.power_plant_weight_text.setText(str(mass_of_power_plant))
        self.mass_of_payload_text.setText(str(mass_of_payload))


    def read_values(self, values={}):
        mass_of_battery = values["mass"]["mass_of_battery"]
        mass_of_power_plant = values["mass"]["mass_of_power_plant"]
        mass_of_payload = values["mass"]["mass_of_payload"]


        return mass_of_battery, mass_of_power_plant,mass_of_payload
    def init_action(self):
        self.parameters = {
            "mass": {
                "mass_of_battery": float(self.mass_of_battery_text.text()),
                "mass_of_power_plant": float(self.power_plant_weight_text.text()),
                "mass_of_payload": float(self.mass_of_payload_text.text()),
                "maximum_take_off_mass":float(self.mass_of_battery_text.text())+float(self.power_plant_weight_text.text())+float(self.mass_of_payload_text.text()),}}
        try:
            Database.update_structure_specifications(key="mass", value=self.parameters["mass"])
        except:
            Database.update_structure_specifications(key="", value=self.parameters)
        return self.parameters

    @staticmethod
    def get_params():
            dialog = WeightDialog(None)
            result = dialog.exec_()
            if result == 1:
                try:
                    params = dialog.init_action()
                    return params, QDialog.Accepted
                except Exception:
                    dialog = QMessageBox()
                    dialog.setIcon(QMessageBox.Critical)
                    dialog.setText("Incorrect or No Values Entered")
                    dialog.addButton(QMessageBox.Ok)
                    dialog.exec()
                    return [], QDialog.Rejected
            else:
                return [], QDialog.Rejected
