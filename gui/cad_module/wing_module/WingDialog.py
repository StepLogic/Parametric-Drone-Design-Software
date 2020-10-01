
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from utils import Database


class WingDialog(QDialog):
    def __init__(self, parent = None):
            super(WingDialog, self).__init__(parent)
            self.setWindowTitle("Wing Structure Info")
            layout= QFormLayout(self)

            ##########################################################################
            ##################################################################################

            self.span_label = QLabel("Span")
            self.span_text = QLineEdit()
            layout.addRow(self.span_label,self.span_text)
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

            self.Wing_profile_label = QLabel("Airfoil(Do not Add NACA)")
            self.Wing_profile_text = QLineEdit()
            layout.addRow(self.Wing_profile_label, self.Wing_profile_text)

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
            self.winglet_tlabel = QLabel("Winglet Center Translation(Enter Zero Into all the fields Below If you wont add a winglet)")
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


            self.toolbox_ = QHBoxLayout()

            self.buttons = QDialogButtonBox(
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
                Qt.Horizontal, self)
            layout.addWidget(self.buttons)

            self.buttons.accepted.connect(self.accept)
            self.buttons.rejected.connect(self.reject)

            try:
                aircraft_specifications = Database.read_aircraft_specifications()
                root_location_x, root_location_y, root_location_z, dihedral, sweep, twist, span, taper_ratio, chord,winglet_width,winglet_rotation,winglet_center_translation_x,winglet_center_translation_y,winglet_center_translation_z ,profile= self.read_vals(
                    part="wing", values=aircraft_specifications)

                self.show_default_values(root_location_x=root_location_x, root_location_y=root_location_y, root_location_z=root_location_z
                                         , dihedral=dihedral, sweep=sweep, twist=twist,
                                         span=span, taper_ratio=taper_ratio, chord=chord,winglet_width=winglet_width,winglet_rotation=winglet_rotation,winglet_center_translation_x=winglet_center_translation_x
                                         ,winglet_center_translation_y=winglet_center_translation_y,winglet_center_translation_z=winglet_center_translation_z,profile=profile)
            except(Exception):
                self.show_default_values()

            self.setLayout(layout)

    ############################################################################
    def show_default_values(self, root_location_x=0, root_location_y=0, root_location_z=0, dihedral=0, sweep=0, twist=0,
                            span=0, taper_ratio=1, chord=0,winglet_width=0,winglet_rotation=0,winglet_center_translation_x=0
                            ,winglet_center_translation_y=0,winglet_center_translation_z=0,profile=""):
        self.span_text.setText(str(span))


        self.chord_length_text.setText(str(chord))

        self.sweep_angle_text.setText(str(sweep))

        self.twist_angle_text.setText(str(twist))

        self.dihedral_angle_text.setText(str(dihedral))

        self.taper_ratio_text.setText(str(taper_ratio))

        self.Wing_profile_text.setText(profile)

        self.Wing_postion_x_text.setText(str(root_location_x))

        self.Wing_postion_y_text.setText(str(root_location_y))

        self.Wing_postion_z_text.setText(str(root_location_z))


        self.winglet_center_translation_x_text.setText(str(winglet_center_translation_x))

        self.winglet_center_translation_y_text.setText(str(winglet_center_translation_y))

        self.winglet_center_translation_z_text.setText(str(winglet_center_translation_z))

        self.winglet_rotation_text.setText(str(winglet_rotation))

        self.winglet_width_text.setText(str(winglet_width))


    def read_vals(self, part="", values=None):
        if values is None:
            values = {}
        root_location_x = values.get(part + "_root_position_x")
        root_location_y = values.get(part + "_root_position_y")
        root_location_z = values.get(part + "_root_position_z")
        chord = values.get(part + "_chord")
        dihedral = values.get(part + "_dihedral")
        sweep = values.get(part + "_sweep")
        twist = values.get(part + "_twist")
        span = values.get(part + "_span")
        taper_ratio = values.get(part + "_taper_ratio")
        profile=values[part+"_profile"]
        winglet_width=values.get("winglet_width")
        winglet_center_translation_x = values.get("winglet_center_translation_x")
        winglet_center_translation_y=values.get("winglet_center_translation_y")
        winglet_center_translation_z=values.get("winglet_center_translation_z")
        winglet_rotation=values.get("winglet_rotation")
        return root_location_x, root_location_y, root_location_z, dihedral, sweep, twist, span, taper_ratio, chord,winglet_width,winglet_rotation,winglet_center_translation_x,winglet_center_translation_y,winglet_center_translation_z,profile


    def init_action(self):
        self.parameters = {
            "wing_main": {
                "wing_root_position_x":float(self.Wing_postion_x_text.text()),
                "wing_root_position_y": float(self.Wing_postion_y_text.text()),
                "wing_root_position_z":float(self.Wing_postion_z_text.text()),
                "wing_span":float(self.span_text.text()),
                "wing_profile":str(self.Wing_profile_text.text()),
                "wing_chord":float(self.chord_length_text.text()),
                "wing_taper_ratio":float(self.taper_ratio_text.text()),
                "wing_sweep": float(self.sweep_angle_text.text()),
                "wing_dihedral": float(self.dihedral_angle_text.text()),
                "wing_twist": float(self.twist_angle_text.text()),
                "winglet_center_translation_x":float(self.winglet_center_translation_x_text.text()),
                "winglet_center_translation_y": float(self.winglet_center_translation_y_text.text()),
                "winglet_center_translation_z": float(self.winglet_center_translation_z_text.text()),
                "winglet_rotation":float(self.winglet_rotation_text.text()),
                "winglet_width":float(self.winglet_width_text.text()),
            }}
        try:
            Database.update_aircraft_specifications(key="wing_main", value=self.parameters["wing_main"])
        except:
            Database.write_aircraft_specification(self.parameters)
        return self.parameters

    @staticmethod
    def get_Wing_Params(parent=None):
        dialog = WingDialog(parent)
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













