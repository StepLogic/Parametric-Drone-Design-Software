from PyQt5.QtWidgets import *

from Utils.data_objects.landing_gear_key import *
from Utils.database import database
from Utils.database.geometry.landing_gear_database import read_landing_gear_values


class landing_gear_tab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout(self)
        ##########################################################################
        ##################################################################################
        self.landing_gear_type_label = QLabel("Configuration(c or t)")
        self.landing_gear_type = QLineEdit()
        layout.addRow(self.landing_gear_type_label, self.landing_gear_type)
        self.struct_length_main_gear_label = QLabel("Main Gear Struct Length")
        self.struct_length_main_gear = QLineEdit()
        layout.addRow(self.struct_length_main_gear_label, self.struct_length_main_gear)

        self.struct_length_aux_label= QLabel("Aux Gear Struct Length")
        self.struct_length_aux = QLineEdit()
        layout.addRow(self.struct_length_aux_label, self.struct_length_aux)

        self.tire_diameter_label = QLabel("Tire Diameter")
        self.tire_diameter_text = QLineEdit()
        layout.addRow(self.tire_diameter_label, self.tire_diameter_text)

        self.wheel_diameter_label = QLabel("Wheel Diameter")
        self.wheel_diameter_text = QLineEdit()
        layout.addRow(self.wheel_diameter_label, self.wheel_diameter_text)

        self.aux_gear_position_label = QLabel("Auxiliary Gear Position")
        layout.addWidget(self.aux_gear_position_label)
        self.aux_gear_position_x_label = QLabel("X")
        self.aux_gear_position_x_text = QLineEdit()
        layout.addRow(self.aux_gear_position_x_label, self.aux_gear_position_x_text)

        self.aux_gear_position_y_label = QLabel("Y")
        self.aux_gear_position_y_text = QLineEdit()
        layout.addRow(self.aux_gear_position_y_label, self.aux_gear_position_y_text)

        self.aux_gear_position_z_label = QLabel("Z")
        self.aux_gear_position_z_text = QLineEdit()
        layout.addRow(self.aux_gear_position_z_label, self.aux_gear_position_z_text)

        self.rol_gear_position_label = QLabel(" Right And Left Gear Position")
        layout.addWidget(self.rol_gear_position_label)
        self.rol_gear_position_x_label = QLabel("X")
        self.rol_gear_position_x_text = QLineEdit()
        layout.addRow(self.rol_gear_position_x_label, self.rol_gear_position_x_text)

        self.rol_gear_position_y_label = QLabel("Y")
        self.rol_gear_position_y_text = QLineEdit()
        layout.addRow(self.rol_gear_position_y_label, self.rol_gear_position_y_text)

        self.rol_gear_position_z_label = QLabel("Z")
        self.rol_gear_position_z_text = QLineEdit()
        layout.addRow(self.rol_gear_position_z_label, self.rol_gear_position_z_text)

        self.toolbox_ = QHBoxLayout()

        widget = QWidget(self)
        widget.setLayout(layout)

        temp_layout = QVBoxLayout(self)
        temp_layout.addWidget(widget)
        self.zero_all_text_fields()
        self.setLayout(temp_layout)

    def zero_all_text_fields(self):
        try:
            landing_gear_type, struct_length_main_gear, struct_length_aux, aux_gear_position_x, aux_gear_position_y,\
            aux_gear_position_z, rol_gear_position_x, rol_gear_position_y, rol_gear_position_z,wheel_diameter_,tire_diameter_= \
                read_landing_gear_values()
            self.show_default_values(landing_gear_type, struct_length_main_gear, struct_length_aux, aux_gear_position_x,
                                     aux_gear_position_y,
                                     aux_gear_position_z, rol_gear_position_x, rol_gear_position_y, rol_gear_position_z,wheel_diameter_,tire_diameter_)
        except Exception as e:
            print(e)
            self.show_default_values()
    ############################################################################
    def show_default_values(self, landing_gear_type_="c", struct_length_main_gear_=0,struct_length_aux_=0, aux_gear_position_x_=0,
                            aux_gear_position_y_=0, aux_gear_position_z_=0, rol_gear_position_x_=0,
                            rol_gear_position_y_=0, rol_gear_position_z_=0,wheel_diameter_=0,tire_diameter_=0):
        self.landing_gear_type.setText(str(landing_gear_type_))
        self.struct_length_main_gear.setText(str(struct_length_main_gear_))

        self.struct_length_aux.setText(str(struct_length_aux_))
        self.tire_diameter_text.setText(str(tire_diameter_))
        self.wheel_diameter_text.setText(str(wheel_diameter_))
        self.aux_gear_position_x_text.setText(str(aux_gear_position_x_))
        self.aux_gear_position_y_text.setText(str(aux_gear_position_y_))
        self.aux_gear_position_z_text.setText(str(aux_gear_position_z_))
        self.rol_gear_position_x_text.setText(str(rol_gear_position_x_))
        self.rol_gear_position_y_text.setText(str(rol_gear_position_y_))
        self.rol_gear_position_z_text.setText(str(rol_gear_position_z_))



    def init_action(self):
        if self.landing_gear_type.text() == "c" or self.landing_gear_type.text() == "t":
            self.parameters = {
                landing_gear: {
                    landing_gear_type: self.landing_gear_type.text(),
                    struct_length_main_gear: float(self.struct_length_main_gear.text()),
                    struct_length_aux: float(self.struct_length_aux.text()),
                    tire_diameter:float(self.tire_diameter_text.text()),
                    wheel_diameter:float(self.wheel_diameter_text.text()),
                    aux_gear_position_x: float(self.aux_gear_position_x_text.text()),
                    aux_gear_position_y: float(self.aux_gear_position_y_text.text()),
                    aux_gear_position_z: float(self.aux_gear_position_z_text.text()),
                    rol_gear_position_x:float( self.rol_gear_position_x_text.text()),
                    rol_gear_position_y: float(self.rol_gear_position_y_text.text()),
                    rol_gear_position_z: float(self.rol_gear_position_z_text.text())
                }}
            try:
                database.update_aircraft_specifications(key=landing_gear, value=self.parameters[landing_gear])
            except:
                database.write_aircraft_specification(self.parameters)
            return self.parameters
        else:
            raise AttributeError("You cannot add instance attributes to %s" % self)

