# SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
from typing import Callable, Optional, cast

from pdkmaster.technology import property_ as _prp, geometry as _geo, primitive as _prm
from pdkmaster.design import circuit as _ckt, layout as _lay, library as _lbry
from pdkmaster.io.klayout import merge

from c4m.flexio import (
    DCDiodeT, IOSpecification, TrackSpecification, IOFrameSpecification,
    GuardRingT, IOFactory
)

from .pdkmaster import tech, cktfab, layoutfab
from .stdcell import stdcell1v2lambdalib

__all__ = [
    "ihpsg13g2_iospec", "ihpsg13g2_ioframespec", "IHPSG13g2IOFactory",
    "ihpsg13g2_iofab", "iolib",
]


_prims = tech.primitives

_cell_width = 80.0
_cell_height = 180.0
ihpsg13g2_iospec = IOSpecification(
    stdcelllib=stdcell1v2lambdalib,
    nmos=cast(_prm.MOSFET, _prims.sg13g2_lv_nmos), pmos=cast(_prm.MOSFET, _prims.sg13g2_lv_pmos),
    ionmos=cast(_prm.MOSFET, _prims.sg13g2_hv_nmos),
    iopmos=cast(_prm.MOSFET, _prims.sg13g2_hv_pmos),
    monocell_width=_cell_width, 
    metal_bigspace=0.6, topmetal_bigspace=4.0,
    clampnmos=None, clampnmos_w=4.4, clampnmos_l=0.6, clampnmos_rows=1,
    clamppmos=None, clamppmos_w=6.66, clamppmos_l=0.6, clamppmos_rows=2,
    clampfingers=0, clampfingers_analog=20, clampdrive={
        "4mA": 2, "8mA": 4, "12mA": 6, "16mA": 8, "20mA": 10,
        "24mA": 12, "30mA": 15,
    },
    rcclampdrive=43, rcclamp_rows=4,
    clampgate_gatecont_space=0.14, clampgate_sourcecont_space=0.24,
    clampgate_draincont_space=0.51,
    add_clampsourcetap=False,
    clampsource_cont_tap_enclosure=_prp.Enclosure((0.265, 0.06)), clampsource_cont_tap_space=0.075,
    clampdrain_layer=None, clampgate_clampdrain_overlap=None, clampdrain_active_ext=None,
    clampdrain_gatecont_space=None, clampdrain_contcolumns=1, clampdrain_via1columns=2,
    nres=cast(_prm.Resistor, _prims.Rppd),
    pres=cast(_prm.Resistor, _prims.Rppd),
    ndiode=cast(_prm.Diode, _prims.ndiode),
    pdiode=cast(_prm.Diode, _prims.pdiode),
    secondres_width=1.0, secondres_length=2.0,
    secondres_active_space=0.6,
    corerow_height=10, corerow_nwell_height=6,
    iorow_height=8.5, iorow_nwell_height=5.25,
    nwell_minspace=2.0, levelup_core_space=1.0,
    resvdd_prim=cast(_prm.Resistor, _prims.Rppd), resvdd_meander=False,
    resvdd_w=1.0, resvdd_lfinger=20.0, resvdd_fingers=26, resvdd_space=0.65,
    invvdd_n_mosfet=cast(_prm.MOSFET, _prims.sg13g2_hv_nmos),
    invvdd_n_l=0.5, invvdd_n_w=9.0, invvdd_n_fingers=6, invvdd_n_rows=2,
    invvdd_p_mosfet=cast(_prm.MOSFET, _prims.sg13g2_hv_pmos),
    invvdd_p_l=0.5, invvdd_p_w=7.0, invvdd_p_fingers=50,
    capvdd_l=9.5, capvdd_w=9.0, capvdd_fingers=7, capvdd_rows=2,
    rcmosfet_row_minspace=0.25,
    add_corem3pins=True, corem3pin_minlength=1.5,
    add_dcdiodes=True,
    dcdiode_actwidth=1.26, dcdiode_actspace=0.99, dcdiode_actspace_end=1.38,
    dcdiode_inneractheight=27.78, dcdiode_diodeguard_space=1.32, dcdiode_fingers=2,
    dcdiode_impant_enclosure=0.42, dcdiode_indicator=_prims["Recog.esd"],
    iovss_ptap_extra=_prims["Substrate"],
)
ihpsg13g2_ioframespec = IOFrameSpecification(
    cell_height=_cell_height,
    tracksegment_viapitch=2.0, trackconn_viaspace=0.3, trackconn_chspace=0.2,
    pad_height=None,
    padpin_height=3.0,
    pad_width=70.0,
    pad_viapitch=None,
    pad_viacorner_distance=23.0, pad_viametal_enclosure=3.0,
    pad_y=55.32,
    tracksegment_maxpitch=30.0, tracksegment_space={
        None: 2.0,
        cast(_prm.MetalWire, _prims.TopMetal2): 5.0,
    },
    acttracksegment_maxpitch=30, acttracksegment_space=1.0,
    track_specs=(
        TrackSpecification(name="iovss", bottom=6.0, width=55.0),
        TrackSpecification(name="iovdd", bottom=65.0, width=55.0),
        TrackSpecification(name="secondiovss", bottom=125.0, width=10.0),
        TrackSpecification(name="vddvss", bottom=(_cell_height - 41.0), width=40.0),
    ),
)
class IHPSG13g2IOFactory(IOFactory):
    iospec = ihpsg13g2_iospec
    ioframespec = ihpsg13g2_ioframespec

    def __init__(self, *,
        lib: _lbry.Library, cktfab: _ckt.CircuitFactory, layoutfab: _lay.LayoutFactory,
    ):
        super().__init__(
            lib=lib, cktfab=cktfab, layoutfab=layoutfab,
            spec=self.iospec, framespec=self.ioframespec,
        )

    def guardring(self, *,
        type_: str, width: float, height: float, fill_well: bool = False, fill_implant: bool = False,
        create_cb: Optional[Callable[[GuardRingT], None]]=None,
    ):
        # For p-type guard ring put substrate label for IHP process
        def guardring_create(gr: GuardRingT) -> None:
            if gr.type_ == "p":
                p = _geo.Point(
                    x=(-0.5*gr.width + 0.5*gr.ringwidth), y=(-0.5*gr.height + 0.5*gr.ringwidth)
                )
                lbl = _geo.Label(origin=p, text="sub!")
                gr.layout.add_shape(
                    shape=lbl, layer=cast(_prm.Auxiliary, _prims["TEXT"]), net=None,
                )
            if create_cb:
                create_cb(gr)

        return super().guardring(
            type_=type_, width=width, height=height, fill_well=fill_well,
            fill_implant=fill_implant, create_cb=guardring_create,
        )

    def dcdiode(self, *,
        type_: str, create_cb: Optional[Callable[[DCDiodeT], None]]=None,
    ) -> DCDiodeT:
        # Add diode label and for p-type outer ring put substrate label for IHP process
        def dcdiode_create(dio: DCDiodeT) -> None:
            TEXT = cast(_prm.Auxiliary, _prims["TEXT"])
            if dio.type_ == "n":
                p = _geo.Point(x=0.5*dio.active_width, y=0.5*dio.active_width)
                lbl = _geo.Label(origin=p, text="sub!")
                dio.layout.add_shape(
                    shape=lbl, layer=TEXT, net=None,
                )
                dio_lbl = "diodevss_4kv"
            else:
                assert dio.type_ == "p"
                dio_lbl = "diodevdd_4kv"
            p = _geo.Point(x=0.5*dio.innerwidth, y=0.5*dio.outerheight)
            lbl = _geo.Label(origin=p, text=dio_lbl)
            dio.layout.add_shape(
                shape=lbl, layer=TEXT, net=None,
            )
            if create_cb:
                create_cb(dio)

        return super().dcdiode(type_=type_, create_cb=dcdiode_create)
iolib = _lbry.Library(name="IOLib", tech=tech)
ihpsg13g2_iofab = IHPSG13g2IOFactory(lib=iolib, cktfab=cktfab, layoutfab=layoutfab)
ihpsg13g2_iofab.get_cell("Gallery").layout
