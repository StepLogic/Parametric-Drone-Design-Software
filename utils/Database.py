import json

from Helper import absolute_path, resource_path

aircraft_specifications_filepath = resource_path(absolute_path + "/resources/Aircraft_Specification.json")
aerodynamic_specification_filepath = resource_path(absolute_path + "/resources/Aircraft_Aerodynamic_Specification.json")
stability_specification_filepath = resource_path(absolute_path + "/resources/Aircraft_Stability_Specification.json")
structure_specification_filepath = absolute_path + "/resources/Aircraft_Structure_Specification.json"


def read_structures_specifications():
    return readFile(structure_specification_filepath)


def update_structure_specifications(key="", value={}):
    data = read_structures_specifications()
    try:
        data[key].update(value)
    except:
        data.update({key: value})
    write_structures_specification(data)


def write_structures_specification(Values={}):
    write(structure_specification_filepath, Values)


def read_aerodynamic_results():
    return readFile(aerodynamic_specification_filepath)


def write_aerodynamic_results(Values={}):
    write(aerodynamic_specification_filepath, Values)


def read_control_specifications():
    return readFile(stability_specification_filepath)


def write_control_specifications(values={}):
    write(stability_specification_filepath, values)


def update_control_specifications(key="", value={}):
    data = read_control_specifications()
    data.update(value)
    write_control_specifications(data)


def read_aircraft_specifications():
    return readFile(aircraft_specifications_filepath)


def write_aircraft_specification(values={}):
    write(aircraft_specifications_filepath, values)


def update_aircraft_specifications(key="", value={}):
    data = read_aircraft_specifications()
    data.update(value)
    write_aircraft_specification(data)


def read_stability_specifications():
    return readFile(stability_specification_filepath)


def write_stability_specification(values={}):
    write(stability_specification_filepath, values)


def update_stability_specifications(key="", value={}):
    data = read_stability_specifications()
    data.update(value)
    write_stability_specification(data)


def readFile(filepath=""):
    with open(filepath) as json_file:
        data = json.load(json_file)
    return data


def write(filepath="", values={}):
    a_file = open(filepath, "w")
    json.dump(values, a_file)
    a_file.close()
