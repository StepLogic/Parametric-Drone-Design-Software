from scipy.interpolate import interpolate

from analysis.aerodynamic_analysis.AerodyamicAnalyzer import run_analysis
from utils import MathLibrary, Database
from utils.Database import read_aircraft_specifications, write_aerodynamic_results, write_control_specifications
from utils.MathLibrary import check_if_nan, find_max_cl, find_alpha_stall, find_velocity_stall, compute_derivative, \
    find_limits

list_of_parameters = ["wing_sweep"]
list_of_aerdynamic_parameters = ["coefficient_of_lift", "coefficient_of_drag", "coefficient_of_sideforce"
    , "coefficient_of_rolling_moment"
    , "coefficient_of_pitching_moment"
    , "coefficient_of_yawing_moment"]

angle_of_attack = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30,
                   "-20": -20, "-10": 10}
slip_angles = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30, "-20": -20,
               "-10": 10}
velocity = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0}
elevator_deflection = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30,
                       "-20": -20, "-10": 10}
rudder_deflection = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30,
                     "-20": -20, "-10": 10}
aileron_deflection = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30,
                      "-20": -20, "-10": 10}
p = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30, "-20": -20,
     "-10": 10}
q = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30, "-20": -20,
     "-10": 10}
r = {"45": 45, "35": 35, "30": 30, "20": 20, "10": 10, "0": 0, "-45": -45, "-35": -35, "-30": -30, "-20": -20,
     "-10": 10}


