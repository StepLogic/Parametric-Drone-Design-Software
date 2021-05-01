from math import *

import numpy as np
# Simple_CD(ZeroLift_drag)_Calculator
from scipy.interpolate import interpolate

coefficient_of_lift = 0.4
coefficient_of_induced_drag = 0.3
interference_factor = {"fuselage": 1.0, "wing": 1.40, "h_stabilizer": 1.08, "vertical_stabilizer": 1.03}
avhb_avb = 1.1
cl_alpha_vtail = 2. * pi
k_m_lambda = 1.0
k_f = 0.85
clb_cl_a = 0.000
k_m_gamma = 1.0
cl_beta_htail = 0.
eta_h = 0.95
cn_beta_wing = 0.
k_n = 0.0011
cy_da = 0
bcld_kappa = 0.18
cld_theory = 3.5
cld_ratio = 1.0
cl_d = cld_ratio * cld_theory
k = 0.0064 / 0.0461
dr_max = 0
k_b = 0.95
c_fe = 0.0065
sideslip_angle = 0
phi = 5. * pi / 180.
cy_beta_cor = 1.4068
cl_beta_cor = 0.7396
cn_beta_cor = 2.6690
cl_da_cor = 0.9202
cn_da_cor = 0.9143
cy_dr_cor = 0.6132
cl_dr_cor = 0.3784
cn_dr_cor = 0.7286
currentlimit = 0


def effective_chord(root=0, tip=0):
    return (root + tip) / 2


def planform_area(span=0, chord=0):
    return span * chord


def battery_capacity(battery_pack_capacity, number_of_batteries):
    return battery_pack_capacity * number_of_batteries


def quater_chord_sweep_to_leading_edge(sweep, area, taper_ratio):
    return atan(tan(radians(sweep)) - ((4 / area) * (-(1 / 4) * ((1 - taper_ratio) / (1 + taper_ratio)))))


def compute_derivative(y, x):
    import numpy as np
    dy = np.gradient(y)
    dx = np.gradient(x)
    val = dy / dx
    return val.tolist()


def find_max_cl(col_alpha):
    return max(col_alpha)


def find_alpha_stall(col_alpha, alpha):
    cl_max = max(col_alpha)
    stall_function = interpolate.interp1d(col_alpha, alpha)
    return float(stall_function(cl_max))


def find_velocity_stall(col_u, v_x):
    cl_max = max(col_u)
    stall_function = interpolate.interp1d(col_u, v_x)
    return float(stall_function(cl_max))


def lift_curve_slope(dCol_alpha):
    return max(dCol_alpha)


def find_limits(derivative, list_x):
    for l in derivative:
        if isnan(l) or isinf(l):
            return list_x[derivative.index(l) - 1]
        else:
            pass
    max_value_derivative = max(derivative)
    min_values = []
    for l in derivative:
        if l == 0:
            min_values.append(list_x[derivative.index(l)])
        else:
            pass
    if len(min_values) > 0:
        min_values.append(list_x[derivative.index(min(derivative))])
        min_value_derivative = min(min_values)
        return [list_x[derivative.index(max_value_derivative) - 1], min_value_derivative]
    else:
        min_value_derivative = min(derivative)
        return [list_x[derivative.index(max_value_derivative) - 1], list_x[derivative.index(min_value_derivative) - 1]]


def cell_voltage(energy_density, number_of_batteries):
    return energy_density * number_of_batteries


def battery_weight(battery_pack_capacity, number_of_batteries, voltage, energy_density):
    return (battery_pack_capacity * number_of_batteries * 0.001 * voltage) / energy_density


def total_mass(battery_weight_ex, airframe_weight, payload_weight):
    return battery_weight_ex + airframe_weight + payload_weight


def wing_area(total_mass_ex, wing_loading):
    return (total_mass_ex * (1000 / wing_loading)) / 100


def semi_span_wing(aspect_ratio, wing_area_ex):
    return sqrt((aspect_ratio * wing_area_ex)) / 2


def root_chord_wing(wing_area_ex, semi_span_ex, taper_ratio):
    return (2 * wing_area_ex) / (2 * semi_span_ex * (1 + taper_ratio))


def tip_chord_wing(root_chord_wing_ex, taper_ratio):
    return root_chord_wing_ex * taper_ratio


def average_chord(wing_area_ex, semi_span_ex):
    return wing_area_ex / (2 * semi_span_ex)


def horizontal_stabilizer_area(wing_area_ex, volume_ratio, average_chord_ex, moment_arm):
    return (volume_ratio * average_chord_ex * wing_area_ex) / moment_arm


def semi_span_horizontal_stabilizer(aspect_ratio, horizontal_stabilizer_area_ex):
    return sqrt((aspect_ratio * horizontal_stabilizer_area_ex)) / 2


def root_chord_horizontal_stabilizer(horizontal_stabilizer_area_ex, semi_span_ex, taper_ratio):
    return (2 * horizontal_stabilizer_area_ex) / (2 * semi_span_ex * (1 + taper_ratio))


