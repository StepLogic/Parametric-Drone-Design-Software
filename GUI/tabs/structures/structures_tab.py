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

        self.mtow_label = QLabel("Span")
        self.mtow_text = QLineEdit()
        layout.addRow(self.mtow_label, self.mtow_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.payload_mass_label = QLabel("Chord Length")
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

        self.center_of_mass_label = QLabel("Twist Angle(⁰)")
        layout.addRow(self.center_of_mass_label)

        ###############################################################################
        ###############################################################################

        self.moments_of_inertia_label = QLabel("Dihedral Angle(⁰)")
        layout.addRow(self.moments_of_inertia_label)

        ##################################################################################

        ##################################################################################
        self.fuselage_mass_label = QLabel("Taper Ratio")
        layout.addRow(self.fuselage_mass_label)

        ##################################################################################

        # ##########################################################################################

        self.wing_mass_label = QLabel("Airfoil(Do not Add NACA)")
        layout.addRow(self.wing_mass_label)

        self.zero_all_text_fields()

    def zero_all_text_fields(self):
        try:
            moments_of_inertia_, \
            mass_of_battery_or_fuel_, \
            mass_of_engine_or_motor_, \
            center_of_gravity_, \
            maximum_takeoff_weight_, \
            mass_of_wing_, \
            mass_of_payload_, \
            mass_of_fuselage_, = get_structures_specifications()
            self.show_default_values(moments_of_inertia_,
                                     mass_of_battery_or_fuel_,
                                     mass_of_engine_or_motor_,
                                     center_of_gravity_,
                                     maximum_takeoff_weight_,
                                     mass_of_wing_,
                                     mass_of_payload_,
                                     mass_of_fuselage_)
        except:
            self.show_default_values()

    def show_default_values(self, moments_of_inertia_=[],
                            mass_of_battery_or_fuel_=0.0,
                            mass_of_engine_or_motor_=0.0,
                            center_of_gravity_=[],
                            maximum_takeoff_weight_=0.0,
                            mass_of_wing_=0.0,
                            mass_of_payload_=0.0,
                            mass_of_fuselage_=0.0):

        self.mtow_text.setText(str(maximum_takeoff_weight_))

        self.battery_mass_text.setText(str(mass_of_battery_or_fuel_))

        self.payload_text.setText(str(mass_of_payload_))

        self.powerplant_mass_text.setText(str(mass_of_engine_or_motor_))

        self.center_of_mass_label.setText(f"{self.center_of_mass_label.text()}:{9}Cm")

        self.moments_of_inertia_label.setText(f"{self.moments_of_inertia_label.text()}:{9}Cm")

        self.fuselage_mass_label.setText(f"{self.fuselage_mass_label.text()}:{mass_of_fuselage_}Cm")
        self.wing_mass_label.setText(f"{self.wing_mass_label.text()}:{mass_of_wing_}Cm")

    def init_action(self):
        parameters = {
            mass_of_battery_or_fuel: float(self.battery_mass_text.text()),
            maximum_takeoff_weight: float(self.mtow_text.text()),
            mass_of_wing: str(self.wing_mass_label.text()),
            mass_of_payload: float(self.payload_text.text()),
            mass_of_fuselage: float(self.fuselage_mass_label.text()),
            mass_of_engine_or_motor: float(self.powerplant_mass_text.text()),

        }
        try:
            set_structure_specifications(parameters)
        except:
           print("Storage Failed")

        return parameters
