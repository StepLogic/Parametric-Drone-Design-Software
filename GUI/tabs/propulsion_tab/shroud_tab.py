from PyQt5.QtWidgets import *

from Utils.data_objects.propulsion_keys import *
from Utils.database import database
from Utils.database.propulsion.propulsion_database import read_shroud_parameters


class shroud_tab(QWidget):
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

        self.inputArea = QTabWidget()
        ##################################################################################

        self.layout = QFormLayout()
        self.shroud_number_label = QLabel("Number of Shrouds")
        self.shroud_number_text = QLineEdit()
        self.layout.addRow(self.shroud_number_label, self.shroud_number_text)

        self.rotation_label = QLabel("Rotation(XYZ)")
        self.layout.addRow(self.rotation_label)

        self.shroud_outer_diameter_label = QLabel("Shroud Outer Diameter")
        self.shroud_outer_diameter_text = QLineEdit()
        self.layout.addRow(self.shroud_outer_diameter_label, self.shroud_outer_diameter_text)

        self.shroud_inner_diameter_label = QLabel("Shroud Inner Diameter")
        self.shroud_inner_diameter_text = QLineEdit()
        self.layout.addRow(self.shroud_inner_diameter_label, self.shroud_inner_diameter_text)

        self.shroud_length_label = QLabel("Shroud Length")
        self.shroud_length_text = QLineEdit()
        self.layout.addRow(self.shroud_length_label, self.shroud_length_text)

        self.shroud_taper_ratio_label = QLabel("Shroud Taper Ratio")
        self.shroud_taper_ratio_text = QLineEdit()
        self.layout.addRow(self.shroud_taper_ratio_label, self.shroud_taper_ratio_text)

        self.XZsymmetryCheck = QCheckBox("Mirror Boom About XZ Plane")
        self.XZsymmetryCheck.toggled.connect(self.xz_mirror_Checked)
        self.layout.addRow(self.XZsymmetryCheck)
        self.YZsymmetryCheck = QCheckBox("Mirror Boom About YZ Plane")
        self.YZsymmetryCheck.toggled.connect(self.yz_mirror_Checked)
        self.layout.addRow(self.YZsymmetryCheck)
        self.XYsymmetryCheck = QCheckBox("Mirror Boom About XY Plane")
        self.XYsymmetryCheck.toggled.connect(self.xy_mirror_Checked)
        self.layout.addRow(self.XYsymmetryCheck)

        self.root_le_position_label = QLabel("Center Position")
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
        ##################################################################################

        ##########################################################################################

        self.zero_all_text_fields()
        return self.layout

    def xz_mirror_Checked(self, button):
        self.xz_mirror_ = button

    def xy_mirror_Checked(self, button):
        self.xy_mirror_ = button

    def yz_mirror_Checked(self, button):
        self.yz_mirror_ = button

    def zero_all_text_fields(self):
        try:
            shroud_length_, root_le_pos_x_, root_le_pos_y_, root_le_pos_z_, shroud_number_, shroud_taper_ratio_, shroud_inner_diameter_, shroud_outer_diameter_, xy_mirror_, xz_mirror_, yz_mirror_ = read_shroud_parameters()

            self.show_default_values(shroud_length_, root_le_pos_x_, root_le_pos_y_, root_le_pos_z_, shroud_number_,
                                     shroud_taper_ratio_, shroud_inner_diameter_, shroud_outer_diameter_, xy_mirror_,
                                     xz_mirror_, yz_mirror_)
        except Exception as e:
            print(e)
            self.show_default_values()

    def show_default_values(self,
                            shroud_length_=0,
                            root_le_pos_x_=0,
                            root_le_pos_y_=0,
                            root_le_pos_z_=0,
                            shroud_number_=0,
                            shroud_taper_ratio_=1,
                            shroud_inner_diameter_=0,
                            shroud_outer_diameter_=0,
                            xy_mirror_=False,
                            xz_mirror_=False,
                            yz_mirror_=False,
                            ):
        self.shroud_number_text.setText(str(shroud_number_))

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

        self.shroud_outer_diameter_text.setText(str(shroud_outer_diameter_))
        self.shroud_length_text.setText(str(shroud_length_))
        self.shroud_inner_diameter_text.setText(str(shroud_inner_diameter_))
        self.shroud_taper_ratio_text.setText(str(shroud_taper_ratio_))

    def init_action(self):
        self.parameters = {
            propeller: {
                shroud: {
                    shroud_number: int(self.shroud_number_text.text()),
                    hub_position_x: float(self.root_le_position_x_text.text()),
                    hub_position_y: float(self.root_le_position_y_text.text()),
                    hub_position_z: float(self.root_le_position_z_text.text()),
                    xy_mirror: self.xy_mirror_,
                    xz_mirror: self.xz_mirror_,
                    yz_mirror: self.yz_mirror_,
                    shroud_outer_diameter: float(self.shroud_outer_diameter_text.text()),
                    shroud_length: float(self.shroud_length_text.text()),
                    shroud_inner_diameter: float(self.shroud_inner_diameter_text.text()),
                    shroud_taper_ratio: float(self.shroud_taper_ratio_text.text()),

                }}}
        try:
            database.update_propulsion_specifications(key=propeller, value=self.parameters[propeller])
        except:
            database.write_propulsion_specifications(self.parameters)

        return self.parameters