def tip_chord_horizontal_stabilizer(root_chord_horizontal_stabilizer_ex, taper_ratio):
    return root_chord_horizontal_stabilizer_ex * taper_ratio


def straight_te_sweep(root_chord_horizontal_stabilizer_ex, tip_chord_horizontal_stabilizer_ex, semi_span_ex):
    return atan(
        (root_chord_horizontal_stabilizer_ex - tip_chord_horizontal_stabilizer_ex) * (0.75 / semi_span_ex) * (180 / pi))


def vertical_stabilizer_area(wing_area_ex, volume_ratio, semi_span_ex, moment_arm):
    return wing_area_ex * volume_ratio * semi_span_ex * (2 / moment_arm)


def vertical_stabilizer_root_chord(vertical_stabilizer_area_ex, semi_span_ex, taper_ratio):
    return (2 * vertical_stabilizer_area_ex) / semi_span_ex * (1 + taper_ratio)


def vertical_stabilizer_tip_chord(vertical_stabilizer_root_chord_ex, taper_ratio):
    return vertical_stabilizer_root_chord_ex * taper_ratio


def mass_fraction(payload_weight, battery_weight_ex, total_mass_ex):
    return ((payload_weight + battery_weight_ex) / total_mass_ex) * 100


def min_drag_airspeed(oswald_efficiency, aspect_ratio,
                      zero_liff_drag_, fuselage_drag_coefficient,
                      total_mass_ex, wing_area_ex, air_density):
    return ((1 / (pi * (oswald_efficiency * aspect_ratio * (zero_liff_drag_ + fuselage_drag_coefficient))) ** (
            1 / 4)) * ((((total_mass_ex * 9.80665 * 2) / wing_area_ex) / air_density) ** (1 / 2)))


def min_power_airspeed(oswald_efficiency, aspect_ratio,
                       zero_liff_drag_, fuselage_drag_coefficient,
                       total_mass_ex, wing_area_ex, air_density):
    return ((2 / (12 * pi * (oswald_efficiency * aspect_ratio * (zero_liff_drag_ + fuselage_drag_coefficient))) ** (
            1 / 4)) * ((((total_mass_ex * 9.80665 * 2) / wing_area_ex) / air_density) ** (1 / 2)))


def min_airspeed_stall(max_lift_coefficient,
                       total_mass_ex, wing_area_ex, air_density):
    return (((2 / max_lift_coefficient) ** (1 / 2)) * (((total_mass_ex * 9.80665) / wing_area_ex) / air_density) ** (
            1 / 2))


def lift_coefficent(total_mass_ex, air_density, cruise_speed, wing_area_ex):
    return (total_mass_ex * 9.80665) / (0.5 * air_density * (cruise_speed ** 2) * wing_area_ex)


def drag_coefficient(fuselage_drag_coefficient, oswald_efficiency, aspect_ratio, zero_lift_coefficent,
                     lift_coeffcient_ex):
    return ((fuselage_drag_coefficient + zero_lift_coefficent) + (lift_coeffcient_ex ** 2) / (
            2 * oswald_efficiency * aspect_ratio))


def lift(lift_coefficient_ex, wing_area_ex, cruise_speed, air_density):
    return (lift_coefficient_ex * 0.5 * air_density * (cruise_speed ** 2) * wing_area_ex) / 9.80665


def drag(drag_coefficient_ex, wing_area_ex, cruise_speed, air_density):
    return (drag_coefficient_ex * 0.5 * air_density * (cruise_speed ** 2) * wing_area_ex) / 9.80665


def convert_mps_to_kmph(speed_value):
    return speed_value * (3600 / 1000)


def convert_mps_to_mph(speed_value):
    return speed_value * 2.23694


def lift_to_drag_ratio(lift_coefficient_ex, drag_coefficient_ex):
    return lift_coefficient_ex / drag_coefficient_ex


def stall_margin(cruise_speed, min_airspeed_stall_ex):
    return cruise_speed - min_airspeed_stall_ex


def estimated_flight_time(battery_pack_capacity_ex, battery_number, battery_capacity_used
                          , cruise_current_draw_ex, payload_power, avionics_power, cell_voltage_ex):
    return (((battery_pack_capacity_ex / 1000) * (battery_number * battery_capacity_used * 0.01)) / (
            cruise_current_draw_ex * (payload_power + avionics_power)) / cell_voltage_ex) * 60


def estimated_flight_range(estimated_flight_time_ex, cruise_speed):
    return (estimated_flight_time_ex * 60) * (cruise_speed / 1000)


def cruise_current_draw(total_mass_ex, cruise_speed, lift_to_drag_ratio_ex, overall_efficency, cell_voltage_ex):
    return (((total_mass_ex * 9.80665 * cruise_speed) / lift_to_drag_ratio_ex) / cell_voltage_ex) * (
            100 / overall_efficency)


