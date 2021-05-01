from DPS_data_objects.placeholders.geometry_placeholder import wing, conventional_design, type
from PyQt5.QtWidgets import *
from utils.database import Database
from utils.database.geometry_database import read_unconv_wing_info


class unconventional_info_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)

    def create_tab(self):
        self.create_widget()
        self.button = QPushButton('Save', self)
        self.button.clicked.connect(self.init_action)
        self.layout.addRow(self.button)
        self.setLayout(self.layout)
        self.zero_all_text_fields()
        return self

    def create_widget(self):

        layout=self.layout
        ##########################################################################
        ##################################################################################

        self.span_label = QLabel("Span")
        self.span_text = QLineEdit()
        layout.addRow(self.span_label, self.span_text)
        ###################################################


        self.dihedral_angle_label = QLabel("Dihedral Angle(⁰)")
        self.dihedral_angle_text = QLineEdit()
        layout.addRow(self.dihedral_angle_label, self.dihedral_angle_text)



        self.Wing_profile_label = QLabel("Airfoil(Do not Add NACA)")
        self.Wing_profile_text = QLineEdit()
        layout.addRow(self.Wing_profile_label, self.Wing_profile_text)

        ##########################################################################################

        self.zero_all_text_fields()
        return layout

    def zero_all_text_fields(self):
        try:
          dihedral,span,profile =read_unconv_wing_info()
          self.show_default_values(dihedral=dihedral,
                                     span=span, profile=profile)

        except(Exception):
            self.show_default_values()
    def show_default_values(self, dihedral=0,
                            span=0, profile=""):
        self.span_text.setText(str(span))



        self.dihedral_angle_text.setText(str(dihedral))


        self.Wing_profile_text.setText(profile)



    def init_action(self):
        self.parameters = {
            wing: {
                type: conventional_design,
                "wing_span": float(self.span_text.text()),
                "wing_profile": str(self.Wing_profile_text.text()),
                "wing_dihedral": float(self.dihedral_angle_text.text()),

            }}
        try:
            Database.update_aircraft_specifications(key=wing, value=self.parameters)
        except:
            Database.write_aircraft_specification(self.parameters)
        return self.parameters
