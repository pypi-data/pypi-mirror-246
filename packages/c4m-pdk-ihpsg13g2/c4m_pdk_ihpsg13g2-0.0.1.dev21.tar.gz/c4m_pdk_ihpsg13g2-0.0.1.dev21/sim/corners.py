#!/bin/false
# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0


__all__ = ["corner_spec"]


_v_vdd_nom = 1.2
_v_iovdd_nom = 3.3
corner_spec = {
    "FAST": (1.1*_v_vdd_nom, 1.1*_v_iovdd_nom, -40.0, ("lvmos_ff", "hvmos_ff", "res_bcs", "dio")),
    "FAST_COMM": (1.1*_v_vdd_nom, 1.1*_v_iovdd_nom, 0.0, ("lvmos_ff", "hvmos_ff", "res_bcs", "dio")),
    "FAST_ROOM": (1.1*_v_vdd_nom, 1.1*_v_iovdd_nom, 25.0, ("lvmos_ff", "hvmos_ff", "res_bcs", "dio")),
    "NOM": (_v_vdd_nom, _v_iovdd_nom, 25, ("lvmos_tt", "hvmos_tt", "res_typ", "dio")),
    "SLOW": (0.9*_v_vdd_nom, 0.9*_v_iovdd_nom, 125.0, ("lvmos_ss", "hvmos_ss", "res_wcs", "dio")),
    "SLOW_COMM": (0.9*_v_vdd_nom, 0.9*_v_iovdd_nom, 70.0, ("lvmos_ss", "hvmos_ss", "res_wcs", "dio")),
    "SLOW_ROOM": (0.9*_v_vdd_nom, 0.9*_v_iovdd_nom, 25.0, ("lvmos_ss", "hvmos_ss", "res_wcs", "dio")),
}