def convert_seconds_to_hours(time):
    return time / 3600


def calculate_wing_span(wing_a, average_c, tip_chord):
    if tip_chord is 0:
        return int((2 * wing_a) / average_c)
    else:
        return int(wing_a / average_c)


def calculate_other_span(semi_span):
    if semi_span * 2 < 1:
        return 1
    else:
        return int(semi_span * 2)


def getArea(radius=0):
    return pi * radius ** 2


def getpostion(length=0, total_length=0):
    return length / total_length


def get_chord_length_at_x(root_chord=0, tip_chord=0, span=0, length=0):
    return ((root_chord - tip_chord) / span) * length


def getZFromDiherdral(wing_dihedral_angle=0, wing_span=0, root_location=0):
    wing_dihedral_angle = np.deg2rad(wing_dihedral_angle)
    return (tan(wing_dihedral_angle) / 2) * wing_span + root_location


def get_total_width(fuselage_diameter=0, wing_span=0):
    return fuselage_diameter + wing_span


def get_total_length(fuselage_length=0):
    return fuselage_length


def get_total_height(fuselage_diameter=0, vtp_span=0):
    return fuselage_diameter + vtp_span


def getXFromSweep(sweep_angle=0, span=0, root_location=0):
    return tan(sweep_angle) * span + root_location


def calculate_lift(cl=0, v_inf=0, density=0, total_area=0):
    return 0.5 * (v_inf ** 2) * density * total_area * cl


def calculate_drag(cd=0, v_inf=0, density=0, total_area=0):
    return 0.5 * (v_inf ** 2) * density * total_area * cd


def check_if_nan(value):
    if isnan(value):
        value = 0
        return value
    else:
        return value


def calculate_total_axial_force(lift=0, angle_of_incidence=0, thrust=0, drag=0, angle_of_thrust_line=0, mass=0,
                                gravity=0, flight_path_angle=0):
    return lift * sin(angle_of_incidence) + thrust * cos(angle_of_thrust_line) - drag * cos(
        angle_of_incidence) - mass * gravity * sin(angle_of_incidence + flight_path_angle)


def calculate_total_normal_force(lift=0, angle_of_incidence=0, thrust=0, drag=0, angle_of_thrust_line=0, mass=0,
                                 gravity=0, flight_path_angle=0):
    return mass * gravity * cos(angle_of_incidence + flight_path_angle) - lift * cos(angle_of_incidence) - drag * sin(
        angle_of_incidence) - thrust * sin(angle_of_thrust_line)


def calculate_total_side_force(cl=0, wing_dihedral=0, fuselage_diameter=0, z_wing=0, hspan_vtail=0, vs_tail_root=0,
                               taper_ratio_vtail=1,
                               wing_area=0, sweep_vtail_1_2=0, depth_of_vs_in_fuselage=0, vs_area=0, hstab_area=0,
                               mach_number=0):
    vs_tip = vs_tail_root / taper_ratio_vtail
    wing_body_interference = calculate_wing_body_interference(fuselage_diameter=fuselage_diameter,
                                                              ac_z_of_wing_position_ref_to_cg=z_wing)
    avb_av = estimate_avb_av(half_span_vertical_stabilizer=hspan_vtail,
                             depth_of_vertical_stabilizer_in_fuse=depth_of_vs_in_fuselage)
    ar_vtail = estimate_ar_vtail(half_span_vertical_stabilizer=hspan_vtail, vertical_stabilizer_area=vs_area)
    k_h = estimate_k_h(half_span_vertical_stabilizer=hspan_vtail, vs_root_chord=vs_tail_root, vs_tip_chord=vs_tip,
                       horizontal_stabilizer_area=hstab_area)
    ar_vtail_eff = estimate_ar_vtail_eff(avb_av=avb_av, k_h=k_h, ar_vtail=ar_vtail)
    k_cy_beta = estimate_k_cy_beta(half_span_vertical_stabilizer=hspan_vtail,
                                   depth_of_vertical_stabilizer_in_fuse=depth_of_vs_in_fuselage)
    cl_alpha_vtail_eff = estimate_cl_vtail_eff(mach_number=mach_number, half_span_vertical_stabilizer=hspan_vtail,
                                               vs_root_chord=vs_tail_root, vs_tip_chord=vs_tip,
                                               sweep_vertical_stabilier=sweep_vtail_1_2, ar_vtail_eff=ar_vtail_eff)
    cy_beta_wing = calculate_cy_beta_wing(dihedral_wing=wing_dihedral)

    cy_beta_fuselage = estimate_side_force_coefficient_due_to_fuselage(fuselage_diameter=fuselage_diameter
                                                                       , wing_body_interference_factor=int(
            wing_body_interference))
    cy_beta_vtail = estimate_vertical_stabilizer_contribution_to_sideforce(half_span_vertical_stabilizer=hspan_vtail,
                                                                           vs_root_chord=vs_tail_root
                                                                           , vs_tip_chord=vs_tip, wing_area=wing_area,
                                                                           sweep_vertical_stabilizer=sweep_vtail_1_2,
                                                                           fuselage_diameter=fuselage_diameter
                                                                           , ac_z_of_wing_position_ref_to_cg=z_wing,
                                                                           ar_vtail_eff=ar_vtail_eff,
                                                                           cl_alpha_vtail_eff=cl_alpha_vtail_eff,
                                                                           k_cy_beta_v=k_cy_beta

                                                                           )
    cy_beta = cy_beta_cor * estimate_total_sideforce(cy_beta_wing=cy_beta_wing, cy_beta_fuse=cy_beta_fuselage,
                                                     cy_beta_vtail=cy_beta_vtail)

    return cy_beta


