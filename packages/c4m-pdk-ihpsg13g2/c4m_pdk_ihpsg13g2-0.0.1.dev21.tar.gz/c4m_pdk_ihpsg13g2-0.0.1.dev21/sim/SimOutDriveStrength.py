#!/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
import sys
from textwrap import dedent
import numpy as np

from c4m import flexio as _io
from c4m.pdk.ihpsg13g2 import pyspicefab, ihpsg13g2_iofab as iofab

from corners import corner_spec

# Determine the order of the corner simulation and output to file
corners = ("NOM", "FAST", "FAST_COMM", "FAST_ROOM", "SLOW", "SLOW_COMM", "SLOW_ROOM")

iospec = iofab.spec
strengths = iospec.clampdrive
assert isinstance(strengths, dict)
cells = (
    *(iofab.out(drivestrength=s) for s in strengths.keys()),
    *(iofab.triout(drivestrength=s) for s in strengths.keys()),
    *(iofab.inout(drivestrength=s) for s in strengths.keys()),
)


with open("SimOutDriveStrength.out", "w") as f:
    f.write(dedent(f"""
        Simulated drive strength of output IO cells.  
        Simulates the sink and source current of the cell when the pad is
        driven to opposite voltage.
    """[1:]))

    for corner in corners:
        print(corner, file=sys.stderr)
        v_vdd, v_iovdd, temp, tc = corner_spec[corner]
        s_tc = ", ".join(tc)
        f.write(dedent(f"""
            # {corner} corner
            
            * Vdd: {v_vdd:.2f}V
            * IO Vdd: {v_iovdd:.2f}V
            * Temperature: {temp:.1f}℃
            * process: {s_tc}

            \t\tSink [mA]\tSource [mA]
        """))

        for cell in cells:
            print("*", cell.name)
            ckt = cell.circuit
            tb = pyspicefab.new_pyspicecircuit(corner=tc, top=ckt)

            tb.V("vss", "vss", tb.gnd, 0.0)
            tb.V("vdd", "vdd", tb.gnd, v_vdd)
            tb.V("iovss", "iovss", tb.gnd, 0.0)
            tb.V("iovdd", "iovdd", tb.gnd, v_iovdd)

            tb.PieceWiseLinearVoltageSource("c2p", "c2p", "vss", dc=0.0, values=(
                (0.0, 0.0),
                (1e-3, 0.0),
                (1.1e-3, v_vdd),
            ))
            if isinstance(cell, (_io.PadTriOutT, _io.PadInOutT)):
                tb.V("c2p_en", "c2p_en", "vss", v_vdd)
            if isinstance(cell, _io.PadInOutT):
                tb.C("p2c", "p2c", "vss", 10e-15)
            tb.PieceWiseLinearVoltageSource("pad", "pad", "iovss", dc=0.0, values=(
                (0.0, 0.0),
                (0.1e-3, v_iovdd),
                (1.0e-3, v_iovdd),
                (1.1e-3, 0.0),
            ))

            sim = tb.simulator(temperature=temp, gmin=1e-9)

            if (corner == "SLOW_COMM") and (cell.name == "IOPadOut4mA"):
                with open(f"SimOutDriveStrength_{corner}.spi", "w") as f2:
                    f2.write(str(sim))

            try:
                trans = sim.transient(step_time=0.1e-3, end_time=2e-3)
            except:
                sink = np.nan
                source = np.nan
            else:
                time = np.array(trans.time)
                i_pad = np.array(trans.vpad)

                sink = -np.interp(0.5e-3, time, i_pad)
                source = np.interp(1.5e-3, time, i_pad)
            print(f"{cell.name}\t{1e3*sink:.2f}\t\t{1e3*source:.2f}", file=f)
