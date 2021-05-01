from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from GUI.dialogs.propulsion_dialogs.propeller.propeller_pane import propeller_pane
from Utils.database.propulsion.propulsion_database import read_propeller_objects, delete_propeller_objects


class propeller_dialog(QDialog):
    def __init__(self, workflow):
      super().__init__()
      self.setMinimumSize(600, 700)
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
      self.load_surfaces()
      self.layout.addRow(self.inputArea)
      self.layout.addRow(self.remove_surface, self.add_surface)
      self.layout.addRow(self.buttons)
      self.setLayout(self.layout)
      self.buttons.accepted.connect(self.accept)
      self.buttons.rejected.connect(self.reject)

    def load_surfaces(self):
            try:
                surface_list = read_propeller_objects()
                if len(surface_list) == 0:
                    self.new_surfaces()
                else:
                    for l in surface_list:
                        print(l)
                        self.surfaca_tab_ = propeller_pane(l)
                        self.surfaces.append(self.surfaca_tab_)
                        self.inputArea.addTab(self.surfaca_tab_, l)
                        self.indexes.append(l)
            except Exception as e:
                print("error",e.__traceback__)
                self.new_surfaces()

    def new_surfaces(self):
            text, ok = QInputDialog.getText(self, 'New Surface', 'Enter Surface Name')
            if ok and not self.indexes.__contains__(text):
                self.surfaca_tab_ = propeller_pane(text)
                self.surfaces.append(self.surfaca_tab_)
                self.inputArea.addTab(self.surfaca_tab_, text)
                self.indexes.append(text)

    def remove_surface_method(self):
            text, ok = QInputDialog.getText(self, 'Remove Surface', 'Enter Surface Name')
            if ok:
                try:
                    self.inputArea.removeTab(self.indexes.index(text))
                    self.surfaces.pop(self.indexes.index(text))
                    self.monitor.viewer.delete_object(part_name=text)
                    delete_propeller_objects(value=text)
                    self.monitor.geometry_object.lifting_surfaces.remove(self.monitor.viewer.get(text))
                except:
                    pass

    def save_all(self):
            for l in self.surfaces:
                l.tab.init_action()