def calculate_total_rolling_moment(cy_beta_vtail=0, z_vtail=0, l_vtail=0, cl=0, hspan_wing=0, fuselage_diameter=0,
                                   mach_number=0, wing_area=0, sweep_wing_1_2=0, hspan_htail=0
                                   , htail_area=0, sweep_htail_1_2=0, wing_dihedral=0, z_wing=0):
    k_wb = estimate_k_wb(fuselage_diameter=fuselage_diameter, wing_half_span=hspan_wing)
    beta_m = estimiate_beta_m(mach_number=mach_number)
    cl_alpha_2d = estimate_cl_aplha_2d(beta_m)
    kappa = estimate_kappa_for_cl_aplha_d(cl_alpha_2d=cl_alpha_2d, beta_m=beta_m)
    aspect_ratio_wing = estimate_aspect_ratio_wing(hspan_wing=hspan_wing, wing_area=wing_area)
    cl_apha_w = estimate_lift_curve_slope_wing_alone_cl_alpha_w(aspect_ratio=aspect_ratio_wing, beta_m=beta_m,
                                                                kappa=kappa, sweep_wing=sweep_wing_1_2)
    cl_apha_wb = estimate_lift_curve_slope_wingbody(lift_curve_slope_loss=k_wb, cl_apha_w=cl_apha_w)
    aspect_ratio_horizontal = aspect_ratio_of_horizontal_stablizer(half_span_htail=hspan_htail,
                                                                   area_horizontal_stabilizer=htail_area)
    cl_alpha_h = lift_curve_slope_horizontal(aspect_ratio_htail=aspect_ratio_horizontal,
                                             sweep_htail_1_2=sweep_htail_1_2, beta_m=beta_m, kappa=kappa)
    cl_alpha = total_lift_curve_slope(cl_alpha_wb=cl_apha_wb, cl_alpha_h=cl_alpha_h,
                                      area_horizontal_stabilizer=htail_area, wing_area=wing_area)
    alpha = calculate_angle_of_attack(cl=cl, cl_alpha=cl_alpha, wing_angle_of_incidence=0)
    cl_beta_vtail = estimate_vtail_cl_beta(cy_beta_vtail=cy_beta_vtail, z_vtail=z_vtail, alpha=alpha, l_vtail=l_vtail,
                                           hspan_wing=hspan_wing)
    wing_sweep_contribution_to_cl = estimate_wing_body_contribution_to_cl(sweep_wing_1_2=sweep_wing_1_2)
    d = estimate_d(fuselage_diameter=fuselage_diameter)
    dclb_gamma = estimate_dclb_gamma(hspan_wing=hspan_wing, aspect_ratio=aspect_ratio_wing, d=d)
    dclb_gamma_zw = estimate_dclb_gamma_zw(hspan_wing=hspan_wing, aspect_ratio=aspect_ratio_wing, d=d, z_wing=z_wing)
    clb_gamma = estimate_clb_gamma(hspan_wing=hspan_wing, wing_area=wing_area)
    cl_beta_wb = cl_beta_cor * estimate_cl_beta_wing_body(cl=cl, wing_sweep_contribution=wing_sweep_contribution_to_cl
                                                          , dihedral_wing=wing_dihedral, dclb_gamma=dclb_gamma,
                                                          clb_gamma=clb_gamma, dclb_zw=dclb_gamma_zw)

    cl_beta = variation_of_cl_beta(cl_beta_htail + cl_beta_vtail + cl_beta_wb)


