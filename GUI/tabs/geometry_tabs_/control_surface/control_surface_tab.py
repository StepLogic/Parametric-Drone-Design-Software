from PyQt5.QtWidgets import *
from Utils.data_objects.lifting_surface_placeholder import *
from Utils.database import database
from Utils.database.geometry.control_surface_database import read_surface_data, write_control_surface_objects, \
    write_control_surface_to_objects

from Utils.database.geometry.lifting_database import read_lifting_surface_objects
from PyQt5.QtWidgets import *

from Utils.data_objects.lifting_surface_placeholder import *
from Utils.database import database
from Utils.database.geometry.control_surface_database import read_surface_data, write_control_surface_objects, \
    write_control_surface_to_objects
from Utils.database.geometry.lifting_database import read_lifting_surface_objects


class control_surface_tab(QWidget):
    def __init__(self, name=""):
        super().__init__()
        self.name = name
        layout = QFormLayout(self)
        self.tab=self
        self.selection_=None
        ##########################################################################
        ##################################################################################
        ##########################################################################
        layout.addRow(QLabel("Select Lifting Surface to attach to"))
        self.itemsComboBox = QComboBox()
        self.itemsComboBox.addItems(read_lifting_surface_objects())
        self.itemsComboBox.currentIndexChanged.connect(self.selectionChanged)
        layout.addRow(self.itemsComboBox)
        ##################################################################################
        self.span_label = QLabel("Span")
        self.span_text = QLineEdit()
        layout.addRow(self.span_label, self.span_text)
        self.rotation_label = QLabel("Rotation(XYZ)")
        layout.addRow(self.rotation_label)

        self.rotation_x_label = QLabel("X")
        self.rotation_x_text = QLineEdit()
        layout.addRow(self.rotation_x_label, self.rotation_x_text)

        self.rotation_y_label = QLabel("Y")
        self.rotation_y_text = QLineEdit()
        layout.addRow(self.rotation_y_label, self.rotation_y_text)

        self.rotation_z_label = QLabel("Z")
        self.rotation_z_text = QLineEdit()
        layout.addRow(self.rotation_z_label, self.rotation_z_text)

        ##################################################################################
        ##############################################################################
        self.chord_length_label = QLabel("Chord Length")
        self.chord_length_text = QLineEdit()
        layout.addRow(self.chord_length_label, self.chord_length_text)

        self.Wing_postion_tlabel = QLabel("Position")
        layout.addWidget(self.Wing_postion_tlabel)

        self.Wing_postion_x_label = QLabel("X")
        self.vtp_position_x_text = QLineEdit()
        layout.addRow(self.Wing_postion_x_label, self.vtp_position_x_text)

        self.Wing_postion_y_label = QLabel("Y")
        self.vtp_position_y_text = QLineEdit()
        layout.addRow(self.Wing_postion_y_label, self.vtp_position_y_text)

        self.Wing_postion_z_label = QLabel("Z")
        self.Wing_postion_z_text = QLineEdit()
        layout.addRow(self.Wing_postion_z_label, self.Wing_postion_z_text)
        self.zero_all_textfields()


    ############################################################################
    def zero_all_textfields(self):
        try:
            root_location_x_, root_location_y_, root_location_z_, rot_x_, rot_y_, rot_z_, \
            span_, chord_, parent__ = read_surface_data(
                surface_name=self.name)
            self.show_default_values(root_location_x_, root_location_y_, root_location_z_,
                                     rot_x_,rot_y_,rot_z_,span_, chord_, parent__,)
        except:
            self.show_default_values()

    def show_default_values(self, root_location_x_=0, root_location_y_=0, root_location_z_=0,
                            rot_x_=0,
                            rot_y_=0,
                            rot_z_=0,
                            span_=0, chord_=0,parent__=""):
        self.span_text.setText(str(span_))
        try:
          self.itemsComboBox.setCurrentIndex(read_lifting_surface_objects().index(parent__))
        except:
         pass
        self.chord_length_text.setText(str(chord_))
        self.rotation_x_text.setText(str(rot_x_))
        self.rotation_y_text.setText(str(rot_y_))
        self.rotation_z_text.setText(str(rot_z_))

        self.vtp_position_x_text.setText(str(root_location_x_))

        self.vtp_position_y_text.setText(str(root_location_y_))

        self.Wing_postion_z_text.setText(str(root_location_z_))

    def init_action(self):
        self.parameters = {
        control_surface:{
            self.name: {
                root_le_position_x: float(self.vtp_position_x_text.text()),
                root_le_position_y: float(self.vtp_position_y_text.text()),
                root_le_position_z: float(self.Wing_postion_z_text.text()),
                parent_: self.selection_ if self.selection_ is not None else read_lifting_surface_objects()[self.itemsComboBox.currentIndex()],
                span: float(self.span_text.text()),
                rotation_x: float(self.rotation_x_text.text()),
                rotation_y: float(self.rotation_y_text.text()),
                rotation_z: float(self.rotation_z_text.text()),
                chord: float(self.chord_length_text.text()),
            }}}
        try:
            database.update_aircraft_specifications(key=control_surface, value=self.parameters[control_surface])
        except:
            database.write_aircraft_specification(self.parameters)
        write_control_surface_objects(value=self.name)
        write_control_surface_to_objects(surface_name=self.name,parent__=self.selection_ if self.selection_ is not None else read_lifting_surface_objects()[self.itemsComboBox.currentIndex()])
        return self.parameters

    def selectionChanged(self, i):
            self.selection_ = read_lifting_surface_objects()[i]


