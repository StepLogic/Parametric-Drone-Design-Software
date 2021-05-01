from Utils.data_objects.landing_gear_key import*
from Utils.database import database


def read_landing_gear_values():
    values = database.read_aircraft_specifications()
    values = values[landing_gear]
    landing_gear_type_ = values.get(landing_gear_type)
    struct_length_main_gear_ = values.get(struct_length_main_gear)
    tire_diameter_=values.get(tire_diameter)
    wheel_diameter_=values.get(wheel_diameter)
    struct_length_aux_ = values.get(struct_length_aux)
    aux_gear_position_x_ = values.get(aux_gear_position_x)
    aux_gear_position_y_ = values.get(aux_gear_position_y)
    aux_gear_position_z_ = values.get(aux_gear_position_z)
    rol_gear_position_x_ = values.get(rol_gear_position_x)
    rol_gear_position_y_ = values.get(rol_gear_position_y)
    rol_gear_position_z_ = values.get(rol_gear_position_z)
    return landing_gear_type_, struct_length_main_gear_, struct_length_aux_, \
           aux_gear_position_x_, aux_gear_position_y_, aux_gear_position_z_, \
           rol_gear_position_x_, rol_gear_position_y_, rol_gear_position_z_,wheel_diameter_,tire_diameter_,