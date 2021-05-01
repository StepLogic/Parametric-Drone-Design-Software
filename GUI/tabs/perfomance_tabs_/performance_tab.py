from PyQt5.QtWidgets import *

from DPS_data_objects.placeholders.performance_placeholders import *
from utils.database.performance_database import write_performance_parameters, read_performance_parameters


class performance_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

    def create_tab(self):
        self.create_widget()
        self.button = QPushButton('Save', self)
        self.button.clicked.connect(self.init_action)
        self.layout.addRow(self.button)
        self.setLayout(self.layout)
        self.zero_all_textfields()
        return self

    def create_widget(self):
        ##########################################################################
        ##################################################################################
        layout = self.layout
        self.landing_distance_label = QLabel("Voltage(Volts)")
        self.landing_distance_text = QLineEdit()
        self.layout.addRow(self.landing_distance_label, self.landing_distance_text)

        self.takeoff_distance_label = QLabel("Current(Amps)")
        self.takeoff_distance_text = QLineEdit()
        self.layout.addRow(self.takeoff_distance_label, self.takeoff_distance_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.rate_climb_label = QLabel("Mass of Motor (Kg)")
        self.rate_of_climb_text = QLineEdit()
        self.layout.addRow(self.rate_climb_label, self.rate_of_climb_text)

        ##################################################################################
        ##############################################################################

        self.maximum_velocity_label = QLabel("V)")
        self.maximum_velocity_text = QLineEdit()
        self.layout.addRow(self.maximum_velocity_label, self.maximum_velocity_text)


        self.zero_all_textfields()

        return self.layout
        ##########################################################################################

    def zero_all_textfields(self):
        try:
            voltage_,max_thrust_,battery_capacity_,discharge_rate_,max_current_ = read_performance_parameters()
            self.show_default_values(voltage_,max_thrust_,battery_capacity_,discharge_rate_,max_current_)
        except(Exception):
            self.show_default_values()

        ############################################################################

    def show_default_values(self,voltage_=0, max_thrust_=0, battery_capacity_=0, discharge_rate_=0,max_current_=0):

        self.takeoff_distance_text.setText(str(max_current_))
        self.landing_distance_text.setText(str(voltage_))
        self.rate_of_climb_text.setText(str(discharge_rate_))
        self.maximum_velocity_text.setText(str(max_thrust_))

    def init_action(self):
        self.parameters = {
            performance: {
                landing_distance : float(self.landing_distance_text.text()),
                takeoff_distance : float(self.takeoff_distance_text.text()),
                rate_of_climb    : float(self.maximum_velocity_text.text()),
                maximum_velocity : float(self.rate_of_climb_text.text()),

                   }}
        write_performance_parameters(self.parameters)
        return self.parameters
