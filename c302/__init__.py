#! /usr/bin/env python

from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import Population
from neuroml import Instance
from neuroml import IncludeType
from neuroml import Location
from neuroml import Input
from neuroml import InputList
from neuroml import Projection
from neuroml import Connection
from neuroml import ConnectionWD
from neuroml import ElectricalProjection
from neuroml import ElectricalConnectionInstanceW
from neuroml import ContinuousProjection
from neuroml import ContinuousConnectionInstanceW
from neuroml import Property
from neuroml import PulseGenerator
from neuroml import SineGenerator
from neuroml import SilentSynapse

import neuroml.writers as writers
import neuroml.loaders as loaders

# import c302.bioparameters

import airspeed

import random
import argparse
import shutil
import os
import logging
import importlib
import math
from lxml import etree
import re

import json


import collections

try:
    from owmeta_core import __version__ as owc_version
    from owmeta_core.bundle import Bundle
    from owmeta_core.context import Context
    from owmeta import __version__ as owmeta_version
    from owmeta.cell import Cell
    from owmeta.neuron import Neuron
    from owmeta.muscle import Muscle

    owmeta_installed = True

except Exception:
    print("owmeta not installed! Proceeding anyway...")
    owmeta_installed = False

try:
    from urllib2 import URLError  # Python 2
except Exception:
    from urllib.error import URLError  # Python 3

logging.basicConfig()

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "__version__.py")) as version_file:
    exec(version_file.read(), about)
__version__ = about["__version__"]

LEMS_TEMPLATE_FILE = "LEMS_c302_TEMPLATE.xml"

MUSCLE_RE = re.compile(r"M([VD][LR])(\d+)")

OWMETA_CACHED_DATA_FILE = (
    os.path.dirname(os.path.abspath(__file__)) + "/data/owmeta_cache.json"
)


def print_(msg, print_it=True):  # print_it=False when not verbose
    if print_it:
        pre = "c302      >>> "
        print("%s %s" % (pre, msg.replace("\n", "\n" + pre)))


def load_data_reader(data_reader="SpreadsheetDataReader"):
    """
    Imports and returns data reader module
    Args:
        data_reader (str): The name of the data reader
    Returns:
        reader (obj): The data reader object
    """
    return importlib.import_module("c302.%s" % data_reader)


def get_str_from_expnotation(num):
    """
    Returns a formatted string representing a floating point number, e.g. 1*0.00001 would result into 1e-05. Returning 0.00001.
    Args:
        num (float): A number. Can be of type int or float,  float can have exponential notation.
    Returns:
       (str): A string representing a float with 15 fractional digits.
    """
    return "{0:.15f}".format(num)


def get_muscle_position(muscle, data_reader="SpreadsheetDataReader"):
    if muscle == "MANAL" or muscle == "MVULVA":
        return 0, 0, 0
    # TODO: Pull these positions from openworm/owmeta-data
    pat1 = r"M([VD])([LR])(\d+)"
    pat2 = r"([VD])([LR])(\d+)"
    md = re.fullmatch(pat1, muscle)
    if not md:
        md = re.fullmatch(pat2, muscle)

    if md:
        dv = md.group(1)
        lr = md.group(2)
        idx = md.group(3)
        x = 80 * (1 if lr == "L" else -1)
        z = 80 * (-1 if dv == "V" else 1)
        y = -300 + 30 * int(idx)
        return x, y, z

    raise Exception("Unrecognized muscle name format %s" % muscle)


def is_muscle(cell_name):
    return MUSCLE_RE.fullmatch(cell_name)


def process_args():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        "c302",
        description="A script which can generate NeuroML2 compliant networks based on the C elegans connectome, along with LEMS files to run them",
    )

    parser.add_argument(
        "reference",
        type=str,
        metavar="<reference>",
        help="Unique reference for new network",
    )

    parser.add_argument(
        "parameters",
        type=str,
        metavar="<parameters>",
        help="Set of biophysical parametes to use, e.g. parameters_A",
    )

    parser.add_argument(
        "-datareader",
        type=str,
        metavar="<data-reader>",
        default="SpreadsheetDataReader",
        help='Use a specific data reader. Possible values are: "SpreadsheetDataReader". (default: SpreadsheetDataReader)',
    )

    parser.add_argument(
        "-cells",
        type=str,
        metavar="<cells>",
        default=None,
        help="List of cells to include in network (default: all)",
    )

    parser.add_argument(
        "-cellstoplot",
        type=str,
        metavar="<cells-to-plot>",
        default=None,
        help="List of cells to plot (default: all)",
    )

    parser.add_argument(
        "-cellstostimulate",
        type=str,
        metavar="<cells-to-stimulate>",
        default=None,
        help="List of cells to stimulate (default: all)",
    )

    parser.add_argument(
        "-connpolarityoverride",
        type=str,
        metavar="<conn-polarity-override>",
        default=None,
        help='Map of connection polarities to override, e.g. {"AVAL-AVBR":"inh", ...} => use inhibitory connection for AVAL-AVBR',
    )

    parser.add_argument(
        "-connnumberoverride",
        type=str,
        metavar="<conn-number-override>",
        default=None,
        help='Map of connection numbers to override, e.g. {"I1L-I3":2.5, "AVAR-AVBL_GJ":2} => use 2.5 connections from I1L to I3, use 2 connections for GJ AVAR-AVBL',
    )

    parser.add_argument(
        "-paramoverride",
        type=str,
        metavar="<param-override>",
        default=None,
        help='Map of parameters to override, e.g. {"unphysiological_offset_current":"2pA", ...} => use 2pA for additional offset currnet',
    )

    parser.add_argument(
        "-connnumberscaling",
        type=str,
        metavar="<conn-number-scaling>",
        default=None,
        help='Map of scaling factors for connection numbers, e.g. {"I1L-I3":2, "AVAR-AVBL_GJ":2} => use 2 times as many connections from I1L to I3, use 2 times as many connections for GJ AVAR-AVBL',
    )

    parser.add_argument(
        "-musclestoinclude",
        type=str,
        metavar="<muscles-to-include>",
        default=[],
        help="List of muscles to include (default: empty list, i.e. none)",
    )

    parser.add_argument(
        "-duration",
        type=float,
        metavar="<duration>",
        default=100,
        help="Duration of simulation in ms",
    )

    parser.add_argument(
        "-dt",
        type=float,
        metavar="<time step>",
        default=0.01,
        help="Timestep for simulations (dt) in ms",
    )

    parser.add_argument(
        "-vmin",
        type=float,
        metavar="<vmin>",
        default=-80,
        help="Minimum voltage for plot in mV",
    )

    parser.add_argument(
        "-vmax",
        type=float,
        metavar="<vmax>",
        default=-40,
        help="Maximum voltage for plot in mV",
    )

    return parser.parse_args()


quadrant0 = "MDR"
quadrant1 = "MVR"
quadrant2 = "MVL"
quadrant3 = "MDL"

# soma positions from http://www.wormatlas.org/neuronalwiring.html - 2.2 Neuron Description (Neuron Types)
VB_soma_pos = {
    "VB1": 0.21,
    "VB2": 0.19,
    "VB3": 0.28,
    "VB4": 0.32,
    "VB5": 0.38,
    "VB6": 0.45,
    "VB7": 0.5,
    "VB8": 0.57,
    "VB9": 0.61,
    "VB10": 0.67,
    "VB11": 0.72,
}

