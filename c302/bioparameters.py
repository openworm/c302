from decimal import Decimal

from neuroml import ExpTwoSynapse, GapJunction, GradedSynapse

'''
    Subject to much change & refactoring once PyOpenWorm is stable...
'''


def split_neuroml_quantity(quantity):

    i=len(quantity)
    while i>0:
        magnitude = quantity[0:i].strip()
        unit = quantity[i:].strip()

        try:
            magnitude = float(magnitude)
            i=0
        except ValueError:
            i -= 1
    return magnitude, unit

class BioParameter():

    def __init__(self, name, value, source, certainty):
        self.name = name
        self.value = value
        self.source = source
        self.certainty = certainty 
    
    def __str__(self):
        return "BioParameter: %s = %s (SRC: %s, certainty %s)"%(self.name, self.value, self.source, self.certainty)
    
    def __repr__(self):
        return self.__str__()
    
    def change_magnitude(self, magnitude):
        
        self.value = '%s %s'%(Decimal(magnitude), split_neuroml_quantity(self.value)[1])
        
    def x(self):
        
        return split_neuroml_quantity(self.value)[0]


class ParameterisedModelPrototype(object):

    #bioparameters = []
    def __init__(self):
        self.bioparameters = []

    def print_(self, msg):
        pre = "c302      >>> "
        print('%s %s'%(pre,msg.replace('\n','\n'+pre)))


    def add_bioparameter(self, name, value, source, certainty):
        found = False
        for bp in self.bioparameters:
            if bp.name == name:
                bp.value = value
                bp.source = source
                bp.certainty = certainty
                found = True
        if not found:
            bp = BioParameter(name, value, source, certainty)
            self.bioparameters.append(bp)


    def add_bioparameter_obj(self, bioparameter):
        for bp in self.bioparameters:
            if bp.name == bioparameter.name:
                self.bioparameters.remove(bp)
                
        self.bioparameters.append(bioparameter)


    def get_bioparameter(self, name, warn_if_missing=False):
        for bp in self.bioparameters:
            if bp.name == name:
                return bp
        if warn_if_missing:
            self.print_('Cannot find bioparameter: %s; %i known: %s'%(name, len(self.bioparameters), [bp.name for bp in self.bioparameters]))
        return None


    def set_bioparameter(self, name, value, source, certainty):

        for bp in self.bioparameters:
            if bp.name == name:
                bp.value = value
                bp.source = source
                bp.certainty = certainty

    def bioparameter_info(self, indent=""):
        info = indent+"Known BioParameters:\n"
        for bp in sorted(self.bioparameters, key=lambda x: x.name):
            info += indent+indent+"%s\n"%bp
        return info
    
    
class c302ModelPrototype(ParameterisedModelPrototype):

    def __init__(self):
        super(c302ModelPrototype, self).__init__()

        self.level = "Level not yet set"
        self.custom_component_types_definitions = None
        self.generic_neuron_cell = None
        self.generic_muscle_cell = None
        self.exc_syn = None
        self.inh_syn = None
        self.elec_syn = None
        self.offset_current = None
        self.concentration_model = None
        self.found_specific_param = False
    
    def is_level_A(self):
        return self.level.startswith('A')
    
    def is_level_B(self):
        return self.level.startswith('B')
    
    def is_level_C(self):
        return self.level.startswith('C')
    
    def is_level_C0(self):
        return self.level == 'C0'

    def is_level_C2(self):
        return self.level == 'C2'
    
    def is_level_D1(self):
        return self.level == 'D1'
    
    def is_level_D(self):
        return self.level.startswith('D')


    def get_conn_param(self, pre_cell, post_cell, specific_conn_template, default_conn_template, param_name):
        param = self.get_bioparameter(specific_conn_template % (pre_cell, post_cell, param_name), warn_if_missing=False)
        if param:
            self.found_specific_param = True
            return param.value
        def_param = self.get_bioparameter(default_conn_template % param_name)
        if not def_param:
            return None
        return def_param.value


    def get_syn(self, pre_cell, post_cell, type, pol):
        if pol == 'elec':
            return self.get_elec_syn(pre_cell, post_cell, type)
        elif pol == 'exc':
            return self.get_exc_syn(pre_cell, post_cell, type)
        elif pol == 'inh':
            return self.get_inh_syn(pre_cell, post_cell, type)


    def create_n_connection_synapse(self, prototype_syn, n, nml_doc, existing_synapses):
        if prototype_syn.id in existing_synapses:
            return existing_synapses[prototype_syn.id]

        existing_synapses[prototype_syn.id] = prototype_syn
        if isinstance(prototype_syn, ExpTwoSynapse):
            nml_doc.exp_two_synapses.append(prototype_syn)
        elif isinstance(prototype_syn, GapJunction):
            nml_doc.gap_junctions.append(prototype_syn)
        elif isinstance(prototype_syn, GradedSynapse):
            nml_doc.graded_synapses.append(prototype_syn)
        else:
            info = '%s conns; %s'%(n, existing_synapses)
            del existing_synapses[prototype_syn.id]
            raise Exception('Unknown synapse type: %s (%s)'%(prototype_syn.id, info))

        return prototype_syn


    def is_analog_conn(self, syn):
        return isinstance(syn, GradedSynapse)

    def is_elec_conn(self, syn):
        return isinstance(syn, GapJunction)
