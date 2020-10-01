import copy

from aerosandbox import *

from utils import MathLibrary, Database
from utils.MathLibrary import *


def run_analysis(values={},alpha=0,beta=0,velocity=0,fast_track=True,p=0,q=0,r=0,aileron_deflection=0,elevator_deflection=0,rudder_deflection=0):
    wing_root_location_x,wing_root_location_y,wing_root_location_z, wing_dihedral, wing_sweep, wing_twist,wing_span, wing_taper_ratio,wing_chord,winglet_width,winglet_rotation,winglet_center_translation_x,winglet_center_translation_y,winglet_center_translation_z,wing_profile=read_w_h_v(values=values,part="wing")
    htp_root_location_x, htp_root_location_y, htp_root_location_z, htp_dihedral, htp_sweep, htp_twist, htp_span, htp_taper_ratio, htp_chord,z1,z2,z3,z4,z5,htp_profile = read_w_h_v(
        values=values, part="htp")
    vtp_root_location_x, vtp_root_location_y, vtp_root_location_z, vtp_dihedral, vtp_sweep, vtp_twist, vtp_span, vtp_taper_ratio, vtp_chord,z1,z2,z3,z4,z5,vtp_profile = read_w_h_v(
        values=values, part="vtp")

    wing_span=wing_span/2
    htp_span=htp_span/2
    vtp_span=vtp_span

    aileron_hinge=values["aileron_root_position_x"]
    elevator_hinge = values["elevator_root_position_x"]
    rudder_hinge = values["rudder_root_position_x"]

    fuselage_diameter,fuselage_length,nose_radius,nose_position_x,nose_position_y,nose_position_z,section_2_radius,section_2_center_position_x,section_2_center_position_y,section_2_center_position_z,section_3_radius,section_3_center_position_x,section_3_center_position_y,section_3_center_position_z,section_4_radius,section_4_center_position_x,section_4_center_position_y,section_4_center_position_z,tail_angle,tail_radius,tail_position_x,tail_position_y,tail_position_z=read_fuselage_values(values=values)
    structure_specs = Database.read_structures_specifications()
    wing_structure=structure_specs["wing_structure"]
    htp_structure=structure_specs["htp_structure"]
    vtp_structure = structure_specs["vtp_structure"]
    wing_sweep =quater_chord_sweep_to_leading_edge(sweep=wing_sweep,taper_ratio=wing_taper_ratio,area=wing_structure["wing_reference_area"])
    vtp_sweep=quater_chord_sweep_to_leading_edge(sweep=vtp_sweep,taper_ratio=vtp_taper_ratio,area=vtp_structure["vtp_reference_area"])
    htp_sweep = quater_chord_sweep_to_leading_edge(sweep=htp_sweep, taper_ratio=htp_taper_ratio,
                                                       area=htp_structure["htp_reference_area"])
    generic_cambered_airfoil = Airfoil(
        CL_function=lambda alpha, Re, mach, deflection,: (  # Lift coefficient function
                (alpha * np.pi / 180) * (2 * np.pi) + 0.4550
        ),
        CDp_function=lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
                (1 + (alpha / 5) ** 2) * 2 * (0.074 / Re ** 0.2)
        ),
        Cm_function=lambda alpha, Re, mach, deflection: (  # Moment coefficient function
            0
        )
    )
    generic_airfoil = Airfoil(
        CL_function=lambda alpha, Re, mach, deflection,: (  # Lift coefficient function
                (alpha * np.pi / 180) * (2 * np.pi)
        ),
        CDp_function=lambda alpha, Re, mach, deflection: (  # Profile drag coefficient function
                (1 + (alpha / 5) ** 2) * 2 * (0.074 / Re ** 0.2)
        ),
        Cm_function=lambda alpha, Re, mach, deflection: (  # Moment coefficient function
            0
        )
    )
    ########## Now, we're ready to start putting together our 3D CasLL1 run! ##########

    opti = cas.Opti()  # Initialize an analysis/optimization environment

    ### Define the 3D geometry you want to analyze/optimize.
    # Here, all distances are in meters and all angles are in degrees.
    airplane = Airplane(
        name="Peter's Glider",
        x_ref=structure_specs["Inertia"]["cg_x"],  # CG location
        y_ref=structure_specs["Inertia"]["cg_y"],  # CG location
        z_ref=structure_specs["Inertia"]["cg_z"],  # CG location
    fuselages=[
            Fuselage(
                name="Fuselage",
                x_le=0,
                y_le=0,
                z_le=0,
                symmetric=False,
                xsecs=[
                    FuselageXSec(
                        x_c=nose_position_x - nose_radius,
                        y_c=nose_position_y,
                        z_c=nose_position_z,
                        radius=0
                    ), FuselageXSec(
                        x_c=nose_position_x - nose_radius / 2,
                        y_c=nose_position_y,
                        z_c=nose_position_z,
                        radius=nose_radius - nose_radius / 2
                    ),
                    FuselageXSec(
                        x_c=nose_position_x,
                        y_c=nose_position_y,
                        z_c=nose_position_z,
                        radius=nose_radius
                    ),
                    FuselageXSec(
                        x_c=section_2_center_position_x,
                        y_c=section_2_center_position_y,
                        z_c=section_2_center_position_z,
                        radius=section_2_radius
                    ),
                    FuselageXSec(
                        x_c=section_3_center_position_x,
                        y_c=section_3_center_position_y,
                        z_c=section_3_center_position_z,
                        radius=section_3_radius
                    ),
                    FuselageXSec(
                        x_c=section_4_center_position_x,
                        y_c=section_4_center_position_y,
                        z_c=section_4_center_position_z,
                        radius=section_4_radius
                    )
                    ,FuselageXSec(
                        x_c=tail_position_x - tail_radius / 2,
                        y_c=tail_position_y,
                        z_c=tail_position_z,
                        radius=tail_radius + tail_radius / 2
                    ),
                    FuselageXSec(
                        x_c=tail_position_x,
                        y_c=tail_position_y,
                        z_c=tail_position_z,
                        radius=tail_radius
                    )

                ]
            )
        ],
        wings=[
            Wing(
                name="Main Wing",
                x_le=wing_root_location_x,  # Coordinates of the wing's leading edge
                y_le=wing_root_location_y,  # Coordinates of the wing's leading edge
                z_le=wing_root_location_z,  # Coordinates of the wing's leading edge
                symmetric=True,  # Should this wing be mirrored across the XZ plane?
                xsecs=[  # The wing's cross ("X") sections
                    WingXSec(  # Root
                        x_le=0,  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                        y_le=0,  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                        z_le=0,  # Coordinates of the XSec's leading edge, relative to the wing's leading edge.
                        chord=wing_chord,
                        twist=wing_twist,# degrees
                        airfoil=Airfoil(name="naca{}".format(wing_profile)),  # Airfoils are blended between a given XSec and the next one.
                        control_surface_type='symmetric',  # Flap (ctrl. surfs. applied between this XSec and the next one.)
                        control_surface_deflection=0,  # degrees
                    ),

                    WingXSec(  # Tip
                        x_le=MathLibrary.getXFromSweep(sweep_angle=wing_sweep,span=wing_span,root_location=0),
                        y_le=wing_span,
                        z_le=MathLibrary.getZFromDiherdral(wing_dihedral_angle=wing_dihedral,wing_span=wing_span,root_location=0),
                        chord=wing_chord/wing_taper_ratio,
                        twist=wing_twist,
                        airfoil=Airfoil(name="naca{}".format(wing_profile)),
                        control_surface_type='asymmetric',
                        control_surface_hinge_point=aileron_hinge,# Aileron
                        control_surface_deflection=aileron_deflection,
                    )

                ]
            ),
            Wing(
                name="Vertical Stabilizer",
                x_le=vtp_root_location_x,
                y_le=vtp_root_location_y,
                z_le=vtp_root_location_z,
                symmetric=False,
                xsecs=[
                    WingXSec(  #
                        x_le=0,
                        y_le=0,
                        z_le=0,
                        chord=vtp_chord,
                        twist=vtp_twist,
                        airfoil=Airfoil(name="naca{}".format(vtp_profile)),
                    ),
                    WingXSec(
                        x_le=MathLibrary.getXFromSweep(sweep_angle=-vtp_sweep, span=vtp_span,
                                  root_location=0),
                        y_le=0,
                        z_le=vtp_span,
                        chord=vtp_chord / vtp_taper_ratio,
                        twist=vtp_twist,
                        airfoil=Airfoil(name="naca{}".format(vtp_profile)),
                        control_surface_type='symmetric',
                        control_surface_hinge_point=rudder_hinge,# rudder
                        control_surface_deflection=rudder_deflection,
                    )
                ]
            ),
            Wing(
                name="Horizontal Stabilizer",
                x_le=htp_root_location_x,
                y_le=htp_root_location_y,
                z_le=htp_root_location_z,
                symmetric=True,
                xsecs=[

                    WingXSec(  #
                        x_le=0,
                        y_le=0,
                        z_le=0,
                        chord=htp_chord,
                        twist=htp_twist,
                        airfoil=Airfoil(name="naca{}".format(htp_profile)),
                    ),
                    WingXSec( #tip
                        x_le=MathLibrary.getXFromSweep(sweep_angle=htp_sweep, span=htp_span,
                                                       root_location=0),
                        y_le=htp_span,
                        z_le=MathLibrary.getZFromDiherdral(wing_dihedral_angle=htp_dihedral, wing_span=htp_span,
                                                           root_location=0),
                        chord=htp_chord/htp_taper_ratio,
                        twist=htp_twist,
                        airfoil=Airfoil(name="naca{}".format(htp_profile)),
                        control_surface_type='symmetric',
                        control_surface_hinge_point=elevator_hinge,
                        control_surface_deflection=elevator_deflection,
                    )
                ]
            )
        ]
    )
    airplane.set_spanwise_paneling_everywhere(8)  # Set the resolution of your analysis
    ap = Casll1(  # Set up the AeroProblem
        airplane=airplane,
        op_point=OperatingPoint(
            density=1.225,  # kg/m^3
            viscosity=1.81e-5,  # kg/m-s
            velocity=velocity,  # m/s
            mach=0,  # Freestream mach number
            alpha=alpha,  # In degrees
            beta=beta,  # In degrees
            p=p,  # About the body x-axis, in rad/sec
            q=q,  # About the body y-axis, in rad/sec
            r=r,  # About the body z-axis, in rad/sec
        ),
        opti=opti  # Pass it an optimization environment to work in
    )

    # Solver options
    p_opts = {}
    s_opts = {}
    s_opts["mu_strategy"] = "adaptive"

    opti.solver('ipopt', p_opts, s_opts)

    # Solve
    try:
        sol = opti.solve()
    except RuntimeError:
        sol = opti.debug

    # Postprocess

    # Create solved object
    ap_sol = copy.deepcopy(ap)
    ap_sol.substitute_solution(sol)
    if(fast_track==False):
        ap_sol.draw(show=True)  # Generates a pretty picture!
    values = {"CL": ap_sol.CL, "CD": ap_sol.CD, "CY": ap_sol.CY, "Cl": ap_sol.Cl, "Cm": ap_sol.Cm, "Cn": ap_sol.Cn}
    return values