DB_soma_pos = {
    "DB1": 0.24,
    "DB2": 0.21,
    "DB3": 0.3,
    "DB4": 0.39,
    "DB5": 0.51,
    "DB6": 0.62,
    "DB7": 0.72,
}


def get_next_stim_id(nml_doc, cell):
    i = 1
    for stim in nml_doc.pulse_generators:
        if stim.id.startswith("%s_%s" % ("stim", cell)):
            i += 1
    id = "%s_%s_%s" % ("stim", cell, i)
    return id


def get_cell_position(cell):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    # cell_file_path = root_dir + "/../../../" if test else root_dir + "/../../"  # if running test
    cell_file_path = root_dir + "/"
    cell_file = cell_file_path + "NeuroML2/%s.cell.nml" % cell
    doc = loaders.NeuroMLLoader.load(cell_file)
    location = doc.cells[0].morphology.segments[0].proximal
    # print "%s, %s, %s" %(location.x, location.y, location.z)
    return location


def append_input_to_nml_input_list(stim, nml_doc, cell, params):
    target = get_cell_id_string(cell, params, muscle=is_muscle(cell))

    input_list = InputList(
        id="Input_%s_%s" % (cell, stim.id), component=stim.id, populations="%s" % cell
    )

    input_list.input.append(Input(id=0, target=target, destination="synapses"))

    nml_doc.networks[0].input_lists.append(input_list)


def add_new_sinusoidal_input(nml_doc, cell, delay, duration, amplitude, period, params):
    id = get_next_stim_id(nml_doc, cell)

    if cell.startswith("VB"):
        phase = VB_soma_pos[cell]
    else:
        phase = DB_soma_pos[cell]
    # phase = get_cell_position(cell).x
    phase = phase * -0.886
    print_("### CELL %s PHASE: %s" % (cell, phase))

    if cell.startswith("VB"):
        if amplitude.startswith("-"):
            amplitude = amplitude[1:]
        else:
            amplitude = "-" + amplitude

    input = SineGenerator(
        id=id,
        delay=delay,
        phase=phase,
        duration=duration,
        amplitude=amplitude,
        period=period,
    )
    nml_doc.sine_generators.append(input)

    append_input_to_nml_input_list(input, nml_doc, cell, params)


def add_new_input(nml_doc, cell, delay, duration, amplitude, params):
    id = get_next_stim_id(nml_doc, cell)
    input = PulseGenerator(id=id, delay=delay, duration=duration, amplitude=amplitude)
    nml_doc.pulse_generators.append(input)

    append_input_to_nml_input_list(input, nml_doc, cell, params)


def get_muscle_names():
    names = []
    for i in range(24):
        names.append("%s%s" % (quadrant0, i + 1 if i > 8 else ("0%i" % (i + 1))))
    for i in range(24):
        names.append("%s%s" % (quadrant1, i + 1 if i > 8 else ("0%i" % (i + 1))))
    for i in range(24):
        names.append("%s%s" % (quadrant2, i + 1 if i > 8 else ("0%i" % (i + 1))))
    for i in range(24):
        names.append("%s%s" % (quadrant3, i + 1 if i > 8 else ("0%i" % (i + 1))))

    return names


def merge_with_template(model, templfile):
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)


def write_to_file(
    nml_doc,
    lems_info,
    reference,
    template_path="",
    validate=True,
    verbose=True,
    target_directory=".",
):
    #######   Write to file  ######

    nml_file = target_directory + "/" + reference + ".net.nml"
    print_("Writing generated network to: %s" % os.path.realpath(nml_file))
    writers.NeuroMLWriter.write(nml_doc, nml_file)

    if verbose:
        print_("Written network file to: " + nml_file)

    lems_file_name = target_directory + "/" + "LEMS_%s.xml" % reference
    with open(lems_file_name, "w") as lems:
        # if running unittest concat template_path
        merged = merge_with_template(lems_info, template_path + LEMS_TEMPLATE_FILE)
        lems.write(merged)

    if verbose:
        print_("Written LEMS file to: " + lems_file_name)

    if validate:
        ###### Validate the NeuroML ######

        from neuroml.utils import validate_neuroml2

        try:
            validate_neuroml2(nml_file)
        except URLError:
            print_("Problem validating against remote Schema!")


# Get the standard name for a network connection
def get_projection_id(pre, post, synclass, syntype):
    proj_id = "NC_%s_%s_%s" % (pre, post, synclass)
    """
    if "GapJunction" in syntype:
       proj_id += '_GJ' """

    return proj_id


def get_random_colour_hex():
    rgb = [
        hex(random.randint(0, 256)),
        hex(random.randint(0, 256)),
        hex(random.randint(0, 256)),
    ]
    col = "#"
    for c in rgb:
        col += c[2:4] if len(c) == 4 else "00"
    return col


def get_file_name_relative_to_c302(file_name):
    if "C302_HOME" in os.environ:
        return os.path.relpath(os.environ["C302_HOME"], file_name)


def get_cell_names_and_connection(data_reader="SpreadsheetDataReader", test=False):
    # Use the spreadsheet reader to give a list of all cells and a list of all connections
    # This could be replaced with a call to "DatabaseReader" or "OpenWormNeuroLexReader" in future...
    # If called from unittest folder ammend path to "../../../../"

    cell_names, conns = load_data_reader(data_reader).read_data(
        include_nonconnected_cells=True
    )

    cell_names.sort()

    return cell_names, conns


def get_cell_muscle_names_and_connection(
    data_reader="SpreadsheetDataReader", test=False
):
    mneurons, all_muscles, muscle_conns = load_data_reader(
        data_reader
    ).read_muscle_data()
    if "MANAL" in all_muscles:
        all_muscles.remove("MANAL")
    if "MVULVA" in all_muscles:
        all_muscles.remove("MVULVA")
    return mneurons, sorted(all_muscles), muscle_conns


def is_cond_based_cell(params):
    return params.is_level_C() or params.is_level_D()


def get_cell_id_string(cell, params, muscle=False):
    if cell in get_muscle_names():
        muscle = True
    if not params.is_level_D():
        if not muscle:
            return "../%s/0/%s" % (cell, params.generic_neuron_cell.id)
        else:
            return "../%s/0/%s" % (cell, params.generic_muscle_cell.id)

    else:
        if not muscle:
            return "../%s/0/%s" % (cell, cell)
        else:
            return "../%s/0/%s" % (cell, params.generic_muscle_cell.id)


def regex_match(pattern, str):
    return is_regex_string(pattern) and re.match(pattern, str)


def is_regex_string(str):
    return "^" in str and "$" in str


def elem_in_coll_matches_conn(coll, conn):
    for elem in coll:
        if regex_match(elem, conn):
            return True
    return False


cached_owmeta_data = None


