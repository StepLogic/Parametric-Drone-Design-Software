import numpy as np

from Utils.data_objects.lifting_surface_placeholder import wing, fin
from Utils.data_objects.placeholder import conventional_design, unconventional_design
from Utils.database import database
from Utils.database.aerodynamics.datcom_database import get_parameters_from_conventional_boom, \
    get_parameters_from_conventional_wing, \
    get_parameters_from_sections_lifting_surface
from Utils.database.aerodynamics.settings_database import get_mach_number_range, get_aoa_range, get_altitude
from Utils.database.geometry.boom_database import read_boom_objects, get_boom_object_data
from Utils.database.geometry.lifting_database import read_lifting_surface_objects, get_surface_object_data


def build_datcom_input():
    boom_list = read_boom_objects()
    surface_list = read_lifting_surface_objects()
    ls_statements = []
    boom_statements = []
    for l in surface_list:
        design_type_, surface_type_ = get_surface_object_data(l)
        span_, tip_chord, root_chord, dihedral_, sweep_ = 0, 0, 0, 0, 0
        if design_type_ == unconventional_design:
            span_, tip_chord, root_chord, dihedral_, sweep_ = get_parameters_from_sections_lifting_surface(l)
        elif design_type_ == conventional_design:
            print(l)
            span_, tip_chord, root_chord, dihedral_, sweep_ = get_parameters_from_conventional_wing(l)

        if surface_type_ == wing:
            ls_statements.append(set_planform_parameters(
                type_1="W,G", tip_chord=tip_chord,
                root_chord=root_chord, semi_span=(span_ / 2), sweep_angle=sweep_,
                dihedral_=1.2,
                profile="0012"
            ))
        elif surface_type_ == fin:
            ls_statements.append(set_planform_parameters(
                type_1="V,T", tip_chord=tip_chord,
                root_chord=root_chord, semi_span=(span_ / 2), sweep_angle=sweep_,
                dihedral_=1.3,
                profile="0012"
            ))
        else:
            ls_statements.append(set_planform_parameters(
                type_1="H,T", tip_chord=tip_chord,
                root_chord=root_chord, semi_span=(span_ / 2), sweep_angle=sweep_,
                dihedral_=1.3,
                profile="0012"
            ))
    for l in boom_list:
        design_type_, surface_type_ = get_boom_object_data(l)
        if design_type_ == unconventional_design:
          pass
        elif design_type_ == conventional_design:
            radii, x, z = get_parameters_from_conventional_boom()
            boom_statements.append(set_body_parameters_radius(section_positions=x, radius_of_sections=radii,
                                                              iter_=(boom_list.index(l) + 1)))


    input_ = "".join([set_flight_conditions(mach_numbers=get_mach_number_range(), angle_of_attack=get_aoa_range(),altitude=get_altitude()),
                      set_synths_parameters(),
                      "".join(ls_statements),
                      "".join(boom_statements),
                      create_footer()])
    database.write_datcom_input(input=input_)


def create_footer():
    return "\nCASEID TESTCRAFT" \
           "\nDIM M" \
           "\nDAMP" \
           "\nBUILD" \
           "\nNEXT CASE"


def split_text(type="W,G"):
    val = type.split(",")
    return val[0] + val[1]


def set_flight_conditions(mach_numbers=None, altitude=401, angle_of_attack=None):
    if angle_of_attack is None:
        angle_of_attack = []
    if mach_numbers is None:
        mach_numbers = []
    altitude_condition = f"\n $FLTCON NALT=1.0,ALT(1)={float(altitude)}$"
    mach_condition = f"\n $FLTCON NMACH={float(len(mach_numbers))},MACH(1)={create_listing_datcom(mach_numbers)}$"
    angle_of_attack_condition = f"\n $FLTCON NALPHA={float(len(angle_of_attack))},ALSCHD(1)={create_listing_datcom(angle_of_attack)},LOOP=2.0$"
    flight_conditions_block = altitude_condition + angle_of_attack_condition + mach_condition
    return flight_conditions_block


def set_options():
    pass


def set_synths_parameters(center_of_gravity_z=0, center_of_gravity_x=0, wing_tip_position_x=0, wing_tip_position_z=0,
                          htp_tip_position_x=0, htp_tip_position_z=0, vtp_tip_position_z=0, vtp_tip_position_x=0):
    center_of_gravity_parameter = f"\n $SYNTHS XCG={float(center_of_gravity_x)},ZCG={float(center_of_gravity_z)}$"
    wing_tip_position_parameter = f"\n $SYNTHS XW={float(wing_tip_position_x)},ZW={float(wing_tip_position_z)}$"
    tailplane_tip_position_parameter = f"\n $SYNTHS XH={float(htp_tip_position_x)},ZH={float(htp_tip_position_z)}$"
    fin_tip_position_parameter = f"\n $SYNTHS XV={float(vtp_tip_position_x)},ZV={float(vtp_tip_position_z)}$"
    synth_parameters_block = center_of_gravity_parameter + wing_tip_position_parameter + tailplane_tip_position_parameter + fin_tip_position_parameter
    return synth_parameters_block


