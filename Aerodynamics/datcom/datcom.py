from subprocess import Popen, PIPE

from Aerodynamics.datcom.input import build_datcom_input
from Aerodynamics.datcom.processor import process_output
from Utils.database import database
from Utils.database.database import datcom_output_file
from Utils.file_manager.file_manager_ import clean_up_after_datcom


def run_datcom():
    import matlab.engine
    import matlab
    build_datcom_input()
    location = database.datcom_exe
    p = Popen(location, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="UTF8", shell=True)
    command = database.datcom_input_file
    p.stdin.write(command)
    out, err = p.communicate()
    clean_up_after_datcom()
    eng = matlab.engine.start_matlab()
    value = eng.datcomimport(datcom_output_file, True)
    process_output(value=value)