def calculate_total_yawing_moment(speed_of_sound=0, viscosity=0, density=0, fuselage_length=0, mach_number=0,
                                  fuselage_diameter=0, hspan_wing=0, z_vtail=0, alpha=0, l_vtail=0
                                  , wing_area=0, cy_beta_vtail=0):
    re_fuse = estimate_reynolds_number_for_fuselage(mu_eo=viscosity, density=density, mach_eo=mach_number
                                                    , a_eo=speed_of_sound, fuselage_length=fuselage_length)
    k_r_l = estimate_fuselage_reynolds_number_effect_on_wing_body(re_fuse=re_fuse)
    sbs = estimate_body_side_area(fuselage_diameter=fuselage_diameter, fuselage_length=fuselage_length)
    cn_beta_fuse = estimate_fuselage_contribution_to_cn_beta(k_r_l=k_r_l, sbs=sbs, wing_area=wing_area,
                                                             fuselage_length=fuselage_length, wing_half_span=hspan_wing)
    cn_beta_vtail = vs_contribution_to_cn_beta(cy_beta_vtail=cy_beta_vtail, l_vtail=l_vtail, alpha=alpha,
                                               hspan_wing=hspan_wing, z_vtail=z_vtail)
    cn_beta = cn_beta_cor * total_cn_beta(cn_beta_fuse=cn_beta_fuse, cn_beta_vtail=cn_beta_vtail)


def estimate_clb_gamma(hspan_wing=0, wing_area=0):
    ar = (2. * hspan_wing) ** 2 / wing_area
    return -0.00012 - 0.00013 / 10 * ar


def calculate_beta(v_infinity=0, v=0):
    beta = atan(v / v_infinity)
    return beta


def calculate_cd_zero_lift():
    print("zero-lift_total",
          (c_fe * (calculate_wing_wetted_area() + calculate_fuselage_wetted_area()) / 0.09).__abs__())
    return (c_fe * (calculate_wing_wetted_area() + calculate_fuselage_wetted_area()) / 0.09).__abs__()


def calculate_velocity_from_acceleration(initial_velocity=0, acceleration=0, time_rate=0):
    return initial_velocity + acceleration * time_rate


def translate_v_infinity_into_u_v_w(v_infinity=0, side_slip_angle=0, angle_of_incidence=0):
    u = v_infinity * cos(angle_of_incidence) * cos(side_slip_angle)
    v = v_infinity * sin(side_slip_angle)
    w = v_infinity * sin(angle_of_incidence) * cos(side_slip_angle)
    return u, v, w


def calculate_acceleration_from_thrust(thrust=0.05, drag=0, mass=4, pitching_angle=0):
    return (thrust - (mass * 9.81 * sin(pitching_angle) + drag)) / mass


def calculate_res_force_from_thrust(thrust=0.05, drag=0, mass=4, pitching_angle=0):
    return (thrust - (mass * 9.81 * sin(pitching_angle) + drag))


def calculate_wing_wetted_area(airfoil_thickness_at_tip=0.05, airfoil_thickness_at_root=0.05, taper_ratio=1,
                               wing_area=1):
    airfoil_thickness_ratio = airfoil_thickness_at_tip / airfoil_thickness_at_root
    wing_wet_area = wing_area * 2 * (1 + (0.25 * airfoil_thickness_at_root) * (
            (1 + airfoil_thickness_ratio * taper_ratio) / 1 + taper_ratio))
    return wing_wet_area


def calculate_fuselage_wetted_area(fuselage_diameter=0.01, fuselage_length=0.2,
                                   fuselage_nose_length=0.002,
                                   fuselage_type="cylindrical"):
    fuselage_fineness_ratio = fuselage_diameter / fuselage_length
    fuselage_wet_area = 0
    Re = 38.21 * (fuselage_diameter / 0.00635) ** (1.053)
    c_f_laminar = 1.328 * (Re ** (1 / 2))
    if fuselage_type.startswith("c"):
        fuselage_wet_area = pi * fuselage_diameter * fuselage_length * (
                (1 - (2 / fuselage_fineness_ratio)) ** (2 / 3)) * (1 + 1 / fuselage_fineness_ratio ** 2)
    else:
        fuselage_wet_area = pi * fuselage_diameter * fuselage_length * (
                (0.5 + 0.135 * (fuselage_nose_length / fuselage_fineness_ratio)) ** (2 / 3)) * (
                                    1.015 + 0.3 / fuselage_fineness_ratio ** 1.5)
    return fuselage_wet_area


def calculate_cd_zero_lift_fuselage(wing_area=0.09, fuselage_diameter=0.01, fuselage_length=0.2,
                                    fuselage_nose_length=0.002,
                                    fuselage_type="cylindrical"):
    fuselage_fineness_ratio = fuselage_diameter / fuselage_length
    fuselage_wet_area = 0
    Re = 38.21 * (fuselage_diameter / 0.00635) ** (1.053)
    c_f_laminar = 1.328 * (Re ** (1 / 2))
    if fuselage_type.startswith("c"):
        fuselage_wet_area = pi * fuselage_diameter * fuselage_length * (
                (1 - (2 / fuselage_fineness_ratio)) ** (2 / 3)) * (1 + 1 / fuselage_fineness_ratio ** 2)
    else:
        fuselage_wet_area = pi * fuselage_diameter * fuselage_length * (
                (0.5 + 0.135 * (fuselage_nose_length / fuselage_fineness_ratio)) ** (2 / 3)) * (
                                    1.015 + 0.3 / fuselage_fineness_ratio ** 1.5)
    form_factor_fuselage = (
            1 + ((60 / (fuselage_length / fuselage_diameter)) ** 3) + ((fuselage_length / fuselage_diameter) / 400))
    CD_zero_lift = c_f_laminar * form_factor_fuselage * interference_factor["fuselage"] * (
            fuselage_wet_area / wing_area)

    return fuselage_wet_area


