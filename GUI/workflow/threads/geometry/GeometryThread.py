from PyQt5.QtCore import QRunnable

from Utils.data_objects.workflow_placeholders import build_cs, update_surface_3D_
from Utils.database.geometry.control_surface_database import get_parent_name


class GeometryThread(QRunnable):
    def __init__(self, workflow, command, part_name=None, surface_type=None):
        super().__init__()
        self.command = command
        self.workflow = workflow
        self.part_name = part_name
        self.surface_type = part_name

    def run(self):
        print(self.command)
        if self.command == build_cs:
            self.refresh_lifting_surfaces()
            self.workflow.events.set()
            self.workflow.add_text_to_console("Generating Shape........")
            self.workflow.sendTasks.send(
                [self.command, self.workflow.viewer.current_table])
            for name, loft in self.workflow.receiveLofts.recv().items():
                self.workflow.viewer.update_object(part_name=name, lofts=loft)
            self.workflow.add_text_to_console("Done")

        else:

            self.workflow.add_text_to_console("Modelling.........")
            self.workflow.events.set()
            self.workflow.sendTasks.send([self.command])
            self.workflow.add_text_to_console("Displaying........")
            for name, loft in self.workflow.receiveLofts.recv().items():
                self.workflow.viewer.update_object(part_name=name, lofts=loft)
            self.workflow.add_text_to_console("Done")
    def refresh_lifting_surfaces(self):
        self.workflow.add_text_to_console("Modelling.........")
        self.workflow.events.set()
        self.workflow.sendTasks.send([update_surface_3D_])
        self.workflow.add_text_to_console("Displaying........")
        for name, loft in self.workflow.receiveLofts.recv().items():
            self.workflow.viewer.update_object(part_name=name, lofts=loft)
        self.workflow.add_text_to_console("Done")
