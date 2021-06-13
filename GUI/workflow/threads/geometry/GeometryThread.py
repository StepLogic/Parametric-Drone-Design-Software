import time

from PyQt5.QtCore import QRunnable, pyqtSignal, QTimer

from Utils.data_objects.workflow_placeholders import build_cs, update_surface_3D_, done_, start_, instructions, \
    build_message
from Utils.database.geometry.control_surface_database import get_parent_name


class GeometryThread(QRunnable):

    def __init__(self, workflow, command):
        super().__init__()
        self.command = command
        self.workflow = workflow


    def run(self):
        self.workflow.update_progress(start_)

        if self.command == build_cs:
            self.refresh_lifting_surfaces()
            self.workflow.events.set()
            self.workflow.sendTasks.send(
                [self.command, self.workflow.viewer.current_table])

        else:
            self.workflow.events.set()
            self.workflow.sendTasks.send([self.command])
        for name, loft in self.workflow.receiveLofts.recv().items():
            self.workflow.viewer.update_object(part_name=name, lofts=loft)
        self.workflow.add_text_to_console(instructions)
        self.workflow.update_progress(done_)

    def refresh_lifting_surfaces(self):
        self.workflow.events.set()
        self.workflow.sendTasks.send([update_surface_3D_])
        for name, loft in self.workflow.receiveLofts.recv().items():
            self.workflow.viewer.update_object(part_name=name, lofts=loft)


