from aerosandbox import Fuselage, FuselageXSec, np

from Utils.data_objects.lifting_surface_placeholder import fin
from Utils.data_objects.placeholder import conventional_design, unconventional_design
from Utils.database.aerodynamics.sandbox_database import get_parameters_for_conventional, \
    get_parameters_for_unconventional, get_parameters_for_boom, get_parameters_for_fuselage
from Utils.database.geometry.boom_database import get_boom_object_data, read_boom_objects
from Utils.database.geometry.lifting_database import get_surface_object_data, read_lifting_surface_objects, tailplane


def create_aircraft():
    print(get_booms())
    if len(get_booms()) > 0:
        from aerosandbox import Airplane
        airplane = Airplane(
            fuselages=get_booms(),
            wings=get_lifting_surfaces(type_="CAS")
        )

    else:
        from aerosandbox_legacy_v0 import Airplane
        airplane = Airplane(
            wings=get_lifting_surfaces(type_="vlm")
        )

    return airplane


def get_booms():
    boom_list = read_boom_objects()
    fuselages = []
    for l in boom_list:
        design_type_, surface_type_ = get_boom_object_data(l)
        xsecs = []
        root_position_x_, root_position_y_, root_position_z_ = 0, 0, 0
        xz_mirror_ = False
        if design_type_ == conventional_design:
            radii, x, z, root_position_x_, root_position_y_, root_position_z_, xz_mirror_ = get_parameters_for_fuselage(
                l)
            for radius, x_, z_ in zip(radii, x, z):
                xsecs.append(
                    FuselageXSec(
                        x_c=x_,
                        y_c=0,
                        z_c=z_,
                        radius=radius
                    )
                )
                fuselages.append(Fuselage(
                    name=l,
                    x_le=root_position_x_,
                    y_le=root_position_y_,
                    z_le=root_position_z_,
                    symmetric=xz_mirror_,
                    xsecs=xsecs
                ))
        elif design_type_ == unconventional_design:
            radii, x, z, root_position_x_, root_position_y_, root_position_z_, xz_mirror_ = get_parameters_for_boom(l)
            for radius, x_, z_ in zip(radii, x, z):
                xsecs.append(
                    FuselageXSec(
                        x_c=x_,
                        y_c=0,
                        z_c=z_,
                        radius=radius
                    )
                )
            fuselages.append(Fuselage(
                name=l,
                x_le=root_position_x_,
                y_le=root_position_y_,
                z_le=root_position_z_,
                symmetric=xz_mirror_,
                xsecs=xsecs
            ))
    return fuselages


def get_lifting_surfaces(type_="vlm"):
    if type_ == "vlm":
        return get_surface_for_vlm()
    else:
        return get_surface_for_cas()


def get_surface_for_cas():
    from aerosandbox import WingXSec, Wing, Airfoil
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

    from Utils.data_objects.lifting_surface_placeholder import wing
    wings = []
    surface_list = read_lifting_surface_objects()
    for l in surface_list:
        design_type_, surface_type_ = get_surface_object_data(l)
        if design_type_ == unconventional_design:
            x, y, z, chords, twist_, profile_, root_location_x, root_location_y, root_location_z, xz_mirror_ = get_parameters_for_unconventional(
                l)
            xsecs = []
            for x_, y_, z_, chord_, t in zip(x, y, z, chords, twist_):
                print(profile_)
                xsecs.append(
                    WingXSec(  # Root
                        x_le=x_,
                        y_le=y_,
                        z_le=z_,
                        chord=chord_,
                        twist=t,
                        airfoil=Airfoil(profile_)
                    ))
            wings.append(
                Wing(
                    name=l,
                    x_le=root_location_x,  # Coordinates of the wing's leading edge
                    y_le=root_location_y,  # Coordinates of the wing's leading edge
                    z_le=root_location_z,  # Coordinates of the wing's leading edge
                    symmetric=xz_mirror_,
                    xsecs=xsecs
                ))
        elif design_type_ == conventional_design:
            x, y, z, chords, twist, profile_, root_location_x, root_location_y, root_location_z = get_parameters_for_conventional(
                l, surface_type_)
            xsecs = []
            for x_, y_, z_, chord_ in zip(x, y, z, chords):
                if surface_type_ == wing or surface_type_ == tailplane:
                    xsecs.append(
                        WingXSec(  # Root
                            x_le=x_,
                            y_le=y_,
                            z_le=z_,
                            chord=chord_,
                            twist=twist,
                            airfoil=Airfoil(profile_)
                        ))
                else:
                    print(x_)
                    xsecs.append(
                        WingXSec(  # Root
                            x_le=x_,
                            y_le=z_,
                            z_le=y_,
                            chord=chord_,
                            twist=twist,
                            airfoil=Airfoil(profile_)
                        ))

            wings.append(
                Wing(
                    name=l,
                    x_le=root_location_x,  # Coordinates of the wing's leading edge
                    y_le=root_location_y,  # Coordinates of the wing's leading edge
                    z_le=root_location_z,  # Coordinates of the wing's leading edge
                    symmetric=True if surface_type_ == wing or surface_type_ == tailplane else False,
                    xsecs=xsecs
                )
            )
    return wings


def get_surface_for_vlm():
    from aerosandbox_legacy_v0 import WingXSec, Wing, Airfoil
    from Utils.data_objects.lifting_surface_placeholder import wing
    wings = []
    surface_list = read_lifting_surface_objects()
    for l in surface_list:
        design_type_, surface_type_ = get_surface_object_data(l)
        if design_type_ == unconventional_design:
            from aerosandbox import wing
            x, y, z, chords, twist_, profile_, root_location_x, root_location_y, root_location_z, xz_mirror_ = get_parameters_for_unconventional(
                l)
            xsecs = []
            for x_, y_, z_, chord_, t in zip(x, y, z, chords, twist_):
                xsecs.append(
                    WingXSec(  # Root
                        xyz_le=[x_, y_, z_],
                        chord=chord_,
                        twist=t,
                        airfoil=Airfoil(name=profile_)
                    ))
            wings.append(
                Wing(
                    name=l,
                    xyz_le=[root_location_x, root_location_y, root_location_z],
                    # Coordinates of the wing's leading edge
                    symmetric=xz_mirror_,
                    xsecs=xsecs
                ))
        elif design_type_ == conventional_design:
            x, y, z, chords, twist, profile_, root_location_x, root_location_y, root_location_z = get_parameters_for_conventional(
                l, surface_type_)
            xsecs = []
            for x_, y_, z_, chord_ in zip(x, y, z, chords):
                print(surface_type_)
                if surface_type_ == wing or surface_type_ == tailplane:
                    xsecs.append(
                        WingXSec(  # Root
                            xyz_le=[x_, y_, z_],
                            chord=chord_,
                            twist=twist,
                            airfoil=Airfoil(name=profile_)
                        ))
                elif surface_type_ == fin:
                    print(fin)
                    xsecs.append(
                        WingXSec(  # Root
                            xyz_le=[x_, z_, y_],
                            chord=chord_,
                            twist=twist,
                            airfoil=Airfoil(name=profile_)
                        ))

            wings.append(
                Wing(
                    name=l,
                    xyz_le=[root_location_x, root_location_y, root_location_z],
                    symmetric=True if surface_type_ == wing or surface_type_ == tailplane else False,
                    xsecs=xsecs
                )
            )
    return wings
