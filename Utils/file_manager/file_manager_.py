import os

from Utils.database.database import datcom_output_file


def clean_up_after_datcom():
    import shutil
    shutil.move("datcom.out", datcom_output_file)
    os.remove("for013.dat")
    os.remove("for014.dat")