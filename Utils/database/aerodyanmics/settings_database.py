from Utils.data_objects.aerodynamics_placeholders import aoa_range, mach_number_range, altitude
from Utils.database import database


def get_aoa_range():
    return database.read_work_file()[aoa_range]


def set_aoa_range(max=0, min=0):
    data = database.read_work_file()
    try:
        data[aoa_range] = [(x / 10) for x in range(int(min * 10), int(max * 10 + 10), 10)]
        database.write_work_file(data)
    except Exception as e:
        data.update({aoa_range: [(x / 10) for x in range(int(min * 10), int(max * 10 + 10), 10)]})
        database.write_work_file(data)


def set_mach_number_range(max=0, min=0):
    data = database.read_work_file()
    try:
        data[mach_number_range] = [(x / 100) for x in range(int(min * 100), int(max * 100 + 100), 100)]
        database.write_work_file(data)
    except Exception as e:
        data.update({mach_number_range: [(x / 100) for x in range(int(min * 100), int(max * 100 + 100), 100)]})
        database.write_work_file(data)


def get_mach_number_range():
    return database.read_work_file()[mach_number_range]


def set_altitude(altitude_=0):
    data = database.read_work_file()
    try:
        data[altitude] = altitude_
        database.write_work_file(data)
    except Exception as e:
        data.update({altitude: altitude_})
        database.write_work_file(data)


def get_altitude():
    return database.read_work_file()[altitude]


def read_settings():
    value = database.read_work_file()
    altitude_ = value.get(altitude)
    aoa_range_ = value.get(aoa_range)
    mach_number_range_ = value.get(mach_number_range)
    return altitude_, aoa_range_, mach_number_range_
