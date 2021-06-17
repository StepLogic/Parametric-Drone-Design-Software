import time

from PyQt5 import QtCore
from PyQt5.QtCore import QRunnable, pyqtSignal, QTimer

from Utils.data_objects.workflow_placeholders import build_cs, update_surface_3D_, done_, start_, instructions, \
    build_message
from Utils.database.geometry.control_surface_database import get_parent_name


class GeometryThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

    def setup(self, workflow, command):
        self.command = command
        self.workflow = workflow

    def run(self):
        self.workflow.update_progress(start_)
        self.workflow.events.set()
        self.workflow.sendTasks.send([self.command])
        self.trigger.emit(self.workflow.receiveLofts.recv())




