import c302
import sys
import importlib
import neuroml.writers as writers


def setup(
    parameter_set,
    generate=False,
    duration=3000,
    dt=0.05,
    target_directory="examples",
    data_reader=c302.DEFAULT_DATA_READER,
    param_overrides={},
    config_param_overrides={},
    verbose=True,
):
    ParameterisedModel = getattr(
        importlib.import_module("c302.parameters_%s" % parameter_set),
        "ParameterisedModel",
    )

    params = ParameterisedModel()

    params.set_bioparameter(
        "unphysiological_offset_current", "15pA", "Testing IClamp", "0"
    )
    params.set_bioparameter(
        "unphysiological_offset_current_del", "1 ms", "Testing IClamp", "0"
    )
    params.set_bioparameter(
        "unphysiological_offset_current_dur", "20 ms", "Testing IClamp", "0"
    )

    my_cells = ["AVKR"]
    my_cells = ["RMHR", "DA9", "VA1"]
    muscles_to_include = None

    cells = my_cells

    reference = "c302_%s_TargetMuscle" % parameter_set

    nml_doc = None

    if generate:
        nml_doc = c302.generate(
            reference,
            params,
            cells=cells,
            cells_to_stimulate=[],
            muscles_to_include=muscles_to_include,
            duration=duration,
            dt=dt,
            target_directory=target_directory,
            param_overrides=param_overrides,
            verbose=verbose,
            data_reader=data_reader,
            print_connections=True,
        )

        stim_amplitudes = ["25pA", "25pA", "25pA"]
        start_times = ["10ms", "100ms", "200ms"]

        for i in range(len(stim_amplitudes)):
            start = start_times[i]
            c = my_cells[i]

            c302.add_new_input(nml_doc, c, start, "10ms", stim_amplitudes[i], params)

        nml_file = target_directory + "/" + reference + ".net.nml"
        writers.NeuroMLWriter.write(
            nml_doc, nml_file
        )  # Write over network file written above...

    return cells, cells, params, muscles_to_include, nml_doc


if __name__ == "__main__":
    parameter_set = sys.argv[1] if len(sys.argv) == 2 else "A"

    setup(parameter_set, generate=True)
