import asyncio
import time
from asyncore import loop

from PyQt5.QtCore import QRunnable, pyqtSignal, QTimer

from Utils.data_objects.workflow_placeholders import build_cs, update_surface_3D_, done_, start_, instructions, \
    build_message, done
from Utils.database.geometry.control_surface_database import get_parent_name


class AerodynamicThread(QRunnable):
    def __init__(self, workflow, command):
        super().__init__()
        self.command = command
        self.workflow = workflow
        self.command_run=False

    def run(self):
        self.workflow.update_progress(start_)
        result=""
        while not result==done:
            if self.command_run:
                pass
            else:
                self.workflow.events.set()
                self.workflow.sendTasks.send([self.command])
            loader_points = []
            for i in range(0, 5):
                loader_points.append(".")
                self.workflow.add_text_to_console(build_message + "".join(loader_points))
                time.sleep(0.5)
            result = self.workflow.receiveLofts.recv()

        if result == done:
            self.workflow.add_text_to_console(instructions)
            self.workflow.update_progress(done_)

    def refresh_lifting_surfaces(self):
        self.workflow.events.set()
        self.workflow.sendTasks.send([update_surface_3D_])
        for name, loft in self.workflow.receiveLofts.recv().items():
            self.workflow.viewer.update_object(part_name=name, lofts=loft)


