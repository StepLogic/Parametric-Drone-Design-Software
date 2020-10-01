
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database


class FuselageDialog(QDialog):
    def __init__(self, parent=None):
        super(FuselageDialog, self).__init__(parent)
        scroll=QScrollArea(self)
        layout = QFormLayout(self)
        self.setWindowTitle("Fuselage Structure Info")

        ##########################################################################
        ##################################################################################

        self.length_label = QLabel("Length")
        self.length_text = QLineEdit()
        layout.addRow(self.length_label, self.length_text)

        self.diameter_label = QLabel("Diameter")
        self.diameter_text = QLineEdit()
        layout.addRow( self.diameter_label,self.diameter_text)
        ###################################################
        ##########################################################################
        ##################################################################################

        self.nose_radius_label = QLabel("Nose Radius")
        self.nose_radius_text = QLineEdit()
        layout.addRow(self.nose_radius_label, self.nose_radius_text)

        ##################################################################################

        ##############################################################################
        self.nose_position_label = QLabel("Nose Position ")
        layout.addWidget(self.nose_position_label)

        self.nose_position_x_label = QLabel("X")
        self.nose_position_x_text = QLineEdit()
        layout.addRow(self.nose_position_x_label, self.nose_position_x_text)

        self.nose_position_y_label = QLabel("Y")
        self.nose_position_y_text = QLineEdit()
        layout.addRow(self.nose_position_y_label, self.nose_position_y_text)

        self.nose_postion_z_label = QLabel("Z")
        self.nose_postion_z_text = QLineEdit()
        layout.addRow(self.nose_postion_z_label, self.nose_postion_z_text)

        ##########################################################################################





        ##############################################################################
        self.section1_radius_label = QLabel("Section 1  Radius")
        self.section1_radius_text = QLineEdit()
        layout.addRow(self.section1_radius_label, self.section1_radius_text)
        ##############################################################################
        self.section1_postion_tlabel = QLabel("Section 1 Position(The Default is 0,0,0) ")
        layout.addWidget(self.section1_postion_tlabel)

        self.section1_postion_x_label = QLabel("X")
        self.section1_postion_x_text = QLineEdit()
        layout.addRow(self.section1_postion_x_label, self.section1_postion_x_text)

        self.section1_postion_y_label = QLabel("Y")
        self.section1_postion_y_text = QLineEdit()
        layout.addRow(self.section1_postion_y_label, self.section1_postion_y_text)

        self.section1_postion_z_label = QLabel("Z")
        self.section1_postion_z_text = QLineEdit()
        layout.addRow(self.section1_postion_z_label, self.section1_postion_z_text)

        ##########################################################################################
        ##############################################################################
        self.section2_radius_label = QLabel("Section 2 Radius")
        self.section2_radius_text = QLineEdit()
        layout.addRow(self.section2_radius_label, self.section2_radius_text)
        ##############################################################################
        self.section2_postion_tlabel = QLabel("Section 2 Postion(The Default is 0,0,0) ")
        layout.addWidget(self.section1_postion_tlabel)

        self.section2_postion_x_label = QLabel("X")
        self.section2_postion_x_text = QLineEdit()
        layout.addRow(self.section2_postion_x_label, self.section2_postion_x_text)

        self.section2_postion_y_label = QLabel("Y")
        self.section2_postion_y_text = QLineEdit()
        layout.addRow(self.section2_postion_y_label, self.section2_postion_y_text)

        self.section2_postion_z_label = QLabel("Z")
        self.section2_postion_z_text = QLineEdit()
        layout.addRow(self.section2_postion_z_label, self.section2_postion_z_text)

        ##########################################################################################



        ##############################################################################
        self.section3_radius_label = QLabel("Section 3 radius")
        self.section3_radius_text = QLineEdit()
        layout.addRow(self.section3_radius_label, self.section3_radius_text)
        ##############################################################################
        self.section3_postion_tlabel = QLabel("Section 3 Position")
        layout.addWidget(self.section3_postion_tlabel)

        self.section3_postion_x_label = QLabel("X")
        self.section3_postion_x_text = QLineEdit()
        layout.addRow(self.section3_postion_x_label, self.section3_postion_x_text)

        self.section3_postion_y_label = QLabel("Y")
        self.section3_postion_y_text = QLineEdit()
        layout.addRow(self.section3_postion_y_label, self.section3_postion_y_text)

        self.section3_postion_z_label = QLabel("Z")
        self.section3_postion_z_text = QLineEdit()
        layout.addRow(self.section3_postion_z_label, self.section3_postion_z_text)

        ##########################################################################################


        ##############################################################################
        self.tail_angle_label = QLabel("Tail Angle")
        self.tail_angle_text = QLineEdit()
        layout.addRow(self.tail_angle_label, self.tail_angle_text)
        ##############################################################################

        ##############################################################################
        self.tail_radius_label = QLabel("Tail Height")
        self.tail_radius_text = QLineEdit()
        layout.addRow(self.tail_radius_label, self.tail_radius_text)
        ##############################################################################
        self.tail_position_label = QLabel("Tail Center Position")
        layout.addWidget(self.section3_postion_tlabel)
        self.tail_postion_x_label = QLabel("X")
        self.tail_postion_x_text = QLineEdit()
        layout.addRow(self.tail_postion_x_label, self.tail_postion_x_text)

        self.tail_postion_y_label = QLabel("Y")
        self.tail_postion_y_text = QLineEdit()
        layout.addRow(self.tail_postion_y_label, self.tail_postion_y_text)

        self.tail_postion_z_label = QLabel("Z")
        self.tail_postion_z_text = QLineEdit()
        layout.addRow(self.tail_postion_z_label, self.tail_postion_z_text)

        ##########################################################################################
        self.toolbox_ = QHBoxLayout()

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        widget=QWidget(self)
        widget.setLayout(layout)
        scroll.setWidget(widget)
        temp_layout=QVBoxLayout(self)
        temp_layout.addWidget(scroll)
        self.setLayout(temp_layout)
        try:
                aicraft_specifications = Database.read_aircraft_specifications()
                fuselage_diameter, fuselage_length, nose_radius, nose_position_x, nose_position_y, nose_position_z, section_2_radius, section_2_center_position_x, section_2_center_position_y, section_2_center_position_z, section_3_radius, section_3_center_position_x, section_3_center_position_y, section_3_center_position_z, section_4_radius, section_4_center_position_x, section_4_center_position_y, section_4_center_position_z, tail_angle, tail_radius, tail_position_x, tail_position_y, tail_position_z = self.read_fuselage_values( values=aicraft_specifications)
                self.show_default_values(fuselage_diameter, fuselage_length, nose_radius, nose_position_x, nose_position_y, nose_position_z, section_2_radius, section_2_center_position_x, section_2_center_position_y, section_2_center_position_z, section_3_radius, section_3_center_position_x, section_3_center_position_y, section_3_center_position_z, section_4_radius, section_4_center_position_x, section_4_center_position_y, section_4_center_position_z, tail_angle, tail_radius, tail_position_x, tail_position_y, tail_position_z
)
        except(Exception):
                self.show_default_values()

    ############################################################################
    def show_default_values(self,fuselage_diameter=0, fuselage_length=0,
                            nose_radius=0, nose_position_x=0,
                            nose_position_y=0, nose_position_z=0,
                            section_2_radius=0, section_2_center_position_x=0,
                            section_2_center_position_y=0, section_2_center_position_z=0,
                            section_3_radius=0, section_3_center_position_x=0, section_3_center_position_y=0,
                            section_3_center_position_z=0, section_4_radius=0, section_4_center_position_x=0,
                            section_4_center_position_y=0, section_4_center_position_z=0,
                            tail_angle=0, tail_radius=0, tail_position_x=0, tail_position_y=0, tail_position_z=0):


        self.length_text.setText(str(fuselage_length))
        self.diameter_text.setText(str(fuselage_diameter))
        self.nose_radius_text .setText(str(nose_radius))

        self.nose_position_x_text.setText(str(nose_position_x))

        self.nose_position_y_text .setText(str(nose_position_y))

        self.nose_postion_z_text.setText(str(nose_position_z))

        self.section1_radius_text.setText(str(section_2_radius))


        self.section1_postion_x_text .setText(str(section_2_center_position_x))

        self.section1_postion_y_text .setText(str(section_2_center_position_y))

        self.section1_postion_z_text .setText(str(section_2_center_position_z))


        ##########################################################################################
        self.section2_radius_text.setText(str(section_3_radius))
        self.section2_postion_x_text .setText(str(section_3_center_position_x))

        self.section2_postion_y_text .setText(str(section_3_center_position_y))

        self.section2_postion_z_text.setText(str(section_3_center_position_z))


        ##########################################################################################




        self.section3_radius_text .setText(str(section_4_radius))

        self.section3_postion_x_text .setText(str(section_4_center_position_x))

        self.section3_postion_y_text.setText(str(section_4_center_position_y))

        self.section3_postion_z_text.setText(str(section_4_center_position_z))



        self.tail_angle_text .setText(str(tail_angle))

        self.tail_radius_text .setText(str(tail_radius))

        self.tail_postion_x_text .setText(str(tail_position_x))

        self.tail_postion_y_text .setText(str(tail_position_y))

        self.tail_postion_z_text .setText(str(tail_position_z))



    def read_fuselage_values(self,values={}):

        fuselage_length = values.get("fuselage_length")
        fuselage_diameter = values.get("fuselage_diameter")
        nose_radius = values.get("nose_radius")
        nose_position_x = values.get("nose_center_position_x")
        nose_position_y = values.get("nose_center_position_y")
        nose_position_z = values.get("nose_center_position_z")
        tail_radius = values.get("tail_radius")
        tail_position_x = values.get("tail_center_position_x")
        tail_position_y = values.get("tail_center_position_y")
        tail_position_z = values.get("tail_center_position_z")
        tail_angle = values.get("tail_angle")
        section_2_center_position_x = values.get("section_2_center_position_x")
        section_2_center_position_y = values.get("section_2_center_position_y")
        section_2_center_position_z = values.get("section_2_center_position_z")
        section_2_radius = values.get("section_2_radius")
        section_3_radius = values.get("section_3_radius")
        section_3_center = values.get("section_3_center")
        section_3_center_position_x = values.get("section_3_center_position_x")
        section_3_center_position_y = values.get("section_3_center_position_y")
        section_3_center_position_z = values.get("section_3_center_position_z")
        section_4_center = values.get("section_4_center")
        section_4_center_position_x = values.get("section_4_center_position_x")
        section_4_center_position_y = values.get("section_4_center_position_y")
        section_4_center_position_z = values.get("section_4_center_position_z")
        section_4_radius = values.get("section_4_radius")
        return fuselage_diameter, fuselage_length, nose_radius, nose_position_x, nose_position_y, nose_position_z, section_2_radius, section_2_center_position_x, section_2_center_position_y, section_2_center_position_z, section_3_radius, section_3_center_position_x, section_3_center_position_y, section_3_center_position_z, section_4_radius, section_4_center_position_x, section_4_center_position_y, section_4_center_position_z, tail_angle, tail_radius, tail_position_x, tail_position_y, tail_position_z
    def init_action(self):
        self.parameters = {
            "fuselage":{
                "fuselage_length": float(self.length_text.text()),
                "fuselage_diameter":float(self.diameter_text.text()),
                "nose_radius": float(self.nose_radius_text.text()),
                "nose_center_position_x": float(self.nose_position_x_text.text()),
                "nose_center_position_y": float(self.nose_position_y_text.text()),
                "nose_center_position_z": float(self.nose_postion_z_text.text()),
                "section_2_center_position_x":float(self.section1_postion_x_text.text()),
                "section_2_center_position_y": float(self.section1_postion_y_text.text()),
                "section_2_center_position_z": float(self.section1_postion_z_text.text()),
                "section_2_radius":float(self.section1_radius_text.text()),
                "section_3_center_position_x": float(self.section2_postion_x_text.text()),
                "section_3_center_position_y":  float(self.section2_postion_y_text.text()),
                "section_3_center_position_z": float(self.section2_postion_z_text.text()),
                "section_3_radius":float(self.section2_radius_text.text()),
                "section_4_center_position_x": float(self.section3_postion_x_text.text()),
                "section_4_center_position_y": float(self.section3_postion_y_text.text()),
                "section_4_center_position_z": float(self.section3_postion_z_text.text()),
                "section_4_radius": float(self.section3_radius_text.text()),
                "tail_angle": float(self.tail_angle_text.text()),
                "tail_center_position_x": float(self.tail_postion_x_text.text()),
                "tail_center_position_y": float(self.tail_postion_y_text.text()),
                "tail_center_position_z": float(self.tail_postion_y_text.text()),
                "tail_radius":float(self.tail_radius_text.text()),
            }}
        try:
            Database.update_aircraft_specifications(key="fuselage", value=self.parameters["fuselage"])
        except:
            Database.write_aircraft_specification(self.parameters)
        return self.parameters

    @staticmethod
    def get_params(parent=None):
        dialog = FuselageDialog(parent)
        result = dialog.exec_()
        if (result == 1):
            try:
                params = dialog.init_action()
                return (params, QDialog.Accepted)
            except(Exception):
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Critical)
                dialog.setText("Incorrect or No Values Entered")
                dialog.addButton(QMessageBox.Ok)
                dialog.exec()
                return ([], QDialog.Rejected)
        else:
            return ([], QDialog.Rejected)

