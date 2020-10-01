import numpy as np

from utils.Database import read_aerodynamic_results


class AeroTrim():
    initailized = False

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
        self.value = read_aerodynamic_results()
        self.assign_values(value=self.value)

    def assign_values(self, value={}):
        print(value)
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

        print(value["CL"])
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

    def get_wetted_area(self):
        return self.value["spec"]

    def get_side_force(self, alpha=0, beta=0, u=0, p=0, q=0, r=0, aileron=0, rudder=0, elevator=0):
        cy_beta = np.interp(beta, self.r_x, self.cy_beta)
        cy_alpha = np.interp(alpha, self.r_x, self.cy_alpha)
        cy_u = np.interp(u, self.v_x, self.cy_u)
        cy_p = np.interp(p, self.r_x, self.cy_p)
        cy_q = np.interp(q, self.r_x, self.cy_q)
        cy_r = np.interp(r, self.r_x, self.cy_r)
        cy_aileron = np.interp(aileron, self.r_x, self.cy_aileron)
        cy_elevator = np.interp(elevator, self.r_x, self.cy_elevator)
        cy_rudder = np.interp(rudder, self.r_x, self.cy_rudder)
        cy = cy_beta * beta + cy_alpha * alpha + cy_p * p + cy_q * q + cy_r * r + cy_u * u + cy_elevator * elevator + cy_rudder * rudder + cy_aileron * aileron
        return cy

    def get_cl(self, alpha=0, beta=0, u=0, p=0, q=0, r=0, aileron=0, rudder=0, elevator=0):
        col_beta = np.interp(beta, self.r_x, self.col_beta)
        col_alpha = np.interp(alpha, self.r_x, self.col_alpha)
        col_u = np.interp(u, self.v_x, self.col_u)
        col_p = np.interp(p, self.r_x, self.col_p)
        col_q = np.interp(q, self.r_x, self.col_q)
        col_r = np.interp(r, self.r_x, self.col_r)
        col_aileron = np.interp(aileron, self.r_x, self.col_aileron)
        col_elevator = np.interp(elevator, self.r_x, self.col_elevator)
        col_rudder = np.interp(rudder, self.r_x, self.col_rudder)
        col = col_beta * beta + col_alpha * alpha + col_p * p + col_q * q + col_r * r + col_u * u + col_elevator * elevator + col_rudder * rudder + col_aileron * aileron
        return col

    def get_cd(self, alpha=0, beta=0, u=0, p=0, q=0, r=0, aileron=0, rudder=0, elevator=0):
        print(self.cd_beta, self.r_x)
        cd_beta = np.interp(beta, self.r_x, self.cd_beta)
        cd_alpha = np.interp(alpha, self.r_x, self.cd_alpha)
        cd_u = np.interp(u, self.v_x, self.cd_u)
        cd_p = np.interp(p, self.r_x, self.cd_p)
        cd_q = np.interp(q, self.r_x, self.cd_q)
        cd_r = np.interp(r, self.r_x, self.cd_r)
        cd_aileron = np.interp(aileron, self.r_x, self.cd_aileron)
        cd_elevator = np.interp(elevator, self.r_x, self.cd_elevator)
        cd_rudder = np.interp(rudder, self.r_x, self.cd_rudder)
        cd = cd_beta * beta + cd_alpha * alpha + cd_p * p + cd_q * q + cd_r * r + cd_u * u + cd_elevator * elevator + cd_rudder * rudder + cd_aileron * aileron
        return cd

    def get_yaw_moment(self, alpha=0, beta=0, u=0, p=0, q=0, r=0, aileron=0, rudder=0, elevator=0):
        cn_beta = np.interp(beta, self.r_x, self.cn_beta)
        cn_alpha = np.interp(alpha, self.r_x, self.cn_alpha)
        cn_u = np.interp(u, self.v_x, self.cn_u)
        cn_p = np.interp(p, self.r_x, self.cn_p)
        cn_q = np.interp(q, self.r_x, self.cn_q)
        cn_r = np.interp(r, self.r_x, self.cn_r)
        cn_aileron = np.interp(aileron, self.r_x, self.cn_aileron)
        cn_elevator = np.interp(elevator, self.r_x, self.cn_elevator)
        cn_rudder = np.interp(rudder, self.r_x, self.cn_rudder)
        cn = cn_beta * beta + cn_alpha * alpha + cn_p * p + cn_q * q + cn_r * r + cn_u * u + cn_elevator * elevator + cn_rudder * rudder + cn_aileron * aileron
        return cn

    def get_rolling_moment(self, alpha=0, beta=0, u=0, p=0, q=0, r=0, aileron=0, rudder=0, elevator=0):
        cl_beta = np.interp(beta, self.r_x, self.cl_beta)
        cl_alpha = np.interp(alpha, self.r_x, self.cl_alpha)
        cl_u = np.interp(u, self.v_x, self.cl_u)
        cl_p = np.interp(p, self.r_x, self.cl_p)
        cl_q = np.interp(q, self.r_x, self.cl_q)
        cl_r = np.interp(r, self.r_x, self.cl_r)
        cl_aileron = np.interp(aileron, self.r_x, self.cl_aileron)
        cl_elevator = np.interp(elevator, self.r_x, self.cl_elevator)
        cl_rudder = np.interp(rudder, self.r_x, self.cl_rudder)
        cl = cl_beta * beta + cl_alpha * alpha + cl_p * p + cl_q * q + cl_r * r + cl_u * u + cl_elevator * elevator + cl_rudder * rudder + cl_aileron * aileron
        return cl

    def get_pitching_moment(self, alpha=0, beta=0, u=0, p=0, q=0, r=0, wetted_area=0, aileron=0, rudder=0, elevator=0):
        cm_beta = np.interp(beta, self.r_x, self.cm_beta)
        cm_alpha = np.interp(alpha, self.r_x, self.cm_alpha)
        cm_u = np.interp(u, self.v_x, self.cm_u)
        cm_p = np.interp(p, self.r_x, self.cm_p)
        cm_q = np.interp(q, self.r_x, self.cm_q)
        cm_r = np.interp(r, self.r_x, self.cm_r)
        cm_aileron = np.interp(aileron, self.r_x, self.cm_aileron)
        cm_elevator = np.interp(elevator, self.r_x, self.cm_elevator)
        cm_rudder = np.interp(rudder, self.r_x, self.cm_rudder)
        cm = cm_beta * beta + cm_alpha * alpha + cm_p * p + cm_q * q + cm_r * r + cm_u * u + cm_elevator * elevator + cm_rudder * rudder + cm_aileron * aileron
        return cm
