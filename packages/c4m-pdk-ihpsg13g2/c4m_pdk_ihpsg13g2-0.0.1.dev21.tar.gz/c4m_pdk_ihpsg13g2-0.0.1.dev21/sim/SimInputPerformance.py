#!/bin/env python
# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
import numpy as np
from matplotlib import pyplot as plt

from c4m.pdk.ihpsg13g2 import pyspicefab, iolib

from corners import corner_spec
# v_vdd, v_iovdd, temp, tc = corner_spec["SLOW"]
corner = "SLOW_ROOM"
v_vdd, v_iovdd, temp, tc = corner_spec[corner]

freqs = (10e6, 50e6, 100e6, 200e6)
n_freqs = len(freqs)

ckt = iolib.cells["IOPadIn"].circuit

fig = plt.figure(figsize=(20,30))
for i, freq in enumerate(freqs):
    print(freq/1e6)
    period = 1/freq
    for i2, t_trans in enumerate((0.1*period, 0.2*period)):
        tb = pyspicefab.new_pyspicecircuit(corner=tc, top=ckt)

        tb.V("vss", "vss", tb.gnd, 0.0)
        tb.V("vdd", "vdd", tb.gnd, v_vdd)
        tb.V("iovss", "iovss", tb.gnd, 0.0)
        tb.V("iovdd", "iovdd", tb.gnd, v_iovdd)

        tb.C("p2c", "p2c", "vss", 10e-15)
        tb.PulseVoltageSource(
            "pad", "pad", "iovss",
            delay_time=0.25*period, period=period, pulse_width=(0.5*period - t_trans),
            rise_time=t_trans, fall_time=t_trans, initial_value=0.0, pulsed_value=v_iovdd,
        )

        sim = tb.simulator(temperature=temp, abstol=1e-9)

        plt.subplot(n_freqs, 2, 2*i + i2 + 1)
        trans = None
        try:
            trans = sim.transient(step_time=t_trans/10, end_time=3.5*period)
        except:
            try:
                trans = sim.transient(step_time=t_trans/5, end_time=3.5*period)
            except:
                pass
        if trans is not None:
            time = 1e9*np.array(trans.time)
            pad = np.array(trans.pad)
            p2c = np.array(trans.p2c)

            plt.plot(time, pad, label="pad")
            plt.plot(time, p2c, label="p2c")
            plt.title(f"f={round(freq/1e6)}MHz, t_trans=20% of period={t_trans*1e9}ns")
            plt.xlabel("time [ns]")
            plt.ylabel("voltage [V]")
    plt.legend()
# plt.show()
fig.text(
    x=0.22, y=0.90, s=f"{corner} corner: Vdd={v_vdd:.2f}V, IOVdd={v_iovdd:.2f}V, temp={temp}℃, process={tc}",
    size=15,
)
fig.savefig("SimInputPerformance.png")
fig.savefig("SimInputPerformance.svg")