def run_sandbox_simulation():
    cn_beta = []
    cl_beta = []
    cm_beta = []

    cn_alpha = []
    cl_alpha = []
    cm_alpha = []

    cn_u = []
    cl_u = []
    cm_u = []

    cn_p = []
    cl_p = []
    cm_p = []

    cn_q = []
    cl_q = []
    cm_q = []

    cn_r = []
    cl_r = []
    cm_r = []

    cn_aileron = []
    cl_aileron = []
    cm_aileron = []

    cn_elevator = []
    cl_elevator = []
    cm_elevator = []

    cn_rudder = []
    cl_rudder = []
    cm_rudder = []

    col_beta = []
    cd_beta = []
    cy_beta = []

    col_alpha = []
    cd_alpha = []
    cy_alpha = []

    col_u = []
    cd_u = []
    cy_u = []

    col_p = []
    cd_p = []
    cy_p = []

    col_q = []
    cd_q = []
    cy_q = []

    col_r = []
    cd_r = []
    cy_r = []

    col_aileron = []
    cd_aileron = []
    cy_aileron = []

    col_elevator = []
    cd_elevator = []
    cy_elevator = []

    col_rudder = []
    cd_rudder = []
    cy_rudder = []

    v_x = []
    r_x = []
    specs = []
    value = read_aircraft_specifications()

    aircraft_wetted_area = MathLibrary.calculate_fuselage_wetted_area(fuselage_length=value["fuselage_length"]
                                                                      , fuselage_diameter=value["fuselage_diameter"]
                                                                      , fuselage_nose_length=value[
            "nose_radius"]) + MathLibrary.calculate_wing_wetted_area(
        airfoil_thickness_at_tip=0.25 * value["wing_chord"] / value["wing_taper_ratio"]
        , airfoil_thickness_at_root=value["wing_chord"] * 0.25,
        taper_ratio=value["wing_taper_ratio"],
        wing_area=((value["wing_chord"] / value["wing_taper_ratio"] + value["wing_chord"]) / 2) * value["wing_span"])

    current_angle = -45
    while current_angle < 46:
        r_x.append(current_angle)

        alpha_result = run_analysis(read_aircraft_specifications(), alpha=current_angle, beta=0, velocity=1,
                                    fast_track=True, p=0, q=0, r=0)
        beta_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=current_angle, velocity=1,
                                   fast_track=True, p=0, q=0, r=0)
        p_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=1, fast_track=True,
                                p=current_angle,
                                q=0, r=0)
        q_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=1, fast_track=True, p=0,
                                q=current_angle, r=0)
        r_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=1, fast_track=True, p=0,
                                q=0, r=current_angle)
        aileron_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=1, fast_track=True, p=0,
                                      q=0, r=0, aileron_deflection=current_angle)
        elevator_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=1, fast_track=True,
                                       p=0,
                                       q=0, r=0, elevator_deflection=current_angle)
        rudder_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=1, fast_track=True, p=0,
                                     q=0, r=0, rudder_deflection=current_angle)

        if current_angle > 0:
            v_x.append(current_angle)
            velocity_result = run_analysis(read_aircraft_specifications(), alpha=0, beta=0, velocity=current_angle,
                                           fast_track=True, p=0, q=0, r=0)

            cn_u.append(check_if_nan(velocity_result.get("Cn")))
            cm_u.append(check_if_nan(velocity_result.get("Cm")))
            cl_u.append(check_if_nan(velocity_result.get("Cl")))
            cy_u.append(check_if_nan(velocity_result.get("CY")))
            col_u.append(check_if_nan(velocity_result.get("CL")))
            cd_u.append(check_if_nan(velocity_result.get("CD")))

        cn_alpha.append(check_if_nan(alpha_result.get("Cn")))
        cm_alpha.append(check_if_nan(alpha_result.get("Cm")))
        cl_alpha.append(check_if_nan(alpha_result.get("Cl")))

        cn_beta.append(check_if_nan(beta_result.get("Cn")))
        cm_beta.append(check_if_nan(beta_result.get("Cm")))
        cl_beta.append(check_if_nan(beta_result.get("Cl")))

        cn_p.append(check_if_nan(p_result.get("Cn")))
        cm_p.append(check_if_nan(p_result.get("Cm")))
        cl_p.append(check_if_nan(p_result.get("Cl")))

        cn_q.append(check_if_nan(q_result.get("Cn")))
        cm_q.append(check_if_nan(q_result.get("Cm")))
        cl_q.append(check_if_nan(q_result.get("Cl")))

        cn_r.append(check_if_nan(r_result.get("Cn")))
        cm_r.append(check_if_nan(r_result.get("Cm")))
        cl_r.append(check_if_nan(r_result.get("Cl")))

        cn_aileron.append(check_if_nan(aileron_result.get("Cn")))
        cm_aileron.append(check_if_nan(aileron_result.get("Cm")))
        cl_aileron.append(check_if_nan(aileron_result.get("Cl")))

        cn_elevator.append(check_if_nan(elevator_result.get("Cn")))
        cm_elevator.append(check_if_nan(elevator_result.get("Cm")))
        cl_elevator.append(check_if_nan(elevator_result.get("Cl")))

        cn_rudder.append(check_if_nan(rudder_result.get("Cn")))
        cm_rudder.append(check_if_nan(rudder_result.get("Cm")))
        cl_rudder.append(check_if_nan(rudder_result.get("Cl")))

        col_alpha.append(check_if_nan(alpha_result.get("CL")))
        cd_alpha.append(check_if_nan(alpha_result.get("CD")))
        cy_alpha.append(check_if_nan(alpha_result.get("CY")))

        col_beta.append(check_if_nan(beta_result.get("CL")))
        cd_beta.append(check_if_nan(beta_result.get("CD")))
        cy_beta.append(check_if_nan(beta_result.get("CY")))

        col_p.append(check_if_nan(p_result.get("CL")))
        cd_p.append(check_if_nan(p_result.get("CD")))
        cy_p.append(check_if_nan(p_result.get("CY")))

        col_q.append(check_if_nan(q_result.get("CL")))
        cd_q.append(check_if_nan(q_result.get("CD")))
        cy_q.append(check_if_nan(q_result.get("CY")))

        col_r.append(check_if_nan(r_result.get("CL")))
        cd_r.append(check_if_nan(r_result.get("CD")))
        cy_r.append(check_if_nan(r_result.get("CY")))

        col_aileron.append(check_if_nan(aileron_result.get("CL")))
        cd_aileron.append(check_if_nan(aileron_result.get("CD")))
        cy_aileron.append(check_if_nan(aileron_result.get("CY")))

        col_elevator.append(check_if_nan(elevator_result.get("CL")))
        cd_elevator.append(check_if_nan(elevator_result.get("CD")))
        cy_elevator.append(check_if_nan(elevator_result.get("CY")))

        col_rudder.append(check_if_nan(rudder_result.get("CL")))
        cd_rudder.append(check_if_nan(rudder_result.get("CD")))
        cy_rudder.append(check_if_nan(rudder_result.get("CY")))

        current_angle += 5

    dCol_p = compute_derivative(col_p, r_x)
    dCol_q = compute_derivative(col_q, r_x)
    dCol_r = compute_derivative(col_r, r_x)
    dCol_alpha = compute_derivative(col_alpha, r_x)
    dCol_beta = compute_derivative(col_beta, r_x)
    dCol_aileron = compute_derivative(col_aileron, r_x)
    dCol_elevator = compute_derivative(col_elevator, r_x)
    dCol_rudder = compute_derivative(col_rudder, r_x)
    dCol_u = compute_derivative(col_u, v_x)

    dCd_p = compute_derivative(cd_p, r_x)
    dCd_q = compute_derivative(cd_q, r_x)
    dCd_r = compute_derivative(cd_r, r_x)
    dCd_alpha = compute_derivative(cd_alpha, r_x)
    dCd_beta = compute_derivative(cd_beta, r_x)
    dCd_aileron = compute_derivative(cd_aileron, r_x)
    dCd_elevator = compute_derivative(cd_elevator, r_x)
    dCd_rudder = compute_derivative(cd_rudder, r_x)
    dCd_u = compute_derivative(cd_u, v_x)

    dCl_p = compute_derivative(cl_p, r_x)
    dCl_q = compute_derivative(cl_q, r_x)
    dCl_r = compute_derivative(cl_r, r_x)
    dCl_alpha = compute_derivative(cl_alpha, r_x)
    dCl_beta = compute_derivative(cl_beta, r_x)
    dCl_aileron = compute_derivative(cl_aileron, r_x)
    dCl_elevator = compute_derivative(cl_elevator, r_x)
    dCl_rudder = compute_derivative(cl_rudder, r_x)
    dCl_u = compute_derivative(cl_u, v_x)

    dCm_p = compute_derivative(cm_p, r_x)
    dCm_q = compute_derivative(cm_q, r_x)
    dCm_r = compute_derivative(cm_r, r_x)
    dCm_alpha = compute_derivative(cm_alpha, r_x)
    dCm_beta = compute_derivative(cm_beta, r_x)
    dCm_aileron = compute_derivative(cm_aileron, r_x)
    dCm_elevator = compute_derivative(cm_elevator, r_x)
    dCm_rudder = compute_derivative(cm_rudder, r_x)
    dCm_u = compute_derivative(cm_u, v_x)

    dCn_p = compute_derivative(cn_p, r_x)
    dCn_q = compute_derivative(cn_q, r_x)
    dCn_r = compute_derivative(cn_r, r_x)
    dCn_alpha = compute_derivative(cn_alpha, r_x)
    dCn_beta = compute_derivative(cn_beta, r_x)
    dCn_aileron = compute_derivative(cn_aileron, r_x)
    dCn_elevator = compute_derivative(cn_elevator, r_x)
    dCn_rudder = compute_derivative(cn_rudder, r_x)
    dCn_u = compute_derivative(cn_u, v_x)

    dCy_p = compute_derivative(cy_p, r_x)
    dCy_q = compute_derivative(cy_q, r_x)
    dCy_r = compute_derivative(cy_r, r_x)
    dCy_alpha = compute_derivative(cy_alpha, r_x)
    dCy_beta = compute_derivative(cy_beta, r_x)
    dCy_aileron = compute_derivative(cy_aileron, r_x)
    dCy_elevator = compute_derivative(cy_elevator, r_x)
    dCy_rudder = compute_derivative(cy_rudder, r_x)
    dCy_u = compute_derivative(cy_u, v_x)

    stability_derivatives = {"functions": {
        "Cn": {"cn_alpha": cn_alpha, "cn_beta": cn_beta, "cn_u": cn_u, "cn_p": cn_p, "cn_q": cn_q, "cn_r": cn_q,
               "cn_aileron": cn_aileron, "cn_rudder": cn_rudder, "cn_elevator": cn_elevator},
        "Cl": {"cl_alpha": cl_alpha, "cl_beta": cl_beta, "cl_u": cl_u, "cl_p": cl_p, "cl_q": cl_q, "cl_r": cl_q,
               "cl_aileron": cl_aileron, "cl_rudder": cl_rudder, "cl_elevator": cl_elevator},
        "Cm": {"cm_alpha": cm_alpha, "cm_beta": cm_beta, "cm_u": cm_u, "cm_p": cm_p, "cm_q": cm_q, "cm_r": cm_q,
               "cm_aileron": cm_aileron, "cm_rudder": cm_rudder, "cm_elevator": cm_elevator},
        "CL": {"col_alpha": col_alpha, "col_beta": col_beta, "col_u": col_u, "col_p": col_p, "col_q": col_q,
               "col_r": col_q, "col_aileron": col_aileron, "col_rudder": col_rudder,
               "col_elevator": col_elevator},
        "CD": {"cd_alpha": cd_alpha, "cd_beta": cd_beta, "cd_u": cd_u, "cd_p": cd_p, "cd_q": cd_q, "cd_r": cd_q,
               "cd_aileron": cd_aileron, "cd_rudder": cd_rudder, "cd_elevator": cd_elevator},
        "CY": {"cy_alpha": cy_alpha, "cy_beta": cy_beta, "cy_u": cy_u, "cy_p": cy_p, "cy_q": cy_q, "cy_r": cy_q,
               "cy_aileron": cy_aileron, "cy_rudder": cy_rudder, "cy_elevator": cy_elevator},
        "v_x": v_x,
        "r_x": r_x,
        "spec": aircraft_wetted_area.__abs__()},
        "derivatives": {"dCol": {
            "dCol_alpha": dCol_alpha, "dCol_beta": dCol_beta, "dCol_u": dCol_u,
            "dCol_p": dCol_p, "dCol_q": dCol_q, "dCol_r": dCol_r,
            "dCol_elevator": dCol_elevator, "dCol_aileron": dCol_aileron, "dCol_rudder": dCol_rudder
        }},
        "dCd": {
            "dCd_alpha": dCd_alpha, "dCd_beta": dCd_beta, "dCl_u": dCd_u,
            "dCd_p": dCd_p, "dCd_q": dCd_q, "dCl_r": dCd_r,
            "dCd_elevator": dCd_elevator, "dCl_aileron": dCd_aileron, "dCl_rudder": dCd_rudder
        }
        ,
        "dCl": {
            "dCl_alpha": dCl_alpha, "dCl_beta": dCl_beta, "dCl_u": dCl_u,
            "dCl_p": dCl_p, "dCl_q": dCl_q, "dCl_r": dCl_r,
            "dCl_elevator": dCl_elevator, "dCl_aileron": dCl_aileron, "dCl_rudder": dCl_rudder
        },
        "dCm": {
            "dCm_alpha": dCm_alpha, "dCm_beta": dCm_beta, "dCm_u": dCm_u,
            "dCm_p": dCm_p, "dCm_q": dCm_q, "dCm_r": dCm_r,
            "dCm_elevator": dCm_elevator, "dCm_aileron": dCm_aileron, "dCm_rudder": dCm_rudder
        },
        "dCn": {
            "dCn_alpha": dCn_alpha, "dCn_beta": dCn_beta, "dCn_u": dCn_u,
            "dCn_p": dCn_p, "dCn_q": dCn_q, "dCn_r": dCn_r,
            "dCn_elevator": dCn_elevator, "dCn_aileron": dCn_aileron, "dCn_rudder": dCn_rudder
        },
        "dCy": {
            "dCy_alpha": dCy_alpha, "dCy_beta": dCy_beta, "dCy_u": dCy_u,
            "dCy_p": dCy_p, "dCy_q": dCy_q, "dCy_r": dCy_r,
            "dCy_elevator": dCy_elevator, "dCy_aileron": dCy_aileron, "dCy_rudder": dCy_rudder
        }
    }

    rudder_limits_upper=[]
    rudder_limits_lower = []

    aileron_limits_upper=[]
    aileron_limits_lower=[]

    elevator_limits_upper=[]
    elevator_limits_lower=[]

    var1=[col_rudder,cd_rudder,cl_rudder,cm_rudder,cn_rudder,cy_rudder]
    for l  in var1:
        rudder_limits_upper.append(find_limits(l,r_x)[0])
        rudder_limits_lower.append(find_limits(l, r_x)[1])

    var1 = [col_aileron, cd_aileron, cl_aileron, cm_aileron, cn_aileron, cy_aileron]
    for l in var1:
        aileron_limits_upper.append(find_limits(l, r_x)[0])
        aileron_limits_lower.append(find_limits(l, r_x)[1])

    var1 = [col_elevator, cd_elevator, cl_elevator, cm_elevator, cn_elevator, cy_elevator]
    for l in var1:
        elevator_limits_upper.append(find_limits(l, r_x)[0])
        elevator_limits_lower.append(find_limits(l, r_x)[1])

    rudder_limit_upper=min(rudder_limits_upper)
    elevator_limit_upper=min(elevator_limits_upper)
    aileron_limit_upper=min(aileron_limits_upper)

    rudder_limit_lower = min(rudder_limits_lower)
    elevator_limit_lower = min(elevator_limits_lower)
    aileron_limit_lower = min(aileron_limits_lower)




    aerodynamic_results = {
        "Aerdodynamics": {
            "CL_Max": float(find_max_cl(col_alpha)),
            "alpha_stall": float(find_alpha_stall(col_alpha, r_x)),
            "velocity_stall": float(find_velocity_stall(col_u, v_x)),
        },
        "Max_Deflections":{
            "rudder_limit_lower":float(rudder_limit_lower),
            "elevator_limit_lower": float(elevator_limit_lower),
            "aileron_limit_lower": float(aileron_limit_lower),

            "rudder_limit_upper": float(rudder_limit_upper),
            "elevator_limit_upper":float( elevator_limit_upper),
            "aileron_limit_upper": float(aileron_limit_upper)


        }
    }

    write_control_specifications(stability_derivatives)
    write_aerodynamic_results(aerodynamic_results)
    return 1





def runRoskamSimulation():
    aicraft_specifications = Database.read_aircraft_specifications()
