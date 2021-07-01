import multiprocessing as mp
import sys

import tigl3.configuration
import tigl3.tigl3wrapper
import tixi3.tixi3wrapper

from GUI.workflow import design_workflow, simulator_workflow
from GUI.workflow.main_workflow import work_flow_monitor
from Server.app import server
from Utils.data_objects.workflow_placeholders import shutdown_
from Utils.database.database import resource_dir_cpacs

sendTasks, receiveTasks = mp.Pipe()
sendLofts, receiveLofts = mp.Pipe()
e = mp.Event()
sim_event=mp.Event()


def start(e,sim_event, sendTasks, receiveLofts):
    filename = resource_dir_cpacs + "/empty.cpacs3.xml"
    tixi_h = tixi3.tixi3wrapper.Tixi3()
    tixi_h.open(filename)
    tigl_h = tigl3.tigl3wrapper.Tigl3()
    tigl_h.open(tixi_h, "")
    mgr = tigl3.configuration.CCPACSConfigurationManager_get_instance()
    config_value = mgr.get_configuration(tigl_h._handle.value)
    work_flow = work_flow_monitor(sys.argv)
    work_flow.config = config_value
    work_flow.events = e
    work_flow.sim_events=sim_event
    work_flow.sendTasks = sendTasks
    work_flow.receiveLofts = receiveLofts
    work_flow.execute_design_window()
    code = work_flow.exec_()
    if (code == 0):
        shutdown()
        e.set()
        sendTasks.send([shutdown_])
        sys.exit()


def shutdown():
    receiveTasks.close()
    receiveLofts.close()


if __name__ == '__main__':
   # server.run(host='0.0.0.0', debug=True, threaded=True)
    gui = mp.Process(target=start, args=(e,sim_event, sendTasks, receiveLofts))
    gui.start()
    design = mp.Process(target=design_workflow.start, args=(e, receiveTasks, sendLofts))
    design.start()

