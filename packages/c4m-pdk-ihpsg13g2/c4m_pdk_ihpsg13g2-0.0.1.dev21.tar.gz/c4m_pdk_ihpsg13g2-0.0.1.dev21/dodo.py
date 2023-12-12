# SPDX-License-Identifier: AGPL-3.0-or-later OR GPL-2.0-or-later OR CERN-OHL-S-2.0+ OR Apache-2.0
import os, sys, site, re, yaml
from os.path import basename, relpath
from pathlib import Path
from textwrap import dedent, indent
from typing import List, Tuple, Dict, Set, Optional, cast

from doit import get_var
from doit.action import CmdAction
from doit.tools import check_timestamp_unchanged, create_folder

import pdkmaster, c4m, c4m.flexcell, c4m.flexio

### Config

DOIT_CONFIG = {
    "default_tasks": [
        "install", "open_pdk", "gds", "spice", "liberty", "lef", "doc", "klayout", "coriolis",
    ],
}


### support functions

def get_var_env(name, default=None):
    """Uses get_var to get a command line variable, also checks
    environment variables for default value

    If os.environ[name.upper()] exists that value will override the
    default value given.
    """
    try:
        default = os.environ[name.upper()]
    except:
        # Keep the specified default
        pass
    return get_var(name, default=default)


### globals

top_dir = Path(__file__).parent

dist_dir = top_dir.joinpath("dist")

open_pdk_dir = top_dir.joinpath("open_pdk")
open_pdk_ihpsg13g2_dir = open_pdk_dir.joinpath("C4M.ihpsg13g2")
open_pdk_tech_dir = open_pdk_ihpsg13g2_dir.joinpath("libs.tech")
open_pdk_ref_dir = open_pdk_ihpsg13g2_dir.joinpath("libs.ref")
open_pdk_doc_dir = open_pdk_ihpsg13g2_dir.joinpath("libs.doc")

override_dir = top_dir.joinpath("override")

pdkmaster_inst_dir = Path(pdkmaster.__file__).parent
c4m_local_dir = top_dir.joinpath("c4m")
ihpsg13g2_local_dir = c4m_local_dir.joinpath("pdk", "ihpsg13g2")
c4m_inst_dir = Path(site.getsitepackages()[0]).joinpath("c4m")
ihpsg13g2_inst_dir = c4m_inst_dir.joinpath("pdk", "ihpsg13g2")
flexcell_inst_dir = Path(c4m.flexcell.__file__).parent
flexio_inst_dir = Path(c4m.flexio.__file__).parent

c4m_py_files = tuple(c4m_local_dir.rglob("*.py"))

# variables
python = get_var_env("python", default="python3")
pip = get_var_env("pip", default="pip3")

ihpsg13g2_pdk = get_var_env("ihpsg13g2_pdk")
if ihpsg13g2_pdk is None:
    raise EnvironmentError(
        "ihpsg13g2_pdk variable or IHPSG13G2_PDK environment variable not given"
    )
os.environ["IHPSG13G2_PDK"] = ihpsg13g2_pdk
ihpsg13g2_pdk_dir = Path(ihpsg13g2_pdk)

### cell list

cell_list_file = top_dir.joinpath("cell_list.yml")

def task_cell_list():
    """Regenerate cell list.

    This task is not run by default. It needs to be run manually when the cell list
    has been changed and then the updated file has to be commit to git.
    """
    def write_list():
        import yaml

        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        cell_list = {
            lib.name: list(cell.name for cell in lib.cells)
            for lib in ihpsg13g2.__libs__
        }
        with cell_list_file.open("w") as f:
            yaml.dump(cell_list, f)

    return {
        "title": lambda _: "Creating cell list file",
        "targets": (
            cell_list_file,
        ),
        "actions": (
            write_list,
        ),
    }

# We assume that the cell list is stored in git and is available in the top directory.
assert cell_list_file.exists()
with cell_list_file.open("r") as f:
    cell_list: Dict[str, List[str]]
    cell_list = yaml.safe_load(f)

lib_module_paths = {
    "StdCell1V2Lib": (pdkmaster_inst_dir, flexcell_inst_dir),
    "StdCell3V3Lib": (pdkmaster_inst_dir, flexcell_inst_dir),
    "StdCell1V2LambdaLib": (pdkmaster_inst_dir, flexcell_inst_dir),
    "StdCell3V3LambdaLib": (pdkmaster_inst_dir, flexcell_inst_dir),
    "IOLib": (pdkmaster_inst_dir, flexcell_inst_dir, flexio_inst_dir),
}


### main tasks

#
# dist
def task_dist():
    """Create distributable python module"""

    return {
        "title": lambda _: "Creating wheel",
        "file_dep": (top_dir.joinpath("setup.py"), *c4m_py_files),
        "targets": (dist_dir,),
        "actions": (f"{python} -m build",)
    }


#
# open_pdk
def task_open_pdk():
    """Create open_pdk dir"""
    # This is separate task so we can clean up full open_pdk directory

    return {
        "title": lambda _: "Creating open_pdk directory",
        "targets": (open_pdk_dir,),
        "actions": (
            (create_folder, (open_pdk_dir,)),
        ),
        "clean": (f"rm -fr {str(open_pdk_dir)}",),
    }


#
# gds
def task_gds():
    """Generate GDSII files"""

    gds_dirs = tuple(
        open_pdk_ref_dir.joinpath(lib, "gds") for lib in cell_list.keys()
    )
    gds_files: Dict[str, Tuple[Path, ...]] = {}
    for lib, cells in cell_list.items():
        gds_files[lib] = tuple(
            open_pdk_ref_dir.joinpath(lib, "gds", f"{cell}.gds")
            for cell in cells
        )

    def gen_gds(libname):
        from pdkmaster.io.klayout import merge, export2db
        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        lib = None
        for lib2 in ihpsg13g2.__libs__:
            if lib2.name == libname:
                lib = lib2
                break
        assert lib is not None
        merge(lib)

        out_dir = open_pdk_ref_dir.joinpath(libname, "gds")
        layout = export2db(
            lib, gds_layers=ihpsg13g2.gds_layers, textgds_layers=ihpsg13g2.textgds_layers,
            cell_name=None, merge=False, add_pin_label=True,
        )
        layout.write(str(out_dir.joinpath(f"{libname}.gds")))
        for cell in layout.each_cell():
            assert cell.name != libname
            cell.write(str(out_dir.joinpath(f"{cell.name}.gds")))

    for libname in cell_list.keys():
        yield {
            "name": libname,
            "doc": f"Creating gds files for {libname}",
            "file_dep": c4m_py_files,
            "uptodate": tuple(
                check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[libname]
            ),
            "targets": gds_files[libname],
            "actions": (
                *(
                    (create_folder, (dir_,)) for dir_ in gds_dirs
                ),
                (gen_gds, (libname,)),
            ),
        }


