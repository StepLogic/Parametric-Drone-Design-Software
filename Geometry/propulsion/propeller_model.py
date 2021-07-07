import random
from copy import deepcopy

import numpy as np
import tigl3.configuration
import tigl3.geometry
import tigl3.surface_factories
import tigl3.tigl3wrapper
from OCC.Approx import Approx_Curve3d
from OCC.BRep import BRep_Builder
from OCC.BRepAdaptor import BRepAdaptor_CompCurve, BRepAdaptor_HCompCurve, Handle_BRepAdaptor_HCompCurve
from OCC.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeSolid, BRepBuilderAPI_Sewing
from OCC.GeomAbs import GeomAbs_C2
from OCC.TopoDS import topods, TopoDS_Compound
from Utils.database.propulsion.propulsion_database import read_propeller_parameters
from Utils.maths.math_library import getArea


class propeller_model():
    def __init__(self, name="", config=None):
        self.config = config
        self.name = name

    def get_current_loft(self):
        wires = []
        curves = []
        propeller_number_, xz_mirror_, xy_mirror_, yz_mirror_ \
            , rot_x_, hub_length, pitch_angle, root_le_pos_x_, \
        root_le_pos_y_, root_le_pos_z_, section_1_length_, section_2_length_, \
        section_3_length_, section_4_length_, section_5_length_, section_1_profile_, \
        section_2_profile_, section_3_profile_, section_4_profile_, section_5_profile_, \
        section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_ \
            , section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_, \
        section_5_chord_, section_1_pitch_angle_, section_2_pitch_angle_, \
        section_3_pitch_angle_, section_4_pitch_angle_, section_5_pitch_angle_ = read_propeller_parameters(
            name=self.name)
        interval = 5

        chords = [section_1_chord_, section_1_chord_, section_2_chord_, section_3_chord_, section_4_chord_,
                  section_5_chord_, 0.001]
        profile = [section_1_profile_, section_1_profile_, section_2_profile_, section_3_profile_, section_4_profile_,
                   section_5_profile_, section_5_profile_]
        length = [0, section_1_length_, section_2_length_, section_3_length_, section_4_length_, section_5_length_ / 2,
                  section_5_length_ / 2]
        z = [section_1_z_, section_1_z_, section_2_z_, section_3_z_, section_4_z_, section_5_z_, section_5_z_]
        pitch = [0, section_1_pitch_angle_, section_2_pitch_angle_, section_3_pitch_angle_,
                 section_4_pitch_angle_, section_5_pitch_angle_, section_5_pitch_angle_]

        n = random.random()
        lifting_surface = self.config.get_wings().create_wing(f"{n}", len(chords), f"naca4412")

        sections = [-hub_length / 2,
                    0.1 * hub_length,
                    hub_length / 2]

        radius = [
            0.00,
            rot_x_ / 2,
            rot_x_ / 2,

        ]

        x_ = []
        x_.extend(np.linspace(sections[0], sections[1], num=interval))
        x_.append(0.9 * hub_length)

        radii = []
        radii.extend(np.linspace(radius[0], radius[1], num=interval))
        radii.append((rot_x_ / 2))

        print(x_, radii)

        n = random.random()
        hub = self.config.get_fuselages().create_fuselage(f"hub{n}", len(x_), "circularProfile")
        for (x, rad, index) in zip(x_, radii, range(1, len(x_) + 1)):
            section = hub.get_section(index)
            sectionElement = section.get_section_element(1)
            sectionElementCenter = sectionElement.get_ctigl_section_element()
            sectionElementCenter.set_center(tigl3.geometry.CTiglPoint(x
                                                                      , 0
                                                                      , 0))
            sectionElementCenter.set_area(getArea(rad))

        n_sections = lifting_surface.get_section_count()
        lifting_surface.set_root_leposition(tigl3.geometry.CTiglPoint(-chords[0] / 2, 0, 0))
        print(n_sections)
        y = 0.0
        x = hub_length / 2
        for (z_, chord, length_, pitch_, profile_, idx) in zip(z, chords, length, pitch, profile,
                                                               range(1, n_sections + 1)):
            profile__ = "naca" + profile_
            constant = 0.0
            nacanumber = profile__.split("naca")[1]
            if nacanumber.isdigit():
                if len(nacanumber) == 4:
                    constant = int(nacanumber[2:]) * 0.01
            s = lifting_surface.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            ce.set_width(chord)
            ce.set_height(chord * constant)
            center = ce.get_center()
            y += length_
            center.x = x
            center.y = y
            center.z = 0.0
            ce.set_center(center)
            ce.set_profile_uid(f"{profile_}")
            e.set_rotation(tigl3.geometry.CTiglPoint(0, pitch_, 0))
        lifting_surface.set_rotation(tigl3.geometry.CTiglPoint(0, pitch_angle, 0))
        for idx in range(1, n_sections + 1):
            s = lifting_surface.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            wires.append(ce.get_wire())
        for l in wires:
            adapt = BRepAdaptor_CompCurve(l)
            curve = Handle_BRepAdaptor_HCompCurve(BRepAdaptor_HCompCurve(adapt))
            approx = Approx_Curve3d(curve, 0.001, GeomAbs_C2, 200, 12)
            if (approx.IsDone() and approx.HasResult()):
                curves.append(approx.Curve())

        surface1 = tigl3.surface_factories.interpolate_curves(curves)
        face1 = BRepBuilderAPI_MakeFace(surface1, 1e-6).Face()
        face2 = BRepBuilderAPI_MakeFace(surface1, 1e-6).Face()

        sew = BRepBuilderAPI_Sewing()
        sew.Add(face1)
        sew.Add(face2)
        sew.Perform()
        shape = sew.SewedShape()
        print(shape)

        tds = topods()
        model = BRepBuilderAPI_MakeSolid()
        model.Add(tds.Shell(shape))
        solid = model.Solid()
        print(solid)

        rot_trafo = tigl3.geometry.CTiglTransformation()
        rot_trafo.add_rotation_x(90)

        loft = []
        loft.append(hub.get_loft().shape())
        loft.append(
            tigl3.geometry.CNamedShape(rot_trafo.transform(solid), "cut").shape())

        if propeller_number_ == 2:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[1]), "cut").shape())
        elif propeller_number_ >= 3:
            delta = 360 / propeller_number_
            for i in range(1, propeller_number_ + 1):
                loft_copy = deepcopy(loft[1])
                trafo = tigl3.geometry.CTiglTransformation()
                trafo.add_rotation_x(delta * i)
                print(delta * i)
                loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft_copy), "cut").shape())
        builder = BRep_Builder()
        assembly = TopoDS_Compound()
        builder.MakeCompound(assembly)
        for l in loft:
            builder.Add(assembly, l)
        trafo = tigl3.geometry.CTiglTransformation()
        trafo.add_translation(root_le_pos_x_, root_le_pos_y_, root_le_pos_z_)
        assembly = trafo.transform(assembly)

        return [assembly]
