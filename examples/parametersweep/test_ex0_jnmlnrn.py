from GenerateExamples import generate
from neuromllite.NetworkGenerator import check_to_generate_or_run

sim, net = generate(
    "GenericNeuronCellW2D",
    10000,
    config="IClamp",
    parameters={"stim_amp": "1pA"},
)

check_to_generate_or_run(["-jnmlnrn"], sim)