#
# spice_models
open_pdk_spice_dir = open_pdk_tech_dir.joinpath("ngspice")
spice_pdk_files = (
    "sg13g2_moslv_mod.lib", "sg13g2_moslv_parm.lib", "sg13g2_moslv_stat.lib", "cornerMOSlv.lib",
    "sg13g2_moshv_mod.lib", "sg13g2_moshv_parm.lib", "sg13g2_moshv_stat.lib", "cornerMOShv.lib",
    "resistors_mod.lib", "resistors_parm.lib", "resistors_stat.lib", "cornerRES.lib",
    "diodes.lib",
)
spice_models_all_lib = open_pdk_spice_dir.joinpath("all.spice")
spice_models_tgts = (
    *(open_pdk_spice_dir.joinpath(file) for file in spice_pdk_files),
    spice_models_all_lib,
)
def task_spice_models():
    "Copy and generate C4M version of the models"
    ihpsg13g2_pdk_spice_dir = ihpsg13g2_pdk_dir.joinpath("libs.tech", "ngspice", "models")

    def write_all():
        with spice_models_all_lib.open("w") as f:
            f.write(dedent("""
                * All corners file

                * lvmos
                .lib lvmos_tt
                .lib "cornerMOSlv.lib" mos_tt
                .endl

                .lib lvmos_ff
                .lib "cornerMOSlv.lib" mos_ff
                .endl

                .lib lvmos_ss
                .lib "cornerMOSlv.lib" mos_ss
                .endl

                .lib lvmos_fs
                .lib "cornerMOSlv.lib" mos_fs
                .endl

                .lib lvmos_sf
                .lib "cornerMOSlv.lib" mos_sf
                .endl

                * hvmos
                .lib hvmos_tt
                .lib "cornerMOShv.lib" mos_tt
                .endl

                .lib hvmos_ff
                .lib "cornerMOShv.lib" mos_ff
                .endl

                .lib hvmos_ss
                .lib "cornerMOShv.lib" mos_ss
                .endl

                .lib hvmos_fs
                .lib "cornerMOShv.lib" mos_fs
                .endl

                .lib hvmos_sf
                .lib "cornerMOShv.lib" mos_sf
                .endl

                * resistors
                .lib res_typ
                .lib "cornerRES.lib" res_typ
                .endl

                * resistors
                .lib res_bcs
                .lib "cornerRES.lib" res_bcs
                .endl

                * resistors
                .lib res_wcs
                .lib "cornerRES.lib" res_wcs
                .endl

                * diodes
                .lib dio
                .include "diodes.lib"
                .endl
            """[1:]))

    return {
        "file_dep": tuple(
            ihpsg13g2_pdk_spice_dir.joinpath(file) for file in spice_pdk_files
        ),
        "targets": spice_models_tgts,
        "actions": (
            (create_folder, (open_pdk_spice_dir,)),
            *(
                f"cp {str(ihpsg13g2_pdk_spice_dir.joinpath(file))}"
                f" {str(open_pdk_spice_dir.joinpath(file))}"
                for file in spice_pdk_files
            ),
            write_all,
        )
    }


#
# spice_models_python (copy inside python module)
python_models_dir = ihpsg13g2_local_dir.joinpath("models")
def _repl_dir(p: Path) -> Path:
    b = basename(str(p))
    return python_models_dir.joinpath(b)
python_models_srctgts = tuple(
    (file, _repl_dir(file))
    for file in spice_models_tgts
)
python_models_init_file = python_models_dir.joinpath("__init__.py")
python_models_deps = tuple(scr for (scr, _) in python_models_srctgts)
python_models_tgts = tuple(tgt for (_, tgt) in python_models_srctgts)
def task_spice_models_python():
    """Copy SPICE models inside pdk module

    This way they can be used by pyspicefactory without needing separate
    PDK install"""
    def write_init():
        with python_models_init_file.open("w") as f:
            f.write(dedent("""
                # Autogenerated module
            """[1:]))

    return {
        "file_dep": python_models_deps,
        "targets": (*python_models_tgts, python_models_init_file),
        "actions": (
            (create_folder, (python_models_dir,)),
            write_init,
            *(
                f"cp {str(python_models_deps[n])} {str(python_models_tgts[n])}"
                for n in range(len(python_models_tgts))
            )
        )
    }


#
# manifest
manifest_file = top_dir.joinpath("MANIFEST.in")
def task_manifest():
    """Create MANIFEST.in"""
    def write_manifest():
        with manifest_file.open("w") as f:
            for tgt in python_models_tgts:
                print(f"include c4m/pdk/ihpsg13g2/models/{basename(str(tgt))}", file=f)

    return {
        "file_dep": python_models_tgts,
        "targets": (
            manifest_file,
        ),
        "actions": (
            write_manifest,
        ),
    }


#
# install
def task_install():
    """Install the python module

    It will not install dependencies to avoid overwriting locally installed versions
    with release versions.
    """

    return {
        "title": lambda _: "Installing python module",
        "file_dep": (
            *c4m_py_files, manifest_file, *python_models_tgts,
        ),
        "targets": (ihpsg13g2_inst_dir,),
        "actions": (
            f"{pip} install --no-deps {top_dir}",
            f"{pip} check",
        ),
    }


