import logging

from Utils.data_objects.structures_placeholder import center_of_gravity, moments_of_inertia, mass_of_battery_or_fuel, \
    mass_of_payload, mass_of_wing, mass_of_fuselage, maximum_takeoff_weight, mass_of_engine_or_motor
from Utils.database import database


def get_center_of_mass():
    return database.read_structures_specifications()[center_of_gravity]


def set_center_of_mass(value=None):
    if value is None:
        value = {}
    data = database.read_structures_specifications()
    try:
        data[center_of_gravity].update(value)
        database.write_structures_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({center_of_gravity: value})
        database.write_structures_specification(data)


def get_moments_of_inertia():
    return database.read_structures_specifications()[moments_of_inertia]


def set_moments_of_inertia(value=None):
    if value is None:
        value = {}
    data = database.read_structures_specifications()
    try:
        data[moments_of_inertia].update(value)
        database.write_structures_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({moments_of_inertia: value})
        database.write_structures_specification(data)


def set_mass_of_battery_or_fuel(value=None):
    if value is None:
        value = {}
    data = database.read_structures_specifications()
    try:
        data[mass_of_battery_or_fuel].update(value)
        database.write_structures_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({mass_of_battery_or_fuel: value})
        database.write_structures_specification({mass_of_battery_or_fuel: value})

def get_mass_of_battery_or_fuel():
    return database.read_structures_specifications()[mass_of_battery_or_fuel]



def set_mass_of_engine_or_motor(value=None):
    if value is None:
        value = {}
    data = database.read_structures_specifications()
    try:
        data[mass_of_engine_or_motor].update(value)
        database.write_structures_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({mass_of_battery_or_fuel: value})
        database.write_structures_specification({mass_of_engine_or_motor: value})



def get_mass_of_engine_or_motor():
    return database.read_structures_specifications()[mass_of_engine_or_motor]


def set_mass_of_payload(value=0.0):
    data = database.read_structures_specifications()
    try:
        data[mass_of_payload] = value
        database.write_structures_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({mass_of_payload: value})
        database.write_structures_specification(data)


def get_mass_of_payload():
    return database.read_structures_specifications()[mass_of_payload]


def set_mass_of_wing(value=0.0):
    data = database.read_structures_specifications()
    try:
        data[mass_of_wing] = value
        database.write_aircraft_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({mass_of_wing: value})
        database.write_structures_specification(data)


def get_mass_of_wing():
    return database.read_structures_specifications()[mass_of_wing]


def set_mass_of_fuselage(value=0.0):
    data = database.read_structures_specifications()
    try:
        data[mass_of_fuselage] = value
        database.write_aircraft_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({mass_of_fuselage: value})
        database.write_structures_specification(data)


def get_mass_of_fuselage():
    return database.read_structures_specifications()[mass_of_fuselage]


def set_maximum_takeoff_weight(value=0.0):
    data = database.read_structures_specifications()
    try:
        data[maximum_takeoff_weight] = value
        database.write_aircraft_specification(data)
    except Exception as e:
        logging.error(e)
        data.update({maximum_takeoff_weight: value})
        database.write_structures_specification(data)


def get_maximum_takeoff_weight():
    return database.read_structures_specifications()[maximum_takeoff_weight]


def get_structures_specifications():
    value = database.read_structures_specifications()

    mass_of_battery_or_fuel_ = value[mass_of_battery_or_fuel]

    maximum_takeoff_weight_ = value[maximum_takeoff_weight]

    mass_of_payload_ = value[mass_of_payload]

    mass_of_engine_or_motor_=value[mass_of_engine_or_motor]
    return mass_of_battery_or_fuel_,\
           mass_of_engine_or_motor_,\
           maximum_takeoff_weight_, \
           mass_of_payload_, \



def set_structure_specifications(value=None):
    if value is None:
        value = {}
    database.write_structures_specification(value)
