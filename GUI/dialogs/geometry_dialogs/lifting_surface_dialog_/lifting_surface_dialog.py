from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.alerts.lifting_surface_delete_dialog import lifting_surface_delete_dialog
from GUI.alerts.surface_design_dialog import surface_design_dialog
from GUI.dialogs.geometry_dialogs.lifting_surface_dialog_.lifting_surface_pane import lifting_surface_pane
from GUI.tabs.geometry_tabs_.conventional_geometry.h_stab_tab_.conventional_h_stab_tab import h_stab_tab
from GUI.tabs.geometry_tabs_.conventional_geometry.v_stab_tab_.conventional_v_stab_tab import v_stab_tab
from GUI.tabs.geometry_tabs_.conventional_geometry.wing_tab_.conventional_wing_tab import wing_tab
from Utils.data_objects.lifting_surface_placeholder import fin, tailplane
from Utils.data_objects.placeholder import unconventional_design, conventional_design
from Utils.database.geometry.lifting_database import read_lifting_surface_objects, get_surface_object_data, \
    delete_lifting_surface_objects, delete_lifting_surface_from_objects, write_lifting_surface_to_objects, \
    write_lifting_surface_objects


class lifting_surface_dialog(QDialog):
    def __init__(self, workflow):
        super().__init__()
        self.indexes = []
        self.surfaces = []
        self.monitor = workflow
        self.layout = QFormLayout()
        self.inputArea = QTabWidget()
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.add_surface = QPushButton('New Surface', self)
        self.add_surface.clicked.connect(self.new_surfaces)
        self.remove_surface = QPushButton('Remove Surface', self)
        self.remove_surface.clicked.connect(self.remove_surface_method)
        self.layout.addRow(self.inputArea)
        self.layout.addRow(self.remove_surface, self.add_surface)
        self.layout.addRow(self.buttons)
        self.setLayout(self.layout)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.load_surfaces()


    def load_surfaces(self):
        try:
            surface_list = read_lifting_surface_objects()
            if len(surface_list) == 0:
                self.new_surfaces()
            else:
                for l in surface_list:
                    design_type_, surface_type_ = get_surface_object_data(l)
                    if design_type_ == unconventional_design:
                        self.surfaca_tab_ = lifting_surface_pane(l, surface_type_, design_type_)
                        self.surfaces.append(self.surfaca_tab_)
                        self.inputArea.addTab(self.surfaca_tab_, l)
                        self.indexes.append(l)
                    elif design_type_ == conventional_design:
                        if surface_type_ == fin:
                            self.surfaca_tab_ = v_stab_tab(l, surface_type_, design_type_)
                            self.surfaces.append(self.surfaca_tab_)
                            self.inputArea.addTab(self.surfaca_tab_,l)
                            self.indexes.append(l)
                        elif surface_type_ == tailplane:
                            self.surfaca_tab_ = h_stab_tab(l, surface_type_, design_type_)
                            self.surfaces.append(self.surfaca_tab_)
                            self.inputArea.addTab(self.surfaca_tab_,l)
                            self.indexes.append(l)
                        else:
                            self.surfaca_tab_ = wing_tab(l, surface_type_, design_type_)
                            self.surfaces.append(self.surfaca_tab_)
                            self.inputArea.addTab(self.surfaca_tab_,l)
                            self.indexes.append(l)
        except:
            self.new_surfaces()

    def new_surfaces(self):
        dialog = surface_design_dialog()
        results = dialog.exec_()
        if results == 1:
            text, surface_type_, design_type_ = dialog.accept_inputs()
            if not self.indexes.__contains__(text):
                if design_type_ == unconventional_design:
                    self.surfaca_tab_ = lifting_surface_pane(text, surface_type_, design_type_)
                    self.surfaces.append(self.surfaca_tab_)
                    self.inputArea.addTab(self.surfaca_tab_, text)
                    self.indexes.append(text)
                elif design_type_ == conventional_design:
                    if surface_type_==fin:
                        self.surfaca_tab_ = v_stab_tab(text, surface_type_, design_type_)
                        self.surfaces.append(self.surfaca_tab_)
                        self.inputArea.addTab(self.surfaca_tab_, text)
                        self.indexes.append(text)
                    elif surface_type_==tailplane:
                        self.surfaca_tab_ = h_stab_tab(text, surface_type_, design_type_)
                        self.surfaces.append(self.surfaca_tab_)
                        self.inputArea.addTab(self.surfaca_tab_, text)
                        self.indexes.append(text)
                    else:
                            self.surfaca_tab_ = wing_tab(text, surface_type_, design_type_)
                            self.surfaces.append(self.surfaca_tab_)
                            self.inputArea.addTab(self.surfaca_tab_, text)
                            self.indexes.append(text)
                write_lifting_surface_objects(value=text)
                write_lifting_surface_to_objects(surface_name=text, design_type_=design_type_,
                                                     surface_type_=surface_type_)


        else:
            raise Exception("error")

    def remove_surface_method(self):
        dialog = lifting_surface_delete_dialog()
        results = dialog.exec_()
        if results == 1:
            text = dialog.accept_inputs()
            try:
                self.inputArea.removeTab(self.indexes.index(text))
                self.surfaces.pop(self.indexes.index(text))
                self.monitor.viewer.delete_object(part_name=text)
                delete_lifting_surface_objects(value=text)
                delete_lifting_surface_from_objects(surface_name=text)
            except:
                pass

    def save_all(self):
        for l in self.surfaces:
            l.tab_.init_action()

