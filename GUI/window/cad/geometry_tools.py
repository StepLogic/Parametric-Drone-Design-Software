import tigl3.geometry

from GUI.window.cad.airconics_tools import boolean_cut


def cut_wing(shapeToCutFrom, cuttingShape):
    from tigl3.boolean_ops import CCutShape
    # cut the box from the wing
    cutter = CCutShape(tigl3.geometry.CNamedShape(shapeToCutFrom,"cut"), tigl3.geometry.CNamedShape(cuttingShape,"cut"))
    cutted_wing_shape = cutter.named_shape()

    return cutted_wing_shape.shape()