def read_w_h_v(part="",values={}):
    root_location_x = values.get(part+"_root_position_x")
    root_location_y = values.get(part+"_root_position_y")
    root_location_z = values.get(part+"_root_position_z")
    chord=values.get(part+"_chord")
    dihedral=values.get(part+"_dihedral")
    sweep=values.get(part+"_sweep")
    twist=values.get(part+"_twist")
    profile=values[part+"_profile"]
    span=values.get(part+"_span")
    taper_ratio=values.get(part+"_taper_ratio")
    if part=="wing":
        winglet_width=values.get("winglet_width")
        winglet_center_translation_x = values.get("winglet_center_translation_x")
        winglet_center_translation_y=values.get("winglet_center_translation_y")
        winglet_center_translation_z=values.get("winglet_center_translation_z")
        winglet_rotation=values.get("winglet_rotation")
    else:
        winglet_width = 0
        winglet_center_translation_x =0
        winglet_center_translation_y = 0
        winglet_center_translation_z = 0
        winglet_rotation =0



    return root_location_x,root_location_y,root_location_z,dihedral,sweep,twist,span,taper_ratio,chord,winglet_width,winglet_rotation,winglet_center_translation_x,winglet_center_translation_y,winglet_center_translation_z,profile
def read_fuselage_values(values={}):

    fuselage_length=values.get("fuselage_length")
    fuselage_diameter= values.get("fuselage_diameter")
    nose_radius = values.get("nose_radius")
    nose_position_x= values.get("nose_center_position_x")
    nose_position_y = values.get("nose_center_position_y")
    nose_position_z = values.get("nose_center_position_z")
    tail_radius = values.get("tail_radius")
    tail_position_x = values.get("tail_center_position_x")
    tail_position_y = values.get("tail_center_position_y")
    tail_position_z = values.get("tail_center_position_z")
    tail_angle=values.get("tail_angle")
    section_2_center_position_x = values.get("section_2_center_position_x")
    section_2_center_position_y = values.get("section_2_center_position_y")
    section_2_center_position_z = values.get("section_2_center_position_z")
    section_2_radius=values.get("section_2_radius")
    section_3_radius = values.get("section_3_radius")
    section_3_center=values.get("section_3_center")
    section_3_center_position_x= values.get("section_3_center_position_x")
    section_3_center_position_y= values.get("section_3_center_position_y")
    section_3_center_position_z = values.get("section_3_center_position_z")
    section_4_center=values.get("section_4_center")
    section_4_center_position_x=values.get("section_4_center_position_x")
    section_4_center_position_y= values.get("section_4_center_position_y")
    section_4_center_position_z = values.get("section_4_center_position_z")
    section_4_radius=values.get("section_4_radius")
    return fuselage_diameter,fuselage_length,nose_radius,nose_position_x,nose_position_y,nose_position_z,section_2_radius,section_2_center_position_x,section_2_center_position_y,section_2_center_position_z,section_3_radius,section_3_center_position_x,section_3_center_position_y,section_3_center_position_z,section_4_radius,section_4_center_position_x,section_4_center_position_y,section_4_center_position_z,tail_angle,tail_radius,tail_position_x,tail_position_y,tail_position_z