#
# spice
def task_spice():
    """Generate SPICE files"""

    spice_dirs = tuple(
        open_pdk_ref_dir.joinpath(lib, "spice") for lib in cell_list.keys()
    )
    spice_files = {}
    for lib, cells in cell_list.items():
        lib_spice_files = []
        lib_spice_files.append(open_pdk_ref_dir.joinpath(lib, "spice", f"{lib}.spi"))
        for cell in cells:
            lib_spice_files.append(open_pdk_ref_dir.joinpath(lib, "spice", f"{cell}.spi"))
            lib_spice_files.append(open_pdk_ref_dir.joinpath(lib, "spice", f"{cell}_hier.spi"))
        spice_files[lib] = lib_spice_files

    def gen_spice(libname):
        from pdkmaster.design import circuit as _ckt
        from c4m.pdk import ihpsg13g2

        lib = None
        for lib2 in ihpsg13g2.__libs__:
            if lib2.name == libname:
                lib = lib2
                break
        assert lib is not None

        def iter_cell_hierordered(cells, seen: Optional[Set]=None):
            if seen is None:
                seen = set()
            for cell in cells:
                if cell in seen:
                    continue
                yield from iter_cell_hierordered(
                    (inst.cell for inst in cell.circuit.instances.__iter_type__(_ckt._CellInstance)),
                    seen=seen,
                )
                seen.add(cell)
                yield cell

        lib_spice_dir = open_pdk_ref_dir.joinpath(lib.name, "spice")
        with lib_spice_dir.joinpath(f"{lib.name}.spi").open("w") as f_lib:
            f_lib.write(f"* {lib.name}\n")
            for cell in iter_cell_hierordered(lib.cells):
                # Write cell only to spice file
                pyspicesubckt = ihpsg13g2.pyspicefab.new_pyspicesubcircuit(
                    circuit=cell.circuit
                )
                s = f"* {cell.name}\n" + str(pyspicesubckt)
                f_lib.write("\n" + s)
                with lib_spice_dir.joinpath(f"{cell.name}.spi").open("w") as f_cell:
                    f_cell.write(s)

                # Write cell hierarchy to file; make order so that each cell is in
                # the file before is is being used.
                with lib_spice_dir.joinpath(f"{cell.name}_hier.spi").open("w") as f_cell:
                    s = ""
                    for cell2 in iter_cell_hierordered((cell,)):
                        pyspicesubckt = ihpsg13g2.pyspicefab.new_pyspicesubcircuit(
                            circuit=cell2.circuit, lvs=True,
                        )
                        s += f"\n* {cell2.name}\n"
                        s_ckt = str(pyspicesubckt)
                        s_ckt = s_ckt.replace("Ohm", "")
                        # s_ckt = s_ckt.replace("(", "[").replace(")", "]")
                        s += s_ckt
                    f_cell.write(f"* {cell.name} hierarchy\n{s}")

    for lib in cell_list.keys():
        yield {
            "name": lib,
            "doc": f"Creating spice files for library {lib}",
            "file_dep": c4m_py_files,
            "uptodate": tuple(
                check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[lib]
            ),
            "targets": spice_files[lib],
            "actions": (
                *(
                    (create_folder, (dir_,)) for dir_ in spice_dirs
                ),
                (gen_spice, (lib,)),
            ),
        }


