from PyQt5.QtWidgets import *

from Utils.data_objects.boom_placeholders import *
from Utils.data_objects.placeholder import design_type
from Utils.database import database
from Utils.database.geometry.boom_database import write_boom_objects, read_boom_data, write_boom_to_objects
from Utils.maths.geometry_math_tools import get_fuselage_length, get_diameter


class boom_tab(QWidget):
    def __init__(self, name="", boom_type_="", design_type_=""):
        super().__init__()
        self.tab_ = self
        self._name = name
        self.boom_type_ = boom_type_
        self.design_type_ = design_type_
        self.cockpitCheckMark = None
        self.xz_mirror_ = None
        self.xy_mirror_ = None
        self.yz_mirror_ = None
        self.inputArea = QTabWidget()
        ##################################################################################

        self.layout = QFormLayout()
        self.length_label = QLabel("Length")
        self.length_text = QLabel("")
        self.layout.addRow(QLabel("Design Overview"))
        self.layout.addRow(self.length_label, self.length_text)

        self.diameter_label = QLabel("Diameter")
        self.diameter_text = QLabel("")
        self.layout.addRow(self.diameter_label, self.diameter_text)

        self.XZsymmetryCheck = QCheckBox("Mirror Boom About XZ Plane")
        self.XZsymmetryCheck.toggled.connect(self.xz_mirror_Checked)
        self.layout.addRow(self.XZsymmetryCheck)
        self.YZsymmetryCheck = QCheckBox("Mirror Boom About YZ Plane")
        self.YZsymmetryCheck.toggled.connect(self.yz_mirror_Checked)
        self.layout.addRow(self.YZsymmetryCheck)
        self.XYsymmetryCheck = QCheckBox("Mirror Boom About XY Plane")
        self.XYsymmetryCheck.toggled.connect(self.xy_mirror_Checked)
        self.layout.addRow(self.XYsymmetryCheck)

        self.root_le_position_label = QLabel("Root Position")
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
        ###################################################
        ##########################################################################
        ##################################################################################
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Incase of Cylindrical Profile Radius as Both Height and Width"))
        self.nose_width_label = QLabel("Nose Width")
        self.nose_width_text = QLineEdit()
        self.layout.addRow(self.nose_width_label, self.nose_width_text)

        self.nose_height_label = QLabel("Nose Height")
        self.nose_height_text = QLineEdit()
        self.layout.addRow(self.nose_height_label, self.nose_height_text)

        self.nose_profile_label = QLabel("Nose Profile")
        self.nose_profile_combo = QComboBox()
        self.nose_profile_combo.addItems(fuselage_profiles)
        self.nose_profile_selection = None
        self.nose_profile_combo.currentIndexChanged.connect(self.nose_profile_selectionChanged)
        self.layout.addRow(self.nose_profile_label, self.nose_profile_combo)

        self.nose_length_label = QLabel("Nose Length")
        self.nose_length_text = QLineEdit()
        self.layout.addRow(self.nose_length_label, self.nose_length_text)

        self.nose_position_z_label = QLabel("Nose Position Z")
        self.nose_position_z_text = QLineEdit()
        self.layout.addRow(self.nose_position_z_label, self.nose_position_z_text)

        self.nose_tip_position_label = QLabel("Nose Tip Position(Z)")
        self.nose_tip_position_text = QLineEdit()
        self.layout.addRow(self.nose_tip_position_label, self.nose_tip_position_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Nose Design")
        ##############################################################################
        self.cockpitCheck = QCheckBox("Add Cockpit To Design")
        self.cockpitCheck.toggled.connect(self.cockPitChecked)
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Cockpit"))
        self.cockpit_height_label = QLabel("Cockpit Height")
        self.cockpit_height_text = QLineEdit()
        self.layout.addRow(self.cockpitCheck)
        self.layout.addRow(self.cockpit_height_label, self.cockpit_height_text)
        ############################################################################
        self.cockpit_width_label = QLabel(" Cockpit Width")
        self.cockpit_width_text = QLineEdit()
        self.layout.addRow(self.cockpit_width_label, self.cockpit_width_text)
        ##############################################################################

        self.cockpit_length_label = QLabel("Cockpit Length")
        self.cockpit_length_text = QLineEdit()
        self.layout.addRow(self.cockpit_length_label, self.cockpit_length_text)

        ##########################################################################################
        self.cockpit_position_x_label = QLabel(" Cockpit(1)Position X")
        self.cockpit_position_x_text = QLineEdit()
        self.layout.addRow(self.cockpit_position_x_label, self.cockpit_position_x_text)

        self.cockpit_position_y_label = QLabel(" Cockpit(1)Position Y")
        self.cockpit_position_y_text = QLineEdit()
        self.layout.addRow(self.cockpit_position_y_label, self.cockpit_position_y_text)

        self.cockpit_position_z_label = QLabel(" Cockpit(1)Position Z")
        self.cockpit_position_z_text = QLineEdit()
        self.layout.addRow(self.cockpit_position_z_label, self.cockpit_position_z_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Cockpit Design")

        ################################################################################
        self.layout = QFormLayout()
        self.section_1_width_label = QLabel("Section (1) Width")
        self.section_1_width_text = QLineEdit()
        self.layout.addRow(self.section_1_width_label, self.section_1_width_text)
        ##############################################################################
        self.section_1_height_label = QLabel("Section (1) Height")
        self.section_1_height_text = QLineEdit()
        self.layout.addRow(self.section_1_height_label, self.section_1_height_text)

        self.section_1_profile_label = QLabel("Section (1) Profile")
        self.section_1_profile_combo = QComboBox()
        self.section_1_profile_combo.addItems(fuselage_profiles)
        self.section_1_profile_selection = None
        self.section_1_profile_combo.currentIndexChanged.connect(self.section_1_profile_selectionChanged)
        self.layout.addRow(self.section_1_profile_label, self.section_1_profile_combo)

        self.section_1_length_label = QLabel("Section(1) Length")
        self.section_1_length_text = QLineEdit()
        self.layout.addRow(self.section_1_length_label, self.section_1_length_text)

        ##########################################################################################

        self.section_1_position_z_label = QLabel(" Section(1)Position Z")
        self.section_1_position_z_text = QLineEdit()
        self.layout.addRow(self.section_1_position_z_label, self.section_1_position_z_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section One Design")
        ##############################################################################
        self.layout = QFormLayout()
        self.section_2_width_label = QLabel("Section (2) Width")
        self.section_2_width_text = QLineEdit()
        self.layout.addRow(self.section_2_width_label, self.section_2_width_text)
        ##############################################################################
        self.section_2_height_label = QLabel("Section (2) Height")
        self.section_2_height_text = QLineEdit()
        self.layout.addRow(self.section_2_height_label, self.section_2_height_text)

        self.section_2_profile_label = QLabel("Section (2) Profile")
        self.section_2_profile_combo = QComboBox()
        self.section_2_profile_combo.addItems(fuselage_profiles)
        self.section_2_profile_selection = None
        self.section_2_profile_combo.currentIndexChanged.connect(self.section_3_profile_selectionChanged)
        self.layout.addRow(self.section_2_profile_label, self.section_2_profile_combo)

        self.section_2_length_label = QLabel("Section (2) Length")
        self.section_2_length_text = QLineEdit()
        self.layout.addRow(self.section_2_length_label, self.section_2_length_text)

        ##########################################################################################
        self.section_2_position_z_label = QLabel(" Section(2)Position Z")
        self.section_2_position_z_text = QLineEdit()
        self.layout.addRow(self.section_2_position_z_label, self.section_2_position_z_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Two Design")
        ##############################################################################
        self.layout = QFormLayout()
        self.section_3_width_label = QLabel("Section (3) radius")
        self.section_3_width_text = QLineEdit()
        self.layout.addRow(self.section_3_width_label, self.section_3_width_text)
        ##############################################################################

        self.section_3_height_label = QLabel("Section (2) Height")
        self.section_3_height_text = QLineEdit()
        self.layout.addRow(self.section_3_height_label, self.section_3_height_text)

        self.section_3_profile_label = QLabel("Section (3) Profile")
        self.section_3_profile_combo = QComboBox()
        self.section_3_profile_combo.addItems(fuselage_profiles)
        self.section_3_profile_selection = None
        self.section_3_profile_combo.currentIndexChanged.connect(self.section_3_profile_selectionChanged)
        self.layout.addRow(self.section_3_profile_label, self.section_3_profile_combo)

        self.section_3_length_label = QLabel("Section (3) Length")
        self.section_3_length_text = QLineEdit()
        self.layout.addRow(self.section_3_length_label, self.section_3_length_text)

        ##########################################################################################
        self.section_3_position_z_label = QLabel(" Section(3)Position Z")
        self.section_3_position_z_text = QLineEdit()
        self.layout.addRow(self.section_3_position_z_label, self.section_3_position_z_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Section Three Design")
        ##############################################################################

        self.layout = QFormLayout()

        self.tail_profile_label = QLabel("Tail Profile")
        self.tail_profile_combo = QComboBox()
        self.tail_profile_combo.addItems(fuselage_profiles)
        self.tail_profile_selection = None
        self.tail_profile_combo.currentIndexChanged.connect(self.tail_profile_selectionChanged)
        self.layout.addRow(self.tail_profile_label, self.tail_profile_combo)

        self.tail_position_z_label = QLabel("Tail Position Z")
        self.tail_position_z_text = QLineEdit()
        self.layout.addRow(self.tail_position_z_label, self.tail_position_z_text)
        ##############################################################################

        ##############################################################################
        self.tail_width_label = QLabel("Tail Width")
        self.tail_width_text = QLineEdit()
        self.layout.addRow(self.tail_width_label, self.tail_width_text)

        self.tail_height_label = QLabel("Tail Height")
        self.tail_height_text = QLineEdit()
        self.layout.addRow(self.tail_height_label, self.tail_height_text)
        ##############################################################################

        self.tail_length_label = QLabel("Tail Length")
        self.tail_length_text = QLineEdit()
        self.layout.addRow(self.tail_length_label, self.tail_length_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Tail Design")

        self.layout = QFormLayout()
        self.tip_width_label = QLabel("Tip width")
        self.tip_width_text = QLineEdit()
        self.layout.addRow(self.tip_width_label, self.tip_width_text)
        self.tip_height_label = QLabel("Tip height")
        self.tip_height_text = QLineEdit()
        self.layout.addRow(self.tip_height_label, self.tip_height_text)

        self.tail_tip_position_label = QLabel("Tail Tip Position(Z)")
        self.tail_tip_position_text = QLineEdit()
        self.layout.addRow(self.tail_tip_position_label, self.tail_tip_position_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Tip Design")
        layout = QFormLayout()
        layout.addWidget(self.inputArea)
        self.zero_all_textfields()
        self.setLayout(layout)

        ##########################################################################################

    def cockPitChecked(self, button):
        self.cockpitCheckMark = button

    def xz_mirror_Checked(self, button):
        self.xz_mirror_ = button

    def xy_mirror_Checked(self, button):
        self.xy_mirror_ = button

    def yz_mirror_Checked(self, button):
        self.yz_mirror_ = button

    def get_tab_widget(self):
        self.create_widget()
        return self.inputArea

    def zero_all_textfields(self):
        try:
            tail_profile_, nose_profile_, \
            section_1_profile_, section_2_profile_, \
            section_3_profile_, \
            cockPitDesign, xz_mirror_, xy_mirror_, yz_mirror_, \
            root_position_x_, root_position_y_, root_position_z_, \
            nose_tip_position_, tail_tip_position_, \
            fuselage_diameter, fuselage_length, nose_width_, nose_height_, \
            cockpit_height_, cockpit_length_, cockpit_width_, \
            cockpit_position_x_, cockpit_position_y_, cockpit_position_z_, \
            nose_length_, nose_position_z_, section_1_width_, section_1_height_, \
            section_1_length_, section_1_position_z_, \
            section_2_width_, section_2_height_, section_2_length_, \
            section_2_position_z_, \
            section_3_width_, section_3_height_, \
            section_3_length_, \
            section_3_position_z_, \
            tip_width_, tail_height_, tail_width_, tip_height_, \
            tail_length_, tail_position_z_, \
                = read_boom_data(self._name)

            self.show_default_values(tail_profile_, nose_profile_,
                                     section_1_profile_, section_2_profile_,
                                     section_3_profile_, cockPitDesign,
                                     xz_mirror_, xy_mirror_, yz_mirror_,
                                     root_position_x_, root_position_y_, root_position_z_,
                                     nose_tip_position_, tail_tip_position_, fuselage_diameter, fuselage_length,
                                     cockpit_height_, cockpit_length_, cockpit_width_,
                                     cockpit_position_x_, cockpit_position_y_, cockpit_position_z_, nose_width_,
                                     nose_height_,
                                     nose_length_, nose_position_z_, section_1_width_, section_1_height_,
                                     section_1_length_, section_1_position_z_,
                                     section_2_width_, section_2_height_, section_2_length_,
                                     section_2_position_z_,
                                     section_3_width_, section_3_height_,
                                     section_3_length_,
                                     section_3_position_z_,
                                     tip_width_, tail_height_, tail_width_, tip_height_,
                                     tail_length_, tail_position_z_)
        except Exception as e:
            print(e)
            self.show_default_values()

        ############################################################################

    def show_default_values(self, tail_profile_=fuselage_profiles[0], nose_profile_=fuselage_profiles[0],
                            section_1_profile_=fuselage_profiles[0], section_2_profile_=fuselage_profiles[0],
                            section_3_profile_=fuselage_profiles[0], cockPitDesign=True,
                            xz_mirror_=False, xy_mirror_=False, yz_mirror_=False, root_position_x_=0,

                            root_position_y_=0, root_position_z_=0,
                            nose_tip_position_=0, tail_tip_position_=0, fuselage_diameter=0,
                            fuselage_length=0,
                            cockpit_height_=0, cockpit_length_=0, cockpit_width_=0,
                            cockpit_position_x_=0, cockpit_position_y_=0, cockpit_position_z_=0,
                            nose_width_=0, nose_height_=0, nose_length_=0, nose_position_z_=0,
                            section_1_width_=0, section_1_height_=0, section_1_length_=0, section_1_position_z_=0,
                            section_2_width_=0, section_2_height_=0, section_2_length_=0, section_2_position_z_=0,
                            section_3_width_=0, section_3_height_=0, section_3_length_=0, section_3_position_z_=0,
                            tip_width_=0, tail_height_=0, tail_width_=0, tip_height_=0, tail_length_=0,
                            tail_position_z_=0, ):

        self.length_text.setText(str(fuselage_length))
        self.diameter_text.setText(str(fuselage_diameter))

        self.XYsymmetryCheck.setChecked(xy_mirror_)
        self.xy_mirror_ = xy_mirror_

        self.XZsymmetryCheck.setChecked(xz_mirror_)
        self.xz_mirror_ = xz_mirror_

        self.YZsymmetryCheck.setChecked(yz_mirror_)
        self.yz_mirror_ = yz_mirror_

        self.root_le_position_x_text.setText(str(root_position_x_))
        self.root_le_position_y_text.setText(str(root_position_y_))
        self.root_le_position_z_text.setText(str(root_position_z_))

        self.cockpit_height_text.setText(str(cockpit_height_))
        self.cockpit_length_text.setText(str(cockpit_length_))
        self.cockpit_width_text.setText(str(cockpit_width_))
        self.cockpitCheck.setChecked(cockPitDesign)
        self.cockpitCheckMark = cockPitDesign

        self.cockpit_position_x_text.setText(str(cockpit_position_x_))
        self.cockpit_position_y_text.setText(str(cockpit_position_y_))
        self.cockpit_position_z_text.setText(str(cockpit_position_z_))

        self.nose_width_text.setText(str(nose_width_))
        self.nose_height_text.setText(str(nose_height_))
        self.nose_length_text.setText(str(nose_length_))
        self.nose_profile_combo.setCurrentIndex(fuselage_profiles.index(nose_profile_))
        self.nose_position_z_text.setText(str(nose_position_z_))

        self.nose_tip_position_text.setText(str(nose_tip_position_))
        self.tail_tip_position_text.setText(str(tail_tip_position_))

        self.section_1_width_text.setText(str(section_1_width_))
        self.section_1_height_text.setText(str(section_1_height_))
        self.section_1_profile_combo.setCurrentIndex(fuselage_profiles.index(section_1_profile_))
        self.section_1_length_text.setText(str(section_1_length_))
        self.section_1_position_z_text.setText(str(section_1_position_z_))

        ##########################################################################################
        self.section_2_width_text.setText(str(section_2_width_))
        self.section_2_height_text.setText(str(section_2_height_))
        self.section_2_profile_combo.setCurrentIndex(fuselage_profiles.index(section_2_profile_))
        self.section_2_length_text.setText(str(section_2_length_))
        self.section_2_position_z_text.setText(str(section_2_position_z_))
        ##########################################################################################

        self.section_3_width_text.setText(str(section_3_width_))
        self.section_3_height_text.setText(str(section_3_height_))
        self.section_3_profile_combo.setCurrentIndex(fuselage_profiles.index(section_3_profile_))
        self.section_3_length_text.setText(str(section_3_length_))
        self.section_3_position_z_text.setText(str(section_3_position_z_))

        self.tail_profile_combo.setCurrentIndex(fuselage_profiles.index(tail_profile_))
        self.tip_width_text.setText(str(tip_width_))
        self.tail_width_text.setText(str(tail_width_))
        self.tip_height_text.setText(str(tip_height_))
        self.tail_height_text.setText(str(tail_height_))
        self.tail_length_text.setText(str(tail_length_))
        self.tail_position_z_text.setText(str(tail_position_z_))

    def init_action(self):
        self.accept_inputs()

        self.parameters = {
            boom: {
                self._name: {
                    design_type: self.design_type_,
                    boom_type: self.boom_type_,
                    boom_length: float(

                        get_fuselage_length([float(self.nose_length_text.text()),
                                             float(self.section_1_length_text.text()),
                                             float(self.section_2_length_text.text()),
                                             float(self.section_3_length_text.text()),
                                             float(self.tail_length_text.text())])),
                    boom_diameter: float(
                        get_diameter([float(self.nose_width_text.text()), float(self.section_1_width_text.text()),
                                      float(self.section_2_width_text.text()),
                                      float(self.section_3_width_text.text()),
                                      float(self.tail_width_text.text()), float(self.tip_width_text.text())])),
                    nose_width: float(self.nose_width_text.text()),
                    nose_height: float(self.nose_height_text.text()),
                    nose_profile:  str(self.nose_profile_selection),
                    nose_length: float(self.nose_length_text.text()),
                    nose_position_z: float(self.nose_position_z_text.text()),
                    nose_tip_position: float(self.nose_tip_position_text.text()),
                    design_cockpit: self.cockpitCheckMark,
                    xy_mirror: self.xy_mirror_,
                    xz_mirror: self.xz_mirror_,
                    yz_mirror: self.yz_mirror_,
                    root_position_x: float(self.root_le_position_x_text.text()),
                    root_position_y: float(self.root_le_position_y_text.text()),
                    root_position_z: float(self.root_le_position_z_text.text()),
                    section_1_length: float(self.section_1_length_text.text()),
                    section_1_width: float(self.section_1_width_text.text()),
                    section_1_height: float(self.section_1_height_text.text()),
                    section_1_profile: str(self.section_1_profile_selection),
                    section_1_position_z: float(self.section_1_position_z_text.text()),
                    section_2_length: float(self.section_2_length_text.text()),
                    section_2_width: float(self.section_2_width_text.text()),
                    section_2_height: float(self.section_2_height_text.text()),
                    section_2_profile:  str(self.section_2_profile_selection),
                    section_2_position_z: float(self.section_2_position_z_text.text()),
                    section_3_length: float(self.section_3_length_text.text()),
                    section_3_width: float(self.section_3_width_text.text()),
                    section_3_height: float(self.section_3_height_text.text()),
                    section_3_profile:  str(self.section_3_profile_selection),
                    section_3_position_z: float(self.section_3_position_z_text.text()),
                    tip_width: float(self.tip_width_text.text()),
                    tip_height: float(self.tip_height_text.text()),
                    tail_profile:  str(self.tail_profile_selection),
                    tail_tip_position: float(self.tail_tip_position_text.text()),
                    tail_length: float(self.tail_length_text.text()),
                    tail_width: float(self.tail_width_text.text()),
                    tail_height: float(self.tail_height_text.text()),
                    tail_position_z: float(self.tail_position_z_text.text()),

                }}}
        if self.cockpitCheckMark == True:
            self.parameters[boom][self._name].update({
                cockpit_height: float(self.cockpit_height_text.text()),
                cockpit_width: float(self.cockpit_width_text.text()),
                cockpit_length: float(self.cockpit_length_text.text()),
                cockpit_position_x: float(self.cockpit_position_x_text.text()),
                cockpit_position_y: float(self.cockpit_position_y_text.text()),
                cockpit_position_z: float(self.cockpit_position_z_text.text()),
            })
        else:
            self.parameters[boom][self._name].update({
                cockpit_height: float(0),
                cockpit_width: float(0),
                cockpit_length: float(0),
                cockpit_position_x: float(0),
                cockpit_position_y: float(0),
                cockpit_position_z: float(0),
            })

        try:
            database.update_aircraft_specifications(key=boom, value=self.parameters[boom])
        except:
            database.write_aircraft_specification(self.parameters)
        write_boom_objects(value=self._name)
        write_boom_to_objects(boom_name=self._name, design_type_=self.design_type_,
                              boom_type_=self.boom_type_)

        return self.parameters

    def section_1_profile_selectionChanged(self, i):
        self.section_1_profile_selection = fuselage_profiles[i]

    def section_2_profile_selectionChanged(self, i):
        self.section_2_profile_selection = fuselage_profiles[i]

    def section_3_profile_selectionChanged(self, i):
        self.section_3_profile_selection = fuselage_profiles[i]

    def nose_profile_selectionChanged(self, i):
        self.nose_profile_selection = fuselage_profiles[i]

    def tail_profile_selectionChanged(self, i):
        self.tail_profile_selection = fuselage_profiles[i]

    def accept_inputs(self):
        if self.tail_profile_selection is None:
            self.tail_profile_selection = fuselage_profiles[self.tail_profile_combo.currentIndex()]
        if self.nose_profile_selection is None:
            self.nose_profile_selection = fuselage_profiles[self.nose_profile_combo.currentIndex()]
        if self.section_3_profile_selection is None:
            self.section_3_profile_selection = fuselage_profiles[self.section_3_profile_combo.currentIndex()]
        if self.section_2_profile_selection is None:
            self.section_2_profile_selection = fuselage_profiles[self.section_2_profile_combo.currentIndex()]
        if self.section_1_profile_selection is None:
            self.section_1_profile_selection = fuselage_profiles[self.section_1_profile_combo.currentIndex()]
