from math import radians

from Aerodynamics.sandbox.functions_sandbox import f_q, f_alpha, f_beta, f_p, f_r
from Utils.data_objects.aerodynamics_placeholders import *
from Utils.database import database
from Utils.database.aerodynamics.sandbox_database import get_free_stream_velocity_range
from Utils.database.aerodynamics.settings_database import get_aoa_range


# TODO Remove multiple mach number support
def run_sandbox_simulation():
    cnb = []
    clb = []
    cyb = []

    cnp = []
    clp = []
    cyp = []

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

            cnb_temp.append((f_beta(angle + h, velocity)["Cn"] - f_beta(angle, velocity)["Cn"]) / h)
            clb_temp.append((f_beta(angle + h, velocity)["Cl"] - f_beta(angle, velocity)["Cl"]) / h)
            cyb_temp.append((f_beta(angle + h, velocity)["CY"] - f_beta(angle, velocity)["CY"]) / h)

            cnp_temp.append((f_p(radians(angle + h), velocity)["Cn"] - f_p(radians(angle), velocity)["Cn"]) / h)
            clp_temp.append((f_p(radians(angle + h), velocity)["Cl"] - f_p(radians(angle), velocity)["Cl"]) / h)
            cyp_temp.append((f_p(radians(angle + h), velocity)["CY"] - f_p(radians(angle), velocity)["CY"]) / h)

            cnr_temp.append((f_r(radians(angle + h), velocity)["Cn"] - f_r(radians(angle), velocity)["Cn"]) / h)
            clr_temp.append((f_r(radians(angle + h), velocity)["Cl"] - f_r(radians(angle), velocity)["Cl"]) / h)
            cyr_temp.append((f_r(radians(angle + h), velocity)["CY"] - f_r(radians(angle), velocity)["CY"]) / h)

        col_a.append(col_a_temp)
        cd_.append(cd_temp)
        cm_a.append(cm_a_temp)

        col_q_.append(col_q_temp)
        cm_q_.append(cm_q_temp)
        cd_q_.append(cd_temp)

        cnb.append(cnb_temp)
        clb.append(clb_temp)
        cyb.append(cyb_temp)

        cnr.append(cnr_temp)
        clr.append(clr_temp)
        cyr.append(cyr_temp)

        cnp.append(cnp_temp)
        clp.append(clp_temp)
        cyp.append(cyp_temp)

    stability_derivatives = {
        Cn: {cn: [], cn_beta: cnb[0], cn_p: cnp[0], cn_r: cnr[0]},
        Cl: {cl_beta: clb[0], cl_p: clp[0], cl_r: clr[0]},
        Cm: {cm_alpha: cm_a[0], cm_q: cm_q_[0]},
        CL: {col_alpha: col_a[0], col_q: col_q_[0]},
        CD: {cd: cd_[0], cd_q: cd_q_[0]},
        CY: {cy_beta: cyb[0], cy_p: cyp[0]}}

    database.write_stability_specification(stability_derivatives)

    return 1
