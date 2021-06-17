from Utils.data_objects.aerodynamics_placeholders import aoa_range, mach_number, altitude
from Utils.database import database


def get_aoa_range():
    return database.read_work_file()[aoa_range]


def set_aoa_range(max=0, min=0):
    data = database.read_work_file()
    try:
        delta = max / 10
        array = []
        counter = min
        while counter < max or counter == max:
            array.append(round(counter, 2))
            counter += delta
        data[aoa_range] = array
        database.write_work_file(data)
    except Exception as e:
        delta = max / 10
        array = []
        counter = min
        while counter < max or counter == max:
            array.append(round(counter, 2))
            counter += delta
        data.update({aoa_range: array})
        database.write_work_file(data)


def set_mach_number(value=0.0):
    data = database.read_work_file()
    try:
        data[mach_number] = value
        database.write_work_file(data)
    except Exception as e:
        data.update({mach_number: value})
        database.write_work_file(data)


def get_mach_number():
    return database.read_work_file()[mach_number]


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
    mach_number_range_ = value.get(mach_number)
    return altitude_, aoa_range_, mach_number_range_
