import random

import tigl3
import tigl3.surface_factories
from OCC.Approx import Approx_Curve3d
from OCC.BRepAdaptor import BRepAdaptor_CompCurve, BRepAdaptor_HCompCurve, Handle_BRepAdaptor_HCompCurve
from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCC.GeomAbs import GeomAbs_C2
from OCC.TopoDS import topods

from Utils.database.geometry.lifting_database import read_surface_data


class lifting_surface_model:
    def __init__(self, config=None, name="", surface_type_="", design_type_=""):
        print(name)
        super().__init__()
        self._name = name
        self.surface_type_=surface_type_
        self.design_type_=design_type_
        self.airfoil_type = "NACA0012"
        self.current_loft = None
        self.name_ = name
        self.aircraft = config
        self.wings = self.aircraft.get_wings()
        self.old_profile = ""
        self.lifting_surface = None

        self.root_le_pos_x_ = 0
        self.root_le_pos_y_ = 0
        self.root_le_pos_z_ = 0
        self.rot_x_ = 0
        self.rot_y_ = 0
        self.rot_z_ = 0

        self.section_1_chord_ = 0
        self.section_1_x_ = 0
        self.section_1_y_ = 0
        self.section_1_z_ = 0
        self.section_1_twist_angle_ = 0

        self.section_2_chord_ = 0
        self.section_2_x_ = 0
        self.section_2_y_ = 0
        self.section_2_z_ = 0
        self.section_2_twist_angle_ = 0

        self.section_3_chord_ = 0
        self.section_3_x_ = 0
        self.section_3_y_ = 0
        self.section_3_z_ = 0
        self.section_3_twist_angle_ = 0

        self.section_4_chord_ = 0
        self.section_4_x_ = 0
        self.section_4_y_ = 0
        self.section_4_z_ = 0
        self.section_4_twist_angle_ = 0

        self.section_5_chord_ = 0
        self.section_5_x_ = 0
        self.section_5_y_ = 0
        self.section_5_z_ = 0
        self.section_5_twist_angle_ = 0

    def get_airfoil_notation(self):
        pass

    def read_parameters(self):
        try:
            self.airfoil_type,self.surfaceType_,self.xz_mirror_,self.xy_mirror_,self.yz_mirror_ ,self.rot_x_, self.rot_y_, self.rot_z_, self.root_le_pos_x_, self.root_le_pos_y_, self.root_le_pos_z_, \
            self.section_1_x_, self.section_2_x_, self.section_3_x_, self.section_4_x_, self.section_5_x_, \
            self.section_1_y_, self.section_2_y_, self.section_3_y_, self.section_4_y_, self.section_5_y_, \
            self.section_1_z_, self.section_2_z_, self.section_3_z_, self.section_4_z_, self.section_5_z_, \
            self.section_1_chord_, self.section_2_chord_, self.section_3_chord_, self.section_4_chord_, \
            self.section_5_chord_, self.section_1_twist_angle_, self.section_2_twist_angle_, \
            self.section_3_twist_angle_, self.section_4_twist_angle_, self.section_5_twist_angle_ = read_surface_data(self._name)
        except(Exception):
            self.airfoil_type = "NACA0012"

    def get_current_loft(self):
        self.read_parameters()
        if self.surfaceType_:
            return self.curved_surface()
        else:
            return self.straight_surface()



    def straight_surface(self):


        n = random.random()
        self.lifting_surface = self.wings.create_wing(f"{n}", 5, "NACA0012")

        chords = [self.section_1_chord_, self.section_2_chord_, self.section_3_chord_, self.section_4_chord_,
                  self.section_5_chord_]
        y = [self.section_1_y_, self.section_2_y_, self.section_3_y_, self.section_4_y_, self.section_5_y_]
        x = [self.section_1_x_, self.section_2_x_, self.section_3_x_, self.section_4_x_, self.section_5_x_]
        z = [self.section_1_z_, self.section_2_z_, self.section_3_z_, self.section_4_z_, self.section_5_z_]
        twist = [self.section_1_twist_angle_, self.section_2_twist_angle_, self.section_3_twist_angle_,
                 self.section_4_twist_angle_, self.section_5_twist_angle_]

        profile = self.airfoil_type
        constant = 0.0
        nacanumber = profile.split("NACA")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01
        # decrease section size towards wing tips
        print()
        wires=[]
        curves=[]
        n_sections = self.lifting_surface.get_section_count()
        print(n_sections)
        for idx in range(1, n_sections + 1):
            s = self.lifting_surface.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            ce.set_width(chords[idx - 1])
            ce.set_height(chords[idx - 1] * constant)
            center = ce.get_center()

            center.x = x[idx - 1]
            center.y = y[idx - 1]
            center.z =z[idx - 1]
            ce.set_center(center)

        # create winglet
        self.lifting_surface.set_rotation(tigl3.geometry.CTiglPoint(self.rot_x_, self.rot_y_, self.rot_z_))
        self.lifting_surface.set_root_leposition(tigl3.geometry.CTiglPoint(self.root_le_pos_x_
                                                                           , self.root_le_pos_y_
                                                                   , self.root_le_pos_z_))
        print("vstab", self.root_le_pos_y_)
        loft = []
        loft.append(self.lifting_surface.get_loft().shape())
        if self.xy_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xyplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif self.xz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif self.yz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_yzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        self.old_profile = self.airfoil_type

        print(loft)
        return loft


    def curved_surface(self):
        self.read_parameters()
        n = random.random()
        self.lifting_surface = self.wings.create_wing(f"{n}", 5, self.airfoil_type)
        print(self.name_,(self.root_le_pos_x_,self.root_le_pos_y_, self.root_le_pos_z_))


        chords = [self.section_1_chord_, self.section_2_chord_, self.section_3_chord_, self.section_4_chord_,
                  self.section_5_chord_]
        y = [self.section_1_y_, self.section_2_y_, self.section_3_y_, self.section_4_y_, self.section_5_y_]
        x = [self.section_1_x_, self.section_2_x_, self.section_3_x_, self.section_4_x_, self.section_5_x_]
        z = [self.section_1_z_, self.section_2_z_, self.section_3_z_, self.section_4_z_, self.section_5_z_]
        twist = [self.section_1_twist_angle_, self.section_2_twist_angle_, self.section_3_twist_angle_,
                 self.section_4_twist_angle_, self.section_5_twist_angle_]

        profile =self.airfoil_type
        constant = 0.5
        nacanumber = profile.split("naca")[1]
        if nacanumber.isdigit():
            if len(nacanumber) == 4:
                constant = int(nacanumber[2:]) * 0.01
        # decrease section size towards wing tips
        print()
        wires=[]
        curves=[]
        print(constant)
        n_sections = self.lifting_surface.get_section_count()
        print(n_sections)
        for idx in range(1, n_sections + 1):
            s = self.lifting_surface.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            ce.set_width(chords[idx - 1])
            ce.set_height(chords[idx - 1] * constant)
            center = ce.get_center()

            center.x = x[idx - 1]
            center.y = y[idx - 1]
            center.z =z[idx - 1]
            ce.set_center(center)

        self.lifting_surface.set_rotation(tigl3.geometry.CTiglPoint(self.rot_x_, self.rot_y_, self.rot_z_))
        self.lifting_surface.set_root_leposition(tigl3.geometry.CTiglPoint(self.root_le_pos_x_
                                                                           , self.root_le_pos_y_
                                                                           , self.root_le_pos_z_))
        for idx in range(1, n_sections + 1):
            s = self.lifting_surface.get_section(idx)
            e = s.get_section_element(1)
            ce = e.get_ctigl_section_element()
            wires.append(ce.get_wire())


        for l in wires:
            adapt=BRepAdaptor_CompCurve(l)
            curve = Handle_BRepAdaptor_HCompCurve(BRepAdaptor_HCompCurve(adapt))
            approx=Approx_Curve3d(curve, 0.001, GeomAbs_C2, 200, 12)
            if (approx.IsDone() and approx.HasResult()):
                        curves.append(approx.Curve())

        surface = tigl3.surface_factories.interpolate_curves(curves)
        sew = BRepBuilderAPI_Sewing()
        face1=BRepBuilderAPI_MakeFace(surface, 1e-6).Face()
        face2=BRepBuilderAPI_MakeFace(surface, 1e-6).Face()
        sew.Add(face1)
        sew.Add(face2)
        sew.Perform()
        shape = sew.SewedShape()

        tds = topods()
        model = BRepBuilderAPI_MakeSolid()
        model.Add(tds.Shell(shape))
        solid = model.Solid()
        loft = []
        loft.append(solid)
        if self.xy_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xyplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif self.xz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_xzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        elif self.yz_mirror_:
            trafo = tigl3.geometry.CTiglTransformation()
            trafo.add_mirroring_at_yzplane()
            loft.append(tigl3.geometry.CNamedShape(trafo.transform(loft[0]), "cut").shape())
        self.old_profile = self.airfoil_type
        return loft