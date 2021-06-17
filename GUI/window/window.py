import logging
import os
import sys

from OCC.Display.OCCViewer import OffscreenRenderer
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel

from GUI.window.cad.display_engine import display_engine
from Utils.data_objects.workflow_placeholders import done_, instructions

log = logging.getLogger(__name__)


def check_callable(_callable):
    if not callable(_callable):
        raise AssertionError("The function supplied is not callable")


def init_display(backend_str=None, app=None):
    if os.getenv("PYTHONOCC_OFFSCREEN_RENDERER") == "1":
        # create the offscreen renderer
        offscreen_renderer = OffscreenRenderer()

        def do_nothing(*kargs, **kwargs):
            """ takes as many parameters as you want,
                ans does nothing
                """
            pass

        def call_function(s, func):
            """ A function that calls another function.
                Helpfull to bypass add_function_to_menu. s should be a string
                """
            check_callable(func)
            log.info("Execute %s :: %s menu fonction" % (s, func.__name__))
            func()
            log.info("done")

        # returns empty classes and functions
        return offscreen_renderer, do_nothing, do_nothing, call_function

    # Qt based simple GUI
    if True:
        class MainWindow(QtWidgets.QMainWindow):

            def __init__(self, *args):
                QtWidgets.QMainWindow.__init__(self, *args)

                self.canva = display_engine()
                self.setWindowTitle("Aerosoft")
                self.mainvbox_ = QVBoxLayout()
                self.console = QLabel(instructions)
                self.console.setFixedHeight(20)

                self.mainvbox_.addWidget(self.console)
                self.mainvbox_.addWidget(self.canva)

                self.central_widget = QWidget()
                self.central_widget.setLayout(self.mainvbox_)
                self.setCentralWidget(self.central_widget)
                if sys.platform != 'darwin':
                    self.menu_bar = self.menuBar()
                else:
                    self.menu_bar = QtWidgets.QMenuBar()
                self._menus = {}
                self._menu_methods = {}
                # place the window in the center of the screen, at half the
                # screen size
                self.centerOnScreen()

            def add_text_to_console(self, message):
                self.console.setText(message)

            def update_progress(self, value):
                if value== done_:
                    self.menu_bar.setEnabled(True)
                else:
                    self.menu_bar.setDisabled(True)

            def centerOnScreen(self):
                '''Centers the window on the screen.'''
                resolution = QtWidgets.QApplication.desktop().screenGeometry()
                x = (resolution.width() - self.frameSize().width()) / 3
                y = (resolution.height() - self.frameSize().height()) / 1
                self.move(x, y)

            def add_menu(self, menu_name):
                _menu = self.menu_bar.addMenu("&" + menu_name)
                self._menus[menu_name] = _menu

            def add_sub_menu_to_menu(self, sub_menu_name, menu_name):
                _menu = self._menus[menu_name]
                sub_menu = _menu.addMenu(sub_menu_name)
                self._menus[sub_menu_name] = sub_menu

            def add_function_to_sub_menu(self, menu_name, _callable):
                check_callable(_callable)
                try:
                    _action = QtWidgets.QAction(_callable.__name__.replace('_', ' ').lower(), self)
                    # if not, the "exit" action is now shown...
                    _action.setMenuRole(QtWidgets.QAction.NoRole)
                    _action.triggered.connect(_callable)

                    self._menus[menu_name].addAction(_action)
                except KeyError:
                    raise ValueError('the menu item %s does not exist' % menu_name)

            def add_function_to_menu(self, menu_name, _callable):
                check_callable(_callable)
                try:
                    _action = QtWidgets.QAction(_callable.__name__.replace('_', ' ').lower(), self)
                    # if not, the "exit" action is now shown...
                    _action.setMenuRole(QtWidgets.QAction.NoRole)
                    _action.triggered.connect(_callable)

                    self._menus[menu_name].addAction(_action)
                except KeyError:
                    raise ValueError('the menu item %s does not exist' % menu_name)

        # following couple of lines is a tweak to enable ipython --gui='qt'

        win = MainWindow()
        win.width = 700
        win.height = 600
        win.show()
        win.centerOnScreen()
        win.canva.InitDriver()
        win.canva.init2()
        win.setFixedWidth(700)
        win.setFixedHeight(600)
        win.canva.qApp = app

        global viewer
        viewer = win.canva

        def update_progress(*args, **kwargs):
            win.update_progress(*args, **kwargs)

        def add_text_to_console(*args, **kwargs):
            win.add_text_to_console(*args, **kwargs)

        def add_menu(*args, **kwargs):
            win.add_menu(*args, **kwargs)

        def add_sub_menu_to_menu(*args, **kwargs):
            win.add_sub_menu_to_menu(*args, **kwargs)

        def add_function_to_sub_menu(*args, **kwargs):
            win.add_function_to_sub_menu(*args, **kwargs)

        def add_function_to_menu(*args, **kwargs):
            win.add_function_to_menu(*args, **kwargs)

        def start_display():
            win.raise_()  # make the application float to the top

        def close():
            win.close()

        return viewer, start_display, add_menu, add_function_to_menu, add_sub_menu_to_menu, add_function_to_sub_menu, add_text_to_console,update_progress, close