#
# liberty
def task_liberty():
    liberty_io_dir = open_pdk_ref_dir.joinpath("IOLib", "liberty")
    liberty_io_file = liberty_io_dir.joinpath("IOLib_dummy.lib")

    def inputpin_str(*, name: str, ispad: bool=False, domain: str):
        if domain == "core":
            vss = "vss"
            vdd = "vdd"
        elif domain == "io":
            vss = "iovss"
            vdd = "iovdd"
        else:
            assert False, f"Internal error: unhandled domain '{domain}'"

        s = dedent(f"""
            pin ({name}) {{
                direction : input;
        """[1:])
        if ispad:
            s += "    is_pad : true;\n"
        s += dedent(f"""
                input_voltage : {domain}_input;
                related_ground_pin : {vss};
                related_power_pin : {vdd};
                max_transition : 200;
                capacitance : 15.0;
                rise_capacitance : 15.0;
                rise_capacitance_range (12.0, 15.0);
                fall_capacitance : 15.0;
                fall_capacitance_range (12.0, 15.0);
            }}
        """[1:])

        return s

    def outputpin_str(*,
        name: str, ispad: bool=False, related: str, tri: Optional[str]=None, inout: bool=False,
        domain: str,
    ):
        if domain == "core":
            vss = "vss"
            vdd = "vdd"
        elif domain == "io":
            vss = "iovss"
            vdd = "iovdd"
        else:
            assert False, f"Internal error: unhandled domain '{domain}'"

        s = dedent(f"""
            pin ({name}) {{
                direction : {"output" if not inout else "inout"};
                function : "({related})";
        """[1:])
        if tri is not None:
            s += f'    three_state: "({tri})";\n'
        if ispad:
            s += f"    is_pad : true;\n"
        s += indent(dedent(f"""
                output_voltage : {domain}_output;
                related_ground_pin : {vss};
                related_power_pin : {vdd};
                max_capacitance : 500;
                max_transition : 200;
                timing () {{
                    related_pin : "{related}";
                    timing_type : combinational;
                    cell_rise (delay_template_2x2) {{
                        values ( \\
                            "1000, 1000", \\
                            "1000, 1000" \\
                        );
                    }}
                    rise_transition (delay_template_2x2) {{
                        values ( \\
                            "200, 200", \\
                            "200, 200" \\
                        );
                    }}
                    cell_fall (delay_template_2x2) {{
                        values ( \\
                            "1000, 1000", \\
                            "1000, 1000" \\
                        );
                    }}
                    fall_transition (delay_template_2x2) {{
                        values ( \\
                            "200, 200", \\
                            "200, 200" \\
                        );
                    }}
                }}
        """[1:]), "    ")
        if tri is not None:
            s += indent(dedent(f"""
                timing () {{
                    related_pin : "{tri}";
                    timing_sense : positive_unate;
                    timing_type : three_state_enable;
                    cell_rise (delay_template_2x2) {{
                        values ( \\
                            "1000, 1000", \\
                            "1000, 1000" \\
                        );
                    }}
                    rise_transition (delay_template_2x2) {{
                        values ( \\
                            "200, 200", \\
                            "200, 200" \\
                        );
                    }}
                    cell_fall (delay_template_2x2) {{
                        values ( \\
                            "1000, 1000", \\
                            "1000, 1000" \\
                        );
                    }}
                    fall_transition (delay_template_2x2) {{
                        values ( \\
                            "200, 200", \\
                            "200, 200" \\
                        );
                    }}
                }}
                timing () {{
                    related_pin : "{tri}";
                    timing_sense : negative_unate;
                    timing_type : three_state_disable;
                    cell_rise (delay_template_2x2) {{
                        values ( \\
                            "1000, 1000", \\
                            "1000, 1000" \\
                        );
                    }}
                    rise_transition (delay_template_2x2) {{
                        values ( \\
                            "200, 200", \\
                            "200, 200" \\
                        );
                    }}
                    cell_fall (delay_template_2x2) {{
                        values ( \\
                            "1000, 1000", \\
                            "1000, 1000" \\
                        );
                    }}
                    fall_transition (delay_template_2x2) {{
                        values ( \\
                            "200, 200", \\
                            "200, 200" \\
                        );
                    }}
                }}
            """[1:]), "    ")
        s += "        }"

        return s

    def gen_liberty():
        from c4m import flexio as _io
        from c4m.pdk.ihpsg13g2 import iolib

        with liberty_io_file.open(mode="w") as f:
            f.write(dedent("""
                library (IOLib_dummy) {
                    delay_model : table_lookup;
                    capacitive_load_unit (1,ff);
                    current_unit : "1mA";
                    leakage_power_unit : "1mW";
                    pulling_resistance_unit : "1kohm";
                    time_unit : "1ps";
                    voltage_unit : "1V";
                    voltage_map (vss, 0.0);
                    voltage_map (vdd, 1.2);
                    voltage_map (iovss, 0.0);
                    voltage_map (iovdd, 3.3);
                    default_cell_leakage_power : 0;
                    default_fanout_load : 1;
                    default_inout_pin_cap : 1;
                    default_input_pin_cap : 1;
                    default_leakage_power_density : 0;
                    default_max_fanout : 30;
                    default_max_transition : 5000;
                    default_output_pin_cap : 0;
                    in_place_swap_mode : match_footprint;
                    input_threshold_pct_fall : 50;
                    input_threshold_pct_rise : 50;
                    nom_process : 1;
                    nom_temperature : 25;
                    nom_voltage : 1.8;
                    output_threshold_pct_fall : 50;
                    output_threshold_pct_rise : 50;
                    slew_derate_from_library : 1;
                    slew_lower_threshold_pct_fall : 20;
                    slew_lower_threshold_pct_rise : 20;
                    slew_upper_threshold_pct_fall : 80;
                    slew_upper_threshold_pct_rise : 80;
                    operating_conditions ("typ") {
                        process : 1;
                        temperature : 25;
                        voltage : 1.8;
                        tree_type: "balanced_tree";
                    }
                    default_operating_conditions : "typ";
                    input_voltage (core_input) {
                        vih : 1.2;
                        vil : 0;
                        vimax : 1.2;
                        vimin : 0;
                    }
                    output_voltage (core_output) {
                        voh : 1.2;
                        vol : 0;
                        vomax : 1.2;
                        vomin : 0;
                    }
                    input_voltage (io_input) {
                        vih : 3.3;
                        vil : 0;
                        vimax : 3.3;
                        vimin : 0;
                    }
                    output_voltage (io_output) {
                        voh : 3.3;
                        vol : 0;
                        vomax : 3.3;
                        vomin : 0;
                    }
                    lu_table_template (delay_template_2x2) {
                        variable_1 : input_net_transition;
                        variable_2 : total_output_net_capacitance;
                        index_1 ("10, 200");
                        index_2 ("500, 30000");
                    }
            """[1:]))
            for cell in iolib.cells:
                if isinstance(cell, (
                    _io.PadInT, _io.PadOutT, _io.PadTriOutT, _io.PadInOutT,
                    _io.PadVssT, _io.PadVddT, _io.PadIOVssT, _io.PadIOVddT,
                )):
                    s = indent(dedent(f"""
                        cell ({cell.name}) {{
                            area: 14400;
                            dont_touch : true;
                            dont_use : true;
                            timing_model_type : abstracted;
                            pad_cell : true;
                            pg_pin (vss) {{
                                pg_type : primary_ground;
                                voltage_name : "vss";
                    """), "    ")
                    if isinstance(cell, _io.PadVssT):
                        s += "            is_pad : true;\n"
                    s += indent(dedent(f"""
                            }}
                            pg_pin (vdd) {{
                                pg_type : primary_power;
                                voltage_name : "vdd";
                    """[1:]), "        ")
                    if isinstance(cell, _io.PadVddT):
                        s += "            is_pad : true;\n"
                    s += indent(dedent(f"""
                            }}
                            pg_pin (iovss) {{
                                pg_type : primary_ground;
                                voltage_name : "iovss";
                    """[1:]), "        ")
                    if isinstance(cell, _io.PadIOVssT):
                        s += "            is_pad : true;\n"
                    s += indent(dedent(f"""
                            }}
                            pg_pin (iovdd) {{
                                pg_type : primary_power;
                                voltage_name : "iovdd";
                    """[1:]), "        ")
                    if isinstance(cell, _io.PadIOVddT):
                        s += "            is_pad : true;\n"
                    s += "        }\n"
                    if isinstance(cell, _io.PadInT):
                        s += indent(
                            (
                                outputpin_str(name="p2c", related="pad", domain="core")
                                + inputpin_str(name="pad", ispad=True, domain="io")
                            ),
                            "        "
                        )
                    elif isinstance(cell, _io.PadOutT):
                        s += indent(
                            (
                                inputpin_str(name="c2p", domain="core")
                                + outputpin_str(name="pad", ispad=True, related="c2p", domain="io")
                            ),
                            "        "
                        )
                    elif isinstance(cell, _io.PadTriOutT):
                        s += indent(
                            (
                                inputpin_str(name="c2p", domain="core")
                                + inputpin_str(name="c2p_en", domain="core")
                                + outputpin_str(
                                    name="pad", ispad=True, related="c2p", tri="c2p_en",
                                    domain="io",
                                )
                            ),
                            "        "
                        )
                    elif isinstance(cell, _io.PadInOutT):
                        s += indent(
                            (
                                outputpin_str(name="p2c", related="pad", domain="core")
                                + inputpin_str(name="c2p", domain="core")
                                + inputpin_str(name="c2p_en", domain="core")
                                + outputpin_str(
                                    name="pad", ispad=True, related="c2p", tri="c2p_en",
                                    inout=True, domain="io",
                                )
                            ),
                            "        "
                        )
                    elif isinstance(cell, (_io.PadVssT, _io.PadVddT, _io.PadIOVssT, _io.PadIOVddT)):
                        # No extra pins
                        pass
                    else:
                        assert False, "Internal error"
                    s += "    }\n"
                    f.write(s)
            f.write("}\n")

    yield {
        "name": "IOLib",
        "doc": "Creating lef file for IOLib",
        "file_dep": (*c4m_py_files, __file__),
        "uptodate": tuple(
            check_timestamp_unchanged(str(dir))
            for dir in lib_module_paths["IOLib"]
        ),
        "targets": (liberty_io_file,),
        "actions": (
            (create_folder, (liberty_io_dir,)),
            gen_liberty,
        )
    }


