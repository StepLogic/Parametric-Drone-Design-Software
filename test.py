from Utils.database import database
from parse import DatcomParser

parser = DatcomParser(database.datcom_output_file)
dict = parser.get_common()
print(dict)