from PyQt5.QtWidgets import *



class propulsion_tab(QWidget):
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
        self.voltage_label = QLabel("Voltage(Volts)")
        self.voltage_text = QLineEdit()
        self.layout.addRow(self.voltage_label, self.voltage_text)

        self.current_label = QLabel("Current(Amps)")
        self.current_text = QLineEdit()
        self.layout.addRow(self.current_label, self.current_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.mass_motor_label = QLabel("Mass of Motor (Kg)")
        self.mass_text = QLineEdit()
        self.layout.addRow(self.mass_motor_label, self.mass_text)

        ##################################################################################
        ##############################################################################

        self.thrust_label = QLabel("Thrust(kg)")
        self.thrust_text = QLineEdit()
        self.layout.addRow(self.thrust_label, self.thrust_text)

        ##########################################################################################

        self.battery_capacity_label = QLabel("Battery Capacity(mAh)")
        self.battery_capacity_text = QLineEdit()
        layout.addRow(self.battery_capacity_label, self.battery_capacity_text)
        ##############################################################################

        self.battery_mass_label = QLabel("Mass Battery(kg)")
        self.battery_mass_text = QLineEdit()
        self.layout.addRow(self.battery_mass_label, self.battery_mass_text)
        ############################################################################
        self.discharge_rate_label = QLabel("Discharge Rate(C)")
        self.discharge_rate_text = QLineEdit()
        layout.addRow(self.discharge_rate_label, self.discharge_rate_text)

        self.zero_all_textfields()

        return self.layout
        ##########################################################################################

    def zero_all_textfields(self):
        try:
            voltage_,max_thrust_,battery_capacity_,discharge_rate_,max_current_ = read_propulsion_parameters()
            self.show_default_values(voltage_,max_thrust_,battery_capacity_,discharge_rate_,max_current_)
        except(Exception):
            self.show_default_values()

        ############################################################################

    def show_default_values(self,voltage_=0, max_thrust_=0, battery_capacity_=0, discharge_rate_=0,max_current_=0):

        self.current_text.setText(str(max_current_))
        self.voltage_text.setText(str(voltage_))

        self.discharge_rate_text.setText(str(discharge_rate_))
        self.battery_capacity_text.setText(str(battery_capacity_))
        self.thrust_text.setText(str(max_thrust_))

    def init_action(self):
        self.parameters = {
            propulsion: {
                voltage: float(self.voltage_text.text()),
                max_current: float(self.current_text.text()),
                discharge_rate: float(self.discharge_rate_text.text()),
                max_thrust: float(self.thrust_text.text()),
                battery_capacity: float(self.battery_capacity_text.text()),
                   }}
        write_propulsion_parameters(self.parameters)
        return self.parameters
