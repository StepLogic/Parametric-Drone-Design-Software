import copy

from aerosandbox import *

from Aerodynamics.sandbox.input import create_aircraft
from Aerodynamics.sandbox.vlm_sandbox import f_alpha_vlm, f_beta_vlm, f_p_vlm, f_r_vlm, f_q_vlm
from Utils.maths.math_library import check_if_nan


def f_alpha(x, velocity):
    airplane = create_aircraft()
    try:
        airplane.set_spanwise_paneling_everywhere(8)  # Set the resolution of your analysis
        opti = cas.Opti()
        ap = Casll1(  # Set up the AeroProblem
            airplane=airplane,
            op_point=OperatingPoint(
                density=1.225,  # kg/m^3
                viscosity=1.81e-5,  # kg/m-s
                velocity=velocity,  # m/s070
                mach=0,  # Freestream mach number
                alpha=x,  # In degrees
                beta=0,  # In degrees
                p=0,  # About the body x-axis, in rad/sec
                q=0,  # About the body y-axis, in rad/sec
                r=0,  # About the body z-axis, in rad/sec
            ),
            opti=opti  # Pass it an optimization environment to work in
        )
        p_opts = {}
        s_opts = {}
        s_opts["mu_strategy"] = "adaptive"
        opti.solver('ipopt', p_opts, s_opts)
        try:
            sol = opti.solve()
        except RuntimeError:
            sol = opti.debug
        ap_sol = copy.deepcopy(ap)
        ap_sol.substitute_solution(sol)

        values = {"CL": check_if_nan(ap_sol.CL), "CD": check_if_nan(ap_sol.CD), "CY": check_if_nan(ap_sol.CY),
                  "Cl": check_if_nan(ap_sol.Cl), "Cm": check_if_nan(ap_sol.Cm), "Cn": check_if_nan(ap_sol.Cn)}
    except:
        values = f_alpha_vlm(x, velocity, airplane)
    return values


def f_beta(x, velocity):
    airplane = create_aircraft()
    try:
        airplane.set_spanwise_paneling_everywhere(8)  # Set the resolution of your analysis
        opti = cas.Opti()
        ap = Casll1(  # Set up the AeroProblem
            airplane=airplane,
            op_point=OperatingPoint(
                density=1.225,  # kg/m^3
                viscosity=1.81e-5,  # kg/m-s
                velocity=velocity,  # m/s070
                mach=0,  # Freestream mach number
                alpha=0,  # In degrees
                beta=x,  # In degrees
                p=0,  # About the body x-axis, in rad/sec
                q=0,  # About the body y-axis, in rad/sec
                r=0,  # About the body z-axis, in rad/sec
            ),
            opti=opti  # Pass it an optimization environment to work in
        )
        p_opts = {}
        s_opts = {}
        s_opts["mu_strategy"] = "adaptive"
        opti.solver('ipopt', p_opts, s_opts)
        try:
            sol = opti.solve()
        except RuntimeError:
            sol = opti.debug
        ap_sol = copy.deepcopy(ap)
        ap_sol.substitute_solution(sol)

        values = {"CL": check_if_nan(ap_sol.CL), "CD": check_if_nan(ap_sol.CD), "CY": check_if_nan(ap_sol.CY),
                  "Cl": check_if_nan(ap_sol.Cl), "Cm": check_if_nan(ap_sol.Cm), "Cn": check_if_nan(ap_sol.Cn)}
    except:
        values = f_beta_vlm(x, velocity, airplane)
    return values


