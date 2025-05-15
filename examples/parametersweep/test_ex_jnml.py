from CanonicalCircuit import generate
from neuromllite.NetworkGenerator import check_to_generate_or_run

sim, net = generate(duration=3000, paramset="W2D")

check_to_generate_or_run(["-jnml"], sim)
