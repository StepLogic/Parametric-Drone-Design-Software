import copy

from aerosandbox import cas, Casll1, OperatingPoint

from Aerodynamics.sandbox.input import create_aircraft

# TODO Remove multiple mach number support
from Aerodynamics.sandbox.vlm_sandbox import start_vlm


def run_analysis():
    airplane = create_aircraft()
    try:
        opti = cas.Opti()
        ap = Casll1(  # Set up the AeroProblem
            airplane=airplane,
            op_point=OperatingPoint(
                density=1.225,  # kg/m^3
                viscosity=1.81e-5,  # kg/m-s
                velocity=10,  # m/s070
                mach=0,  # Freestream mach number
                alpha=10,  # In degrees
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
        ap_sol.draw(show=True)  # Generates a pretty picture!
        values = {"type": "CAS", "CL": ap_sol.CL, "CD": ap_sol.CD, "CY": ap_sol.CY, "Cl": ap_sol.Cl, "Cm": ap_sol.Cm,
                  "Cn": ap_sol.Cn}
    except:
        values=start_vlm(airplane)
    print(values)
    return values
