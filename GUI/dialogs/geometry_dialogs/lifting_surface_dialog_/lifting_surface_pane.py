from PyQt5.QtWidgets import *
import pyqtgraph as pg
from scipy.interpolate import interpolate

from GUI.tabs.geometry_tabs_.unconventional_geometry.lifiting_surface_tabs.lifting_surface_tab import \
    lifting_surface_tab
from Utils.data_objects.lifting_surface_placeholder import *
from Utils.data_objects.placeholder import surface_curve_type


class lifting_surface_pane(QWidget):
    def __init__(self, name="", surface_type_="",design_type_=""):
        super().__init__()
        self.graphWidget = pg.PlotWidget()
        plot_button = QPushButton("Plot")
        plot_button.clicked.connect(self.plot)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.graphWidget)
        main_layout.addWidget(plot_button)

        temp = QWidget()
        temp.setLayout(main_layout)

        self.tab_ = lifting_surface_tab(name=name, surface_type_=surface_type_,design_type_=design_type_,lifting_surface_pane=temp)
        self.name_=name
        section_widget = QWidget()
        section_widget.setLayout(self.tab_.create_widget())

        final_layout = QVBoxLayout()
        temp.setLayout(main_layout)
        final_layout.addWidget(section_widget)


        self.setLayout(final_layout)

    def plot(self):
            parameters = self.tab_.init_action()[lifting_surface][self.name_]
            x_upper = []
            x_lower = []
            x_mid = []
            x_list = [parameters[section_1_x], parameters[section_2_x], parameters[section_3_x], parameters[section_4_x],
                      parameters[section_5_x]]
            y_list = [parameters[section_1_y], parameters[section_2_y], parameters[section_3_y], parameters[section_4_y],
                      parameters[section_5_y]]
            chords = [parameters[section_1_chord], parameters[section_2_chord], parameters[section_3_chord],
                      parameters[section_4_chord], parameters[section_5_chord]]
            print(y_list)
            for x, y, length in zip(x_list, y_list, chords):
                x_upper.append(x + (length / 2))
                x_lower.append(x - (length / 2))
                x_mid.append(x)
            x_mid, y = self.interpolate_coordinates(x_mid, y_list,parameters[surface_curve_type])
            x_upper, y = self.interpolate_coordinates(x_upper, y_list,parameters[surface_curve_type])
            x_lower, y = self.interpolate_coordinates(x_lower, y_list,parameters[surface_curve_type])
            pen = pg.mkPen(color=(255, 0, 0))
            self.graphWidget.clear()
            self.graphWidget.showGrid(x=True, y=True)
            self.graphWidget.plot(y, x_mid,symbol='+',  pen=pen)
            self.graphWidget.plot(y,x_lower,symbol='+',  pen=pen)
            self.graphWidget.plot(y, x_upper,symbol='+', pen=pen)
            self.graphWidget.plot([max(y),max(y)],[max(x_upper),max(x_lower)],pen=pen)
            self.graphWidget.plot([min(y), min(y)], [min(x_upper), min(x_lower)], pen=pen)



    def interpolate_coordinates(self, x_list, y_list,curve_extrusion):
        y_temp = []
        x_temp = []
        if curve_extrusion:
          interp_func = interpolate.interp1d(y_list, x_list, kind="cubic", fill_value="extrapolate")
        else:
          interp_func = interpolate.interp1d(y_list, x_list, kind="linear", fill_value="extrapolate")
        delta = 0.01
        for x, y in zip(x_list, y_list):
            index = y
            try:
                while index < y_list[y_list.index(y) + 1]:
                    index += delta
                    x_index = float(interp_func(index))
                    x_temp.append(x_index)
                    y_temp.append(index)
            except:
                pass
        return x_temp, y_temp
    def save(self):
        self.tab_.init_action()

