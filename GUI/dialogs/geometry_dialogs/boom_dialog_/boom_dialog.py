from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.alerts.boom_delete_dialog import boom_delete_dialog
from GUI.alerts.boom_design_dialog import boom_design_dialog
from GUI.tabs.geometry_tabs_.conventional_geometry.fuselage_tab_.fuselage_tab import fuselage_tab
from GUI.tabs.geometry_tabs_.unconventional_geometry.boom_tabs.boom_tab import boom_tab
from Utils.data_objects.placeholder import conventional_design, unconventional_design
from Utils.database.geometry.boom_database import delete_boom_objects, read_boom_objects, get_boom_object_data, \
    delete_boom_from_objects, write_boom_objects, write_boom_to_objects


class boom_dialog(QDialog):
    def __init__(self, workflow):
        super().__init__()
        self.indexes = []
        self.setMinimumSize(900, 450)
        self.booms = []
        self.monitor = workflow
        self.layout = QFormLayout()
        self.inputArea = QTabWidget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.add_new = QPushButton('New Boom', self)
        self.add_new.clicked.connect(self.new_boom)
        self.remove_boom = QPushButton('Remove Boom', self)
        self.remove_boom.clicked.connect(self.remove_boom_method)
        self.layout.addRow(self.inputArea)
        self.layout.addRow(self.remove_boom, self.add_new)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.load_booms()

    def load_booms(self):
        try:
            boom_list = read_boom_objects()
            if len(boom_list) == 0:
                self.new_boom()
            for l in boom_list:
                design_type_, boom_type_ = get_boom_object_data(l)
                if design_type_ == unconventional_design:
                    self.boom_tab_ = boom_tab(l, boom_type_, design_type_)
                    self.booms.append(self.boom_tab_)
                    self.booms.append(self.boom_tab_)
                    self.inputArea.addTab(self.boom_tab_, l)
                    self.indexes.append(l)
                elif design_type_ == conventional_design:
                    self.boom_tab_ = fuselage_tab(l, boom_type_, design_type_)
                    self.booms.append(self.boom_tab_)
                    self.booms.append(self.boom_tab_)
                    self.inputArea.addTab(self.boom_tab_, l)
                    self.indexes.append(l)

        except:
            self.new_boom()

    def new_boom(self):
        dialog = boom_design_dialog()
        results = dialog.exec_()
        if results == 1:
            text, boom_type_, design_type_ = dialog.accept_inputs()
            if not self.indexes.__contains__(text):
                if design_type_ == unconventional_design:
                    print("dialog", boom_type_)
                    self.boom_tab_ = boom_tab(text, boom_type_, design_type_)
                    self.booms.append(self.boom_tab_)
                    self.inputArea.addTab(self.boom_tab_, text)
                    self.indexes.append(text)
                    self.update()
                elif design_type_ == conventional_design:
                    self.boom_tab_ = fuselage_tab(text, boom_type_, design_type_)
                    self.booms.append(self.boom_tab_)
                    self.inputArea.addTab(self.boom_tab_, text)
                    self.indexes.append(text)
                    self.update()
                write_boom_objects(value=text)
                write_boom_to_objects(boom_name=text, design_type_=design_type_,
                                      boom_type_=boom_type_)

        else:
            raise Exception("cancel")

    def remove_boom_method(self):
        dialog = boom_delete_dialog()
        results = dialog.exec_()
        if results == 1:
            text = dialog.accept_inputs()
            try:
                self.inputArea.removeTab(self.indexes.index(text))
                delete_boom_objects(value=text)
                delete_boom_from_objects(surface_name=text)
                self.monitor.viewer.delete_object(part_name=text)
            except:
                pass


    def save_all(self):
        for l in self.booms:
            l.init_action()
            print('dialog-init', read_boom_objects())
