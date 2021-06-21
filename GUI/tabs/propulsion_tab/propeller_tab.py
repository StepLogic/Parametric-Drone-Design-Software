from PyQt5.QtWidgets import *

from Utils.data_objects.propulsion_keys import *
from Utils.database import database
from Utils.database.propulsion.propulsion_database import write_propeller_objects, read_propeller_parameters


class propeller_tab(QWidget):
    def __init__(self, name=""):
        super().__init__()
        self._name = name
        self.xz_mirror_ = None
        self.xy_mirror_ = None
        self.yz_mirror_ = None
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

        ##########################################################################
        ##################################################################################
        self.inputArea = QTabWidget()
        self.layout = QFormLayout()
        self.propeller_number_label = QLabel("Propeller Number")
        self.propeller_number_text = QLineEdit()
        self.layout.addRow(self.propeller_number_label, self.propeller_number_text)

        self.rotation_label = QLabel("Rotation(XYZ)")
        self.layout.addRow(self.rotation_label)

        self.hub_diameter_label = QLabel("Hub Diameter")
        self.hub_diameter_text = QLineEdit()
        self.layout.addRow(self.hub_diameter_label, self.hub_diameter_text)

        self.hub_length_label = QLabel("Hub Length")
        self.hub_length_text = QLineEdit()
        self.layout.addRow(self.hub_length_label, self.hub_length_text)

        self.pitch_angle_label = QLabel("Pitch Angle")
        self.pitch_angle_text = QLineEdit()
        self.layout.addRow(self.pitch_angle_label, self.pitch_angle_text)

        self.XZsymmetryCheck = QCheckBox("Mirror Boom About XZ Plane")
        self.XZsymmetryCheck.toggled.connect(self.xz_mirror_Checked)
        self.layout.addRow(self.XZsymmetryCheck)
        self.YZsymmetryCheck = QCheckBox("Mirror Boom About YZ Plane")
        self.YZsymmetryCheck.toggled.connect(self.yz_mirror_Checked)
        self.layout.addRow(self.YZsymmetryCheck)
        self.XYsymmetryCheck = QCheckBox("Mirror Boom About XY Plane")
        self.XYsymmetryCheck.toggled.connect(self.xy_mirror_Checked)
        self.layout.addRow(self.XYsymmetryCheck)

        self.root_le_position_label = QLabel("Root Leading Edge Position")
        self.layout.addWidget(self.root_le_position_label)

        self.root_le_position_x_label = QLabel("X")
        self.root_le_position_x_text = QLineEdit()
        self.layout.addRow(self.root_le_position_x_label, self.root_le_position_x_text)

        self.root_le_position_y_label = QLabel("Y")
        self.root_le_position_y_text = QLineEdit()
        self.layout.addRow(self.root_le_position_y_label, self.root_le_position_y_text)

        self.root_le_position_z_label = QLabel("Z")
        self.root_le_position_z_text = QLineEdit()
        self.layout.addRow(self.root_le_position_z_label, self.root_le_position_z_text)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Design Overview")
        ##################################################################################
        self.layout = QFormLayout()
        self.section_1_label = QLabel("Section 1")
        self.layout.addRow(self.section_1_label)

        self.section_1_chord_label = QLabel("Chord Length")
        self.section_1_chord_text = QLineEdit()
        self.layout.addRow(self.section_1_chord_label, self.section_1_chord_text)

        self.section_1_length_label = QLabel("Length")
        self.section_1_length_text = QLineEdit()
        self.layout.addRow(self.section_1_length_label, self.section_1_length_text)

        self.section_1_profile_label = QLabel("Profile")
        self.section_1_profile_text = QLineEdit()
        self.layout.addRow(self.section_1_profile_label, self.section_1_profile_text)

        self.section_1_z_label = QLabel("Z")
        self.section_1_z_text = QLineEdit()
        self.layout.addRow(self.section_1_z_label, self.section_1_z_text)

        self.section_1_pitch_label = QLabel("Pitch(⁰)")
        self.section_1_pitch_angle_text = QLineEdit()
        self.layout.addRow(self.section_1_pitch_label, self.section_1_pitch_angle_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section One")
        ###############################################################################

        ############################################Y#####################################
        ##################################################################################
        ##############################################################################
        ##################################################################################

        ##################################################################################
        self.layout = QFormLayout()
        self.section_2_label = QLabel("Section 2")
        self.layout.addRow(self.section_2_label)

        self.section_2_chord_label = QLabel("Chord Length")
        self.section_2_chord_text = QLineEdit()
        self.layout.addRow(self.section_2_chord_label, self.section_2_chord_text)

        self.section_2_length_label = QLabel("length")
        self.section_2_length_text = QLineEdit()
        self.layout.addRow(self.section_2_length_label, self.section_2_length_text)

        self.section_2_profile_label = QLabel("Profile")
        self.section_2_profile_text = QLineEdit()
        self.layout.addRow(self.section_2_profile_label, self.section_2_profile_text)

        self.section_2_z_label = QLabel("Z")
        self.section_2_z_text = QLineEdit()
        self.layout.addRow(self.section_2_z_label, self.section_2_z_text)

        self.section_2_pitch_angle_label = QLabel("Pitch(⁰)")
        self.section_2_pitch_angle_text = QLineEdit()
        self.layout.addRow(self.section_2_pitch_angle_label, self.section_2_pitch_angle_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Three")
        ###############################################################################
        ##################################################################################

        ##################################################################################
        self.layout = QFormLayout()
        self.section_3_label = QLabel("Section 3")
        self.layout.addRow(self.section_3_label)

        self.section_3_chord_label = QLabel("Chord Length")
        self.section_3_chord_text = QLineEdit()
        self.layout.addRow(self.section_3_chord_label, self.section_3_chord_text)

        self.section_3_x_label = QLabel("Length")
        self.section_3_x_text = QLineEdit()
        self.layout.addRow(self.section_3_x_label, self.section_3_x_text)

        self.section_3_y_label = QLabel("Profile")
        self.section_3_y_text = QLineEdit()
        self.layout.addRow(self.section_3_y_label, self.section_3_y_text)

        self.section_3_z_label = QLabel("Z")
        self.section_3_z_text = QLineEdit()
        self.layout.addRow(self.section_3_z_label, self.section_3_z_text)

        self.section_3_twist_label = QLabel("Twist(⁰)")
        self.section_3_pitch_angle_text = QLineEdit()
        self.layout.addRow(self.section_3_twist_label, self.section_3_pitch_angle_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Three")
        ###############################################################################
        ##################################################################################
        ##################################################################################

        ##################################################################################
        self.layout = QFormLayout()
        self.section_4_label = QLabel("Section 4")
        self.layout.addRow(self.section_4_label)

        self.section_4_chord_label = QLabel("Chord Length")
        self.section_4_chord_text = QLineEdit()
        self.layout.addRow(self.section_4_chord_label, self.section_4_chord_text)

        self.section_4_x_label = QLabel("Length")
        self.section_4_x_text = QLineEdit()
        self.layout.addRow(self.section_4_x_label, self.section_4_x_text)

        self.section_4_profile_label = QLabel("Profile")
        self.section_4_profile_text = QLineEdit()
        self.layout.addRow(self.section_4_profile_label, self.section_4_profile_text)

        self.section_4_z_label = QLabel("Z")
        self.section_4_z_text = QLineEdit()
        self.layout.addRow(self.section_4_z_label, self.section_4_z_text)

        self.section_4_pitch_label = QLabel("Pitch(⁰)")
        self.section_4_pitch_angle_text = QLineEdit()
        self.layout.addRow(self.section_4_pitch_label, self.section_4_pitch_angle_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Four")
        ###############################################################################

        ##################################################################################

        ##################################################################################
        self.layout = QFormLayout()
        self.section_5_label = QLabel("Section 5")
        self.layout.addRow(self.section_5_label)

        self.section_5_chord_label = QLabel("Chord Length")
        self.section_5_chord_text = QLineEdit()
        self.layout.addRow(self.section_5_chord_label, self.section_5_chord_text)

        self.section_5_x_label = QLabel("Length")
        self.section_5_x_text = QLineEdit()
        self.layout.addRow(self.section_5_x_label, self.section_5_x_text)

        self.section_5_y_label = QLabel("Y")
        self.section_5_profile_text = QLineEdit()
        self.layout.addRow(self.section_5_y_label, self.section_5_profile_text)

        self.section_5_z_label = QLabel("Z")
        self.section_5_z_text = QLineEdit()
        self.layout.addRow(self.section_5_z_label, self.section_5_z_text)

        self.section_5_twist_label = QLabel("Twist(⁰)")
        self.section_5_pitch_angle_text = QLineEdit()
        self.layout.addRow(self.section_5_twist_label, self.section_5_pitch_angle_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Five")
        ###############################################################################

        # ##########################################################################################

        ##########################################################################################

        self.zero_all_text_fields()
        self.layout = QFormLayout()
        self.layout.addRow(self.inputArea)
        return self.layout

    def xz_mirror_Checked(self, button):
        self.xz_mirror_ = button

    def xy_mirror_Checked(self, button):
        self.xy_mirror_ = button

    def yz_mirror_Checked(self, button):
        self.yz_mirror_ = button

    def zero_all_text_fields(self):
        try:
            propeller_number_, xz_mirror_, xy_mirror_, yz_mirror_ \
                , rot_x_, rot_y_, rot_z_, root_le_pos_x_, \
            root_le_pos_y_, root_le_pos_z_, section_1_length_, section_2_length_, \
            section_3_length_, section_4_length_, section_5_length_, section_1_profile_, \
            section_2_profile_, section_3_profile_, section_4_profile_, section_5_profile_, \
            section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_ \
                , section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, \
            section_5_chord_, section_1_pitch_angle_, section_2_pitch_angle_, \
            section_3_pitch_angle_, section_4_pitch_angle_, section_5_pitch_angle_ = read_propeller_parameters(
                self._name)

            self.show_default_values(propeller_number_=propeller_number_,
                                     xz_mirror_=xz_mirror_,
                                     xy_mirror_=xy_mirror_,
                                     yz_mirror_=yz_mirror_,
                                     rot_x_=rot_x_,
                                     rot_y_=rot_y_,
                                     rot_z_=rot_z_,
                                     root_le_pos_x_=root_le_pos_x_,
                                     root_le_pos_y_=root_le_pos_y_,
                                     root_le_pos_z_=root_le_pos_z_,
                                     section_1_length_=section_1_length_,
                                     section_2_length_=section_2_length_,
                                     section_3_length_=section_3_length_,
                                     section_4_length_=section_4_length_,
                                     section_5_length_=section_5_length_,
                                     section_1_profile_=section_1_profile_,
                                     section_2_profile_=section_2_profile_,
                                     section_3_profile_=section_3_profile_,
                                     section_4_profile_=section_4_profile_,
                                     section_5_profile_=section_5_profile_,
                                     section_1_z_=section_1_z_,
                                     section_2_z_=section_2_z_,
                                     section_3_z_=section_3_z_,
                                     section_4_z_=section_4_z_,
                                     section_5_z_=section_5_z_,
                                     section_1_chord_=section_1_chord_,
                                     section_2_chord_=section_2_chord_,
                                     section_3_chord_=section_3_chord_,
                                     section_4_chord_=section_4_chord_,
                                     section_5_chord_=section_5_chord_,
                                     section_1_pitch_angle_=section_1_pitch_angle_,
                                     section_2_pitch_angle_=section_2_pitch_angle_,
                                     section_3_pitch_angle_=section_3_pitch_angle_,
                                     section_4_pitch_angle_=section_4_pitch_angle_,
                                     section_5_pitch_angle_=section_5_pitch_angle_)
        except Exception as e:
            print("error", e)
            print(self._name)
            self.show_default_values()

    def show_default_values(self,
                            propeller_number_=0,
                            rot_x_=0,
                            rot_y_=0,
                            rot_z_=0,
                            xz_mirror_=False,
                            xy_mirror_=False,
                            yz_mirror_=False,
                            root_le_pos_x_=0,
                            root_le_pos_y_=0,
                            root_le_pos_z_=0,
                            section_1_length_=0,
                            section_2_length_=0,
                            section_3_length_=0,
                            section_4_length_=0,
                            section_5_length_=0,
                            section_1_profile_=0,
                            section_2_profile_=0,
                            section_3_profile_=0,
                            section_4_profile_=0,
                            section_5_profile_=0,
                            section_1_z_=0,
                            section_2_z_=0,
                            section_3_z_=0,
                            section_4_z_=0,
                            section_5_z_=0,
                            section_1_chord_=0,
                            section_2_chord_=0,
                            section_3_chord_=0,
                            section_4_chord_=0,
                            section_5_chord_=0,
                            section_1_pitch_angle_=0,
                            section_2_pitch_angle_=0,
                            section_3_pitch_angle_=0,
                            section_4_pitch_angle_=0,
                            section_5_pitch_angle_=0):
        self.propeller_number_text.setText(str(propeller_number_))

        self.root_le_position_x_text.setText(str(root_le_pos_x_))
        self.root_le_position_y_text.setText(str(root_le_pos_y_))
        self.root_le_position_z_text.setText(str(root_le_pos_z_))

        self.XYsymmetryCheck.setChecked(xy_mirror_)
        self.xy_mirror_ = xy_mirror_

        self.XZsymmetryCheck.setChecked(xz_mirror_)
        self.xz_mirror_ = xz_mirror_

        print("yz_mirror", yz_mirror_, xy_mirror_, xz_mirror_)
        self.YZsymmetryCheck.setChecked(yz_mirror_)
        self.yz_mirror_ = yz_mirror_

        self.hub_diameter_text.setText(str(rot_x_))
        self.hub_length_text.setText(str(rot_y_))
        self.pitch_angle_text.setText(str(rot_z_))

        self.section_1_length_text.setText(str(section_1_length_))
        self.section_1_profile_text.setText(str(section_1_profile_))
        self.section_1_z_text.setText(str(section_1_z_))
        self.section_1_chord_text.setText(str(section_1_chord_))
        self.section_1_pitch_angle_text.setText(str(section_1_pitch_angle_))

        self.section_2_length_text.setText(str(section_2_length_))
        self.section_2_profile_text.setText(str(section_2_profile_))
        self.section_2_z_text.setText(str(section_2_z_))
        self.section_2_chord_text.setText(str(section_2_chord_))
        self.section_2_pitch_angle_text.setText(str(section_2_pitch_angle_))

        self.section_3_x_text.setText(str(section_3_length_))
        self.section_3_y_text.setText(str(section_3_profile_))
        self.section_3_z_text.setText(str(section_3_z_))
        self.section_3_chord_text.setText(str(section_3_chord_))
        self.section_3_pitch_angle_text.setText(str(section_3_pitch_angle_))

        self.section_4_x_text.setText(str(section_4_length_))
        self.section_4_profile_text.setText(str(section_4_profile_))
        self.section_4_z_text.setText(str(section_4_z_))
        self.section_4_chord_text.setText(str(section_4_chord_))
        self.section_4_pitch_angle_text.setText(str(section_4_pitch_angle_))

        self.section_5_x_text.setText(str(section_5_length_))
        self.section_5_profile_text.setText(str(section_5_profile_))
        self.section_5_z_text.setText(str(section_5_z_))
        self.section_5_chord_text.setText(str(section_5_chord_))
        self.section_5_pitch_angle_text.setText(str(section_5_pitch_angle_))

    def init_action(self):
        self.parameters = {
            propeller: {
                self._name: {
                    propeller_number: int(self.propeller_number_text.text()),
                    hub_position_x: float(self.root_le_position_x_text.text()),
                    hub_position_y: float(self.root_le_position_y_text.text()),
                    hub_position_z: float(self.root_le_position_z_text.text()),
                    xy_mirror: self.xy_mirror_,
                    xz_mirror: self.xz_mirror_,
                    yz_mirror: self.yz_mirror_,
                    rotation_x: float(self.hub_diameter_text.text()),
                    rotation_y: float(self.hub_length_text.text()),
                    pitch_angle: int(self.pitch_angle_text.text()),
                    section_1_length: float(self.section_1_length_text.text()),
                    section_1_profile: self.section_1_profile_text.text(),
                    section_1_z: float(self.section_1_z_text.text()),
                    section_1_chord: float(self.section_1_chord_text.text()),
                    section_1_pitch_angle: float(self.section_1_pitch_angle_text.text()),
                    section_2_length: float(self.section_2_length_text.text()),
                    section_2_profile: self.section_2_profile_text.text(),
                    section_2_z: float(self.section_2_z_text.text()),
                    section_2_chord: float(self.section_2_chord_text.text()),
                    section_2_pitch_angle: float(self.section_2_pitch_angle_text.text()),
                    section_3_length: float(self.section_3_x_text.text()),
                    section_3_profile: self.section_3_y_text.text(),
                    section_3_z: float(self.section_3_z_text.text()),
                    section_3_chord: float(self.section_3_chord_text.text()),
                    section_3_pitch_angle: float(self.section_3_pitch_angle_text.text()),
                    section_4_length: float(self.section_4_x_text.text()),
                    section_4_profile: self.section_4_profile_text.text(),
                    section_4_z: float(self.section_4_z_text.text()),
                    section_4_chord: float(self.section_4_chord_text.text()),
                    section_4_pitch_angle: float(self.section_4_pitch_angle_text.text()),
                    section_5_length: float(self.section_5_x_text.text()),
                    section_5_profile: self.section_5_profile_text.text(),
                    section_5_z: float(self.section_5_z_text.text()),
                    section_5_chord: float(self.section_5_chord_text.text()),
                    section_5_pitch_angle: float(self.section_5_pitch_angle_text.text()),

                }}}
        try:
            database.update_propulsion_specifications(key=propeller, value=self.parameters[propeller])
        except:
            database.write_propulsion_specifications(self.parameters)
        write_propeller_objects(self._name)

        return self.parameters
