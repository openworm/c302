import c302
import sys
import neuroml.writers as writers
import importlib


def setup(
    parameter_set,
    generate=False,
    duration=1000,
    dt=0.05,
    target_directory="examples",
    data_reader="SpreadsheetDataReader",
    param_overrides={},
    verbose=True,
):
    ParameterisedModel = getattr(
        importlib.import_module("c302.parameters_%s" % parameter_set),
        "ParameterisedModel",
    )
    params = ParameterisedModel()

    my_cells = ["RIAL", "RIAR", "SMDDL", "SMDVL"]
    muscles_to_include = []

    cells = my_cells
    cells_total = my_cells + muscles_to_include

    reference = "c302_%s_RIA" % parameter_set
    nml_doc = None

    if generate:
        nml_doc = c302.generate(
            reference,
            params,
            cells=cells,
            cells_to_stimulate=muscles_to_include,
            muscles_to_include=muscles_to_include,
            duration=duration,
            dt=dt,
            target_directory=target_directory,
            param_overrides=param_overrides,
            verbose=verbose,
            data_reader=data_reader,
        )

        start1 = "100ms"
        dur1 = "100ms"
        stim_amplitude1 = "4pA"
        start2 = "400ms"
        dur2 = "100ms"
        stim_amplitude2 = "4pA"

        c302.add_new_input(nml_doc, "SMDDL", start1, dur1, stim_amplitude1, params)
        c302.add_new_input(nml_doc, "SMDVL", start2, dur2, stim_amplitude2, params)

        nml_file = target_directory + "/" + reference + ".net.nml"
        writers.NeuroMLWriter.write(
            nml_doc, nml_file
        )  # Write over network file written above...

        c302.print_("(Re)written network file to: " + nml_file)

    return cells, cells_total, params, muscles_to_include, nml_doc


if __name__ == "__main__":
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else "D1"

    setup(parameter_set, generate=True)
