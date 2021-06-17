import pandas as pd

from Utils.data_objects.aerodynamics_placeholders import *
from Utils.database import database
from Utils.database.aerodynamics.sandbox_database import get_free_stream_velocity_range
from Utils.database.aerodynamics.settings_database import get_aoa_range, get_mach_number


def get_pandas_datcom_table(type_="", major_key="", name=""):
    if type_ == datcom_data:
        values = database.read_datcom_stability_specifications()[major_key]
    else:
        values = database.read_stability_specifications()[major_key]
    val = values.get(name)
    y = []
    j_y = []
    prev = 0
    for i in range(9, len(val) + 1, 9):
        y.append(val[prev:i:1])
        prev = i
    for i in y:
        try:
            j_y.append(i[0])
        except:
            pass

    value = {}
    for vel, y_ in zip(get_free_stream_velocity_range(), y):
        value.update({vel: {
            alpha: get_aoa_range(),
            name: y_
        }})
    df = pd.DataFrame(value)
    return df.to_string()


def get_pandas_sandbox_table(type_="", major_key="", name=""):
    if type_ == datcom_data:
        values = database.read_datcom_stability_specifications()[major_key]
    else:
        values = database.read_stability_specifications()[major_key]

    y = values.get(name)
    value = {}
    for vel, y_ in zip(get_free_stream_velocity_range(), y):
        value.update({vel: {
            alpha: get_aoa_range(),
            name: y_
        }})
    df = pd.DataFrame(value)
    return df.to_string()


def read_datcom_table_data(type_="", major_key="", key=""):
    if type_ == datcom_data:
        values = database.read_datcom_stability_specifications()[major_key]
    else:
        values = database.read_stability_specifications()[major_key]
    val = values.get(key)
    x_label = alpha
    alpha_ = get_aoa_range()
    velocity_ = get_free_stream_velocity_range()
    y = []
    j_y = []
    prev = 0
    for i in range(9, len(val) + 1, 9):
        y.append(val[prev:i:1])
        prev = i
    for i in y:
        try:
            j_y.append(i[0])
        except:
            pass

    return alpha_, velocity_, j_y


def read_sandbox_table_data(type_="", major_key="", key=""):
    if type_ == datcom_data:
        values = database.read_datcom_stability_specifications()[major_key]
    else:
        values = database.read_stability_specifications()[major_key]
    val = values.get(key)
    x_label = alpha
    alpha_ = get_aoa_range()
    velocity_ = get_free_stream_velocity_range()
    y = val

    return alpha_, velocity_, y
