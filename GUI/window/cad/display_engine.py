import os

from PyQt5.QtWidgets import QMessageBox

from GUI.window.cad._viewer_ import _viewer_
from Utils.database.database import model_filepath, model_dir
from Utils.database.geometry.control_surface_database import get_surface_type
import meshio

from Utils.file_manager.file_manager_ import clean_after_moveables, clean_after_body


class display_engine(_viewer_):
    def __init__(self):
        super().__init__()
        self.current_table = {}
        self.parts_table = []

    def show_object(self, part_name="", lofts=None):
      try:
        for loft in lofts:
            self.add(loft)
      except:
          try:
                 self.add(lofts)
          except:
              msg = QMessageBox()
              msg.setIcon(QMessageBox.Warning)
              msg.setText("Error")
              msg.setInformativeText("ERROR!")
              msg.setWindowTitle("Aerosoft")
              msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
      self.current_table[part_name] = lofts
      self.parts_table.append(part_name)

    def delete_object(self, part_name=""):

        if self.current_table.get(part_name) is not None:
            lofts = self.current_table[part_name]
            for loft in lofts:
                self.remove(loft)
            self.parts_table.remove(part_name)
        else:
            pass

    def update_object(self, part_name="", lofts=None):
        if self.current_table.get(part_name) is None:
            self.show_object(part_name=part_name, lofts=lofts)
        else:
            self.delete_object(part_name=part_name)
            self.show_object(part_name=part_name, lofts=lofts)

    def refresh(self, parts=[]):
        self.eraseAll()
        for l in parts:
            if self.current_table.__contains__(l):
                self.show_object(part_name=l, lofts=self.current_table[l])
            else:
                pass

    def get(self, value=""):
        if not self.table.get[value] is None:
            return self.table.get[value]
        else:
            return None

    def update_raw_object(self, part_name="", lofts=None):
        if self.current_table.get(part_name) is None:
            self.add(lofts)
            self.current_table[part_name] = lofts
        else:
            self.remove(self.current_table[part_name])
            self.add(lofts)
            self.current_table[part_name] = lofts

    def save_model(self):
        from OCC.StlAPI import StlAPI_Writer
        stl_writer = StlAPI_Writer()
        stl_writer.SetASCIIMode(True)
        for part in self.current_table.values():
            for loft in part:
                stl_writer.Write(loft, model_filepath)

    def switch_to_normal(self):
        self.eraseAll()
        for name, lofts in self.current_table.values():
            self.show_object(part_name=name, lofts=lofts)

    def export_files_for_simulation(self,control_surface={},body={}):
        from OCC.StlAPI import StlAPI_Writer
        stl_writer = StlAPI_Writer()
        stl_writer.SetASCIIMode(True)

        for part, loft in body.items():

            try:
                for l in loft:
                     stl_writer.Write(l, "airplane.stl")
                os.system(f"meshio-convert airplane.stl   airplane.obj")
                clean_after_body("airplane")
            except:
                stl_writer.Write(loft, part + ".stl")
                os.system(f"meshio-convert {part}.stl  {part}.obj")
                clean_after_moveables(part)

