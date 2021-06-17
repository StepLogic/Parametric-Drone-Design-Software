import os

import tigl3.configuration
from tigl3 import tigl3wrapper
from tixi3 import tixi3wrapper
from Geometry.unconventional.lifting_surface.lifting_surface_model import lifting_surface_model
from Utils.database.database import resource_dir_cpacs

tixi_h = tixi3wrapper.Tixi3()
tigl_h = tigl3wrapper.Tigl3()

dir_path = os.path.dirname(os.path.realpath(__file__))
tixi_h.open(resource_dir_cpacs + "/temp.xml")
tigl_h.open(tixi_h, "")

mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()

config = mgr.get_configuration(tigl_h._handle.value)
print(lifting_surface_model(config,name="wim",design_type_="unconventional",surface_type_="wing").get_lower_surface())
