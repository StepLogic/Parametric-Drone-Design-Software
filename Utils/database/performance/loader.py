import pandas as pd

from Utils.data_objects.aerodynamics_placeholders import *
from Utils.database import database
from Utils.database.aerodynamics.sandbox_database import get_free_stream_velocity_range
from Utils.database.aerodynamics.settings_database import get_aoa_range, get_mach_number


def read_data(key=""):
    values = database.read_performance_specifications()
    val = values.get(key)
    time = values.get("time")
    y = val

    return time, y
