from PyQt5.QtCore import QRunnable


class ReceiverThread(QRunnable):
    def __init__(self, workflow):
        super().__init__()
        self.workflow=workflow
    def run(self):
        while 1:
            self.workflow.viewer.update_object(part_name=self.part, lofts=self.workflow.receiveLofts.recv())
            break

