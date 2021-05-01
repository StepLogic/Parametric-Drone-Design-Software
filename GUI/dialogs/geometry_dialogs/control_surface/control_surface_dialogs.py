from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.alerts.control_surface_delete_dialog import control_surface_delete_dialog
from GUI.tabs.geometry_tabs_.control_surface.control_surface_tab import control_surface_tab
from Utils.database.geometry.control_surface_database import read_control_surface_objects, \
    delete_control_surface_from_objects, delete_control_surface_objects


class control_surface_dialog(QDialog):
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
            surface_list = read_control_surface_objects()
            if len(surface_list) == 0:
                self.new_surfaces()
            else:
                for l in surface_list:
                    self.surfaca_tab_ = control_surface_tab(l)
                    self.surfaces.append(self.surfaca_tab_)
                    self.inputArea.addTab(self.surfaca_tab_, l)
                    self.indexes.append(l)
        except :
            self.new_surfaces()
    def new_surfaces(self):
        text, ok = QInputDialog.getText(self, 'New Surface', 'Enter Surface Name')
        if ok and not self.indexes.__contains__(text):
                self.surfaca_tab_ = control_surface_tab(text)
                self.surfaces.append(self.surfaca_tab_)
                self.inputArea.addTab(self.surfaca_tab_,text)
                self.indexes.append(text)

        else:
            raise Exception("error")

    def remove_surface_method(self):
        dialog = control_surface_delete_dialog()
        results = dialog.exec_()
        if results == 1:
            text = dialog.accept_inputs()
            try:
                self.inputArea.removeTab(self.indexes.index(text))
                self.surfaces.pop(self.indexes.index(text))
                self.monitor.viewer.delete_object(part_name=text)
                delete_control_surface_objects(value=text)
                delete_control_surface_from_objects(surface_name=text)
            except:
                pass

    def save_all(self):
        for l in self.surfaces:
            l.tab.init_action()
