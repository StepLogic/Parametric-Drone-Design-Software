import json

from Helper import absolute_path, resource_path
airfoil_path = resource_path(absolute_path + "/Resources/airfoil/export/names.txt")
resource_dir_cpacs = resource_path(absolute_path + "/Resources/cpacs")
resource_dir_cpacs_out = resource_path(absolute_path + "/Resources/cpacs/structure.xml")
work_file_path = resource_path(absolute_path + "/Resources/json/workfile.json")
aircraft_specifications_filepath = resource_path(absolute_path + "/Resources/json/specification.json")
aerodynamic_specification_filepath = resource_path(absolute_path + "/Resources/json/aerodynamic_specification.json")
stability_specification_filepath = resource_path(absolute_path + "/Resources/json/stability_specification.json")
structure_specification_filepath = absolute_path + "/Resources/json/structure_specification.json"
propulsion_specification_filepath = absolute_path + "/Resources/json/propulsion_specification.json"
performance_specification_filepath = absolute_path + "/Resources/json/performance_specification.json"
datcom_input_file = absolute_path + "/Resources/datcom_files/input.inp"
datcom_output_file = absolute_path + "/Resources/datcom_files/datcom.out"
datcom_temp_dir=absolute_path+"Aerodynamics/datcom"
datcom_exe = absolute_path + "/Resources/programs_exe/datcom.exe"
datcom_stability_specification_filepath = resource_path(
    absolute_path + "/Resources/json/datcom_stability_specification.json")
model_filepath = resource_path(absolute_path + "/Resources/model/model.stl")
sim_export_fixed = resource_path(absolute_path + "/Resources/model/body")
sim_export_moveable = resource_path(absolute_path + "/Resources/model/moveables")
model_dir = resource_path(absolute_path + "/Resources/model")
settings_filepath = absolute_path + "/Resources/json/settings.json"


def read_settings():
    return readFile(settings_filepath)


def update_settings(key="", value=None):
    if value is None:
        value = {}
    data = read_settings()
    try:
        data[key].update(value)
    except:
        data.update({key: value})
    write_settings(data)


def write_settings(values=None):
    if values is None:
        values = {}
    write(settings_filepath, values)




def write_datcom_input(input=""):
    with open(datcom_input_file, "w") as datcom:
        datcom.flush()
        datcom.write(input)

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


def read_work_file():
    return readFile(work_file_path)


def update_work_file(key="", value={}):
    data = read_work_file()
    try:
        data[key].update(value)
    except:
        data.update({key: value})
    write_work_file(data)


def write_work_file(value={}):
    write(work_file_path, value)


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


#########################################################
def read_propulsion_specifications():
    return readFile(propulsion_specification_filepath)


def write_propulsion_specifications(values={}):
    write(propulsion_specification_filepath, values)


def update_propulsion_specifications(key="", value={}):
    data = read_propulsion_specifications()
    try:
        data[key].update(value)
    except:
        data.update({key: value})
    write_propulsion_specifications(data)


########################################################################################
def read_performance_specifications():
    return readFile(propulsion_specification_filepath)


def write_performance_specification(values=None):
    if values is None:
        values = {}
    write(propulsion_specification_filepath, values)


def update_performance_specifications(key="", value=None):
    if value is None:
        value = {}
    data = read_propulsion_specifications()
    try:
        data[key].update(value)
    except:
        data.update({key: value})
    write_propulsion_specifications(data)


#########################################################
def read_aircraft_specifications():
    return readFile(aircraft_specifications_filepath)


def write_aircraft_specification(values={}):
    write(aircraft_specifications_filepath, values)


def update_aircraft_specifications(key="", value={}):
    data = read_aircraft_specifications()
    try:
        data[key].update(value)
    except:
        data.update({key: value})
    write_aircraft_specification(data)


def read_stability_specifications():
    return readFile(stability_specification_filepath)


def write_stability_specification(values={}):
    write(stability_specification_filepath, values)


def update_stability_specifications(key="", value={}):
    data = read_stability_specifications()
    data.update({key: value})
    write_stability_specification(data)


def read_datcom_stability_specifications():
    return readFile(datcom_stability_specification_filepath)


def write_datcom_stability_specification(values={}):
    write(datcom_stability_specification_filepath, values)


def update_datcom_stability_specifications(key="", value={}):
    data = read_datcom_stability_specifications()
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