def calculate_cd_zero_lift_wing_or_h_or_v_stab(mach_number=0.003, sweep_angle=0.07, airfoil_thickness_at_root=0.005,
                                               airfoil_thickness_at_tip=0.0007, airfoil_maximum_thickness=0.0003,
                                               taper_ratio=2, wing_span=0.04, wing_area=0.09,
                                               postion_of_maximum_thickness=0.3, ):
    airfoil_thickness_ratio = airfoil_thickness_at_tip / airfoil_thickness_at_root
    wing_wet_area = wing_area * 2 * (1 + (0.25 * airfoil_thickness_at_root) * (
            (1 + airfoil_thickness_ratio * taper_ratio) / 1 + taper_ratio))
    Re = 38.21 * (airfoil_maximum_thickness / 0.00635) ** 1.053
    c_f_laminar = 1.328 * (Re ** (1 / 2))
    form_factor_wing = (1 + (
            0.6 / postion_of_maximum_thickness * airfoil_maximum_thickness) + 100 * airfoil_maximum_thickness) * (
                               134 * mach_number ** 0.18 * cos(sweep_angle) ** 0.18)
    CD_zero_lift = c_f_laminar * form_factor_wing * interference_factor["wing"] * (wing_wet_area / wing_area)
    print(CD_zero_lift.__abs__())
    return wing_wet_area


def calculate_initial_ground_speed(thrust=5, mass=10, time_frame=1):
    return thrust / mass * time_frame


def calculate_ground_speed(thrust=5, mass=10, time_frame=1, drag=0):
    return ((thrust - drag) / mass) * time_frame


def calculate_final_velocity(intial_velocity=0, acceleration=0, time=0):
    return intial_velocity + acceleration * time


def calculate_cy_beta_wing(dihedral_wing=0):
    return -0.0001 * abs(dihedral_wing) * 180. / pi


def calculate_wing_body_interference(fuselage_diameter=0, ac_z_of_wing_position_ref_to_cg=0):
    wing_body_interference_factor = 0
    if ac_z_of_wing_position_ref_to_cg / (fuselage_diameter / 2) < 0:
        wing_body_interference_factor = 0.85 * (-ac_z_of_wing_position_ref_to_cg / (fuselage_diameter / 2)) + 1
    elif ac_z_of_wing_position_ref_to_cg / (fuselage_diameter / 2) > 0:
        wing_body_interference_factor = 0.5 * ac_z_of_wing_position_ref_to_cg / (fuselage_diameter / 2) + 1.
    return wing_body_interference_factor


def estimate_side_force_coefficient_due_to_fuselage(wing_body_interference_factor=0, fuselage_diameter=0):
    return -2 * wing_body_interference_factor * (pi * (fuselage_diameter / 2.) ** 2)


def estimate_k_cy_beta(half_span_vertical_stabilizer=0, depth_of_vertical_stabilizer_in_fuse=0):
    x = half_span_vertical_stabilizer / depth_of_vertical_stabilizer_in_fuse
    empirical_factor = 0
    if x < 2:
        empirical_factor = 0.75
    elif x > 2 and x < 3.5:
        empirical_factor = x / 6. + 5. / 12.
    elif x < 3.5:
        empirical_factor = 1
    return empirical_factor


def estimate_avb_av(half_span_vertical_stabilizer=0, depth_of_vertical_stabilizer_in_fuse=0):
    x = half_span_vertical_stabilizer / depth_of_vertical_stabilizer_in_fuse
    return 0.002 * x ** 5 - 0.0464 * x ** 4 + 0.404 * x ** 3 - 1.6217 * x ** 2 + 2.7519 * x + 0.0408


def estimate_k_h(half_span_vertical_stabilizer=0, vs_root_chord=0, vs_tip_chord=0, horizontal_stabilizer_area=0):
    sv = half_span_vertical_stabilizer * (vs_root_chord + vs_tip_chord) / 2.
    x = horizontal_stabilizer_area / sv
    return -0.0328 * x ** 4 + 0.2885 * x ** 3 - 0.9888 * x ** 2 + 1.6554 * x & 0.0067


def estimate_ar_vtail(half_span_vertical_stabilizer=0, vertical_stabilizer_area=0):
    ar_vtail = half_span_vertical_stabilizer ** 2 / vertical_stabilizer_area
    return ar_vtail


def estimate_ar_vtail_eff(avb_av=0, k_h=0, ar_vtail=0):
    return avb_av * ar_vtail * (1. + k_h * (avhb_avb - 1.))