def f_p(x, velocity):
    airplane = create_aircraft()
    try:
        airplane.set_spanwise_paneling_everywhere(8)  # Set the resolution of your analysis
        opti = cas.Opti()
        ap = Casll1(  # Set up the AeroProblem
            airplane=airplane,
            op_point=OperatingPoint(
                density=1.225,  # kg/m^3
                viscosity=1.81e-5,  # kg/m-s
                velocity=velocity,  # m/s070
                mach=0,  # Freestream mach number
                alpha=0,  # In degrees
                beta=0,  # In degrees
                p=x,  # About the body x-axis, in rad/sec
                q=0,  # About the body y-axis, in rad/sec
                r=0,  # About the body z-axis, in rad/sec
            ),
            opti=opti  # Pass it an optimization environment to work in
        )
        p_opts = {}
        s_opts = {}
        s_opts["mu_strategy"] = "adaptive"
        opti.solver('ipopt', p_opts, s_opts)
        try:
            sol = opti.solve()
        except RuntimeError:
            sol = opti.debug
        ap_sol = copy.deepcopy(ap)
        ap_sol.substitute_solution(sol)

        values = {"CL": check_if_nan(ap_sol.CL), "CD": check_if_nan(ap_sol.CD), "CY": check_if_nan(ap_sol.CY),
                  "Cl": check_if_nan(ap_sol.Cl), "Cm": check_if_nan(ap_sol.Cm), "Cn": check_if_nan(ap_sol.Cn)}
    except:
        values = f_p_vlm(x, velocity, airplane)
    return values


def f_q(x, velocity):
    airplane = create_aircraft()
    try:
        airplane.set_spanwise_paneling_everywhere(8)  # Set the resolution of your analysis
        opti = cas.Opti()
        ap = Casll1(  # Set up the AeroProblem
            airplane=airplane,
            op_point=OperatingPoint(
                density=1.225,  # kg/m^3
                viscosity=1.81e-5,  # kg/m-s
                velocity=velocity,  # m/s070
                mach=0,  # Freestream mach number
                alpha=0,  # In degrees
                beta=0,  # In degrees
                p=0,  # About the body x-axis, in rad/sec
                q=x,  # About the body y-axis, in rad/sec
                r=0,  # About the body z-axis, in rad/sec
            ),
            opti=opti  # Pass it an optimization environment to work in
        )
        p_opts = {}
        s_opts = {}
        s_opts["mu_strategy"] = "adaptive"
        opti.solver('ipopt', p_opts, s_opts)
        try:
            sol = opti.solve()
        except RuntimeError:
            sol = opti.debug
        ap_sol = copy.deepcopy(ap)
        ap_sol.substitute_solution(sol)

        values = {"CL": check_if_nan(ap_sol.CL), "CD": check_if_nan(ap_sol.CD), "CY": check_if_nan(ap_sol.CY),
                  "Cl": check_if_nan(ap_sol.Cl), "Cm": check_if_nan(ap_sol.Cm), "Cn": check_if_nan(ap_sol.Cn)}
    except:
        values = f_q_vlm(x, velocity, airplane)
    return values


def f_r(x, velocity):
    airplane = create_aircraft()
    try:
        airplane.set_spanwise_paneling_everywhere(8)  # Set the resolution of your analysis
        opti = cas.Opti()
        ap = Casll1(  # Set up the AeroProblem
            airplane=airplane,
            op_point=OperatingPoint(
                density=1.225,  # kg/m^3
                viscosity=1.81e-5,  # kg/m-s
                velocity=velocity,  # m/s070
                mach=0,  # Freestream mach number
                alpha=0,  # In degrees
                beta=0,  # In degrees
                p=0,  # About the body x-axis, in rad/sec
                q=0,  # About the body y-axis, in rad/sec
                r=x,  # About the body z-axis, in rad/sec
            ),
            opti=opti  # Pass it an optimization environment to work in
        )
        p_opts = {}
        s_opts = {}
        s_opts["mu_strategy"] = "adaptive"
        opti.solver('ipopt', p_opts, s_opts)
        try:
            sol = opti.solve()
        except RuntimeError:
            sol = opti.debug
        ap_sol = copy.deepcopy(ap)
        ap_sol.substitute_solution(sol)

        values = {"CL": check_if_nan(ap_sol.CL), "CD": check_if_nan(ap_sol.CD), "CY": check_if_nan(ap_sol.CY),
                  "Cl": check_if_nan(ap_sol.Cl), "Cm": check_if_nan(ap_sol.Cm), "Cn": check_if_nan(ap_sol.Cn)}
    except:
        values = f_r_vlm(x, velocity, airplane)
    return values