#
# LEF
def task_lef():
    """Generate LEF files"""
    # Currenlty only implemented ad-hoc for IO library

    from datetime import datetime

    from pdkmaster.technology import geometry as _geo
    from pdkmaster.design import layout as _lay, circuit as _ckt, library as _lbry
    from c4m.flexio import IOFrameSpecification, FactoryCellT

    lef_io_cells = (
        "Corner", "Filler200", "Filler400", "Filler1000", "Filler2000", "Filler4000", "Filler10000",
        "IOPadIn",
        "IOPadOut4mA", "IOPadOut8mA", "IOPadOut12mA", "IOPadOut16mA", "IOPadOut20mA",
        "IOPadOut24mA", "IOPadOut30mA",
        "IOPadTriOut4mA", "IOPadTriOut8mA", "IOPadTriOut12mA", "IOPadTriOut16mA", "IOPadTriOut20mA",
        "IOPadTriOut24mA", "IOPadTriOut30mA",
        "IOPadInOut4mA", "IOPadInOut8mA", "IOPadInOut12mA", "IOPadInOut16mA", "IOPadInOut20mA",
        "IOPadInOut24mA", "IOPadInOut30mA",
        "IOPadAnalog",
        "IOPadIOVss", "IOPadIOVdd", "IOPadVss", "IOPadVdd",
    )
    lef_io_dir = open_pdk_ref_dir.joinpath("IOLib", "lef")
    lef_io_file = lef_io_dir.joinpath("IOLib.lef")
    lef_ionotrack_file = lef_io_dir.joinpath("IOLib_notracks.lef")

    track_metals = ("Metal3", "Metal4", "Metal5", "TopMetal1", "TopMetal2")
    pin_metals = ("Metal1", "Metal2", *track_metals)

    dir_lookup: Dict[str, str] = {
        "iovss": "INOUT",
        "iovdd": "INOUT",
        "vss": "INOUT",
        "vdd": "INOUT",
        "pad": "INOUT",
        "padres": "INOUT",
        "p2c": "OUTPUT",
        "c2p": "INPUT",
        "c2p_en": "INPUT",
    }
    use_lookup: Dict[str, str] = {
        "iovss": "GROUND",
        "iovdd": "POWER",
        "vss": "GROUND",
        "vdd": "POWER",
        "pad": "SIGNAL",
        "padres": "SIGNAL",
        "p2c": "SIGNAL",
        "c2p": "SIGNAL",
        "c2p_en": "SIGNAL",
    }

    def rect_str(*, r: _geo.RectangularT):
        return f"RECT {r.left:.3f} {r.bottom:.3f} {r.right:.3f} {r.top:.3f}"

    def obs_str(*, shape: _geo.RectangularT, track_shape):
        s = "  OBS\n"
        s += "".join(
            f"    LAYER {l} ;\n"
            f"      {rect_str(r=track_shape if l in track_metals else shape)} ;\n"
            for l in pin_metals
        )
        s += "  END\n"

        return s

    def pin_str(*,
        net: _ckt.CircuitNetT, add_tracks: bool, tracks_only: bool,
        layout: _lay.LayoutT, bnd: _geo.RectangularT,
    ) -> str:
        s = (
            f"  PIN {net.name}\n"
            f"    DIRECTION {dir_lookup[net.name]} ;\n"
            f"    USE {use_lookup[net.name]} ;\n"
        )

        # Sort the shapes
        # track_shapes is of the DC tracks in the IO cell
        pin_shapes: Dict[str, List[_geo.Rect]] = {n: [] for n in pin_metals}
        # track_shapes is of the DC tracks in the IO cell
        track_shapes: Dict[str, List[_geo.Rect]] = {n: [] for n in pin_metals}
        # pad_shapes is for pad pin e.g. the pins touching the bottom of the cell
        pad_shapes: Dict[str, List[_geo.Rect]] = {n: [] for n in pin_metals}
        for ms in layout.filter_polygons(net=net, split=True, depth=0):
            mask = ms.mask
            shape = ms.shape

            if ms.mask.name.endswith(".pin"):
                assert isinstance(shape, _geo.Rect)

                layer_name = mask.name[:-4]
                assert layer_name in pin_metals
                if (not tracks_only) and (shape.top > (bnd.top - _geo.epsilon)):
                    pin_shapes[layer_name].append(shape)
                elif (not tracks_only) and (shape.bottom < (bnd.bottom + _geo.epsilon)):
                    pad_shapes[layer_name].append(shape)
                else:
                    track_shapes[layer_name].append(shape)

        if any(pin_shapes.values()):
            s += "    PORT\n"
            for metal_name in pin_metals:
                shapes = pin_shapes[metal_name]
                if shapes:
                    s += f"      LAYER {metal_name} ;\n"
                    for shape in shapes:
                        s += f"        {rect_str(r=shape)} ;\n"
            s += "    END\n"

        if any(pad_shapes.values()):
            s += "    PORT\n"
            for metal_name in pin_metals:
                shapes = pad_shapes[metal_name]
                if shapes:
                    s += f"      LAYER {metal_name} ;\n"
                    for shape in shapes:
                        s += f"        {rect_str(r=shape)} ;\n"
            s += "    END\n"

        if add_tracks:
            for metal_name in pin_metals:
                shapes = track_shapes[metal_name]
                if shapes:
                    s += "".join(
                        "    PORT\n"
                        f"      LAYER {metal_name} ;\n"
                        f"        {rect_str(r=shape)} ;\n"
                        "    END\n"
                        for shape in shapes
                    )

        s += f"  END {net.name}\n"

        return s

    def gen_lef(add_tracks: bool):
        from c4m.pdk.ihpsg13g2 import ihpsg13g2_ioframespec, iolib
        iolib: _lbry.Library
        ihpsg13g2_ioframespec: IOFrameSpecification

        lib_name = iolib.name
        site_name = f"{lib_name}Site"
        file = lef_io_file if add_tracks else lef_ionotrack_file
        with file.open(mode="w") as f:
            f.write(dedent(
                f"""
                # Autogenerated file; please don't edit
                # date: {datetime.now()}

                VERSION 5.8 ;

                SITE {site_name}
                  CLASS PAD ;
                  SYMMETRY R90 ;
                  SIZE 1.00 BY {ihpsg13g2_ioframespec.cell_height:.2f} ;
                END {site_name}
                """[1:]
            ))

            class_lookup: Dict[str, str] = {
                "Corner": "SPACER",
                "Filler200": "SPACER",
                "Filler400": "SPACER",
                "Filler1000": "SPACER",
                "Filler2000": "SPACER",
                "Filler4000": "SPACER",
                "Filler10000": "SPACER",
                "IOPadIn": "INPUT",
                "IOPadOut4mA": "OUTPUT",
                "IOPadOut8mA": "OUTPUT",
                "IOPadOut12mA": "OUTPUT",
                "IOPadOut16mA": "OUTPUT",
                "IOPadOut20mA": "OUTPUT",
                "IOPadOut24mA": "OUTPUT",
                "IOPadOut30mA": "OUTPUT",
                "IOPadTriOut4mA": "OUTPUT",
                "IOPadTriOut8mA": "OUTPUT",
                "IOPadTriOut12mA": "OUTPUT",
                "IOPadTriOut16mA": "OUTPUT",
                "IOPadTriOut20mA": "OUTPUT",
                "IOPadTriOut24mA": "OUTPUT",
                "IOPadTriOut30mA": "OUTPUT",
                "IOPadInOut4mA": "INOUT",
                "IOPadInOut8mA": "INOUT",
                "IOPadInOut12mA": "INOUT",
                "IOPadInOut16mA": "INOUT",
                "IOPadInOut20mA": "INOUT",
                "IOPadInOut24mA": "INOUT",
                "IOPadInOut30mA": "INOUT",
                "IOPadAnalog": "INOUT",
                "IOPadIOVss": "POWER",
                "IOPadIOVdd": "POWER",
                "IOPadVss": "POWER",
                "IOPadVdd": "POWER",
            }
            for cell_name in lef_io_cells:
                cell = cast(FactoryCellT, iolib.cells[cell_name])
                ckt = cell.circuit
                layout = cell.layout
                tracks_only = (cell_name.startswith("Corner") or cell_name.startswith("Filler"))
                nets = ckt.nets

                bnd = cell.layout.boundary
                assert bnd is not None

                # header
                f.write(dedent(
                    f"""
                    MACRO {cell.name}
                      CLASS PAD {class_lookup[cell.name]} ;
                      ORIGIN {-bnd.left:.3f} {-bnd.bottom:.3f} ;
                      FOREIGN {cell.name} 0 0 ;
                      SIZE {bnd.width:.3f} BY {bnd.height:.3f} ;
                      SYMMETRY X Y R90 ;
                      SITE {site_name} ;
                    """
                ))

                # pins
                for pin_name in sorted(port.name for port in ckt.ports):
                    net = nets[pin_name]
                    f.write(pin_str(
                        net=net, add_tracks=add_tracks, tracks_only=tracks_only,
                        layout=layout, bnd=bnd))

                # OBS
                if cell_name != "Corner":
                    track_shape = _geo.Rect.from_rect(
                        rect=bnd, top=ihpsg13g2_ioframespec._track_specs_dict["vddvss"].top,
                    )
                else:
                    track_shape = bnd
                f.write(obs_str(shape=bnd, track_shape=track_shape))
                f.write(f"END {cell.name}\n")

    yield {
        "name": "IOLib",
        "doc": "Creating lef file for",
        "file_dep": c4m_py_files,
        "uptodate": tuple(
            check_timestamp_unchanged(str(dir))
            for dir in lib_module_paths["IOLib"]
        ),
        "targets": (lef_io_file, lef_ionotrack_file),
        "actions": (
            (create_folder, (lef_io_dir,)),
            (gen_lef, (True,)),
            (gen_lef, (False,)),
        )
    }


