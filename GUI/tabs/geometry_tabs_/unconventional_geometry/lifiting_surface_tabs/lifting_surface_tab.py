from PyQt5.QtWidgets import *

from Utils.data_objects.lifting_surface_placeholder import *
from Utils.data_objects.placeholder import surface_curve_type
from Utils.database import database
from Utils.database.geometry.lifting_database import write_lifting_surface_objects, read_surface_data, \
    write_lifting_surface_to_objects, airfoil_profiles


class lifting_surface_tab(QWidget):
    def __init__(self, name="", surface_type_="", design_type_="", lifting_surface_pane=None):
        super().__init__()
        self.wing_profile_selection = None
        self._name = name
        self.surface_type_ = surface_type_
        self.design_type_ = design_type_
        self.xz_mirror_ = None
        self.xy_mirror_ = None
        self.yz_mirror_ = None
        self.surface_curve_type_ = None
        self.lifting_surface_pane = lifting_surface_pane

    def create_tab(self):
        self.create_widget()
        self.button = QPushButton('Save', self)
        self.button.clicked.connect(self.init_action)
        self.layout.addRow(self.button)
        self.setLayout(self.layout)
        self.zero_all_text_fields()
        return self

    def create_widget(self):

        self.inputArea = QTabWidget()
        self.layout = QFormLayout()

        self.wing_profile_label = QLabel("Airfoil")
        self.wing_profile_combo = QComboBox()
        self.wing_profile_combo.addItems(airfoil_profiles())
        self.wing_profile_combo.currentIndexChanged.connect(self.wing_profile_selectionChanged)
        self.layout.addRow(self.wing_profile_label, self.wing_profile_combo)

        self.rotation_label = QLabel("Rotation(XYZ)")
        self.layout.addRow(self.rotation_label)

        self.rotation_x_label = QLabel("X")
        self.rotation_x_text = QLineEdit()
        self.layout.addRow(self.rotation_x_label, self.rotation_x_text)

        self.rotation_y_label = QLabel("Y")
        self.rotation_y_text = QLineEdit()
        self.layout.addRow(self.rotation_y_label, self.rotation_y_text)

        self.rotation_z_label = QLabel("Z")
        self.rotation_z_text = QLineEdit()
        self.layout.addRow(self.rotation_z_label, self.rotation_z_text)

        self.typeCheck = QCheckBox("Curve Extrusion")
        self.typeCheck.toggled.connect(self.surfaceType_Checked)
        self.layout.addRow(self.typeCheck)

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
        self.inputArea.addTab(self.lifting_surface_pane, "Preview")
        ##################################################################################
        ##################################################################################

        self.layout = QFormLayout()
        self.section_1_label = QLabel("Section 1")
        self.layout.addRow(self.section_1_label)

        self.section_1_chord_label = QLabel("Chord Length")
        self.section_1_chord_text = QLineEdit()
        self.layout.addRow(self.section_1_chord_label, self.section_1_chord_text)

        self.section_1_x_label = QLabel("X")
        self.section_1_x_text = QLineEdit()
        self.layout.addRow(self.section_1_x_label, self.section_1_x_text)

        self.section_1_y_label = QLabel("Y")
        self.section_1_y_text = QLineEdit()
        self.layout.addRow(self.section_1_y_label, self.section_1_y_text)

        self.section_1_z_label = QLabel("Z")
        self.section_1_z_text = QLineEdit()
        self.layout.addRow(self.section_1_z_label, self.section_1_z_text)

        self.section_1_twist_label = QLabel("Twist(⁰)")
        self.section_1_twist_angle_text = QLineEdit()
        self.layout.addRow(self.section_1_twist_label, self.section_1_twist_angle_text)
        ###############################################################################
        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section One")
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

        self.section_2_x_label = QLabel("X")
        self.section_2_x_text = QLineEdit()
        self.layout.addRow(self.section_2_x_label, self.section_2_x_text)

        self.section_2_y_label = QLabel("Y")
        self.section_2_y_text = QLineEdit()
        self.layout.addRow(self.section_2_y_label, self.section_2_y_text)

        self.section_2_z_label = QLabel("Z")
        self.section_2_z_text = QLineEdit()
        self.layout.addRow(self.section_2_z_label, self.section_2_z_text)

        self.section_2_twist_label = QLabel("Twist(⁰)")
        self.section_2_twist_angle_text = QLineEdit()
        self.layout.addRow(self.section_2_twist_label, self.section_2_twist_angle_text)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Two")
        ###############################################################################
        ##################################################################################

        ##################################################################################

        self.layout = QFormLayout()
        self.section_3_label = QLabel("Section 3")
        self.layout.addRow(self.section_3_label)

        self.section_3_chord_label = QLabel("Chord Length")
        self.section_3_chord_text = QLineEdit()
        self.layout.addRow(self.section_3_chord_label, self.section_3_chord_text)

        self.section_3_x_label = QLabel("X")
        self.section_3_x_text = QLineEdit()
        self.layout.addRow(self.section_3_x_label, self.section_3_x_text)

        self.section_3_y_label = QLabel("Y")
        self.section_3_y_text = QLineEdit()
        self.layout.addRow(self.section_3_y_label, self.section_3_y_text)

        self.section_3_z_label = QLabel("Z")
        self.section_3_z_text = QLineEdit()
        self.layout.addRow(self.section_3_z_label, self.section_3_z_text)

        self.section_3_twist_label = QLabel("Twist(⁰)")
        self.section_3_twist_angle_text = QLineEdit()
        self.layout.addRow(self.section_3_twist_label, self.section_3_twist_angle_text)
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

        self.section_4_x_label = QLabel("X")
        self.section_4_x_text = QLineEdit()
        self.layout.addRow(self.section_4_x_label, self.section_4_x_text)

        self.section_4_y_label = QLabel("Y")
        self.section_4_y_text = QLineEdit()
        self.layout.addRow(self.section_4_y_label, self.section_4_y_text)

        self.section_4_z_label = QLabel("Z")
        self.section_4_z_text = QLineEdit()
        self.layout.addRow(self.section_4_z_label, self.section_4_z_text)

        self.section_4_twist_label = QLabel("Twist(⁰)")
        self.section_4_twist_angle_text = QLineEdit()
        self.layout.addRow(self.section_4_twist_label, self.section_4_twist_angle_text)
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

        self.section_5_x_label = QLabel("X")
        self.section_5_x_text = QLineEdit()
        self.layout.addRow(self.section_5_x_label, self.section_5_x_text)

        self.section_5_y_label = QLabel("Y")
        self.section_5_y_text = QLineEdit()
        self.layout.addRow(self.section_5_y_label, self.section_5_y_text)

        self.section_5_z_label = QLabel("Z")
        self.section_5_z_text = QLineEdit()
        self.layout.addRow(self.section_5_z_label, self.section_5_z_text)

        self.section_5_twist_label = QLabel("Twist(⁰)")
        self.section_5_twist_angle_text = QLineEdit()
        self.layout.addRow(self.section_5_twist_label, self.section_5_twist_angle_text)
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

    def surfaceType_Checked(self, button):
        self.surface_curve_type_ = button

    def xz_mirror_Checked(self, button):
        self.xz_mirror_ = button

    def xy_mirror_Checked(self, button):
        self.xy_mirror_ = button

    def yz_mirror_Checked(self, button):
        self.yz_mirror_ = button

    def zero_all_text_fields(self):
        try:
            profile_, surfaceType_, xz_mirror_, xy_mirror_, yz_mirror_, rot_x_, rot_y_, rot_z_, root_le_pos_x_, root_le_pos_y_, root_le_pos_z_, \
            section_1_x_, section_2_x_, section_3_x_, section_4_x_, section_5_x_, \
            section_1_y_, section_2_y_, section_3_y_, section_4_y_, section_5_y_, \
            section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_, \
            section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, \
            section_5_chord_, section_1_twist_angle_, section_2_twist_angle_, \
            section_3_twist_angle_, section_4_twist_angle_, section_5_twist_angle_ = read_surface_data(self._name)

            self.show_default_values(profile_=profile_,
                                     surfaceType_=surfaceType_,
                                     xz_mirror_=xz_mirror_,
                                     xy_mirror_=xy_mirror_,
                                     yz_mirror_=yz_mirror_,
                                     rot_x_=rot_x_,
                                     rot_y_=rot_y_,
                                     rot_z_=rot_z_,
                                     root_le_pos_x_=root_le_pos_x_,
                                     root_le_pos_y_=root_le_pos_y_,
                                     root_le_pos_z_=root_le_pos_z_,
                                     section_1_x_=section_1_x_,
                                     section_2_x_=section_2_x_,
                                     section_3_x_=section_3_x_,
                                     section_4_x_=section_4_x_,
                                     section_5_x_=section_5_x_,
                                     section_1_y_=section_1_y_,
                                     section_2_y_=section_2_y_,
                                     section_3_y_=section_3_y_,
                                     section_4_y_=section_4_y_,
                                     section_5_y_=section_5_y_,
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
                                     section_1_twist_angle_=section_1_twist_angle_,
                                     section_2_twist_angle_=section_2_twist_angle_,
                                     section_3_twist_angle_=section_3_twist_angle_,
                                     section_4_twist_angle_=section_4_twist_angle_,
                                     section_5_twist_angle_=section_5_twist_angle_)
        except:
            self.show_default_values()

    def show_default_values(self,
                            name="",
                            profile_=airfoil_profiles()[0],
                            surfaceType_=False,
                            rot_x_=0,
                            rot_y_=0,
                            rot_z_=0,
                            xz_mirror_=False,
                            xy_mirror_=False,
                            yz_mirror_=False,
                            root_le_pos_x_=0,
                            root_le_pos_y_=0,
                            root_le_pos_z_=0,
                            section_1_x_=0,
                            section_2_x_=0,
                            section_3_x_=0,
                            section_4_x_=0,
                            section_5_x_=0,
                            section_1_y_=0,
                            section_2_y_=0,
                            section_3_y_=0,
                            section_4_y_=0,
                            section_5_y_=0,
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
                            section_1_twist_angle_=0,
                            section_2_twist_angle_=0,
                            section_3_twist_angle_=0,
                            section_4_twist_angle_=0,
                            section_5_twist_angle_=0):

        self.root_le_position_x_text.setText(str(root_le_pos_x_))
        self.root_le_position_y_text.setText(str(root_le_pos_y_))
        self.root_le_position_z_text.setText(str(root_le_pos_z_))

        self.XYsymmetryCheck.setChecked(xy_mirror_)
        self.xy_mirror_ = xy_mirror_
        if surfaceType_ is None:
            self.typeCheck.setChecked(False)
            self.surface_curve_type_ = False
        else:
            self.typeCheck.setChecked(surfaceType_)
            self.surface_curve_type_ = surfaceType_

        self.XZsymmetryCheck.setChecked(xz_mirror_)
        self.xz_mirror_ = xz_mirror_

        self.wing_profile_combo.setCurrentIndex(airfoil_profiles().index(profile_) if profile_ is not None else 1)

        self.YZsymmetryCheck.setChecked(yz_mirror_)
        self.yz_mirror_ = yz_mirror_

        self.rotation_x_text.setText(str(rot_x_))
        self.rotation_y_text.setText(str(rot_y_))
        self.rotation_z_text.setText(str(rot_z_))

        self.section_1_x_text.setText(str(section_1_x_))
        self.section_1_y_text.setText(str(section_1_y_))
        self.section_1_z_text.setText(str(section_1_z_))
        self.section_1_chord_text.setText(str(section_1_chord_))
        self.section_1_twist_angle_text.setText(str(section_1_twist_angle_))

        self.section_2_x_text.setText(str(section_2_x_))
        self.section_2_y_text.setText(str(section_2_y_))
        self.section_2_z_text.setText(str(section_2_z_))
        self.section_2_chord_text.setText(str(section_2_chord_))
        self.section_2_twist_angle_text.setText(str(section_2_twist_angle_))

        self.section_3_x_text.setText(str(section_3_x_))
        self.section_3_y_text.setText(str(section_3_y_))
        self.section_3_z_text.setText(str(section_3_z_))
        self.section_3_chord_text.setText(str(section_3_chord_))
        self.section_3_twist_angle_text.setText(str(section_3_twist_angle_))

        self.section_4_x_text.setText(str(section_4_x_))
        self.section_4_y_text.setText(str(section_4_y_))
        self.section_4_z_text.setText(str(section_4_z_))
        self.section_4_chord_text.setText(str(section_4_chord_))
        self.section_4_twist_angle_text.setText(str(section_4_twist_angle_))

        self.section_5_x_text.setText(str(section_5_x_))
        self.section_5_y_text.setText(str(section_5_y_))
        self.section_5_z_text.setText(str(section_5_z_))
        self.section_5_chord_text.setText(str(section_5_chord_))
        self.section_5_twist_angle_text.setText(str(section_5_twist_angle_))

    def init_action(self):
        self.accept_inputs()
        self.parameters = {
            lifting_surface: {
                str(self._name): {
                    design_type: self.design_type_,
                    surface_type: self.surface_type_,
                    root_le_position_x: float(self.root_le_position_x_text.text()),
                    root_le_position_y: float(self.root_le_position_y_text.text()),
                    root_le_position_z: float(self.root_le_position_z_text.text()),
                    xy_mirror: self.xy_mirror_,
                    xz_mirror: self.xz_mirror_,
                    yz_mirror: self.yz_mirror_,
                    profile: str(self.wing_profile_selection),
                    surface_curve_type: self.surface_curve_type_,
                    rotation_x: float(self.rotation_x_text.text()),
                    rotation_y: float(self.rotation_y_text.text()),
                    rotation_z: float(self.rotation_z_text.text()),
                    section_1_x: float(self.section_1_x_text.text()),
                    section_1_y: float(self.section_1_y_text.text()),
                    section_1_z: float(self.section_1_z_text.text()),
                    section_1_chord: float(self.section_1_chord_text.text()),
                    section_1_twist_angle: float(self.section_1_twist_angle_text.text()),
                    section_2_x: float(self.section_2_x_text.text()),
                    section_2_y: float(self.section_2_y_text.text()),
                    section_2_z: float(self.section_2_z_text.text()),
                    section_2_chord: float(self.section_2_chord_text.text()),
                    section_2_twist_angle: float(self.section_2_twist_angle_text.text()),
                    section_3_x: float(self.section_3_x_text.text()),
                    section_3_y: float(self.section_3_y_text.text()),
                    section_3_z: float(self.section_3_z_text.text()),
                    section_3_chord: float(self.section_3_chord_text.text()),
                    section_3_twist_angle: float(self.section_3_twist_angle_text.text()),
                    section_4_x: float(self.section_4_x_text.text()),
                    section_4_y: float(self.section_4_y_text.text()),
                    section_4_z: float(self.section_4_z_text.text()),
                    section_4_chord: float(self.section_4_chord_text.text()),
                    section_4_twist_angle: float(self.section_4_twist_angle_text.text()),
                    section_5_x: float(self.section_5_x_text.text()),
                    section_5_y: float(self.section_5_y_text.text()),
                    section_5_z: float(self.section_5_z_text.text()),
                    section_5_chord: float(self.section_5_chord_text.text()),
                    section_5_twist_angle: float(self.section_5_twist_angle_text.text()),

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

