from math import isnan

import numpy as np

from Aerodynamics.datcom.processor.parser import DatcomParser
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


def process_output():
    parser = DatcomParser(database.datcom_output_file)
    dict = parser.get_common()
    stability_derivatives = dict
    database.write_datcom_stability_specification(stability_derivatives)