def _get_cell_info(bnd, cells):
    global cached_owmeta_data
    # print('------ Getting the cell info for %s'%cells)
    all_neuron_info = collections.OrderedDict()
    all_muscle_info = collections.OrderedDict()

    if bnd is None:
        if cached_owmeta_data is None:
            print_("Loading owmeta cached data from: %s" % OWMETA_CACHED_DATA_FILE)
            with open(OWMETA_CACHED_DATA_FILE) as f:
                cached_owmeta_data = json.load(f)

        for cell in cells:
            if is_muscle(cell):
                all_muscle_info[cell] = cached_owmeta_data["muscle_info"][cell]
            else:
                all_neuron_info[cell] = cached_owmeta_data["neuron_info"][cell]

    else:
        ctx = bnd(Context)(ident="http://openworm.org/data").stored
        # Go through our list and get the neuron object associated with each name.
        # Store these in another list.
        fixed_up_names = []
        for name in cells:
            match = is_muscle(name)
            if match:
                name = match.group(1) + str(int(match.group(2)))
            fixed_up_names.append(name)
        # fixed_up_names.remove('MANAL')
        # fixed_up_names.remove('MVULVA')

        for name in fixed_up_names:
            cell = next(ctx(Cell).query(name=name).load(), None)
            if cell is None:
                # print_("No matching cell for %s" % name)
                continue

            normalized_name = cell.name()
            short = ") %s" % normalized_name
            color = ".5 0 0"
            if isinstance(cell, Neuron):
                neuron_types = cell.type()
                if "sensory" in neuron_types:
                    short = "Se%s" % short
                    color = "1 .2 1"
                if "interneuron" in neuron_types:
                    short = "In%s" % short
                    color = "1 0 .4"
                if "motor" in neuron_types:
                    short = "Mo%s" % short
                    color = ".5 .4 1"

                neurotransmitter = cell.neurotransmitter()
            elif isinstance(cell, Muscle):
                neuron_types = ()
                neurotransmitter = ()
                color = "0 0.6 0"
                short = "Mu%s" % short
            else:
                # At this point, we should only have Neurons and Muscles because the reader
                # filters them out
                raise Exception("Got an unexpected cell type")

            short = "(%s" % short
            receptor = cell.receptor()
            if "GABA" in neurotransmitter:
                short = "- %s" % short
            elif len(neurotransmitter) == 0:
                short = "? %s" % short
            else:
                short = "+ %s" % short

            info = (cell, neuron_types, receptor, neurotransmitter, short, color)

            if isinstance(cell, Muscle):
                all_muscle_info[cell.name()] = info
            elif isinstance(cell, Neuron):
                all_neuron_info[cell.name()] = info

    # print('==== Returning %s; %s'%(all_neuron_info, all_muscle_info))
    return all_neuron_info, all_muscle_info


def set_param(params, param, value):
    v = params.get_bioparameter(param, warn_if_missing=False)
    if v:
        if v == value:
            return
        print_("Setting parameter %s = %s" % (param, value))
        params.set_bioparameter(param, value, "Set with param_overrides", 0)
    else:
        print_("Adding parameter %s = %s" % (param, value))
        params.add_bioparameter(param, value, "Add with param_overrides", 0)


def mirror_param(params, k, v):
    pattern = k.split("_")
    pre = pattern[0]
    pattern[0] = "%s"
    post = pattern[2]
    pattern[2] = "%s"
    tmp_param = pattern[5]
    pattern[5] = "%s"
    pattern = "_".join(pattern)

    override_key1 = pattern % (pre, post, tmp_param)
    override_key2 = pattern % (post, pre, tmp_param)

    set_param(params, override_key1, v)
    set_param(params, override_key2, v)


