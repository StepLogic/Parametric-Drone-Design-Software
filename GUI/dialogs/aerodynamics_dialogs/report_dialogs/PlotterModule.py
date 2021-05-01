import matplotlib.pyplot as plt
from utils.database.Database import read_control_specifications

from Helper import absolute_path


class PlotterModule():

    def __init__(self):
        self.cn_beta = []
        self.cl_beta = []
        self.cm_beta = []
        self.cn_alpha = []
        self.cl_alpha = []
        self.cm_alpha = []
        self.cn_u = []
        self.cl_u = []
        self.cm_u = []
        self.cn_p = []
        self.cl_p = []
        self.cm_p = []
        self.cn_q = []
        self.cl_q = []
        self.cm_q = []
        self.cn_r = []
        self.cl_r = []
        self.cm_r = []

        self.cn_aileron = []
        self.cl_aileron = []
        self.cm_aileron = []

        self.cn_elevator = []
        self.cl_elevator = []
        self.cm_elevator = []

        self.cn_rudder = []
        self.cl_rudder = []
        self.cm_rudder = []

        self.col_beta = []
        self.cd_beta = []
        self.cy_beta = []

        self.col_alpha = []
        self.cd_alpha = []
        self.cy_alpha = []

        self.col_u = []
        self.cd_u = []
        self.cy_u = []

        self.col_p = []
        self.cd_p = []
        self.cy_p = []

        self.col_q = []
        self.cd_q = []
        self.cy_q = []

        self.col_r = []
        self.cd_r = []
        self.cy_r = []

        self.col_aileron = []
        self.cd_aileron = []
        self.cy_aileron = []

        self.col_elevator = []
        self.cd_elevator = []
        self.cy_elevator = []

        self.col_rudder = []
        self.cd_rudder = []
        self.cy_rudder = []

        self.r_x = []
        self.v_x = []
        self.value = read_control_specifications()
        self.assign_values(value=self.value)

    def assign_values(self, value={}):
        value=value["functions"]
        self.cn_beta = value["Cn"]["cn_beta"]
        self.cn_alpha = value["Cn"]["cn_alpha"]
        self.cn_u = value["Cn"]["cn_u"]
        self.cn_p = value["Cn"]["cn_p"]
        self.cn_q = value["Cn"]["cn_q"]
        self.cn_r = value["Cn"]["cn_r"]
        self.cn_elevator = value["Cn"]["cn_elevator"]
        self.cn_aileron = value["Cn"]["cn_aileron"]
        self.cn_rudder = value["Cn"]["cn_rudder"]

        self.cl_beta = value["Cl"]["cl_beta"]
        self.cl_alpha = value["Cl"]["cl_alpha"]
        self.cl_u = value["Cl"]["cl_u"]
        self.cl_p = value["Cl"]["cl_p"]
        self.cl_q = value["Cl"]["cl_q"]
        self.cl_r = value["Cl"]["cl_r"]
        self.cl_elevator = value["Cl"]["cl_elevator"]
        self.cl_aileron = value["Cl"]["cl_aileron"]
        self.cl_rudder = value["Cl"]["cl_rudder"]

        self.cm_beta = value["Cm"]["cm_beta"]
        self.cm_alpha = value["Cm"]["cm_alpha"]
        self.cm_u = value["Cm"]["cm_u"]
        self.cm_p = value["Cm"]["cm_p"]
        self.cm_q = value["Cm"]["cm_q"]
        self.cm_r = value["Cm"]["cm_r"]
        self.cm_elevator = value["Cm"]["cm_elevator"]
        self.cm_aileron = value["Cm"]["cm_aileron"]
        self.cm_rudder = value["Cm"]["cm_rudder"]

        self.cd_beta = value["CD"]["cd_beta"]
        self.cd_alpha = value["CD"]["cd_alpha"]
        self.cd_u = value["CD"]["cd_u"]
        self.cd_p = value["CD"]["cd_p"]
        self.cd_q = value["CD"]["cd_q"]
        self.cd_r = value["CD"]["cd_r"]
        self.cd_elevator = value["CD"]["cd_elevator"]
        self.cd_aileron = value["CD"]["cd_aileron"]
        self.cd_rudder = value["CD"]["cd_rudder"]

        self.col_beta = value["CL"]["col_beta"]
        self.col_alpha = value["CL"]["col_alpha"]
        self.col_u = value["CL"]["col_u"]
        self.col_p = value["CL"]["col_p"]
        self.col_q = value["CL"]["col_q"]
        self.col_r = value["CL"]["col_r"]
        self.col_elevator = value["CL"]["col_elevator"]
        self.col_aileron = value["CL"]["col_aileron"]
        self.col_rudder = value["CL"]["col_rudder"]

        self.cy_beta = value["CY"]["cy_beta"]
        self.cy_alpha = value["CY"]["cy_alpha"]
        self.cy_u = value["CY"]["cy_u"]
        self.cy_p = value["CY"]["cy_p"]
        self.cy_q = value["CY"]["cy_q"]
        self.cy_r = value["CY"]["cy_r"]
        self.cy_elevator = value["CY"]["cy_elevator"]
        self.cy_aileron = value["CY"]["cy_aileron"]
        self.cy_rudder = value["CY"]["cy_rudder"]

        self.v_x = value["v_x"]
        self.r_x = value["r_x"]
    def plot_common(self):
        self.plot_cd_against_cl()
        self.plot_cd_against_alpha()
        self.plot_cl_against_alpha()

    def plot_cl_against_alpha(self):
        self.plot2d(
            title='Cl against Alpha',
            x_name=self.r_x, x_label='Alpha,deg',
            y_name=self.cm_alpha, y_label='CL')
    def plot_cd_against_cl(self):
        self.plot2d(
            title='Drag Polar',
            x_name=self.cl_alpha, x_label='CL',
            y_name=self.cd_alpha, y_label='CD')

    def plot_cy_against_p(self):
        self.plot2d(
            title='Roll Rate effect on Side Force Coefficient',
            x_name=self.r_x, x_label='P, deg',
            y_name=self.cy_p, y_label='Cy')

    def plot_cy_against_alpha(self):
        self.plot2d(
            title='Basic Side Force Coefficient',
            x_name=self.r_x, x_label='Alpha, deg',
            y_name=self.cy_alpha, y_label="Cy")

    def plot_cl_roll_against_aileron_deflection(self):
        self.plot2d(
            title='Aileron effect on Roll Moment Coefficient',
            x_name=self.r_x, x_label='Aileron, deg',
            y_name=self.col_aileron, y_label='Cl')

    def plot_cl_roll_against_beta(self):
        self.plot2d(
            title='Side slip effect on Roll Moment Coefficient',
            x_name=self.r_x, x_label='beta, deg',
            y_name=self.col_beta, y_label="Cl")

    def plot_cl_roll_against_p(self):
        self.plot2d(
            title='RollRate effect on Roll Moment Coefficient',
            x_name='alpha', x_label='p, deg',
            y_name=self.col_r, y_label='Cl')

    def plot_cl_roll_against_r(self):
        self.plot2d(
            title='YawRate effect on Roll Moment Coefficient',
            x_name=self.r_x, x_label='r, deg',
            y_name=self.col_r, y_label='Cl')

    def plot_cm_against_q(self):
        self.plot2d(
            title='{name}-Pitch Rate effect on Pitch Moment Coefficient',
            x_name=self.r_x, x_label='q, deg',
            y_name=self.cm_q, y_label='Cm')

    def plot_cm_against_elevator_deflection(self):
        self.plot2d(
            title='Elevator effect on Pitch Moment Coefficient',
            x_name=self.r_x, x_label='Elevator, deg',
            y_name=self.cn_elevator, y_label='Cm')

    def plot_cn_against_beta(self):
        self.plot2d(
            title='Side Slip effect on Yaw Moment Coefficient',
            x_name=self.r_x, x_label='beta,deg',
            y_name=self.cn_beta, y_label='Cn')

    def plot_cn_against_r(self):
        self.plot2d(
            title='Yaw Rate effect on Yaw Moment Coefficient',
            x_name=self.r_x, x_label='r,deg',
            y_name=self.cn_r, y_label='Cn')

    def plot_cm_against_alpha(self):
        self.plot2d(title="plot_cm_against_alpha", x_name=self.r_x, y_name=self.cl_alpha, y_label="Cm", x_label="Alpha")

    def plot_cy_against_beta(self):
        self.plot2d(title="plot_cy_against_beta", x_name=self.r_x, y_name=self.cy_beta, y_label="Cy", x_label="Beta")

    def plot_cd_against_alpha(self):
        self.plot2d(title="plot_cd_against_alpha", x_name=self.r_x, y_name=self.cd_alpha, y_label="Cd", x_label="Alpha")

    def plot_cd_against_aileron_deflection(self):
        self.plot2d(title="plot_cd_against_aileron_deflection", x_name=self.r_x, y_name=self.cd_aileron, y_label="Cd",
                    x_label="Aileron")

    def plot2d(self, title, x_name, x_label, y_name, y_label):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        y = y_name
        x = x_name
        ax.plot(x, y)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid()
        plt.show()
        plt.savefig(absolute_path + "/resources/results/{}.png".format(title))
        plt.close(fig)
    @staticmethod
    def plot_scatter_3D(x,y,z):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z)
        plt.show()