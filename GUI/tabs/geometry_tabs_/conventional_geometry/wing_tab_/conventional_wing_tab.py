from PyQt5.QtWidgets import *

from Utils.data_objects.lifting_surface_placeholder import *
from Utils.data_objects.placeholder import design_type
from Utils.database import database
from Utils.database.geometry.lifting_database import write_lifting_surface_objects, \
    write_lifting_surface_to_objects, read_surface_data, airfoil_profiles


class wing_tab(QWidget):
    def __init__(self,text, surface_type_, design_type_):
        super().__init__()
        self.layout = QFormLayout(self)
        self.text=text
        self.surface_type_=surface_type_
        self.design_type_=design_type_

        self.tab_=self
        layout = self.layout
        ##########################################################################
        ##################################################################################


        self.span_label = QLabel("Span")
        self.span_text = QLineEdit()
        layout.addRow(self.span_label, self.span_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.chord_length_label = QLabel("Chord Length")
        self.chord_length_text = QLineEdit()
        layout.addRow(self.chord_length_label, self.chord_length_text)

        ##################################################################################
        ##############################################################################

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

        # ##########################################################################################

        self.wing_profile_label = QLabel("Airfoil Profile")
        self.wing_profile_combo = QComboBox()
        self.wing_profile_combo.addItems(airfoil_profiles())
        self.wing_profile_selection = None
        self.wing_profile_combo.currentIndexChanged.connect(self.wing_profile_selectionChanged)
        self.layout.addRow(self.wing_profile_label, self.wing_profile_combo)



        ##########################################################################################

        self.Wing_postion_tlabel = QLabel("Wing Position(The Reference is ths middle of the center of the fuselage!!")
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

        self.winglet_vbox = QVBoxLayout()
        self.winglet_tlabel = QLabel(
            "Winglet Center Translation(Enter Zero Into all the fields Below If you wont add a winglet)")
        layout.addWidget(self.winglet_tlabel)

        self.winglet_center_translation_x_label = QLabel("X")
        self.winglet_center_translation_x_text = QLineEdit()
        layout.addRow(self.winglet_center_translation_x_label, self.winglet_center_translation_x_text)

        self.winglet_center_translation_y_label = QLabel("Y")
        self.winglet_center_translation_y_text = QLineEdit()
        layout.addRow(self.winglet_center_translation_y_label, self.winglet_center_translation_y_text)

        self.winglet_center_translation_z_label = QLabel("Z")
        self.winglet_center_translation_z_text = QLineEdit()
        layout.addRow(self.winglet_center_translation_z_label, self.winglet_center_translation_z_text)

        self.winglet_rotation_label = QLabel("Winglet Rotation")
        self.winglet_rotation_text = QLineEdit()
        layout.addRow(self.winglet_rotation_label, self.winglet_rotation_text)

        self.winglet_width_label = QLabel("Winglet Width")
        self.winglet_width_text = QLineEdit()
        layout.addRow(self.winglet_width_label, self.winglet_width_text)
        self.zero_all_text_fields()

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
        ##########################################################################
        ##################################################################################

        self.chord_length_label = QLabel("Chord Length")
        self.chord_length_text = QLineEdit()
        layout.addRow(self.chord_length_label, self.chord_length_text)

        ##################################################################################
        ##############################################################################

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

        # ##########################################################################################

        self.wing_profile_label = QLabel("Airfoil Profile")
        self.wing_profile_combo = QComboBox()
        self.wing_profile_combo.addItems(airfoil_profiles())
        self.wing_profile_selection = None
        self.wing_profile_combo.currentIndexChanged.connect(self.wing_profile_selectionChanged)
        self.layout.addRow(self.wing_profile_label, self.wing_profile_combo)

        ##########################################################################################

        self.Wing_postion_tlabel = QLabel("Wing Position(The Reference is ths middle of the center of the fuselage!!")
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

        self.winglet_vbox = QVBoxLayout()
        self.winglet_tlabel = QLabel(
            "Winglet Center Translation(Enter Zero Into all the fields Below If you wont add a winglet)")
        layout.addWidget(self.winglet_tlabel)

        self.winglet_center_translation_x_label = QLabel("X")
        self.winglet_center_translation_x_text = QLineEdit()
        layout.addRow(self.winglet_center_translation_x_label, self.winglet_center_translation_x_text)

        self.winglet_center_translation_y_label = QLabel("Y")
        self.winglet_center_translation_y_text = QLineEdit()
        layout.addRow(self.winglet_center_translation_y_label, self.winglet_center_translation_y_text)

        self.winglet_center_translation_z_label = QLabel("Z")
        self.winglet_center_translation_z_text = QLineEdit()
        layout.addRow(self.winglet_center_translation_z_label, self.winglet_center_translation_z_text)

        self.winglet_rotation_label = QLabel("Winglet Rotation")
        self.winglet_rotation_text = QLineEdit()
        layout.addRow(self.winglet_rotation_label, self.winglet_rotation_text)

        self.winglet_width_label = QLabel("Winglet Width")
        self.winglet_width_text = QLineEdit()
        layout.addRow(self.winglet_width_label, self.winglet_width_text)
        self.zero_all_text_fields()
        return layout

    def surfaceType_Checked(self, button):
        self.surface_curve_type_= button
    def zero_all_text_fields(self):
        try:
            root_location_x, root_location_y, root_location_z, dihedral, sweep, twist, span, taper_ratio, chord, winglet_width, winglet_rotation, winglet_center_translation_x, winglet_center_translation_y, winglet_center_translation_z, profile = \
                read_surface_data(self.text)
            self.show_default_values(
                                     root_location_x=root_location_x, root_location_y=root_location_y,
                                     root_location_z=root_location_z
                                     , dihedral=dihedral, sweep=sweep, twist=twist,
                                     span=span, taper_ratio=taper_ratio, chord=chord, winglet_width=winglet_width,
                                     winglet_rotation=winglet_rotation,
                                     winglet_center_translation_x=winglet_center_translation_x
                                     , winglet_center_translation_y=winglet_center_translation_y,
                                     winglet_center_translation_z=winglet_center_translation_z, profile=profile)
        except:
            self.show_default_values()


    def show_default_values(self,root_location_x=0, root_location_y=0, root_location_z=0, dihedral=0, sweep=0, twist=0,
                            span=0, taper_ratio=1, chord=0, winglet_width=0, winglet_rotation=0,
                            winglet_center_translation_x=0
                            , winglet_center_translation_y=0, winglet_center_translation_z=0, profile="naca0006"):



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

        self.winglet_center_translation_x_text.setText(str(winglet_center_translation_x))

        self.winglet_center_translation_y_text.setText(str(winglet_center_translation_y))

        self.winglet_center_translation_z_text.setText(str(winglet_center_translation_z))

        self.winglet_rotation_text.setText(str(winglet_rotation))

        self.winglet_width_text.setText(str(winglet_width))


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
                winglet_center_translation_x: float(self.winglet_center_translation_x_text.text()),
                winglet_center_translation_y: float(self.winglet_center_translation_y_text.text()),
                winglet_center_translation_z: float(self.winglet_center_translation_z_text.text()),
                winglet_rotation: float(self.winglet_rotation_text.text()),
                winglet_width: float(self.winglet_width_text.text()),
            }}}
        try:
            database.update_aircraft_specifications(key=lifting_surface, value=self.parameters[lifting_surface])
        except:
            database.write_aircraft_specification(self.parameters)

        return self.parameters
    def wing_profile_selectionChanged(self, i):
        self.wing_profile_selection = airfoil_profiles()[i]

    def accept_inputs(self):
        if self.wing_profile_selection is None:
            self.wing_profile_selection = airfoil_profiles()[self.wing_profile_combo.currentIndex()]