#
# klayout
klayout_dir = open_pdk_tech_dir.joinpath("klayout")
klayout_tech_dir = klayout_dir.joinpath("tech", "C4M.ihpsg13g2")
klayout_bin_dir = klayout_dir.joinpath("bin")
klayout_lvs_script = klayout_bin_dir.joinpath("lvs_ihpsg13g2")
klayout_drc_script = klayout_bin_dir.joinpath("drc_ihpsg13g2")
def task_klayout():
    """Generate klayout files"""

    klayout_drc_dir = klayout_tech_dir.joinpath("drc")
    klayout_lvs_dir = klayout_tech_dir.joinpath("lvs")
    klayout_share_dir = klayout_dir.joinpath("share")

    klayout_lyt_file = klayout_tech_dir.joinpath("C4M.ihpsg13g2.lyt")
    klayout_drc_lydrc_file = klayout_drc_dir.joinpath("DRC.lydrc")
    klayout_extract_lylvs_file = klayout_lvs_dir.joinpath("Extract.lylvs")
    klayout_drc_file = klayout_share_dir.joinpath("ihpsg13g2.drc")
    klayout_extract_file = klayout_share_dir.joinpath("ihpsg13g2_extract.lvs")
    klayout_extract_script = klayout_bin_dir.joinpath("extract_ihpsg13g2")
    klayout_lvs_file = klayout_share_dir.joinpath("ihpsg13g2.lvs")

    def gen_klayout():
        from pdkmaster.io.klayout import FileExporter
        from c4m.pdk import ihpsg13g2
        from xml.etree.ElementTree import ElementTree

        expo = FileExporter(
            tech=ihpsg13g2.tech, gds_layers=ihpsg13g2.gds_layers,
            export_name=f"C4M.{ihpsg13g2.tech.name}",
            prims_spiceparams=ihpsg13g2.prims_spiceparams,
        )()

        # DRC
        with klayout_drc_file.open("w") as f:
            f.write(expo["drc"])
        with klayout_drc_script.open("w") as f:
            relfile = relpath(klayout_drc_file, klayout_bin_dir)
            f.write(dedent(f"""
                #!/bin/sh
                d=`dirname $0`
                deck=`realpath $d/{relfile}`

                if [ $# -ne 2 ]
                then
                    echo "Usage `basename $0` input report"
                    exit 20
                fi

                export SOURCE_FILE=$1 REPORT_FILE=$2
                klayout -b -r ${{deck}}
            """[1:]))
        klayout_drc_script.chmod(0o755)

        # Extract
        with klayout_extract_file.open("w") as f:
            f.write(expo["extract"])
        with klayout_extract_script.open("w") as f:
            relfile = relpath(klayout_extract_file, klayout_bin_dir)
            f.write(dedent(f"""
                #!/bin/sh
                d=`dirname $0`
                deck=`realpath $d/{relfile}`

                if [ $# -ne 2 ]
                then
                    echo "Usage `basename $0` input spice_out"
                    exit 20
                fi

                export SOURCE_FILE=$1 SPICE_FILE=$2
                klayout -b -r ${{deck}}
            """[1:]))
        klayout_extract_script.chmod(0o755)

        # LVS
        with klayout_lvs_file.open("w") as f:
            f.write(expo["lvs"])
        with klayout_lvs_script.open("w") as f:
            relfile = relpath(klayout_lvs_file, klayout_bin_dir)
            f.write(dedent(f"""
                #!/bin/sh
                d=`dirname $0`
                deck=`realpath $d/{relfile}`

                if [ $# -ne 3 ]
                then
                    echo "Usage `basename $0` gds spice report"
                    exit 20
                fi

                export SOURCE_FILE=`realpath $1` SPICE_FILE=`realpath $2` REPORT_FILE=$3
                klayout -b -r ${{deck}}
            """[1:]))
        klayout_lvs_script.chmod(0o755)

        # klayout technology
        et = ElementTree(expo["ly_drc"])
        et.write(klayout_drc_lydrc_file, encoding="utf-8", xml_declaration=True)
        et = ElementTree(expo["ly_extract"])
        et.write(klayout_extract_lylvs_file, encoding="utf-8", xml_declaration=True)
        et = ElementTree(expo["ly_tech"])
        et.write(klayout_lyt_file, encoding="utf-8", xml_declaration=True)

    return {
        "title": lambda _: "Creating klayout files",
        "file_dep": c4m_py_files,
        "uptodate": (
            check_timestamp_unchanged(str(pdkmaster_inst_dir)),
        ),
        "targets": (
            klayout_lyt_file, klayout_drc_lydrc_file, klayout_extract_lylvs_file,
            klayout_drc_file, klayout_drc_script, klayout_extract_file,
            klayout_extract_script, klayout_lvs_file, klayout_lvs_script,
        ),
        "actions": (
            (create_folder, (klayout_share_dir,)),
            (create_folder, (klayout_bin_dir,)),
            (create_folder, (klayout_drc_dir,)),
            (create_folder, (klayout_lvs_dir,)),
            gen_klayout,
        ),
    }


