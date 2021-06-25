from os import walk

from Helper import resource_path, absolute_path
from Utils.database.database import airfoil_path

_, _, filenames = next(walk(resource_path(absolute_path + "/Resources/airfoil/profiles")))
value = []
names = []


def cv(name, x, y):
    x_v = []
    z_v = []
    y_v = []
    if len(x) == len(y):
        names.append("{},".format(f.split(".")[0]))
        for x_, y_ in zip(x, y):
                x_v.append(f"{x_};")
                z_v.append(f"{y_};")
                y_v.append(f"{0.0};")

        x_v.reverse()
        z_v.reverse()
        x__ = "".join(x_v)
        z__ = "".join(z_v)
        y__ = "".join(y_v)
        return f"<wingAirfoil uID=\"{name}\"><name>{name}</name>" \
               f"<description>{name}</description>" \
               f"<pointList> " \
               f"<x mapType=\"vector\">{x__}</x>" \
               f"<y mapType=\"vector\">{y__}</y>" \
               f"<z mapType=\"vector\">{z__}</z>" \
               f"</pointList>" \
               f"</wingAirfoil>"

    else:
        print(name,len(x),len(y))

for f in filenames:
    if f.__contains__("naca"):
        x = []
        y = []
        with open(resource_path(absolute_path + "/Resources/airfoil/profiles/") + f"{f}") as p:
            for line in p.readlines():
                split_values = line.split(" ")
                count = 0
                for i in split_values:
                    try:
                        if float(i)>1.0:
                            pass
                        else:
                            if count == 0:
                                x.append(float(i))
                                count = 1
                            else:
                                y.append(float(i))
                    except:
                        pass

















            value.append(cv(f.split(".")[0], x, y))

for i in value:
    if i is not None:
        print("\n", i)
with open('names.txt', 'w') as f:
    f.write('readme')
a_file = open(resource_path(absolute_path + "/Resources") + "/airfoil/export/names.txt", "w")
a_file.writelines("".join(names))
a_file.close()
