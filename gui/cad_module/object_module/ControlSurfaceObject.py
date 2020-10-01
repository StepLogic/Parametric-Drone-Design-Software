import tigl3.configuration
import tigl3.geometry
import tigl3.tigl3wrapper
import tixi3.tixi3wrapper
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Display.SimpleGui import init_display
import OCC.Quantity
from tigl3.boolean_ops import CCutShape

import Helper
from utils import MathLibrary
from utils.Database import read_aircraft_specifications


def create_wing(aircraft, sweep, wing_span, chord, taper_ratio, x, y, z, type="wing"):
    wings = aircraft.get_wings()
    wing_main = wings.create_wing("wing_main_{}".format(type), 3, "NACA0012")
    wing_main.set_symmetry(tigl3.geometry.TIGL_X_Z_PLANE)

    wing_main.set_root_leposition(tigl3.geometry.CTiglPoint(x, y, z))
    wing_main.scale(1)
    wing_main_half_span = wing_span
    if type == "rudder":
        wing_main.set_half_span_keep_ar(wing_main_half_span)
    elif type == "elevator":
        wing_main.set_half_span_keep_ar(wing_main_half_span)
    elif type == "aileron":
        wing_main.set_half_span_keep_ar(wing_main_half_span)


    # move second to last section towards tip
    tip_idx = wing_main.get_section_count()
    tip = wing_main.get_section(tip_idx).get_section_element(1).get_ctigl_section_element().get_center()
    pre_tip = wing_main.get_section(tip_idx - 2).get_section_element(1).get_ctigl_section_element().get_center()
    s = wing_main.get_section(tip_idx - 1)
    e = s.get_section_element(1)
    ce = e.get_ctigl_section_element()
    center = ce.get_center()
    theta = 0.95
    center.x = theta * tip.x + (1 - theta) * pre_tip.x
    center.y = theta * tip.y + (1 - theta) * pre_tip.y
    center.z = theta * tip.z + (1 - theta) * pre_tip.z
    ce.set_center(center)

    # decrease section size towards wing tips
    root_width = chord
    root_height = 0.25 * chord
    tip_width = chord / taper_ratio
    tip_height = 0.25 * tip_width

    n_sections = wing_main.get_section_count()
    for idx in range(1, n_sections + 1):
        s = wing_main.get_section(idx)
        e = s.get_section_element(1)
        ce = e.get_ctigl_section_element()
        theta = ce.get_center().y / wing_main_half_span

        ce.set_width((1 - theta) * root_width + theta * tip_width)
        ce.set_height((1 - theta) * root_height + theta * tip_height)

    wing_main.set_sweep(sweep)
    wing_main.set_dihedral(0)
    if type == "rudder":
        wing_main.set_rotation(tigl3.geometry.CTiglPoint(90, 0, 0))

    return wing_main


def show_lofts(viewer, lofts, prev_cs_loft, update):
    for loft in lofts:
        if update:
            for l in prev_cs_loft:
                viewer.remove(l.shape())
            viewer.add(loft.shape())
        else:
            viewer.add(loft.shape())
            viewer._display.View.SetProj(-2, -1, 1)
            viewer._display.View.SetScale(90)


