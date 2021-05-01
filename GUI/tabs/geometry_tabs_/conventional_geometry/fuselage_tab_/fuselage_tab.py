from PyQt5.QtWidgets import *

from Utils.data_objects.boom_placeholders import *
from Utils.data_objects.placeholder import design_type
from Utils.database import database
from Utils.database.geometry.boom_database import read_boom_data, write_boom_objects, write_boom_to_objects
from Utils.maths.geometry_math_tools import get_diameter, get_fuselage_length


class fuselage_tab(QWidget):
    def __init__(self, text="", boom_type_="", design_type_=""):
        super().__init__()
        self.cockpitCheckMark = None
        self.text = text
        self.boom_type_ = boom_type_
        self.design_type_ = design_type_
        self.inputArea = QTabWidget()
        ##################################################################################
        self.tab_ = self
        self.layout = QFormLayout()
        self.length_label = QLabel("Length")
        self.length_text = QLabel("")
        self.layout.addRow(QLabel("Design Overview"))
        self.layout.addRow(self.length_label, self.length_text)

        self.diameter_label = QLabel("Diameter")
        self.diameter_text = QLabel("")
        self.layout.addRow(self.diameter_label, self.diameter_text)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Design Overview")
        ###################################################
        ##########################################################################
        ##################################################################################
        self.layout = QFormLayout()
        self.nose_radius_label = QLabel("Nose Radius")
        self.nose_radius_text = QLineEdit()
        self.layout.addRow(self.nose_radius_label, self.nose_radius_text)

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
        self.section_1_radius_label = QLabel("Section (1) Radius")
        self.section_1_radius_text = QLineEdit()
        self.layout.addRow(self.section_1_radius_label, self.section_1_radius_text)
        ##############################################################################

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
        self.section_2_radius_label = QLabel("Section (2) Radius")
        self.section_2_radius_text = QLineEdit()
        self.layout.addRow(self.section_2_radius_label, self.section_2_radius_text)
        ##############################################################################

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
        self.section_3_radius_label = QLabel("Section (3) radius")
        self.section_3_radius_text = QLineEdit()
        self.layout.addRow(self.section_3_radius_label, self.section_3_radius_text)
        ##############################################################################

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
        self.tail_position_z_label = QLabel("Tail Position Z")
        self.tail_position_z_text = QLineEdit()
        self.layout.addRow(self.tail_position_z_label, self.tail_position_z_text)
        ##############################################################################

        ##############################################################################
        self.tail_radius_label = QLabel("Tail Radius")
        self.tail_radius_text = QLineEdit()
        self.layout.addRow(self.tail_radius_label, self.tail_radius_text)
        ##############################################################################

        self.tail_length_label = QLabel("Tail Length")
        self.tail_length_text = QLineEdit()

        self.tip_radius_label = QLabel("Tip Radius")
        self.tip_radius_text = QLineEdit()

        self.tail_tip_position_label = QLabel("Tail Tip Position(Z)")
        self.tail_tip_position_text = QLineEdit()
        self.layout.addRow(self.tail_tip_position_label, self.tail_tip_position_text)

        self.layout.addRow(self.tip_radius_label, self.tip_radius_text)
        self.layout.addRow(self.tail_length_label, self.tail_length_text)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.inputArea.addTab(widget, "Tail Design")
        layout = QFormLayout()
        layout.addRow(self.inputArea)
        self.setLayout(layout)
        self.zero_all_textfields()

        ##########################################################################################

    def cockPitChecked(self, button):
        self.cockpitCheckMark = button

    def get_tab_widget(self):
        self.create_widget()
        return self.inputArea

    def zero_all_textfields(self):
        try:
            cockPitDesign, nose_tip_position_, tail_tip_position_, \
            fuselage_diameter, fuselage_length, nose_radius_, \
            cockpit_height_, cockpit_length_, cockpit_width_, \
            cockpit_position_x_, cockpit_position_y_, cockpit_position_z_, \
            nose_length_, nose_position_z_, section_1_radius_, \
            section_1_length_, section_1_position_z_, \
            section_2_radius_, section_2_length_, \
            section_2_position_z_, \
            section_3_radius_, \
            section_3_length_, \
            section_3_position_z_, \
            tip_raidus_, tail_radius_, \
            tail_length_, tail_position_z_ = \
                read_boom_data(self.text)
            self.show_default_values(cockPitDesign,
                                     nose_tip_position_, tail_tip_position_, fuselage_diameter, fuselage_length,
                                     cockpit_height_, cockpit_length_, cockpit_width_,
                                     cockpit_position_x_, cockpit_position_y_, cockpit_position_z_, nose_radius_,
                                     nose_length_, nose_position_z_, section_1_radius_,
                                     section_1_length_, section_1_position_z_,
                                     section_2_radius_, section_2_length_,
                                     section_2_position_z_,
                                     section_3_radius_,
                                     section_3_length_,
                                     section_3_position_z_,
                                     tip_raidus_, tail_radius_,
                                     tail_length_, tail_position_z_)
        except(Exception):
            self.show_default_values()

        ############################################################################

    def show_default_values(self, cockPitDesign=True,
                            nose_tip_position_=0, tail_tip_position_=0, fuselage_diameter=0, fuselage_length=0,
                            cockpit_height_=0, cockpit_length_=0, cockpit_width_=0,
                            cockpit_position_x_=0, cockpit_position_y_=0, cockpit_position_z_=0,
                            nose_radius_=0, nose_length_=0, nose_position_z_=0,
                            section_1_radius_=0, section_1_length_=0, section_1_position_z_=0,

                            section_2_radius_=0, section_2_length_=0, section_2_position_z_=0,
                            section_3_radius_=0, section_3_length_=0, section_3_position_z_=0,
                            tip_radius_=0, tail_radius_=0, tail_length_=0, tail_position_z_=0, ):

        self.length_text.setText(str(fuselage_length))
        self.diameter_text.setText(str(fuselage_diameter))

        self.cockpit_height_text.setText(str(cockpit_height_))
        self.cockpit_length_text.setText(str(cockpit_length_))
        self.cockpit_width_text.setText(str(cockpit_width_))
        self.cockpitCheck.setChecked(cockPitDesign)
        self.cockpitCheckMark = cockPitDesign

        self.cockpit_position_x_text.setText(str(cockpit_position_x_))
        self.cockpit_position_y_text.setText(str(cockpit_position_y_))
        self.cockpit_position_z_text.setText(str(cockpit_position_z_))

        self.nose_radius_text.setText(str(nose_radius_))
        self.nose_length_text.setText(str(nose_length_))
        self.nose_position_z_text.setText(str(nose_position_z_))

        self.nose_tip_position_text.setText(str(nose_tip_position_))
        self.tail_tip_position_text.setText(str(tail_tip_position_))

        self.section_1_radius_text.setText(str(section_1_radius_))
        self.section_1_length_text.setText(str(section_1_length_))
        self.section_1_position_z_text.setText(str(section_1_position_z_))

        ##########################################################################################
        self.section_2_radius_text.setText(str(section_2_radius_))
        self.section_2_length_text.setText(str(section_2_length_))
        self.section_2_position_z_text.setText(str(section_2_position_z_))
        ##########################################################################################

        self.section_3_radius_text.setText(str(section_3_radius_))
        self.section_3_length_text.setText(str(section_3_length_))
        self.section_3_position_z_text.setText(str(section_3_position_z_))

        self.tip_radius_text.setText(str(tip_radius_))
        self.tail_radius_text.setText(str(tail_radius_))
        self.tail_length_text.setText(str(tail_length_))
        self.tail_position_z_text.setText(str(tail_position_z_))

    def init_action(self):
        self.parameters = {
            boom: {
                self.text: {
                    design_type: self.design_type_,
                    boom_type: self.boom_type_,
                    fuselage_length: float(
                        get_fuselage_length([float(self.nose_length_text.text()),
                                             float(self.section_1_length_text.text()),
                                             float(self.section_2_length_text.text()),
                                             float(self.section_3_length_text.text()),
                                             float(self.tail_length_text.text())])),
                    fuselage_diameter: float(
                        get_diameter([float(self.nose_radius_text.text()), float(self.section_1_radius_text.text()),
                                      float(self.section_2_radius_text.text()),
                                      float(self.section_3_radius_text.text()),
                                      float(self.tail_radius_text.text()), float(self.tip_radius_text.text())])),
                    nose_width: float(self.nose_radius_text.text()),
                    nose_length: float(self.nose_length_text.text()),
                    nose_position_z: float(self.nose_position_z_text.text()),
                    nose_tip_position: float(self.nose_tip_position_text.text()),
                    design_cockpit: self.cockpitCheckMark,

                    section_1_length: float(self.section_1_length_text.text()),
                    section_1_width: float(self.section_1_radius_text.text()),
                    section_1_position_z: float(self.section_1_position_z_text.text()),
                    section_2_length: float(self.section_2_length_text.text()),
                    section_2_width: float(self.section_2_radius_text.text()),
                    section_2_position_z: float(self.section_2_position_z_text.text()),
                    section_3_length: float(self.section_3_length_text.text()),
                    section_3_width: float(self.section_3_radius_text.text()),
                    section_3_position_z: float(self.section_3_position_z_text.text()),
                    tip_width: float(self.tip_radius_text.text()),
                    tail_tip_position: float(self.tail_tip_position_text.text()),
                    tail_length: float(self.tail_length_text.text()),
                    tail_width: float(self.tail_radius_text.text()),
                    tail_position_z: float(self.tail_position_z_text.text()),

                }}}
        if self.cockpitCheckMark == True:
            self.parameters[boom][self.text].update({
                cockpit_height: float(self.cockpit_height_text.text()),
                cockpit_width: float(self.cockpit_width_text.text()),
                cockpit_length: float(self.cockpit_length_text.text()),
                cockpit_position_x: float(self.cockpit_position_x_text.text()),
                cockpit_position_y: float(self.cockpit_position_y_text.text()),
                cockpit_position_z: float(self.cockpit_position_z_text.text()),
            })
        else:
            self.parameters[boom][self.text].update({
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
        write_boom_objects(value=self.text)
        write_boom_to_objects(boom_name=self.text, design_type_=self.design_type_,
                              boom_type_=self.boom_type_)
        return self.parameters
