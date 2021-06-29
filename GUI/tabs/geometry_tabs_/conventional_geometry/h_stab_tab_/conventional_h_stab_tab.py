from PyQt5.QtWidgets import *
from Utils.data_objects.lifting_surface_placeholder import *
from Utils.database import database
from Utils.database.geometry.lifting_database import write_lifting_surface_objects, write_lifting_surface_to_objects, \
    read_surface_data, airfoil_profiles
from PyQt5.QtWidgets import *

from Utils.data_objects.lifting_surface_placeholder import *
from Utils.database import database
from Utils.database.geometry.lifting_database import write_lifting_surface_objects, write_lifting_surface_to_objects, \
    read_surface_data


class h_stab_tab(QWidget):
    def __init__(self,text, surface_type_, design_type_):
        super().__init__()
        layout = QFormLayout(self)
        self.text=text
        self.surface_type_=surface_type_
        self.design_type_=design_type_
        self.tab_=self
        ##################################################################################
        self.span_label = QLabel("Span")
        self.span_text = QLineEdit()
        layout.addRow(self.span_label, self.span_text)
        ##############################################################################
        self.chord_length_label = QLabel("Chord Length")
        self.chord_length_text = QLineEdit()
        layout.addRow(self.chord_length_label, self.chord_length_text)
        self.sweep_angle_label = QLabel("Sweep Angle(⁰)")
        self.sweep_angle_text = QLineEdit()
        layout.addRow(self.sweep_angle_label, self.sweep_angle_text)

        ##################################################################################

        self.twist_angle_label = QLabel("Twist Angle(⁰)")
        self.twist_angle_text = QLineEdit()
        layout.addRow(self.twist_angle_label, self.twist_angle_text)

        ###############################################################################
        ###############################################################################

        self.dihedral_angle_label = QLabel("Dihedral Angle(⁰)")
        self.dihedral_angle_text = QLineEdit()
        layout.addRow(self.dihedral_angle_label, self.dihedral_angle_text)

        ##################################################################################

        ##################################################################################
        self.taper_ratio_label = QLabel("Taper Ratio")
        self.taper_ratio_text = QLineEdit()
        layout.addRow(self.taper_ratio_label, self.taper_ratio_text)

        ##################################################################################
        self.wing_profile_label = QLabel("Airfoil Profile")
        self.wing_profile_combo = QComboBox()
        self.wing_profile_combo.addItems(airfoil_profiles())
        self.wing_profile_selection = None
        self.wing_profile_combo.currentIndexChanged.connect(self.wing_profile_selectionChanged)
        layout.addRow(self.wing_profile_label, self.wing_profile_combo)

        ##################################################################################

        self.Wing_postion_tlabel = QLabel("Tailplane Leading Edge Position")
        layout.addWidget(self.Wing_postion_tlabel)

        self.Wing_postion_x_label = QLabel("X")
        self.Wing_postion_x_text = QLineEdit()
        layout.addRow(self.Wing_postion_x_label, self.Wing_postion_x_text)

        self.Wing_postion_y_label = QLabel("Y")
        self.Wing_postion_y_text = QLineEdit()
        layout.addRow(self.Wing_postion_y_label, self.Wing_postion_y_text)

        self.Wing_postion_z_label = QLabel("Z")
        self.Wing_postion_z_text = QLineEdit()

        layout.addRow(self.Wing_postion_z_label, self.Wing_postion_z_text)
        self.zero_all_text_fields()


    def zero_all_text_fields(self):
        try:

            root_location_x, root_location_y, root_location_z, dihedral, sweep, twist, span, taper_ratio, chord, profile =read_surface_data(self.text)

            self.show_default_values(root_location_x=root_location_x, root_location_y=root_location_y,
                                     root_location_z=root_location_z
                                     , dihedral=dihedral, sweep=sweep, twist=twist,
                                     span=span, taper_ratio=taper_ratio, chord=chord, profile=profile)
        except(Exception):
            self.show_default_values()
    ############################################################################
    def show_default_values(self, root_location_x=0, root_location_y=0, root_location_z=0, dihedral=0, sweep=0, twist=0,
                            span=0, taper_ratio=1, chord=0,profile=airfoil_profiles()[0]):
        self.span_text.setText(str(span))

        self.chord_length_text.setText(str(chord))

        self.sweep_angle_text.setText(str(sweep))

        self.twist_angle_text.setText(str(twist))

        self.dihedral_angle_text.setText(str(dihedral))

        self.taper_ratio_text.setText(str(taper_ratio))

        self.wing_profile_combo.setCurrentIndex(airfoil_profiles().index(profile))

        self.Wing_postion_x_text.setText(str(root_location_x))

        self.Wing_postion_y_text.setText(str(root_location_y))

        self.Wing_postion_z_text.setText(str(root_location_z))


    def init_action(self):
        self.accept_inputs()
        self.parameters = {
            lifting_surface: {
                str(self.text): {

                    design_type: self.design_type_,
                    surface_type: self.surface_type_,
                    root_le_position_x: float(self.Wing_postion_x_text.text()),
                    root_le_position_y: float(self.Wing_postion_y_text.text()),
                    root_le_position_z: float(self.Wing_postion_z_text.text()),
                    span: float(self.span_text.text()),
                    profile: str(self.wing_profile_selection),
                    chord: float(self.chord_length_text.text()),
                    taper_ratio: float(self.taper_ratio_text.text()),
                    sweep: float(self.sweep_angle_text.text()),
                    dihedral: float(self.dihedral_angle_text.text()),
                    twist: float(self.twist_angle_text.text()),
            }
        }}
        try:
            print(self.parameters)
            database.update_aircraft_specifications(key=lifting_surface, value=self.parameters[lifting_surface])
        except:
            database.write_aircraft_specification(self.parameters)
        return self.parameters

    def wing_profile_selectionChanged(self, i):
        self.wing_profile_selection = airfoil_profiles()[i]

    def accept_inputs(self):
        if self.wing_profile_selection is None:
            self.wing_profile_selection = airfoil_profiles()[self.wing_profile_combo.currentIndex()]


