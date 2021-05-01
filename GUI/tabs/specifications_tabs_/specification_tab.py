
from DPS_data_objects.placeholders.geometry_placeholder import *
from PyQt5.QtWidgets import *


class specification_tab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QFormLayout(self)


    def create_tab(self):
        self.create_widget()
        self.button = QPushButton('Save', self)
        self.button.clicked.connect(self.init_action)
        self.layout.addRow(self.button)
        self.setLayout(self.layout)
        return self

    def create_widget(self):
        ##########################################################################
        ##################################################################################

        layout = self.layout
        checks=[]
        texts=[]
        layout.addRow(QLabel("Check Values You will Input"))
        # Wing Loading
        self.wing_loading_text = QTextEdit()
        self.wing_loading_check = QCheckBox(wing_loading)
        self.wing_loading_text.setDisabled(self.wing_loading_check.isChecked())
        self.wing_loading_check.toggled.connect(
            lambda: self.on_geometry_checks(self.wing_loading_check, self.wing_loading_text))
        layout.addRow(self.wing_loading_check, self.wing_loading_text)

        # Weight
        self.weight_constraint_text = QTextEdit()
        self.weight_constraint_check = QCheckBox(weight_constraint)
        self.weight_constraint_text.setDisabled(self.weight_constraint_check.isChecked())
        self.weight_constraint_check.toggled.connect(
            lambda: self.on_geometry_checks(self.weight_constraint_check, self.weight_constraint_text))
        layout.addRow(self.weight_constraint_check, self.weight_constraint_text)
        #chord_length
        self.chord_length_text = QTextEdit()
        self.chord_length_check = QCheckBox(weight_constraint)
        self.chord_length_text.setDisabled(self.chord_length_check.isChecked())
        self.chord_length_check.toggled.connect(
            lambda: self.on_geometry_checks(self.chord_length_check, self.chord_length_text))
        layout.addRow(self.chord_length_check, self.chord_length_text)
        #takeoff
        self.takeoff_text = QTextEdit()
        self.takeoff_check = QCheckBox(weight_constraint)
        self.takeoff_text.setDisabled(self.takeoff_check.isChecked())
        self.takeoff_check.toggled.connect(
            lambda: self.on_geometry_checks(self.takeoff_check, self.takeoff_text))
        layout.addRow(self.takeoff_check, self.takeoff_text)


        return self.layout
        ##########################################################################################

    def on_geometry_checks(self, button, textfield):
        textfield.setDisabled(button.isChecked())
    def zero_all_textfields(self):
       pass

        ############################################################################

    def show_default_values(self):
      pass

    def init_action(self):
        pass