def generate(
    net_id,
    params,
    data_reader="SpreadsheetDataReader",
    cells=None,
    cells_to_plot=None,
    cells_to_stimulate=None,
    muscles_to_include=[],
    conns_to_include=[],
    conns_to_exclude=[],
    conn_number_override=None,
    conn_number_scaling=None,
    conn_polarity_override=None,
    duration=500,
    dt=0.01,
    vmin=None,
    vmax=None,
    seed=1234,
    test=False,
    verbose=True,
    print_connections=False,
    param_overrides={},
    target_directory="./",
):
    validate = not (
        params.is_level_B()
        or params.is_level_C0()
        or params.is_level_C2
        or params.is_level_D1()
    )

    root_dir = os.path.dirname(os.path.abspath(__file__))

    regex_param_overrides = {"mirrored_elec_conn_params": {}}
    if param_overrides:
        for k, v in param_overrides.items():
            if k == "mirrored_elec_conn_params":
                for mk, mv in v.items():
                    if is_regex_string(mk):
                        regex_param_overrides["mirrored_elec_conn_params"][mk] = mv
                        continue
                    else:
                        mirror_param(params, mk, mv)

            elif k == "custom_component_type_gate_overrides":
                continue  # channel params

            elif is_regex_string(k):
                regex_param_overrides[k] = v
                continue  # Add specific param later (e.g. add 'AVB.-DB\d+_elec_syn_gbase' during connection parsing)
            else:
                set_param(params, k, v)

    params.create_models()

    if vmin is None:
        if params.is_level_A() or params.is_level_B():
            vmin = -52
        elif params.is_level_C():
            vmin = -60
        elif params.is_level_D():
            vmin = -60
        else:
            vmin = -52

    if vmax is None:
        if params.is_level_A() or params.is_level_B():
            vmax = -28
        elif params.is_level_C():
            vmax = 25
        elif params.is_level_D():
            vmax = 25
        else:
            vmax = -28

    random.seed(seed)

    info = (
        "\n\nParameters and setting used to generate this network:\n\n"
        + "    Data reader:                    %s\n" % data_reader
        + "    c302 version:                   %s\n" % __version__
        + "    owmeta version:                 %s\n"
        % ("- not installed -" if not owmeta_installed else owmeta_version)
        + "    owmeta_core version:            %s\n"
        % ("- not installed -" if not owmeta_installed else owc_version)
        + "    Cells:                          %s\n"
        % (cells if cells is not None else "All cells")
        + "    Cell stimulated:                %s\n"
        % (cells_to_stimulate if cells_to_stimulate is not None else "All neurons")
        + "    Connection:                     %s\n"
        % (conns_to_include if conns_to_include is not None else "All connections")
        + "    Connection numbers overridden:  %s\n"
        % (conn_number_override if conn_number_override is not None else "None")
        + "    Connection numbers scaled:      %s\n"
        % (conn_number_scaling if conn_number_scaling is not None else "None")
        + "    Connection polarities override: %s\n" % conn_polarity_override
        + "    Muscles:                        %s\n"
        % (muscles_to_include if muscles_to_include is not None else "All muscles")
    )

    info_settings = info
    if verbose:
        print_(info)
    info += "\n%s\n" % (params.bioparameter_info("    "))

    nml_doc = NeuroMLDocument(id=net_id, notes=info)

    if params.is_level_A() or params.is_level_B() or params.level == "BC1":
        nml_doc.iaf_cells.append(params.generic_muscle_cell)
        nml_doc.iaf_cells.append(params.generic_neuron_cell)
    elif params.is_level_C():
        nml_doc.cells.append(params.generic_muscle_cell)
        nml_doc.cells.append(params.generic_neuron_cell)
    elif params.is_level_D():
        nml_doc.cells.append(params.generic_muscle_cell)
    elif params.is_level_X():
        nml_doc.cells.append(params.generic_muscle_cell)
        nml_doc.cells.append(params.generic_neuron_cell)

    net = Network(id=net_id)

    nml_doc.networks.append(net)

    net.properties.append(Property("recommended_duration_ms", duration))
    net.properties.append(Property("recommended_dt_ms", dt))

    nml_doc.pulse_generators.append(params.offset_current)

    if is_cond_based_cell(params):
        if isinstance(params.concentration_model, list):
            nml_doc.fixed_factor_concentration_models.extend(params.concentration_model)
        else:
            nml_doc.fixed_factor_concentration_models.append(params.concentration_model)

    cell_names, conns = get_cell_names_and_connection(data_reader)

    # To hold all Cell NeuroML objects vs. names
    all_cells = {}

    # lems_file = ""
    lems_info = {
        "comment": info,
        "reference": net_id,
        "duration": duration,
        "dt": dt,
        "vmin": vmin,
        "vmax": vmax,
    }

    lems_info["plots"] = []
    lems_info["activity_plots"] = []
    lems_info["muscle_plots"] = []
    lems_info["muscle_activity_plots"] = []

    lems_info["to_save"] = []
    lems_info["activity_to_save"] = []
    lems_info["muscles_to_save"] = []
    lems_info["muscles_activity_to_save"] = []
    lems_info["cells"] = []
    lems_info["muscles"] = []
    lems_info["includes"] = []

    if params.custom_component_types_definitions:
        if isinstance(params.custom_component_types_definitions, str):
            params.custom_component_types_definitions = [
                params.custom_component_types_definitions
            ]
        for ctd in params.custom_component_types_definitions:
            if target_directory != "./":
                # def_file = './%s' % ctd
                def_file = "%s/%s" % (os.path.dirname(os.path.abspath(__file__)), ctd)

                if (
                    param_overrides
                    and "custom_component_type_gate_overrides" in param_overrides
                    and param_overrides["custom_component_type_gate_overrides"]
                ):
                    root = etree.parse(def_file).getroot()

                    for k, v in param_overrides[
                        "custom_component_type_gate_overrides"
                    ].items():
                        channel_id = k.split("__")[0]
                        gate_id = k.split("__")[1]
                        gate_attr = k.split("__")[2]

                        for c1 in root:
                            if (
                                c1.tag != "ionChannel"
                                and c1.attrib.get("id") != channel_id
                            ):
                                continue
                            for c2 in c1:
                                if (
                                    c2.tag != "gateHHtauInf"
                                    and c2.attrib.get("id") != gate_id
                                ):
                                    continue
                                for child in c2:
                                    if child.attrib.get(gate_attr):
                                        child.set(gate_attr, v)
                    etree.ElementTree(root).write(
                        os.path.join(target_directory, ctd), pretty_print=True
                    )
                else:
                    shutil.copy(def_file, target_directory)

            if target_directory == "./" and not os.path.isfile(ctd):
                ctd = "%s/%s" % (os.path.dirname(__file__), ctd)

            lems_info["includes"].append(ctd)
            nml_doc.includes.append(IncludeType(href=ctd))

    import c302.backers

    cells_vs_name = c302.backers.get_adopted_cell_names()

    count = 0

    try:
        with Bundle("openworm/owmeta-data", version=6) as bnd:
            all_neuron_info, all_muscle_info = _get_cell_info(bnd, set(cell_names))
    except Exception as e:
        print_('Unable to open "openworm/owmeta-data" bundle: %s' % e)
        all_neuron_info, all_muscle_info = _get_cell_info(None, set(cell_names))

    for cell in cell_names:
        if cells is None or cell in cells:
            inst = Instance(id="0")

            if not params.is_level_D():
                # build a Population data structure out of the cell name
                pop0 = Population(
                    id=cell,
                    component=params.generic_neuron_cell.id,
                    type="populationList",
                    size="1",
                )
                cell_id = params.generic_neuron_cell.id
            else:
                # build a Population data structure out of the cell name
                pop0 = Population(
                    id=cell, component=cell, type="populationList", size="1"
                )
                cell_id = cell

            # neuron, neuron.type(), neuron.receptor(), neuron.neurotransmitter(), short, color
            if all_neuron_info is not None:
                pop0.properties.append(Property("color", all_neuron_info[cell][5]))
                types = sorted(all_neuron_info[cell][1])
                pop0.properties.append(Property("type", str("; ".join(types))))
                recps = sorted(all_neuron_info[cell][2])
                pop0.properties.append(Property("receptor", str("; ".join(recps))))
                nt_sorted = sorted(all_neuron_info[cell][3])
                pop0.properties.append(
                    Property("neurotransmitter", str("; ".join(nt_sorted)))
                )

            pop0.instances.append(inst)

            # put that Population into the Network data structure from above
            net.populations.append(pop0)

            if cell in cells_vs_name:
                p = Property(
                    tag="OpenWormBackerAssignedName", value=cells_vs_name[cell]
                )
                pop0.properties.append(p)

            # also use the cell name to grab the morphology file, as a NeuroML data structure
            #  into the 'all_cells' dict
            cell_file_path = (
                root_dir + "/../" if test else root_dir + "/"
            )  # if running test
            cell_file = cell_file_path + "NeuroML2/%s.cell.nml" % cell
            doc = loaders.NeuroMLLoader.load(cell_file)
            all_cells[cell] = doc.cells[0]

            if params.is_level_D():
                new_cell = params.create_neuron_cell(cell, doc.cells[0].morphology)

                nml_cell_doc = NeuroMLDocument(id=cell)
                nml_cell_doc.cells.append(new_cell)
                new_cell_file = "cells/" + cell + "_D.cell.nml"
                nml_file = target_directory + "/" + new_cell_file
                print_("Writing new cell to: %s" % os.path.realpath(nml_file))
                writers.NeuroMLWriter.write(nml_cell_doc, nml_file)

                nml_doc.includes.append(IncludeType(href=new_cell_file))
                lems_info["includes"].append(new_cell_file)

                inst.location = Location(0, 0, 0)
            else:
                location = doc.cells[0].morphology.segments[0].proximal

                inst.location = Location(
                    float(location.x), float(location.y), float(location.z)
                )

            if verbose:
                print_(
                    "Loaded morphology: %s; id: %s; placing at location: (%s, %s, %s)"
                    % (
                        os.path.realpath(cell_file),
                        all_cells[cell].id,
                        inst.location.x,
                        inst.location.y,
                        inst.location.z,
                    )
                )

            if cells_to_stimulate is None or cell in cells_to_stimulate:
                target = "../%s/0/%s" % (pop0.id, cell_id)

                input_list = InputList(
                    id="Input_%s_%s" % (cell, params.offset_current.id),
                    component=params.offset_current.id,
                    populations="%s" % cell,
                )

                i0 = Input(id=0, target=target, destination="synapses")

                if params.is_level_D():
                    i0.segment_id = 0

                input_list.input.append(i0)

                net.input_lists.append(input_list)

            if cells_to_plot is None or cell in cells_to_plot:
                plot = {}

                plot["cell"] = cell
                plot["colour"] = get_random_colour_hex()
                plot["quantity"] = "%s/0/%s/v" % (cell, cell_id)
                lems_info["plots"].append(plot)

                if params.is_level_B():
                    plot = {}

                    plot["cell"] = cell
                    plot["colour"] = get_random_colour_hex()
                    plot["quantity"] = "%s/0/%s/activity" % (cell, cell_id)
                    lems_info["activity_plots"].append(plot)

                if is_cond_based_cell(params):
                    plot = {}

                    plot["cell"] = cell
                    plot["colour"] = get_random_colour_hex()
                    plot["quantity"] = "%s/0/%s/caConc" % (cell, cell_id)
                    lems_info["activity_plots"].append(plot)

            save = {}
            save["cell"] = cell
            save["quantity"] = "%s/0/%s/v" % (cell, cell_id)
            lems_info["to_save"].append(save)

            if params.is_level_B():
                save = {}
                save["cell"] = cell
                save["quantity"] = "%s/0/%s/activity" % (cell, cell_id)
                lems_info["activity_to_save"].append(save)
            if is_cond_based_cell(params):
                save = {}
                save["cell"] = cell
                save["quantity"] = "%s/0/%s/caConc" % (cell, cell_id)
                lems_info["activity_to_save"].append(save)

            lems_info["cells"].append(cell)

            count += 1

    if verbose:
        print_("Finished loading %i cells" % count)

    mneurons, all_muscles, muscle_conns = get_cell_muscle_names_and_connection(
        data_reader
    )

    # print(all_muscles)
    # if data_reader == "SpreadsheetDataReader":
    #    all_muscles = get_muscle_names()

    if muscles_to_include is None or muscles_to_include is True:
        muscles_to_include = all_muscles
    elif muscles_to_include is False:
        muscles_to_include = []

    for m in muscles_to_include:
        if m not in all_muscles:
            raise Exception("%s is not among the known muscles" % m)

    if len(muscles_to_include) > 0:
        muscle_count = 0
        for muscle in muscles_to_include:
            inst = Instance(id="0")

            # build a Population data structure out of the cell name
            pop0 = Population(
                id=muscle,
                component=params.generic_muscle_cell.id,
                type="populationList",
                size="1",
            )
            pop0.properties.append(Property("color", "0 .6 0"))
            pop0.instances.append(inst)

            # put that Population into the Network data structure from above
            net.populations.append(pop0)

            if muscle in cells_vs_name:
                # No muscles adopted yet, but just in case they are in future...
                p = Property(
                    tag="OpenWormBackerAssignedName", value=cells_vs_name[muscle]
                )
                pop0.properties.append(p)

            x, y, z = get_muscle_position(muscle, data_reader)
            # print_('Positioning muscle: %s at (%s,%s,%s)'%(muscle,x,y,z))
            inst.location = Location(x, y, z)

            # target = "%s/0/%s"%(pop0.id, params.generic_muscle_cell.id) # unused

            plot = {}

            plot["cell"] = muscle
            plot["colour"] = get_random_colour_hex()
            plot["quantity"] = "%s/0/%s/v" % (muscle, params.generic_muscle_cell.id)
            lems_info["muscle_plots"].append(plot)

            if params.generic_muscle_cell.__class__.__name__ == "IafActivityCell":
                plot = {}

                plot["cell"] = muscle
                plot["colour"] = get_random_colour_hex()
                plot["quantity"] = "%s/0/%s/activity" % (
                    muscle,
                    params.generic_muscle_cell.id,
                )
                lems_info["muscle_activity_plots"].append(plot)

            if params.generic_muscle_cell.__class__.__name__ == "Cell":
                plot = {}

                plot["cell"] = muscle
                plot["colour"] = get_random_colour_hex()
                plot["quantity"] = "%s/0/%s/caConc" % (
                    muscle,
                    params.generic_muscle_cell.id,
                )
                lems_info["muscle_activity_plots"].append(plot)

            save = {}
            save["cell"] = muscle
            save["quantity"] = "%s/0/%s/v" % (muscle, params.generic_muscle_cell.id)
            lems_info["muscles_to_save"].append(save)

            if params.generic_muscle_cell.__class__.__name__ == "IafActivityCell":
                save = {}
                save["cell"] = muscle
                save["quantity"] = "%s/0/%s/activity" % (
                    muscle,
                    params.generic_muscle_cell.id,
                )
                lems_info["muscles_activity_to_save"].append(save)
            if params.generic_muscle_cell.__class__.__name__ == "Cell":
                save = {}
                save["cell"] = muscle
                save["quantity"] = "%s/0/%s/caConc" % (
                    muscle,
                    params.generic_muscle_cell.id,
                )
                lems_info["muscles_activity_to_save"].append(save)

            lems_info["muscles"].append(muscle)

            muscle_count += 1

            if cells_to_stimulate is not None and muscle in cells_to_stimulate:
                target = "../%s/0/%s" % (pop0.id, params.generic_muscle_cell.id)

                input_list = InputList(
                    id="Input_%s_%s" % (muscle, params.offset_current.id),
                    component=params.offset_current.id,
                    populations="%s" % pop0.id,
                )

                i0 = Input(id=0, target=target, destination="synapses")

                if params.is_level_D():
                    i0.segment_id = 0

                input_list.input.append(i0)

                net.input_lists.append(input_list)

        if verbose:
            print_("Finished creating %i muscles" % muscle_count)

    existing_synapses = {}

    for conn in conns:
        if conn.pre_cell in lems_info["cells"] and conn.post_cell in lems_info["cells"]:
            # take information about each connection and package it into a
            # NeuroML Projection data structure
            proj_id = get_projection_id(
                conn.pre_cell, conn.post_cell, conn.synclass, conn.syntype
            )
            conn_shorthand = "%s-%s" % (conn.pre_cell, conn.post_cell)

            elect_conn = False
            analog_conn = False

            conn_type = "neuron_to_neuron"
            conn_pol = "exc"

            orig_pol = "exc"

            if "GABA" in conn.synclass:
                conn_pol = "inh"
                orig_pol = "inh"
            if "_GJ" in conn.synclass:
                conn_pol = "elec"
                elect_conn = params.is_elec_conn(params.neuron_to_neuron_elec_syn)
                conn_shorthand = "%s-%s_GJ" % (conn.pre_cell, conn.post_cell)

            for key in regex_param_overrides.keys():
                if key == "mirrored_elec_conn_params":
                    continue

                pattern = key.split("$")[0] + "$"
                pattern = pattern.replace("_to_", "-")

                if re.match(pattern, conn_shorthand):
                    new_param = conn_shorthand.replace("-", "_to_") + key.split("$")[1]
                    new_param = new_param.replace("_GJ", "")
                    new_param_v = regex_param_overrides[key]

                    if new_param in param_overrides:
                        continue
                    # add regex param unless there is a specific param
                    set_param(params, new_param, new_param_v)

            if "mirrored_elec_conn_params" in regex_param_overrides:
                for k, v in regex_param_overrides["mirrored_elec_conn_params"].items():
                    pattern = k.split("$")[0] + "$"
                    pattern = pattern.replace("_to_", "-")

                    if re.match(pattern, conn_shorthand):
                        new_param = (
                            conn_shorthand.replace("-", "_to_") + k.split("$")[1]
                        )
                        new_param = new_param.replace("_GJ", "")
                        new_param_mirrored = (
                            conn.post_cell
                            + "_"
                            + new_param.split("_")[1]
                            + "_"
                            + conn.pre_cell
                            + "_"
                            + "_".join(new_param.split("_")[3:])
                        )
                        new_param_v = v

                        if (
                            new_param in param_overrides["mirrored_elec_conn_params"]
                            or new_param_mirrored
                            in param_overrides["mirrored_elec_conn_params"]
                        ):
                            continue
                        # add regex param unless there is a specific param
                        mirror_param(params, new_param, new_param_v)

            if conns_to_include and conn_shorthand not in conns_to_include:
                # conn_shorthand not in conns_to_include. if there is a regex in conns_to_include which matches the current conn_shorthand -> include
                if not elem_in_coll_matches_conn(conns_to_include, conn_shorthand):
                    continue
            if conns_to_exclude:
                if conn_shorthand in conns_to_exclude:
                    continue
                # conn_shorthand not in conns_to_exclude. if there is a regex in conns_to_exclude which matches the current conn_shorthand -> exclude
                if elem_in_coll_matches_conn(conns_to_exclude, conn_shorthand):
                    continue

            syn0 = params.get_syn(conn.pre_cell, conn.post_cell, conn_type, conn_pol)

            if print_connections:
                print_(
                    conn_shorthand
                    + " "
                    + str(conn.number)
                    + " "
                    + orig_pol
                    + " "
                    + conn.synclass
                    + " "
                    + syn0.id
                )

            polarity = None
            if conn_polarity_override:
                # if elem_in_coll_matches_conn(conn_polarity_override.keys(), conn_shorthand):
                for conn_pol in conn_polarity_override.keys():
                    if conn_pol == conn_shorthand:
                        polarity = conn_polarity_override[conn_shorthand]
                        break
                    elif regex_match(conn_pol, conn_shorthand):
                        polarity = conn_polarity_override[conn_pol]
                        break
            if polarity and not elect_conn:
                syn0 = params.get_syn(
                    conn.pre_cell, conn.post_cell, conn_type, polarity
                )
                if verbose and polarity != orig_pol:
                    print_(
                        ">> Changing polarity of connection %s -> %s: was: %s, becomes %s "
                        % (conn.pre_cell, conn.post_cell, orig_pol, polarity)
                    )

            if params.is_analog_conn(syn0):
                analog_conn = True
                if len(nml_doc.silent_synapses) == 0:
                    nml_doc.silent_synapses.append(SilentSynapse(id="silent"))

            number_syns = conn.number

            if params.get_bioparameter(
                "global_connectivity_power_scaling", warn_if_missing=False
            ):
                scale = params.get_bioparameter("global_connectivity_power_scaling").x()
                # print("Scaling by %s"%scale)
                number_syns = math.pow(number_syns, scale)

            if conn_number_override:
                # number_syns = conn_number_override[conn_shorthand]

                for conn_num_override in conn_number_override.keys():
                    if conn_num_override == conn_shorthand:
                        number_syns = conn_number_override[conn_shorthand]
                        break
                    elif regex_match(conn_num_override, conn_shorthand):
                        number_syns = conn_number_override[conn_num_override]
                        break
            if conn_number_scaling:
                # number_syns = conn.number*conn_number_scaling[conn_shorthand]

                for conn_num_scale in conn_number_scaling.keys():
                    if conn_num_scale == conn_shorthand:
                        number_syns = conn.number * conn_number_scaling[conn_shorthand]
                        break
                    elif regex_match(conn_num_scale, conn_shorthand):
                        number_syns = conn.number * conn_number_scaling[conn_num_scale]
                        break
            """
            else:
                print(conn_shorthand)
                print(conn_number_override)
                print(conn_number_scaling)"""
            """if polarity:
                print "%s %s num:%s" % (conn_shorthand, polarity, number_syns)
            elif elect_conn:
                print "%s num:%s" % (conn_shorthand, number_syns)
            else:
                print "%s %s num:%s" % (conn_shorthand, orig_pol, number_syns)"""

            if number_syns != conn.number:
                if analog_conn or elect_conn:
                    magnitude, unit = c302.bioparameters.split_neuroml_quantity(
                        syn0.conductance
                    )
                else:
                    magnitude, unit = c302.bioparameters.split_neuroml_quantity(
                        syn0.gbase
                    )
                cond0 = "%s%s" % (magnitude * conn.number, unit)
                cond1 = "%s%s" % (
                    get_str_from_expnotation(magnitude * number_syns),
                    unit,
                )
                gj = "" if not elect_conn else " GapJunction"
                if verbose:
                    print_(
                        ">> Changing number of effective synapses connection %s -> %s%s: was: %s (total cond: %s), becomes %s (total cond: %s)"
                        % (
                            conn.pre_cell,
                            conn.post_cell,
                            gj,
                            conn.number,
                            cond0,
                            number_syns,
                            cond1,
                        )
                    )

            # print "######## %s-%s %s %s" % (conn.pre_cell, conn.post_cell, conn.synclass, number_syns)
            # known_motor_prefixes = ["VA"]
            # if conn.pre_cell.startswith(tuple(known_motor_prefixes)) or conn.post_cell.startswith(tuple(known_motor_prefixes)):
            #    print "######### %s-%s %s %s" % (conn.pre_cell, conn.post_cell, number_syns, conn.synclass)

            syn_new = params.create_n_connection_synapse(
                syn0, number_syns, nml_doc, existing_synapses
            )

            if elect_conn:
                proj0 = ElectricalProjection(
                    id=proj_id,
                    presynaptic_population=conn.pre_cell,
                    postsynaptic_population=conn.post_cell,
                )

                net.electrical_projections.append(proj0)

                pre_cell_id = get_cell_id_string(conn.pre_cell, params)
                post_cell_id = get_cell_id_string(conn.post_cell, params)

                # print_("Conn %s -> %s"%(pre_cell_id,post_cell_id))

                # Add a Connection with the closest locations
                conn0 = ElectricalConnectionInstanceW(
                    id="0",
                    pre_cell=pre_cell_id,
                    post_cell=post_cell_id,
                    synapse=syn_new.id,
                    weight=number_syns,
                )

                proj0.electrical_connection_instance_ws.append(conn0)

            elif analog_conn:
                proj0 = ContinuousProjection(
                    id=proj_id,
                    presynaptic_population=conn.pre_cell,
                    postsynaptic_population=conn.post_cell,
                )

                net.continuous_projections.append(proj0)

                pre_cell_id = get_cell_id_string(conn.pre_cell, params)
                post_cell_id = get_cell_id_string(conn.post_cell, params)

                conn0 = ContinuousConnectionInstanceW(
                    id="0",
                    pre_cell=pre_cell_id,
                    post_cell=post_cell_id,
                    pre_component="silent",
                    post_component=syn_new.id,
                    weight=number_syns,
                )

                proj0.continuous_connection_instance_ws.append(conn0)

            else:
                proj0 = Projection(
                    id=proj_id,
                    presynaptic_population=conn.pre_cell,
                    postsynaptic_population=conn.post_cell,
                    synapse=syn_new.id,
                )

                net.projections.append(proj0)

                pre_cell_id = get_cell_id_string(conn.pre_cell, params)
                post_cell_id = get_cell_id_string(conn.post_cell, params)

                conn0 = ConnectionWD(
                    id="0",
                    pre_cell_id=pre_cell_id,
                    post_cell_id=post_cell_id,
                    weight=number_syns,
                    delay="0ms",
                )

                proj0.connection_wds.append(conn0)

    if len(muscles_to_include) > 0:
        for conn in muscle_conns:
            if conn.post_cell not in muscles_to_include:
                continue
            if (
                conn.pre_cell not in lems_info["cells"]
                and conn.pre_cell not in muscles_to_include
            ):
                continue

            # take information about each connection and package it into a
            # NeuroML Projection data structure
            proj_id = get_projection_id(
                conn.pre_cell, conn.post_cell, conn.synclass, conn.syntype
            )
            conn_shorthand = "%s-%s" % (conn.pre_cell, conn.post_cell)

            elect_conn = False
            analog_conn = False

            conn_type = "neuron_to_muscle"
            if conn.pre_cell in muscles_to_include:
                conn_type = "muscle_to_muscle"
            # if conn.post_cell in lems_info['cells']:
            #    conn_type = "muscle_to_neuron"
            conn_pol = "exc"
            orig_pol = "exc"

            if "GABA" in conn.synclass:
                conn_pol = "inh"
                orig_pol = "inh"

            if "_GJ" in conn.synclass:
                conn_pol = "elec"
                orig_pol = "elec"
                elect_conn = params.is_elec_conn(params.neuron_to_neuron_elec_syn)
                conn_shorthand = "%s-%s_GJ" % (conn.pre_cell, conn.post_cell)

            for key in regex_param_overrides.keys():
                if key == "mirrored_elec_conn_params":
                    continue

                pattern = key.split("$")[0] + "$"
                pattern = pattern.replace("_to_", "-")

                if re.match(pattern, conn_shorthand):
                    new_param = conn_shorthand.replace("-", "_to_") + key.split("$")[1]
                    new_param = new_param.replace("_GJ", "")
                    new_param_v = regex_param_overrides[key]

                    if new_param in param_overrides:
                        continue
                    # add regex param unless there is a specific param
                    set_param(params, new_param, new_param_v)

            if "mirrored_elec_conn_params" in regex_param_overrides:
                for k, v in regex_param_overrides["mirrored_elec_conn_params"].items():
                    pattern = k.split("$")[0] + "$"
                    pattern = pattern.replace("_to_", "-")

                    if re.match(pattern, conn_shorthand):
                        new_param = (
                            conn_shorthand.replace("-", "_to_") + k.split("$")[1]
                        )
                        new_param = new_param.replace("_GJ", "")
                        new_param_mirrored = (
                            conn.post_cell
                            + "_"
                            + new_param.split("_")[1]
                            + "_"
                            + conn.pre_cell
                            + "_"
                            + "_".join(new_param.split("_")[3:])
                        )
                        new_param_v = v

                        if (
                            new_param in param_overrides["mirrored_elec_conn_params"]
                            or new_param_mirrored
                            in param_overrides["mirrored_elec_conn_params"]
                        ):
                            continue
                        # add regex param unless there is a specific param
                        mirror_param(params, new_param, new_param_v)

            if conns_to_include and conn_shorthand not in conns_to_include:
                # conn_shorthand not in conns_to_include. if there is a regex in conns_to_include which matches the current conn_shorthand -> include
                if not elem_in_coll_matches_conn(conns_to_include, conn_shorthand):
                    continue
            if conns_to_exclude:
                if conn_shorthand in conns_to_exclude:
                    continue
                # conn_shorthand not in conns_to_exclude. if there is a regex in conns_to_exclude which matches the current conn_shorthand -> exclude
                if elem_in_coll_matches_conn(conns_to_exclude, conn_shorthand):
                    continue

            syn0 = params.get_syn(conn.pre_cell, conn.post_cell, conn_type, conn_pol)

            if print_connections:
                print_(
                    conn_shorthand
                    + " "
                    + str(conn.number)
                    + " "
                    + orig_pol
                    + " "
                    + conn.synclass
                )

            polarity = None
            if conn_polarity_override:
                for conn_pol in conn_polarity_override.keys():
                    if conn_pol == conn_shorthand:
                        polarity = conn_polarity_override[conn_pol]
                        break
                    elif regex_match(conn_pol, conn_shorthand):
                        polarity = conn_polarity_override[conn_pol]
                        break
            if polarity and not elect_conn:
                syn0 = params.get_syn(
                    conn.pre_cell, conn.post_cell, conn_type, polarity
                )
                if verbose and polarity != orig_pol:
                    print_(
                        ">> Changing polarity of connection %s -> %s: was: %s, becomes %s "
                        % (conn.pre_cell, conn.post_cell, orig_pol, polarity)
                    )

            if params.is_analog_conn(syn0):
                analog_conn = True
                if len(nml_doc.silent_synapses) == 0:
                    nml_doc.silent_synapses.append(SilentSynapse(id="silent"))

            number_syns = conn.number

            if params.get_bioparameter(
                "global_connectivity_power_scaling", warn_if_missing=False
            ):
                scale = params.get_bioparameter("global_connectivity_power_scaling").x()
                # print("Scaling by %s"%scale)
                number_syns = math.pow(number_syns, scale)

            if conn_number_override:
                for conn_num_override in conn_number_override.keys():
                    if conn_num_override == conn_shorthand:
                        number_syns = conn_number_override[conn_shorthand]
                        break
                    elif regex_match(conn_num_override, conn_shorthand):
                        number_syns = conn_number_override[conn_num_override]
                        break
            if conn_number_scaling:
                for conn_num_scale in conn_number_scaling.keys():
                    if conn_num_scale == conn_shorthand:
                        number_syns = conn.number * conn_number_scaling[conn_shorthand]
                        break
                    elif regex_match(conn_num_scale, conn_shorthand):
                        number_syns = conn.number * conn_number_scaling[conn_num_scale]
                        break
            """
            else:
                print(conn_shorthand)
                print(conn_number_override)
                print(conn_number_scaling)"""
            """if polarity:
                print "%s %s num:%s" % (conn_shorthand, polarity, number_syns)
            elif elect_conn:
                print "%s num:%s" % (conn_shorthand, number_syns)
            else:
                print "%s %s num:%s" % (conn_shorthand, orig_pol, number_syns)"""

            if number_syns != conn.number:
                if analog_conn or elect_conn:
                    magnitude, unit = c302.bioparameters.split_neuroml_quantity(
                        syn0.conductance
                    )
                else:
                    magnitude, unit = c302.bioparameters.split_neuroml_quantity(
                        syn0.gbase
                    )
                cond0 = "%s%s" % (magnitude * conn.number, unit)
                cond1 = "%s%s" % (
                    get_str_from_expnotation(magnitude * number_syns),
                    unit,
                )
                gj = "" if not elect_conn else " GapJunction"
                if verbose:
                    print_(
                        ">> Changing number of effective synapses connection %s -> %s%s: was: %s (total cond: %s), becomes %s (total cond: %s)"
                        % (
                            conn.pre_cell,
                            conn.post_cell,
                            gj,
                            conn.number,
                            cond0,
                            number_syns,
                            cond1,
                        )
                    )

            syn_new = params.create_n_connection_synapse(
                syn0, number_syns, nml_doc, existing_synapses
            )

            if elect_conn:
                proj0 = ElectricalProjection(
                    id=proj_id,
                    presynaptic_population=conn.pre_cell,
                    postsynaptic_population=conn.post_cell,
                )

                net.electrical_projections.append(proj0)

                pre_cell_id = get_cell_id_string(conn.pre_cell, params)
                post_cell_id = get_cell_id_string(conn.post_cell, params, muscle=True)

                # print_("Conn %s -> %s"%(pre_cell_id,post_cell_id))

                # Add a Connection with the closest locations
                conn0 = ElectricalConnectionInstanceW(
                    id="0",
                    pre_cell=pre_cell_id,
                    post_cell=post_cell_id,
                    synapse=syn_new.id,
                    weight=number_syns,
                )

                proj0.electrical_connection_instance_ws.append(conn0)

            elif analog_conn:
                proj0 = ContinuousProjection(
                    id=proj_id,
                    presynaptic_population=conn.pre_cell,
                    postsynaptic_population=conn.post_cell,
                )

                net.continuous_projections.append(proj0)

                pre_cell_id = get_cell_id_string(conn.pre_cell, params)
                post_cell_id = get_cell_id_string(conn.post_cell, params, muscle=True)

                conn0 = ContinuousConnectionInstanceW(
                    id="0",
                    pre_cell=pre_cell_id,
                    post_cell=post_cell_id,
                    pre_component="silent",
                    post_component=syn_new.id,
                    weight=number_syns,
                )

                proj0.continuous_connection_instance_ws.append(conn0)

            else:
                proj0 = Projection(
                    id=proj_id,
                    presynaptic_population=conn.pre_cell,
                    postsynaptic_population=conn.post_cell,
                    synapse=syn_new.id,
                )

                net.projections.append(proj0)

                # Add a Connection with the closest locations

                pre_cell_id = get_cell_id_string(conn.pre_cell, params)
                post_cell_id = get_cell_id_string(conn.post_cell, params, muscle=True)

                conn0 = Connection(
                    id="0", pre_cell_id=pre_cell_id, post_cell_id=post_cell_id
                )

                proj0.connections.append(conn0)

    if param_overrides and param_overrides.keys():
        info_new = info_settings + "\n%s\n" % (params.bioparameter_info("    "))
        nml_doc.notes = info_new
        lems_info["comment"] = info_new

    # import pprint
    # pprint.pprint(lems_info)
    template_path = root_dir + "/../" if test else root_dir + "/"  # if running test
    write_to_file(
        nml_doc,
        lems_info,
        net_id,
        template_path,
        validate=validate,
        verbose=verbose,
        target_directory=target_directory,
    )

    return nml_doc


