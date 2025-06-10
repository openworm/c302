from neuromllite import (
    Cell,
    InputSource,
)

from neuromllite.NetworkGenerator import check_to_generate_or_run
from neuromllite.utils import create_new_model
import sys

sys.path.append("..")


colors = {
    "GenericNeuronCell": "0 0 0.8",
    "GenericNeuronCellW2D": "0 0 0.8",
    "GenericMuscleCell": "0.8 0 0",
}


def generate(cell, duration=3000, config="IClamp", parameters=None):
    reference = "%s_%s" % (config, cell)

    cell_id = "%s" % cell

    if cell_id == "GenericNeuronCellW2D":
        cell_nmll = Cell(id=cell_id, lems_source_file="../../c302/cell_W2D.xml")
    else:
        cell_nmll = Cell(id=cell_id, neuroml2_source_file="%s.cell.nml" % (cell))

    ################################################################################
    ###   Add some inputs

    if "IClamp" in config:
        if not parameters:
            parameters = {}
            parameters["stim_amp"] = ".350"

        parameters["stim_delay"] = "2000ms"
        parameters["stim_duration"] = "6000ms"

        if cell_id != "GenericNeuronCellW2D":
            parameters["stim_delay"] = "500ms"
            parameters["stim_duration"] = "2000ms"
            input_source = InputSource(
                id="iclamp_0",
                neuroml2_input="PulseGenerator",
                parameters={
                    "amplitude": "stim_amp",
                    "delay": "stim_delay",
                    "duration": "stim_duration",
                },
            )
        else:
            input_source = InputSource(
                id="iclamp_0",
                neuroml2_input="PulseGenerator",
                parameters={
                    "amplitude": "stim_amp",
                    "delay": "stim_delay",
                    "duration": "stim_duration",
                },
            )

    else:
        if not parameters:
            parameters = {}
            parameters["average_rate"] = "100 Hz"
            parameters["number_per_cell"] = "10"

        """ Not yet tested..?
        input_source = InputSource(
            id="pfs0",
            neuroml2_input="PoissonFiringSynapse",
            parameters={
                "average_rate": "average_rate",
                "synapse": syn_exc.id,
                "spike_target": "./%s" % syn_exc.id,
            },
        )"""

    sim, net = create_new_model(
        reference,
        duration,
        dt=0.025,  # ms
        temperature=34,  # degC
        default_region="Worm",
        parameters=parameters,
        cell_for_default_population=cell_nmll,
        color_for_default_population=colors[cell],
        input_for_default_population=input_source,
    )

    if cell_id == "GenericNeuronCellW2D":
        sim.record_traces = {"all": "*"}
        sim.record_variables = {
            "state": {"all": "*"},
            "output": {"all": "*"},
        }

    # qprint(dir(sim))
    sim.to_json_file()

    return sim, net


if __name__ == "__main__":
    if "-all" in sys.argv:
        for cell in colors:
            generate(cell, 3000, config="IClamp", parameters={"stim_amp": "4pA"})

    elif "-w2d" in sys.argv:
        sim, net = generate(
            "GenericNeuronCellW2D",
            10000,
            config="IClamp",
            parameters={"stim_amp": "1pA"},
        )
        check_to_generate_or_run(sys.argv, sim)

    else:
        # sim, net = generate('cADpyr229_L23_PC_c292d67a2e_0_0', 3000, config="IClamp")
        sim, net = generate(
            "GenericMuscleCell", 3000, config="IClamp", parameters={"stim_amp": "4pA"}
        )
        check_to_generate_or_run(sys.argv, sim)

        sim, net = generate(
            "GenericNeuronCell", 3000, config="IClamp", parameters={"stim_amp": "4pA"}
        )

        check_to_generate_or_run(sys.argv, sim)