def draw_control_surface(display, part, params, prev_wing_loft, prev_cs_loft, update):
    # initialize an empty aircraft from "empty.cpacs3.xml"

    t_h_1 = tixi3.tixi3wrapper.Tixi3()
    t_h_1.open(Helper.absolute_path + "/resources/empty.cpacs3.xml")
    tg_h_1 = tigl3.tigl3wrapper.Tigl3()
    tg_h_1.open(t_h_1, "")

    # initialize an empty ...........  ######
    mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()
    aircraft = mgr.get_configuration(tg_h_1._handle.value)
    lofts = []
    wing_main = prev_wing_loft

    from tigl3.geometry import CTiglTransformation

    span = params[part][part + "_span"]
    chord = params[part][part + "_chord"]
    position_x = params[part][part + "_root_position_x"]
    position_y = params[part][part + "_root_position_y"]
    position_z = params[part][part + "_root_position_z"]
    sweep = 0
    if part == "aileron":

        values = read_aircraft_specifications()
        par = "wing"
        sweep = values[par + "_sweep"]
        root_location_x = values.get(par + "_root_position_x")
        root_location_y = values.get(par + "_root_position_y")
        root_location_z = values.get(par + "_root_position_z")
        position_x = position_x + root_location_x
        position_y = position_y + root_location_y
        position_z = position_z + root_location_z



    elif part == "rudder":
        values = read_aircraft_specifications()
        par = "vtp"
        sweep = values[par + "_sweep"]
        root_location_x = values.get(par + "_root_position_x")
        root_location_y = values.get(par + "_root_position_y")
        root_location_z = values.get(par + "_root_position_z")
        position_x = position_x + root_location_x
        position_y = position_y + root_location_y
        position_z = position_z + root_location_z
    elif part == "elevator":
        values = read_aircraft_specifications()
        par = "htp"
        sweep = values.get(par + "_sweep")
        root_location_x = values.get(par + "_root_position_x")
        root_location_y = values.get(par + "_root_position_y")
        root_location_z = values.get(par + "_root_position_z")
        position_x = position_x+root_location_x
        position_y =position_y+ root_location_y
        position_z = position_z +root_location_z


    wing_loft = []
    if part == "aileron":
        control_surface = create_wing(aircraft, sweep=0, taper_ratio=1, wing_span=span,
                                      chord=chord, x=0, y=0, z=0, type=part)

        from tigl3.geometry import CNamedShape
        trafo = CTiglTransformation()
        trafo.add_translation(position_x, position_y, position_z - 0.3)
        traf = CTiglTransformation()
        traf.add_rotation_z(-sweep)
        box = BRepPrimAPI_MakeBox(chord, span, 10).Solid()
        moved_box = traf.transform(box)
        move_again = trafo.transform(moved_box)

        control_surface_cut_out = move_again
        tr = CTiglTransformation()
        tr.add_rotation_z(sweep)
        cs_object = control_surface.get_loft().shape()
        cs_n = traf.transform(cs_object)

        trafo = CTiglTransformation()

        trafo.add_translation(position_x,
                              position_y,
                              position_z)
        cs_wing = trafo.transform(cs_n)

        wing_1 = CNamedShape(cs_wing, "loft")
        lofts.append(wing_1)

        tr = CTiglTransformation()
        tr.add_mirroring_at_xzplane()

        wing_2 = CNamedShape(tr.transform(cs_wing), "loft")
        lofts.append(wing_2)

        cut_out_1 = control_surface_cut_out
        trafo = CTiglTransformation()
        trafo.add_mirroring_at_xzplane()
        cut_out_2 = trafo.transform(control_surface_cut_out)

        namedBox = CNamedShape(cut_out_1, "CutOut")
        cutter = CCutShape(wing_main[0], namedBox)
        cutted_wing_shape = cutter.named_shape()
        wing_loft.append(cutted_wing_shape)

        namedBox = CNamedShape(cut_out_2, "CutOut")
        cutter = CCutShape(wing_main[1], namedBox)
        cutted_wing_shape = cutter.named_shape()
        wing_loft.append(cutted_wing_shape)

    elif part == "elevator":
        control_surface = create_wing(aircraft, sweep=0, taper_ratio=1, wing_span=span,
                                      chord=chord, x=0, y=0, z=0, type=part)
        from tigl3.geometry import CNamedShape
        trafo = CTiglTransformation()
        trafo.add_translation(float(position_x), position_y, position_z - 0.3)
        traf = CTiglTransformation()
        traf.add_rotation_z(-sweep)
        box = BRepPrimAPI_MakeBox(chord, span, 10).Solid()
        moved_box = traf.transform(box)
        move_again = trafo.transform(moved_box)

        control_surface_cut_out = move_again
        tr = CTiglTransformation()
        tr.add_rotation_z(sweep)
        cs_object = control_surface.get_loft().shape()
        cs_n = traf.transform(cs_object)

        trafo = CTiglTransformation()

        trafo.add_translation(position_x,
                              position_y,
                              position_z)
        cs_wing = trafo.transform(cs_n)

        wing_1 = CNamedShape(cs_wing, "loft")
        lofts.append(wing_1)

        tr = CTiglTransformation()
        tr.add_mirroring_at_xzplane()

        wing_2 = CNamedShape(tr.transform(cs_wing), "loft")
        lofts.append(wing_2)

        cut_out_1 = control_surface_cut_out

        trafo = CTiglTransformation()
        trafo.add_mirroring_at_xzplane()
        cut_out_2 = trafo.transform(control_surface_cut_out)

        namedBox = CNamedShape(cut_out_1, "CutOut")
        cutter = CCutShape(wing_main[0], namedBox)
        cutted_wing_shape = cutter.named_shape()
        wing_loft.append(cutted_wing_shape)

        namedBox = CNamedShape(cut_out_2, "CutOut")
        cutter = CCutShape(wing_main[1], namedBox)
        cutted_wing_shape = cutter.named_shape()
        wing_loft.append(cutted_wing_shape)


    elif part=="rudder":
        control_surface = create_wing(aircraft, sweep=0, taper_ratio=1, wing_span=span,
                                      chord=chord, x=0, y=0, z=0, type=part)
        from tigl3.geometry import CNamedShape
        trafo = CTiglTransformation()
        trafo.add_translation(float(position_x), position_y, position_z - 0.3)
        traf = CTiglTransformation()
        traf.add_rotation_y(sweep)
        box = BRepPrimAPI_MakeBox(chord, span, 10).Solid()
        moved_box = traf.transform(box)
        move_again = trafo.transform(moved_box)

        control_surface_cut_out = move_again
        tr = CTiglTransformation()
        tr.add_rotation_z(sweep)
        cs_object = control_surface.get_loft().shape()
        cs_n = traf.transform(cs_object)

        trafo = CTiglTransformation()

        trafo.add_translation(position_x,
                              position_y,
                              position_z)
        cs_wing = trafo.transform(cs_n)

        wing_1 = CNamedShape(cs_wing, "loft")
        lofts.append(wing_1)



        cut_out_1 = control_surface_cut_out

        trafo = CTiglTransformation()
        trafo.add_mirroring_at_xzplane()
        cut_out_2 = trafo.transform(control_surface_cut_out)

        namedBox = CNamedShape(cut_out_1, "CutOut")
        cutter = CCutShape(wing_main[0], namedBox)
        cutted_wing_shape = cutter.named_shape()
        wing_loft.append(cutted_wing_shape)



    if update:
            show_lofts(display, lofts, prev_cs_loft, update)
            show_lofts(display, wing_loft, prev_wing_loft, update=False)
    else:
            show_lofts(display,lofts, prev_cs_loft, update)
            show_lofts(display, wing_loft, prev_wing_loft, update=True)
    lofts.extend(wing_loft)
    return lofts
