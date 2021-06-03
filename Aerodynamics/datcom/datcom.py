from subprocess import Popen, PIPE

from Aerodynamics.datcom.input import build_datcom_input
from Aerodynamics.datcom.processor_1 import process_output

from Utils.database import database
from Utils.database.database import datcom_output_file
from Utils.file_manager.file_manager_ import clean_up_after_datcom

def run_datcom():
    location = database.datcom_exe
    p = Popen(location, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="UTF8", shell=True)
    command = database.datcom_input_file
    p.stdin.write(command)
    out, err = p.communicate()
    clean_up_after_datcom()
    process_output()

