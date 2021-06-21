from Utils.data_objects.workflow_placeholders import designs_
from Utils.database import database
from Utils.database.database import saved_designs_dir, aircraft_specifications_filepath


def save_design(value=""):
    data = database.read_saved_designs()
    try:
        array = data[designs_]
        array.append(value)
        data[designs_] = array
    except(Exception):
        data.update({designs_: [value]})
    database.write_saved_designs(data)
    database.write(saved_designs_dir, value)


def open_design(values):
    from shutil import copyfile
    copyfile(saved_designs_dir + values+".json", aircraft_specifications_filepath)


def read_designs():
    data = database.read_saved_designs()
    try:
        return data[designs_]
    except:
        return []