def estimate_cl_vtail_eff(mach_number=0,
                          half_span_vertical_stabilizer=0
                          , vs_root_chord=0, vs_tip_chord=0, sweep_vertical_stabilier=0,
                          ar_vtail_eff=0):
    kappa = cl_alpha_vtail / (2 * pi)
    beta_m = sqrt(1 - mach_number ** 2)
    sweep_vtail_1_2 = atan(((vs_root_chord / 4) + half_span_vertical_stabilizer * tan(sweep_vertical_stabilier) + (
            vs_tip_chord / 4) - vs_tip_chord / 2.) / half_span_vertical_stabilizer)
    return (2. * pi * ar_vtail_eff / (2. + sqrt(
        ar_vtail_eff ** 2 * beta_m ** 2 / kappa ** 2 * (1. + tan(sweep_vtail_1_2) ** 2 / beta_m ** 2) + 4.)))


def estimate_vertical_stabilizer_contribution_to_sideforce(half_span_vertical_stabilizer=0
                                                           , vs_root_chord=0, vs_tip_chord=0, wing_area=0,
                                                           sweep_vertical_stabilizer=0, fuselage_diameter=0,
                                                           ac_z_of_wing_position_ref_to_cg=0, ar_vtail_eff=0,
                                                           cl_alpha_vtail_eff=0, k_cy_beta_v=0):
    sv = half_span_vertical_stabilizer * (vs_root_chord + vs_tip_chord) / 2.
    eff_vtail = 0.724 + 3.06 * sv / wing_area / (1 + cos(
        sweep_vertical_stabilizer)) + 0.4 * ac_z_of_wing_position_ref_to_cg / fuselage_diameter + 0.009 * ar_vtail_eff
    return -k_cy_beta_v * cl_alpha_vtail_eff * eff_vtail * sv / wing_area


def estimate_total_sideforce(cy_beta_wing=0, cy_beta_fuse=0, cy_beta_vtail=0):
    return cy_beta_wing + cy_beta_fuse + cy_beta_vtail


def estimate_wing_body_contribution_to_cl(sweep_wing_1_2=0):
    return -0.004 / 45 * sweep_wing_1_2 * 180. / pi


def estimate_aspect_ratio_wing(hspan_wing=0, wing_area=0):
    return (2. * hspan_wing) ** 2 / wing_area


def estimate_dihedral_effect_on_sideforce(aspect_ratio):
    return -0.00012 - 0.00013 / 10 * aspect_ratio


def estimate_d(fuselage_diameter=0):
    return sqrt(pi * (fuselage_diameter / 2.) ** 2 / 0.7854)


def estimate_dclb_gamma(hspan_wing=0, aspect_ratio=0, d=0):
    return -0.0005 * sqrt(aspect_ratio) * (d / (2. * hspan_wing)) ** 2


def estimate_dclb_gamma_zw(hspan_wing=0, aspect_ratio=0, d=0, z_wing=0):
    return -1.2 * sqrt(aspect_ratio) / (180. / pi) * z_wing / (2. * hspan_wing) * 2. * d / (2. * hspan_wing)


def estimate_cl_beta_wing_body(cl=0, wing_sweep_contribution=0, dihedral_wing=0, dclb_gamma=0, clb_gamma=0, dclb_zw=0):
    return (cl * (wing_sweep_contribution * k_m_lambda * k_f + clb_cl_a) + dihedral_wing * (
            clb_gamma * k_m_gamma + dclb_gamma) + dclb_zw) * 180. / pi


def estimate_k_wb(fuselage_diameter=0, wing_half_span=0):
    x = fuselage_diameter / (2. * wing_half_span)
    return 1 - 0.25 * x ** 2 + 0.025 * x


def estimiate_beta_m(mach_number=0):
    return (1 - mach_number) ** 2


def estimate_cl_aplha_2d(beta_m=0):
    return 2 * pi / beta_m


def estimate_kappa_for_cl_aplha_d(cl_alpha_2d=0, beta_m=0):
    return cl_alpha_2d / (2. * pi / beta_m)


def estimate_lift_curve_slope_wing_alone_cl_alpha_w(aspect_ratio=0, beta_m=0, kappa=0, sweep_wing=0):
    return 2. * pi * aspect_ratio / (
            2. + sqrt(aspect_ratio ** 2 * beta_m ** 2 / kappa ** 2 * (1. + tan(sweep_wing) ** 2 / beta_m ** 2) + 4.))


def estimate_lift_curve_slope_wingbody(lift_curve_slope_loss=0, cl_alpha_w=0):
    return lift_curve_slope_loss * cl_alpha_w


def aspect_ratio_of_horizontal_stablizer(half_span_htail=0, area_horizontal_stabilizer=0):
    return (2. * half_span_htail) ** 2 / area_horizontal_stabilizer


def lift_curve_slope_horizontal(aspect_ratio_htail=0, sweep_htail_1_2=0, beta_m=0, kappa=0):
    return 2. * pi * aspect_ratio_htail / (2. + sqrt(
        aspect_ratio_htail ** 2 * beta_m ** 2 / kappa ** 2 * (1. + tan(sweep_htail_1_2) ** 2 / beta_m ** 2) + 4.))


