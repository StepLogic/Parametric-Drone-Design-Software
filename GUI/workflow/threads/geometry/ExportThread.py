import time

from PyQt5 import QtCore
from PyQt5.QtCore import QRunnable, pyqtSignal, QTimer

from GUI.workflow.design_workflow import export_files
from Utils.data_objects.workflow_placeholders import build_cs, update_surface_3D_, done_, start_, instructions, \
    build_message
from Utils.database.geometry.control_surface_database import get_parent_name


class ExportThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, workflow):

        self.workflow = workflow

    def run(self):
        self.workflow.viewer.export_files_for_simulation(body=export_files(self.workflow.config))




