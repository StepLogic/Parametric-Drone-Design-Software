from PyQt5.QtWidgets import *

from Utils.database.aerodynamics.settings_database import set_mach_number_range, set_aoa_range, set_altitude, \
    read_settings


class aerodynamic_settings_tab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QFormLayout(self)

        altitude_label = QLabel("Altitude(Metres)")
        self.altitude_text = QLineEdit()
        layout.addRow(altitude_label, self.altitude_text)

        mach_number_label = QLabel("Free Stream Mach Number()"
                                   "\nIf one Mach Number is preferred ,enter same value for Max and Min")
        layout.addRow(mach_number_label)

        min_mach_number_label = QLabel("Min")
        self.min_mach_number_text = QLineEdit()
        layout.addRow(min_mach_number_label, self.min_mach_number_text)

        max_mach_number_label = QLabel("Max")
        self.max_mach_number_text = QLineEdit()
        layout.addRow(max_mach_number_label, self.max_mach_number_text)


        angle_of_attack_label = QLabel("Angle Of Attack()\n"
                                       "If one angle of attack is preferred ,enter same value for Max and Min"
                                       "\nSame angles will be used for control Surface Deflections")
        layout.addRow(angle_of_attack_label)
        min_angle_of_attack_label = QLabel("Min")
        self.min_angle_of_attack_text = QLineEdit()
        layout.addRow(min_angle_of_attack_label, self.min_angle_of_attack_text)

        max_angle_of_attack_label = QLabel("Max")
        self.max_angle_of_attack_text = QLineEdit()
        layout.addRow(max_angle_of_attack_label, self.max_angle_of_attack_text)
        self.zero_all_textfields()

    def zero_all_textfields(self):
            altitude_, aoa_range_, mach_number_range_ = read_settings()
            self.show_default_values(altitude_,aoa_range_,mach_number_range_)

    def show_default_values(self, altitude_=0, aoa_range_=None, mach_number_range_=None):

        if mach_number_range_ is None:
            mach_number_range_ = [0, 0]
        if aoa_range_ is None:
            aoa_range_ = [0, 0]

        self.altitude_text.setText(str(altitude_))
        self.max_angle_of_attack_text.setText(str(max(aoa_range_)))
        self.min_angle_of_attack_text.setText(str(min(aoa_range_)))
        self.max_mach_number_text.setText(str(max(mach_number_range_)))
        self.min_mach_number_text.setText(str(min(mach_number_range_)))


    def init_action(self):
        set_aoa_range(max=float(self.max_angle_of_attack_text.text()),
                      min=float(self.min_angle_of_attack_text.text()))
        set_mach_number_range(max=float(self.max_mach_number_text.text()),
                      min=float(self.min_mach_number_text.text()))
        set_altitude(float(self.altitude_text.text()))




