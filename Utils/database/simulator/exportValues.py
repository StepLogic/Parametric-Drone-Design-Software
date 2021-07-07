from Utils.data_objects.aerodynamics_placeholders import datcom_data
from Utils.database import database
from Utils.database.aerodynamics.loader import read_datcom_table_data
from Utils.database.database import writeTxt, sim_export_txt_dir


def exportValues():
    output=""
    for major_key in database.read_datcom_stability_specifications().keys():
        for key in database.read_datcom_stability_specifications()[major_key].keys():
            alpha_, velocity_, y=read_datcom_table_data(type_=datcom_data, major_key=major_key, key=key)
            try:
                value=y[alpha_.index(0)]
            except:
                value=0
            output=output+f"{key}:{value},"
    for key,value in database.read_propulsion_specifications()["propulsion_dialogs"].items():
        output = output + f"{key}:{value},"
    for key, value in database.read_structures_specifications().items():
        output = output + f"{key}:{value},"
    writeTxt(sim_export_txt_dir,output)