#
# coriolis
def task_coriolis():
    """Generate coriolis support files"""

    coriolis_dir = open_pdk_tech_dir.joinpath("coriolis")
    corio_dir = coriolis_dir.joinpath("techno", "etc", "coriolis2")
    corio_node130_dir = corio_dir.joinpath("node130")
    corio_ihpsg13g2_dir = corio_node130_dir.joinpath("ihpsg13g2")

    corio_nda_init_file = corio_dir.joinpath("__init__.py")
    corio_node130_init_file = corio_node130_dir.joinpath("__init__.py")
    corio_ihpsg13g2_init_file = corio_ihpsg13g2_dir.joinpath("__init__.py")
    corio_ihpsg13g2_techno_file = corio_ihpsg13g2_dir.joinpath("techno.py")
    corio_ihpsg13g2_lib_files = tuple(
        corio_ihpsg13g2_dir.joinpath(f"{lib}.py") for lib in cell_list.keys()
    )

    def gen_init():
        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        with corio_ihpsg13g2_init_file.open("w") as f:
            print("from .techno import *", file=f)
            # for lib in libs.__libs__:
            for lib in ihpsg13g2.__libs__:
                print(f"from .{lib.name} import setup as {lib.name}_setup", file=f)

            print(
                "\n__lib_setups__ = [{}]".format(
                    # ",".join(f"{lib.name}.setup" for lib in libs.__libs__)
                    ",".join(f"{lib.name}.setup" for lib in ihpsg13g2.__libs__)
                ),
                file=f,
            )

    def gen_coriolis():
        from pdkmaster.io import coriolis as _iocorio
        from c4m.flexcell import coriolis_export_spec
        from c4m.pdk import ihpsg13g2
        # from doitlib import libs

        expo = _iocorio.FileExporter(
            tech=ihpsg13g2.tech, gds_layers=ihpsg13g2.gds_layers, spec=coriolis_export_spec,
        )

        with corio_ihpsg13g2_techno_file.open("w") as f:
            f.write(dedent("""
                # Autogenerated file
                # SPDX-License-Identifier: GPL-2.0-or-later OR AGPL-3.0-or-later OR CERN-OHL-S-2.0+
            """))
            f.write(expo())

        # for lib in libs.__libs__:
        for lib in ihpsg13g2.__libs__:
            with corio_ihpsg13g2_dir.joinpath(f"{lib.name}.py").open("w") as f:
                f.write(expo(lib))

    return {
        "title": lambda _: "Creating coriolis files",
        "file_dep": c4m_py_files,
        "uptodate": (
            check_timestamp_unchanged(str(pdkmaster_inst_dir)),
            check_timestamp_unchanged(str(flexcell_inst_dir)),
            check_timestamp_unchanged(str(flexio_inst_dir)),
            # check_timestamp_unchanged(str(flexmem_inst_dir)),
        ),
        "targets": (
            corio_nda_init_file, corio_node130_init_file, corio_ihpsg13g2_init_file,
            corio_ihpsg13g2_techno_file, *corio_ihpsg13g2_lib_files,
        ),
        "actions": (
            (create_folder, (corio_ihpsg13g2_dir,)),
            corio_nda_init_file.touch, corio_node130_init_file.touch,
            gen_init, gen_coriolis,
        ),
    }


