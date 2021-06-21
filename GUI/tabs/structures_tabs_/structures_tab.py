from PyQt5.QtWidgets import *

from Utils.data_objects.structures_placeholder import *
from Utils.database.structures.structures_database import get_structures_specifications, set_structure_specifications


class structures_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

        self.tab_ = self
        layout = self.layout
        ##########################################################################
        ##################################################################################

        self.mtow_label = QLabel("Maximum TakeOff Weight(MTOW)")
        self.mtow_text = QLineEdit()
        layout.addRow(self.mtow_label, self.mtow_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.payload_mass_label = QLabel("Payload Mass")
        self.payload_text = QLineEdit()
        layout.addRow(self.payload_mass_label, self.payload_text)

        ##################################################################################
        ##############################################################################

        self.powerplant_mass_label = QLabel("Powerplant Mass")
        self.powerplant_mass_text = QLineEdit()
        layout.addRow(self.powerplant_mass_label, self.powerplant_mass_text)

        self.battery_mass_label = QLabel("Battery Mass")
        self.battery_mass_text = QLineEdit()
        layout.addRow(self.battery_mass_label, self.battery_mass_text)
        ##################################################################################

        ###############################################################################
        ###############################################################################



        ##################################################################################

        ##################################################################################


        ##################################################################################

        # ##########################################################################################


        self.zero_all_text_fields()

    def zero_all_text_fields(self):
        mass_of_battery_or_fuel_, \
        mass_of_engine_or_motor_, \
        maximum_takeoff_weight_, \
        mass_of_payload_,  = get_structures_specifications()
        self.show_default_values(mass_of_battery_or_fuel_,
           mass_of_engine_or_motor_,
           maximum_takeoff_weight_,
           mass_of_payload_ )


    def show_default_values(self,
                            mass_of_battery_or_fuel_=0.0,
                            mass_of_engine_or_motor_=0.0,
                            maximum_takeoff_weight_=0.0,
                            mass_of_payload_=0.0,
                        ):

        self.mtow_text.setText(str(maximum_takeoff_weight_))

        self.battery_mass_text.setText(str(mass_of_battery_or_fuel_))

        self.payload_text.setText(str(mass_of_payload_))

        self.powerplant_mass_text.setText(str(mass_of_engine_or_motor_))

    def init_action(self):
        parameters = {
            mass_of_battery_or_fuel: float(self.battery_mass_text.text()),
            maximum_takeoff_weight: float(self.mtow_text.text()),
            mass_of_payload: float(self.payload_text.text()),
            mass_of_engine_or_motor: float(self.powerplant_mass_text.text()),

        }
        try:
            set_structure_specifications(parameters)
        except:
           print("Storage Failed")

        return parameters
