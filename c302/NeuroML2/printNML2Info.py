import neuroml

import neuroml.loaders as loaders

import sys


nml2_files = []

if len(sys.argv) >=2:
    for i in range(1,len(sys.argv)):
        nml2_files.append(sys.argv[i])

print("")
for nml2_file in nml2_files:
    nml2_doc = loaders.NeuroMLLoader.load(nml2_file)

    print("-------- File: %s ----------"%nml2_file)

    for cell in nml2_doc.cells:
        print("  Cell: %s; %i segments"%(cell.id, len(cell.morphology.segments)))

    for exp_two_synapse in nml2_doc.exp_two_synapses:
        print("  Synapse: %s"%(exp_two_synapse.id))

    for gap_junction in nml2_doc.gap_junctions:
        print("  Electrical Synapse: %s"%(gap_junction.id))

    for network in nml2_doc.networks:
        print("  Network: %s"%(network.id))
        pops = []
        for pop in network.populations:
            pops.append(pop.id)

        print("    Populations (%i): %s"%(len(pops),pops))
        
        projs = []
        connections = 0
        for proj in network.projections:
            projs.append(proj.id)
            connections+=len(proj.connections)
        
        print("    Projections:            %i with %i connections in total"%(len(projs),connections))
        
        elec_projs = []
        elec_connections = 0
        for elec_proj in network.electrical_projections:
            elec_projs.append(elec_proj.id)
            elec_connections+=len(elec_proj.electrical_connections)
        
        print("    Electrical Projections: %i with %i connections in total"%(len(elec_projs),elec_connections))


    print("")