#
# docs
sim_dir = top_dir.joinpath("sim")
iolib_doc_dir = open_pdk_doc_dir.joinpath("IOLib")
def task_doc():
    """Generate the docs"""

    drivestrength_sim_script_file = sim_dir.joinpath("SimOutDriveStrength.py")
    drivestrength_sim_out_file = sim_dir.joinpath("SimOutDriveStrength.out")
    drivestrength_doc_file = iolib_doc_dir.joinpath("DriveStrengthSim.txt")
    yield {
        "name": "DriveStrength",
        "doc": "Simulate and document output drive strength",
        "file_dep": (
            drivestrength_sim_script_file,
        ),
        "task_dep": (
            "install",
        ),
        "targets": (
            drivestrength_doc_file,
        ),
        "actions": (
            (create_folder, (iolib_doc_dir,)),
            f"cd {str(sim_dir)}; {str(drivestrength_sim_script_file)}",
            f"cp {str(drivestrength_sim_out_file)} {str(drivestrength_doc_file)}",
        ),
    }

    input_sim_script_file = sim_dir.joinpath("SimInputPerformance.py")
    input_sim_out_file = sim_dir.joinpath("SimInputPerformance.svg")
    input_doc_file = iolib_doc_dir.joinpath("InputPerformance.svg")
    yield {
        "name": "InputPerformance",
        "doc": "Simulate and document input performance",
        "file_dep": (
            input_sim_script_file,
        ),
        "task_dep": (
            "install",
        ),
        "targets": (
            input_doc_file,
        ),
        "actions": (
            (create_folder, (iolib_doc_dir,)),
            f"cd {str(sim_dir)}; {str(input_sim_script_file)}",
            f"cp {str(input_sim_out_file)} {str(input_doc_file)}",
        ),
    }


#
# release
def task_tarball():
    """Create a tarball"""
    from datetime import datetime

    tarballs_dir = top_dir.joinpath("tarballs")
    t = datetime.now()
    tarball = tarballs_dir.joinpath(f'{t.strftime("%Y%m%d_%H%M")}_openpdk_c4m_ihpsg13g2.tgz')

    return {
        "title": lambda _: "Create release tarball",
        "task_dep": (
            "gds", "spice", "liberty", "lef", "doc", "klayout", "coriolis",
        ),
        "targets": (tarball,),
        "actions": (
            (create_folder, (tarballs_dir,)),
            f"cd {str(top_dir)}; tar czf {str(tarball)} open_pdk",
        )
    }


#
# drc
def task_drc():
    "Run drc checks"
    drc_dir = top_dir.joinpath("drc")

    def run_drc(lib, cell):
        gds_dir = open_pdk_ref_dir.joinpath(lib, "gds")

        drcrep = drc_dir.joinpath(lib, f"{cell}.rep")
        gdsfile = gds_dir.joinpath(f"{cell}.gds")

        try:
            CmdAction(
                f"{str(klayout_drc_script)} {str(gdsfile)} {str(drcrep)}",
            ).execute()
            with drcrep.open("r") as f:
                # Each DRC error has an <item> section in the output XML
                ok = not any(("<item>" in line for line in f))
        except:
            ok = False
        if not ok:
            print(f"DRC of {lib}/{cell} failed!", file=sys.stderr)

    def lib_rep(lib, cells):
        with drc_dir.joinpath(f"{lib}.rep").open("w") as librep:
            for cell in cells:
                drcrep = drc_dir.joinpath(lib, f"{cell}.rep")
                with drcrep.open("r") as f:
                    # Each DRC error has an <item> section in the output XML
                    ok = not any(("<item>" in line for line in f))

                print(f"{cell}: {'OK' if ok else 'NOK'}", file=librep)

    for lib, cells in cell_list.items():
        drc_lib_dir = drc_dir.joinpath(lib)
        for cell in cells:
            yield {
                "name": f"{lib}:{cell}",
                "doc": f"Running DRC check for lib {lib} cell {cell}",
                "file_dep": c4m_py_files,
                "task_dep": (f"gds:{lib}", "klayout"),
                "uptodate": tuple(
                    check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[lib]
                ),
                "targets": (drc_dir.joinpath(lib, f"{cell}.rep"),),
                "actions": (
                    (create_folder, (drc_lib_dir,)),
                    (run_drc, (lib, cell)),
                ),
            }

        # If there exist a Gallery cell then do only DRC on that cell by default
        if "Gallery" in cells:
            cells = ("Gallery",)

        yield {
            "name": f"{lib}",
            "doc": f"Assembling DRC results for lib",
            "file_dep": c4m_py_files,
            "task_dep": (
                *(f"drc:{lib}:{cell}" for cell in cells),
                "klayout",
            ),
            "uptodate": tuple(
                check_timestamp_unchanged(str(dir)) for dir in lib_module_paths[lib]
            ),
            "targets": (drc_dir.joinpath(f"{lib}.rep"),),
            "actions": (
                (lib_rep, (lib, cells)),
            ),
            "clean": (f"rm -fr {str(drc_lib_dir)}",),
        }
