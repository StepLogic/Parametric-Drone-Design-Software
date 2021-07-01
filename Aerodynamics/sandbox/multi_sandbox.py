from math import radians

from Aerodynamics.sandbox.functions_sandbox import f_q, f_alpha
from Utils.data_objects.aerodynamics_placeholders import *
from Utils.database import database
from Utils.database.aerodynamics.sandbox_database import get_free_stream_velocity_range
from Utils.database.aerodynamics.settings_database import get_aoa_range

#TODO Remove multiple mach number support
def run_sandbox_simulation():
    cnb = []
    clb = []
    cyb = []

    cnp = []
    clp = []
    cyp_ = []

    col_q_ = []
    cd_q_ = []
    cm_q_ = []

    cnr = []
    clr = []
    cyr = []

    col_a = []
    cd_ = []
    cm_a = []

    # nominal value of parameter

    # # Finite Difference
    h = 1e-8  # step size
    r_x = []

    for velocity in get_free_stream_velocity_range():
        cnb_temp = []
        clb_temp = []
        cyb_temp = []

        cnp_temp = []
        clp_temp = []
        cyp_temp = []

        col_q_temp = []
        cd_q_temp = []
        cm_q_temp = []

        cnr_temp = []
        clr_temp = []
        cyr_temp = []

        col_a_temp = []
        cd_temp = []
        cm_a_temp = []
        for angle in get_aoa_range():
            col_a_temp.append((f_alpha(angle + h, velocity)["CL"] - f_alpha(angle, velocity)["CL"]) / h)
            cd_temp.append((f_alpha(angle + h, velocity)["CD"] - f_alpha(angle, velocity)["CD"]) / h)
            cm_a_temp.append((f_alpha(angle + h, velocity)["Cm"] - f_alpha(angle, velocity)["Cm"]) / h)
            col_q_temp.append((f_q(radians(angle + h), velocity)["CL"] - f_q(radians(angle), velocity)["CL"]) / h)
            cd_q_temp.append((f_q(radians(angle + h), velocity)["CD"] - f_q(radians(angle), velocity)["CD"]) / h)
            cm_q_temp.append((f_q(radians(angle + h), velocity)["Cm"] - f_q(radians(angle), velocity)["Cm"]) / h)
        col_a.append(col_a_temp)
        cd_.append(cd_temp)
        col_q_.append(col_q_temp)
        cm_q_.append(cm_q_temp)

    stability_derivatives = {
        Cn: {cn:[],cn_beta: cnb, cn_p: cnp, cn_r: cnr},
        Cl: {cl_beta: clb, cl_p: clp, cl_r: clr},
        Cm: {cm_alpha: cm_a, cm_q:cm_q_},
        CL: {col_alpha: col_a, col_q: col_q_},
        CD: {cd_alpha: cd_, cd_q: cd_q},
        CY: {cy_beta: cyb, cy_p: cyp_}}

    database.write_stability_specification(stability_derivatives)

    return 1