def set_body_parameters_area(section_positions=None, iter_=1, area_of_sections=None):
    if section_positions is None:
        section_positions = []
    if area_of_sections is None:
        area_of_sections = []
    number_of_sections_block = f"\n $BODY NX={float(len(section_positions))}$"
    section_positions_block = f"\n $BODY X({iter_})={create_listing_datcom(section_positions)}$"
    area_of_sections_block = f"\n $BODY S({iter_})={create_listing_datcom(area_of_sections)}$"
    body_parameters_block = number_of_sections_block + section_positions_block + area_of_sections_block
    return body_parameters_block


def set_body_parameters_radius(section_positions=None, iter_=1, radius_of_sections=None):
    if section_positions is None:
        section_positions = []
    if radius_of_sections is None:
        radius_of_sections = []
    number_of_sections_block = f"\n $BODY NX={float(len(section_positions))}$"
    section_positions_block = f"\n $BODY X({iter_})={create_listing_datcom(section_positions)}$"
    area_of_sections_block = f"\n $BODY R({iter_})={create_listing_datcom(radius_of_sections)}$"
    body_parameters_block = number_of_sections_block + section_positions_block + area_of_sections_block
    return body_parameters_block


def set_planform_parameters(type_1="W,G", tip_chord=0, semi_span=0, sweep_angle=0, twist_angle=1.1, dihedral_=1.2,
                            root_chord=0, profile="0012"):
    naca_block = set_airfoil_type(type=type_1.split(",")[0], profile=profile)
    type = split_text(type=type_1)
    root_chord_block = f"\n ${type}PLNF CHRDR={root_chord}$"
    tip_chord_block = f"\n ${type}PLNF CHRDTP={tip_chord}$"
    theoritical_semi_span_block = f"\n ${type}PLNF SSPN={semi_span}$"
    exposed_semi_span_block = f"\n ${type}PLNF SSPNE={semi_span}$"
    sweep_angle_block = f"\n ${type}PLNF SAVSI={sweep_angle}$"
    twist_angle_block = f"\n ${type}PLNF TWISTA={twist_angle}$"
    inboard_dihedral_angle_block = f"\n ${type}PLNF DHDADI={dihedral_}$"
    outboard_dihedral_angle_block = f"\n ${type}PLNF DHDADO={dihedral_}$"
    type_block = f"\n ${type}PLNF TYPE = 1.0,CHSTAT=0.25$"
    planform_parameters_block = naca_block + root_chord_block + tip_chord_block + theoritical_semi_span_block + exposed_semi_span_block + sweep_angle_block + twist_angle_block + sweep_angle_block + outboard_dihedral_angle_block + inboard_dihedral_angle_block + type_block
    return planform_parameters_block


def set_elevator(deflections=None, y_position=0, span=0, chord=1):
    if deflections is None:
        deflections = []
    number_angles = f"\n $SYMFLP NDELTA={float(len(deflections))}$"
    type = f"\n $SYMFLP FTYPE=1.0$"
    angles = f"\n $SYMFLP DELTA(1)={create_listing_datcom(deflections)}$"
    chord_outboard = f"\n $SYMFLP CHRDFO={float(chord)}$"
    chord_inboard = f"\n $SYMFLP CHRDFI={float(chord)}$"
    span_inboard = f"\n $SYMFLP SPANFI={float(y_position)}$"
    span_outboard = f"\n $SYMFLP SPANFO={float(y_position + span)}$"
    parameter_block = number_angles + type + angles + chord_outboard + chord_inboard + span_inboard + span_outboard
    return parameter_block


def set_aileron(deflections=None, y_position=0, span=0, chord=1):
    if deflections is None:
        deflections = []
    aileron_number_angles = f"\n $ASYFLP NDELTA={float(len(deflections))}$"
    type = f"\n $ASYFLP STYPE=4.0$"
    aileron_left_angles = f"\n $ASYFLP DELTAL(1)={create_listing_datcom(deflections)}$"
    aileron_right_angles = f"\n $ASYFLP DELTAR(1)={create_listing_datcom(list(-1 * np.array(deflections)))}$"
    chord_outboard = f"\n $ASYFLP CHRDFO={float(chord)}$"
    chord_inboard = f"\n $ASYFLP CHRDFI={float(chord)}$"
    span_inboard = f"\n $ASYFLP SPANFI={float(y_position)}$"
    span_outboard = f"\n $ASYFLP SPANFO={float(y_position + span)}$"
    aileron_parameter_block = aileron_number_angles + type + aileron_left_angles + aileron_right_angles + chord_outboard + chord_inboard + span_inboard + span_outboard
    return aileron_parameter_block


def set_airfoil_type(type="W", profile="0012"):
    naca_block = f"\nNACA-{type}-4-{profile}"
    return naca_block


def create_listing_datcom(list=None):
    break_point = 0
    if list is None:
        list = []
    _list = ""
    for i in list:
        val = float(i)
        if list.index(i) == len(list) - 1:
            _list = _list + f"{val}"
        else:
            if break_point < 4:
                break_point = break_point + 1
                _list = _list + f"{val},"
            else:
                break_point = 0
                _list = _list + f"\n {val},"

    return _list
