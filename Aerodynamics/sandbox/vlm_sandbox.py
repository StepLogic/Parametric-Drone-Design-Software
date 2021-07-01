from aerosandbox_legacy_v0 import *

from Aerodynamics.sandbox.input import create_aircraft
from Utils.maths.math_library import check_if_nan


def start_vlm(airplane):
    ap = vlm3(
        airplane=airplane,
        op_point=OperatingPoint(
            velocity=10,
            alpha=5,
            beta=0,
            p=0,
            q=0,
            r=0,
        ),
    )
    ap.run()

    return {"type": "VLM", "CL": ap.CL, "CD": ap.CDi, "CY": ap.CY, "Cl": ap.Cl, "Cm": ap.Cm,
            "Cn": ap.Cn}


def f_alpha_vlm(x, velocity, airplane):
    ap = vlm3(
        airplane=airplane,
        op_point=OperatingPoint(
            velocity=velocity,
            alpha=x,
            beta=0,
            p=0,
            q=0,
            r=0,
        ),
    )
    ap.run()

    return {"CL": check_if_nan(ap.CL), "CD": check_if_nan(ap.CDi), "CY": check_if_nan(ap.Cl),
            "Cm": check_if_nan(ap.Cm),
            "Cn": check_if_nan(ap.Cn)}


def f_beta_vlm(x, velocity, airplane):
    ap = vlm3(
        airplane=airplane,
        op_point=OperatingPoint(
            velocity=velocity,
            alpha=0,
            beta=x,
            p=0,
            q=0,
            r=0,
        ),
    )
    ap.run()

    return {"CL": check_if_nan(ap.CL), "CD": check_if_nan(ap.CDi), "CY": check_if_nan(ap.Cl),
            "Cm": check_if_nan(ap.Cm),
            "Cn": check_if_nan(ap.Cn)}


def f_p_vlm(x, velocity, airplane):
    ap = vlm3(
        airplane=airplane,
        op_point=OperatingPoint(
            velocity=velocity,
            alpha=0,
            beta=0,
            p=x,
            q=0,
            r=0,
        ),
    )
    ap.run()

    return {"CL": check_if_nan(ap.CL), "CD": check_if_nan(ap.CDi), "CY": check_if_nan(ap.Cl),
            "Cm": check_if_nan(ap.Cm),
            "Cn": check_if_nan(ap.Cn)}


def f_q_vlm(x, velocity, airplane):
    ap = vlm3(
        airplane=airplane,
        op_point=OperatingPoint(
            velocity=velocity,
            alpha=0,
            beta=0,
            p=0,
            q=x,
            r=0,
        ),
    )
    ap.run()

    return {"CL": check_if_nan(ap.CL), "CD": check_if_nan(ap.CDi), "CY": check_if_nan(ap.Cl),
            "Cm": check_if_nan(ap.Cm),
            "Cn": check_if_nan(ap.Cn)}


def f_r_vlm(x, velocity, airplane):
    ap = vlm3(
        airplane=airplane,
        op_point=OperatingPoint(
            velocity=velocity,
            alpha=0,
            beta=0,
            p=0,
            q=0,
            r=x,
        ),
    )
    ap.run()

    return {"CL": check_if_nan(ap.CL), "CD": check_if_nan(ap.CDi), "CY": check_if_nan(ap.Cl),
            "Cm": check_if_nan(ap.Cm),
            "Cn": check_if_nan(ap.Cn)}
