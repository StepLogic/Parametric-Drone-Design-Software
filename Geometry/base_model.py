from Geometry.conventional.fuselage_model.fuselage_model import fuselage_model
from Geometry.conventional.h_stab_model.h_stab_model import h_stab_model
from Geometry.conventional.v_stab_model.v_stab_model import v_stab_model
from Geometry.conventional.wing_model.wing_model import wing_model
from Geometry.unconventional.boom.boom_model import boom_model
from Geometry.unconventional.lifting_surface.lifting_surface_model import lifting_surface_model
from Utils.data_objects.boom_placeholders import fuselage, boom
from Utils.data_objects.lifting_surface_placeholder import fin, wing, tailplane
from Utils.data_objects.placeholder import conventional_design, unconventional_design
from Utils.database.geometry.boom_database import get_boom_object_data, read_boom_objects
from Utils.database.geometry.lifting_database import get_surface_object_data, read_lifting_surface_objects


def update_surface_3D(workflow=None):
    surface_list = read_lifting_surface_objects()
    for l in surface_list:
        design_type_, surface_type_ = get_surface_object_data(l)
        generate_wing_3D(workflow, l, surface_type_, design_type_)


def generate_wing_3D(workflow=None, name="", surface_type_="", design_type_=""):
    print(name, workflow,surface_type_)
    if surface_type_ == fin and design_type_ == conventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=v_stab_model(workflow=workflow, name=name, surface_type_=surface_type_,
                                                         design_type_=design_type_).get_current_loft())
    elif surface_type_ == fin and design_type_ == unconventional_design:
        workflow.viewer.update_object(part_name=name, lofts=lifting_surface_model(config=workflow, name=name,
                                                                                  surface_type_=surface_type_,
                                                                                  design_type_=design_type_).get_current_loft())
    elif surface_type_ == wing and design_type_ == conventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=wing_model(config=workflow, name=name, surface_type_=surface_type_,
                                                       design_type_=design_type_).get_current_loft())
    elif surface_type_ == wing and design_type_ == unconventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=lifting_surface_model(config=workflow, name=name,
                                                                  surface_type_=surface_type_,
                                                                  design_type_=design_type_).get_current_loft())
    elif surface_type_ == tailplane and design_type_ == conventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=h_stab_model(config=workflow, name=name, surface_type_=surface_type_,
                                                         design_type_=design_type_).get_current_loft())
    elif surface_type_ == tailplane and design_type_ == unconventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=lifting_surface_model(config=workflow, name=name,
                                                                  surface_type_=surface_type_,
                                                                  design_type_=design_type_).get_current_loft())

def update_boom_3D(workflow=None):
    boom_list = read_boom_objects()
    for l in boom_list:
        design_type_, boom_type_ = get_boom_object_data(l)
        generate_boom_3D_model(workflow,name=l,boom_type_=boom_type_,design_type_=design_type_)
def generate_boom_3D_model(workflow=None, name="", boom_type_="", design_type_=""):
    print(name,workflow,)
    if boom_type_== fuselage and design_type_== unconventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=boom_model(config=workflow, text=name,
                                                       boom_type_=boom_type_,
                                                       design_type_=design_type_).get_current_loft())
    elif boom_type_== fuselage and design_type_== conventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=fuselage_model(workflow=workflow, text=name,
                                                                  boom_type_=boom_type_,
                                                                  design_type_=design_type_).get_current_loft())
    elif boom_type_== boom and design_type_== unconventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=boom_model(config=workflow, text=name,
                                                       boom_type_=boom_type_,
                                                       design_type_=design_type_).get_current_loft())
    elif boom_type_== boom and design_type_== conventional_design:
        workflow.viewer.update_object(part_name=name,
                                      lofts=fuselage_model(workflow=workflow, text=name,
                                                                  boom_type_=boom_type_,
                                                                  design_type_=design_type_).get_current_loft())

