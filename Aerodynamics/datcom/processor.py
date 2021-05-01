from math import isnan

import numpy as np

from Utils.data_objects.aerodynamics_placeholders import *
from Utils.database import database


def check_if_nan(value):
    if isnan(value):
        value = 0
        return value
    else:
        return value


def convert_to_float(array):
    new_array = []
    for i in array:
        new_array.append(float(check_if_nan(i)))
    return new_array


def split_array(value):
    array = []
    for i in range(0, len(value)):
        row = value[i]
        for y in range(0, len(row)):
            list_ = list(np.asarray(row[y][0]))
            list_.sort()
            array.append(convert_to_float(list_))
    return array

def process_output(value):
    res_dict = value[0]
    list_variables = list(dict.items(res_dict))
    derivatives = {}
    aerodynamic_specifications = {}
    qqinf = []
    eps = []
    depsdalp = []
    cnp = []
    cd = []
    cl = []
    cm = []
    cn = []
    ca = []
    cma = []
    cyb = []
    cnb = []
    clb = []
    cla = []
    clq = []
    cmq = []
    clad = []
    cmad = []
    clp = []
    cyp = []
    cnp = []
    cnr = []
    clr = []
    for i in list_variables:
        if (i[0] == "xcp"):
            xcp = i[1]
        elif (i[0] == "cn_p"):
            cnp = split_array(list(i[1]))
        elif (i[0] == "cd"):
            cd = split_array(list(i[1]))
        elif (i[0] == "cl"):
            cl = split_array(list(i[1]))
        elif (i[0] == "cm"):
            cm = split_array(list(i[1]))
        elif (i[0] == "cn"):
            cn = split_array(list(i[1]))
        elif (i[0] == "ca"):
            ca = split_array(list(i[1]))
        elif (i[0] == "cma"):
            cma = split_array(list(i[1]))
        elif (i[0] == "cyb"):
            cyb = split_array(list(i[1]))
        elif (i[0] == "cnb"):
            cnb = split_array(list(i[1]))
        elif (i[0] == "clb"):
            clb = split_array(list(i[1]))
        elif (i[0] == "cla"):
            cla = split_array(list(i[1]))
        elif (i[0] == "clq"):
            clq = split_array(list(i[1]))
        elif (i[0] == "cmq"):
            cmq = split_array(list(i[1]))
        elif (i[0] == "clad"):
            clad = split_array(list(i[1]))
        elif (i[0] == "cmad"):
            cmad = split_array(list(i[1]))
        elif (i[0] == "clp"):
            clp = split_array(list(i[1]))
        elif (i[0] == "cyp"):
            cyp = split_array(list(i[1]))
        elif (i[0] == "cnp"):
            cnp = split_array(list(i[1]))
        elif (i[0] == "cnr"):
            cnr = split_array(list(i[1]))
        elif (i[0] == "clr"):
            clr = split_array(list(i[1]))
    stability_derivatives = {
        Cn: {cn_beta: cnb, cn_p: cnp, cn_r: cnr},
        Cl: {cl_beta: clb, cl_p: clp, cl_r: clr},
        Cm: {cm_alpha: cma, cm_q: cmq},
        CL: {col_alpha: cla, col_q: clq},
        CD: {cd_alpha: cd, cd_q: cd},
        CY: {cy_beta: cyb, cy_p: cyp}}
    database.write_datcom_stability_specification(stability_derivatives)