"""
    Input:    string of form ["AVAL","AVBL"]
    returns:  ["AVAL", "AVBL"]
"""


def parse_list_arg(list_arg):
    if list_arg is None:
        return None
    if list_arg == []:
        return []
    entries = list_arg[1:-1].split(",")
    ret = [e for e in entries]
    print_("Command line argument %s parsed as: %s" % (list_arg, ret))
    return ret


"""
    Input:    string of form ["ADAL-AIBL":2.5,"I1L-I1R":0.5]
    returns:  {}
"""


def parse_dict_arg(dict_arg):
    if dict_arg is None or dict_arg == "None":
        return None
    ret = {}
    entries = str(dict_arg[1:-1]).split(",")
    for e in entries:
        try:
            ret[e.split(":")[0]] = float(e.split(":")[1])  # {'AVAL-AVAR':1}
        except ValueError:
            ret[e.split(":")[0]] = str(e.split(":")[1])  # {'AVAL-AVAR':'inh'}
    print_("Command line argument %s parsed as: %s" % (dict_arg, ret))
    return ret


def main():
    import importlib

    print("Starting c302 v%s..." % __version__)
    args = process_args()

    ParameterisedModel = getattr(
        importlib.import_module("c302.%s" % args.parameters),
        "ParameterisedModel",
    )
    params = ParameterisedModel()
    generate(
        args.reference,
        params,
        data_reader=args.datareader,
        cells=parse_list_arg(args.cells),
        cells_to_plot=parse_list_arg(args.cellstoplot),
        cells_to_stimulate=parse_list_arg(args.cellstostimulate),
        conn_polarity_override=parse_dict_arg(args.connpolarityoverride),
        conn_number_override=parse_dict_arg(args.connnumberoverride),
        conn_number_scaling=parse_dict_arg(args.connnumberscaling),
        muscles_to_include=parse_list_arg(args.musclestoinclude),
        param_overrides=parse_dict_arg(args.paramoverride),
        duration=args.duration,
        dt=args.dt,
        vmin=args.vmin,
        vmax=args.vmax,
    )


