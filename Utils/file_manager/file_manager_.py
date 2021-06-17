import os

from Utils.database.database import datcom_output_file, model_dir


def clean_up_after_datcom():
    import shutil
    shutil.move("datcom.out", datcom_output_file)
    os.remove("for013.dat")
    os.remove("for014.dat")
def clean_after_moveables(filename):
    import shutil
    shutil.move(f"{filename}.obj", f"{model_dir}/moveables/{filename}.obj")
    os.remove(f"{filename}.stl")
def clean_after_body(filename):
    import shutil
    shutil.move(f"{filename}.obj", f"{model_dir}/body/{filename}.obj")
    os.remove(f"{filename}.stl")
