from Utils.database import database


def wipe_design_options():
    value = database.read_work_file()
    value.clear()
    database.write_work_file(value=value)


def wipe_design():
    value = {}
    try:
        database.write_aircraft_specification(value)
    except:
        pass
    try:
        database.write_datcom_stability_specification(value)
    except:
        pass
    try:
        database.write_structures_specification(value)
    except:
        pass
    try:
        database.write_aerodynamic_results(value)
    except:
        pass
    try:
        database.write_control_specifications(value)
    except:
        pass
    try:
        database.write_stability_specification(value)
    except:
        pass