if __name__ == "__main__":
    import sys

    if "-cache" in sys.argv:
        print("Starting c302...")
        from c302.ConnectomeReader import PREFERRED_MUSCLE_NAMES
        from c302.ConnectomeReader import PREFERRED_NEURON_NAMES

        all_info = {"neuron_info": {}, "muscle_info": {}}

        from owmeta_core.bundle import Bundle

        from owmeta_core import __version__ as owc_version
        from owmeta import __version__ as owmeta_version

        ver_info = "owmeta v%s (owmeta core v%s)" % (owmeta_version, owc_version)
        all_info["comment"] = "Information exported from " + ver_info

        with Bundle("openworm/owmeta-data", version=6) as bnd:
            for n in PREFERRED_NEURON_NAMES:
                ani, _all_muscle_info = _get_cell_info(bnd, [n])

                print("  > %s; %s" % (ani[n], _all_muscle_info))
                all_info["neuron_info"][n] = (
                    str(ani[n][0]),
                    sorted(list(ani[n][1])),
                    sorted(list(ani[n][2])),
                    sorted(list(ani[n][3])),
                    ani[n][4],
                    ani[n][5],
                )

            for n in PREFERRED_MUSCLE_NAMES:
                _all_neuron_info, ami = _get_cell_info(bnd, [n])

                if not n == "MVULVA" and not n == "MANAL":
                    ow_name = n[1:] if n[3] != "0" else "%s%s" % (n[1:3], n[-1])
                    print("  > %s (%s): %s; %s" % (n, ow_name, _all_neuron_info, ami))

                    all_info["muscle_info"][n] = (
                        str(ami[ow_name][0]),
                        sorted(list(ami[ow_name][1])),
                        sorted(list(ami[ow_name][2])),
                        sorted(list(ami[ow_name][3])),
                        ami[ow_name][4],
                        ami[ow_name][5],
                    )

        with open(OWMETA_CACHED_DATA_FILE, "w") as fp:
            json.dump(all_info, fp, sort_keys=True, indent=4)

    else:
        main()
