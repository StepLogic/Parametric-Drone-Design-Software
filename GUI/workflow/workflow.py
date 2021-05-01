from PyQt5.QtWidgets import *

from GUI.window.menu import setup_ui
from GUI.window.window import init_display


class work_flow_monitor(QApplication):
    def __init__(self, *args, **kwargs):
        super(work_flow_monitor, self).__init__(*args, **kwargs)
        self.events=None
        self.receiveLofts=None
        self.sendTasks=None
        self.viewer = None
        self.start_display = None
        self.add_menu = None
        self.add_function_to_menu = None
        self.add_sub_menu_to_menu = None
        self.add_function_to_sub_menu = None
        self.add_text_to_console = None
        self.config = None
        self.main_window = None
        self.design_window = None
        self.boom_triggers={}

    def execute_design_window(self):
        self.viewer, self.start_display, \
        self.add_menu, self.add_function_to_menu, self.add_sub_menu_to_menu, \
        self.add_function_to_sub_menu, self.add_text_to_console,self.update_progress,self.close_window = init_display(
            "qt-pyqt5", app=self)
        setup_ui(self)




