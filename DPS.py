from gui.cad_module.gui_module.CAD import CAD
import Helper
import tigl3.tigl3wrapper
import tixi3.tixi3wrapper
if __name__ == '__main__':
      filename = Helper.resource_path(Helper.absolute_path + "/resources/empty.cpacs3.xml")
      tixi_h = tixi3.tixi3wrapper.Tixi3()
      tixi_h.open(filename)
      tigl_h = tigl3.tigl3wrapper.Tigl3()
      tigl_h.open(tixi_h, "")
      mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()
      aircraft = mgr.get_configuration(tigl_h._handle.value)
      CAD(aircraft).run()