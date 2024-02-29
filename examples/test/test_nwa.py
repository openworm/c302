import wormneuroatlas as wa

atlas = wa.NeuroAtlas()
# This creates the NeuroAtlas object with the default options. This means
# that neurons are NOT merged in neuron classes and, therefore, in the
# following, we always need to specify individual neuron IDs, like AVAL
# and NOT neuron classes, like AVA. To use neuron classes instead, you
# need to instantiate NeuroAtlas specifying the following parameters 
# setting True or False based on your needs. This combination of options
# will merge bilateral pairs of neurons (AVAL/R as AVA). 
# atlas = wa.NeuroAtlas(merge_bilateral=True, merge_dorsoventral=False,
#                        merge_numbered=False, merge_AWC=False)

metadata = atlas.get_metadata()

for m in metadata:

    print("\n%s:"%(m,))
    for e in metadata[m]:
        print("    %s:\t%s"%(e,metadata[m][e]))

test_cells = ['ADAL','ADEL','RIAL', 'VA3', 'VD3'] 
test_cells = ['NSMR'] 
for c in test_cells:
    atlas.everything_about(c)

print(atlas.neuron_ids)

def get_info(a):
    print("Array %s, %s"%(a.dtype, a.shape))
    print(a)


for index in range(len(atlas.neuron_ids)):
    neuron = atlas.neuron_ids[index]
    ai = atlas.ids_to_ai([neuron])
    print("Index %i: %s = %s"%(index, neuron, ai))
    assert(index==ai)

print("------  Gap junctions: ------ ")
gj = atlas.get_gap_junctions()
print(get_info(gj))

print("------  Chem syns: ------ ")
cs = atlas.get_chemical_synapses()
print(get_info(cs))

print("------  Anatomical conn: ------ ")
ac = atlas.get_anatomical_connectome()
print(get_info(ac))

 
syn_sign = wa.SynapseSign()

for nt in ['Glu', 'ACh', 'GABA']:
    ns = syn_sign.get_neurons_producing(nt, mode='dominant')
    print("------  Neurons producing %s as dominant NT (%i) ------ "%(nt, len(ns)))
    print(ns)
    ns = syn_sign.get_neurons_producing(nt, mode='alternative')
    print("------  Neurons producing %s as alternative NT (%i) ------ "%(nt, len(ns)))
    print(ns)

for c in test_cells:
    print("------------ ")
    print("Connection info on %s, ais: %s"%(c, atlas.ids_to_ai(c)))
    print(c)



        