def total_lift_curve_slope(cl_alpha_wb=0, cl_alpha_h=0, area_horizontal_stabilizer=0, wing_area=0):
    return cl_alpha_wb + cl_alpha_h * eta_h * area_horizontal_stabilizer / wing_area


def calculate_angle_of_attack(cl=0, cl_alpha=0, wing_angle_of_incidence=0):
    return cl / cl_alpha - 5. * pi / 180.


def estimate_vtail_cl_beta(cy_beta_vtail=None, z_vtail=None, alpha=0, l_vtail=None, hspan_wing=None):
    return cy_beta_vtail * (z_vtail * cos(alpha) - l_vtail * sin(alpha)) / (2. * hspan_wing)


def variation_of_cl_beta(cl_beta_wingbody=None, cl_beta_htail_r=None, cl_beta_vtail=None):
    return cl_beta_wingbody + cl_beta_htail_r + cl_beta_vtail


def estimate_reynolds_number_for_fuselage(mu_eo=None, density=None, mach_eo=None, a_eo=None, fuselage_length=None):
    return density * mach_eo * a_eo * fuselage_length / mu_eo


def estimate_fuselage_reynolds_number_effect_on_wing_body(re_fuse=0):
    return 1. + 1.2 / log(350.) * log(re_fuse / 1000000.)


def estimate_body_side_area(fuselage_diameter=0, fuselage_length=0):
    return 0.83 * fuselage_length * fuselage_diameter


def estimate_fuselage_contribution_to_cn_beta(k_r_l=None, sbs=None, wing_area=None, fuselage_length=0,
                                              wing_half_span=0):
    return -180. / pi * k_n * k_r_l * sbs / wing_area * fuselage_length / (2. * wing_half_span)


def vs_contribution_to_cn_beta(cy_beta_vtail=None, l_vtail=None, alpha=None, hspan_wing=None, z_vtail=None):
    return -cy_beta_vtail * (l_vtail * cos(alpha) + z_vtail * sin(alpha)) / (2. * hspan_wing)


def total_cn_beta(cn_beta_fuse=0, cn_beta_vtail=0):
    return cn_beta_wing + cn_beta_fuse + cn_beta_vtail


def estimate_rolling_effectiveness(kappa=0, beta_m=0):
    return kappa / beta_m * bcld_kappa


def estimate_elevator_effectiveness(cl_alpha_2d=None):
    return cl_d / cl_alpha_2d


def determine_change_in_cl_with_change_aileron_deflection(cld_prime=None, alpha_d=0):
    return alpha_d * cld_prime


def real_determine_change_in_cl_with_change_aileron_deflection():
    return cl_d / 2.


def change_in_yawing_moment_with_change_aileron(cl_da=None):
    return k * cl_da


def flap_effectiveness(ar_vtail_eff=None):
    cf_c = 0.33
    alpha_d_cl = -sqrt(1. - (1. - cf_c) ** 2)
    if (alpha_d_cl >= - 0.5):
        flap_eff_ratio = 1.42 + 1.8 * alpha_d_cl
    elif (alpha_d_cl >= - 0.6):
        flap_eff_ratio = 1.32 + 1.6 * alpha_d_cl
    elif (alpha_d_cl > - 0.7):
        flap_eff_ratio = 1.08 + 1.2 * alpha_d_cl
    else:
        flap_eff_ratio = 0.94 + alpha_d_cl
    flap_eff_ratio = 1. + flap_eff_ratio / (ar_vtail_eff & 0.5 * (-alpha_d_cl - 2.1))

    return flap_eff_ratio * alpha_d_cl


def estimate_k_prime():
    x = dr_max
    if (x < 15):
        k_prime = 1.
    else:
        k_prime = 4e-7 * x ** 4 - 7e-5 * x ** 3 + 0.0047 * x ** 2 - 0.1453 * x + 2.3167
    return k_prime


def estimate_change_in_sideforce_with_rudder_deflection(k_prime=None, vtail_area=0, wing_area=None, cf_factor=None,
                                                        cl_alpha_vtail_eff=None):
    return cl_alpha_vtail_eff * cf_factor * k_prime * k_b * vtail_area / wing_area


def change_in_rolling_moment_coefficient_with_rudder_deflection(cy_dr=None, z_vtail=None, l_vtail=None, hspan_wing=0,
                                                                alpha=0):
    return cy_dr * (z_vtail * cos(alpha) - l_vtail * sin(alpha)) / (2. * hspan_wing)


def change_in_yawing_moment_coefficient_with_rudder(l_vtail=0, z_vtail=None, hspan_wing=None, alpha=0, cy_dr=None):
    return -cy_dr * (l_vtail * cos(alpha) + z_vtail * sin(alpha)) / (2. * hspan_wing)
