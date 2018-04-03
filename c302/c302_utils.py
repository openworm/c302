import sys
import os
from pyneuroml import pynml
import matplotlib.pyplot as plt
import numpy as np

import c302

import re
import collections


natsort = lambda s: [int(t) if t.isdigit() else t for t in re.split('(\d+)', s)]


def plots(a_n, info, cells, dt):
    

    c302.print_('Generating plots for: %s'%info)

    heightened = False
    matrix_height_in = None

    if len(cells) > 24:
        matrix_height_in = 10
        heightened = True
    if len(cells) > 100:
        matrix_height_in = 20
    if heightened:
        #fontsize_pt = plt.rcParams['ytick.labelsize']
        #dpi = 72.27

        # comput the matrix height in points and inches
        ##matrix_height_pt = fontsize_pt * a_n.shape[0]
        ##matrix_height_in = float(matrix_height_pt) / dpi
        #matrix_height_in = 10

        # compute the required figure height
        top_margin = 0.04  # in percentage of the figure height
        bottom_margin = 0.04  # in percentage of the figure height
        figure_height = matrix_height_in / (1 - top_margin - bottom_margin)

        fig, ax = plt.subplots(
            figsize=(6, figure_height),
            gridspec_kw=dict(top=1 - top_margin, bottom=bottom_margin))
    else:
        fig, ax = plt.subplots()

    #fig = plt.figure()
    #ax = fig.gca()
    downscale = 10
    
    a_n_ = a_n[:,::downscale]

    plot0 = ax.pcolormesh(a_n_)
    ax.set_yticks(np.arange(a_n_.shape[0]) + 0.5, minor=False)
    ax.set_yticklabels(cells)
    ax.tick_params(axis='y', labelsize=6)
    #plt.setp(ax.get_yticklabels(), rotation=45)

    
    fig.colorbar(plot0)
    
    fig.canvas.set_window_title(info)
    plt.title(info)
    plt.xlabel('Time (ms)')
 
    fig.canvas.draw()

    labels = [] #issue is with unicode
    for label in ax.get_xticklabels():
        if(len(label.get_text()) >0):
            labels.append(float( str((label.get_text())) )*dt*downscale*1000)
        # except:
        #     print "Error value on forming axis values, value: ", label.get_text(), ", length: ",len(label.get_text())
    
    #labels = [float(label.get_text())*dt*downscale*1000 for item in ax.get_xticklabels()]
    ax.set_xticklabels(labels)
    #print labels
    #print plt.xlim()
    plt.xlim(0,a_n_.shape[1])
    #print plt.xlim()

    
def plots_prof(a_n, info, cells, dt):
    cProfile.run('real_plots(a_n, info, cells, dt)')
    
def generate_traces_plot(config,parameter_set,xvals,yvals,info,labels,save,save_fig_path,voltage,muscles):
                         
    file_name = 'traces_%s%s_%s_%s.png'%(('muscles' if muscles else 'neuron'),('' if voltage else '_activity'),config,parameter_set)
    
    pynml.generate_plot(xvals,
                        yvals,
                        info,
                        labels=labels,
                        xaxis="Time (ms)",
                        yaxis="Membrane potential (mV)" if voltage else "Activity",
                        show_plot_already=False,
                        save_figure_to=(None if not save else save_fig_path%(file_name)),
                        cols_in_legend_box=8,
                        title_above_plot=True)
    
    
def plot_c302_results(lems_results, 
                      config, 
                      parameter_set, 
                      directory='./',
                      save=True,
                      show_plot_already=True, 
                      data_reader="SpreadsheetDataReader",
                      plot_ca=True):
    
    
    params = {'legend.fontsize': 8,
              'font.size': 10}
    plt.rcParams.update(params)

    if not directory.endswith('/'):
        directory += '/'
    save_fig_path = directory+'%s'

    #c302.print_("Reloaded data: %s"%lems_results.keys())
    cells = []
    muscles = []
    times = [t*1000 for t in lems_results['t']]
    for cm in lems_results.keys():
        if not cm=='t' and cm.endswith('/v'):
            if c302.is_muscle(cm):
                muscles.append(cm.split('/')[0])
            else:
                cells.append(cm.split('/')[0])
    
    cells.sort(key=natsort)
    cells.reverse()
            
    c302.print_("All cells: %s"%cells)
    dt = lems_results['t'][1]
    
    ################################################
    ## Plot voltages cells
    
    if len(cells) > 0:
        c302.print_("Plotting neuron voltages")
        
        template = '{0}/0/GenericNeuronCell/{1}'
        if parameter_set.startswith('A') or parameter_set.startswith('B'):
            template = '{0}/0/generic_neuron_iaf_cell/{1}'
        if parameter_set.startswith('D'):
            template = '{0}/0/{0}/{1}'
    
        
        xvals = []
        yvals = []
        labels = []
        
        for cell in cells:
            v = lems_results[template.format(cell,'v')]
            
            xvals.append(times)
            labels.append(cell)
            
            if cell==cells[0]:
                volts_n = np.array([[vv*1000 for vv in v]])
            else:
                volts_n = np.append(volts_n,[[vv*1000 for vv in v]],axis=0)
            yvals.append(volts_n[-1])
            
        info = 'Membrane potentials of %i neuron(s) (%s %s)'%(len(cells),config,parameter_set)

        #tasks.append((volts_n, info, cells, dt))
        plots(volts_n, info, cells, dt)

        if save:
            f = save_fig_path%('neurons_%s_%s.png'%(parameter_set,config))
            c302.print_("Saving figure to: %s"%os.path.abspath(f))
            plt.savefig(f,bbox_inches='tight')

        generate_traces_plot(config,
                             parameter_set,
                             xvals,
                             yvals,
                             info,
                             labels,
                             save=save,
                             save_fig_path=save_fig_path,
                             voltage=True,
                             muscles=False)
            
        
    ################################################
    ## Plot voltages muscles

 
    muscles.sort(key=natsort)
    muscles.reverse()

    xvals = []
    yvals = []
    labels = []
    
    if len(muscles)>0:

        c302.print_("Plotting muscle voltages")

        template_m = '{0}/0/GenericMuscleCell/{1}'
        if parameter_set.startswith('A') or parameter_set.startswith('B'):
            template_m = '{0}/0/generic_muscle_iaf_cell/{1}'

        for muscle in muscles:
            mv = lems_results[template_m.format(muscle,'v')]

            xvals.append(times)
            labels.append(muscle)
        
            if muscle==muscles[0]:
                mvolts_n = np.array([[vv*1000 for vv in mv]])
            else:
                mvolts_n = np.append(mvolts_n,[[vv*1000 for vv in mv]],axis=0)
            yvals.append(mvolts_n[-1])

        info = 'Membrane potentials of %i muscle(s) (%s %s)'%(len(muscles),config,parameter_set)

        plots(mvolts_n, info, muscles, dt)
        
        if save:
            f = save_fig_path%('muscles_%s_%s.png'%(parameter_set,config))
            c302.print_("Saving figure to: %s"%os.path.abspath(f))
            plt.savefig(f,bbox_inches='tight')

        generate_traces_plot(config,
                             parameter_set,
                             xvals,
                             yvals,
                             info,
                             labels,
                             save=save,
                             save_fig_path=save_fig_path,
                             voltage=True,
                             muscles=True)
    
    ################################################
    ## Plot activity/[Ca2+] in cells
    
    if plot_ca and parameter_set!='A' and len(cells) > 0:
        
        c302.print_("Plotting neuron activities ([Ca2+])")
        variable = 'activity'
        description = 'Activity'
            
        if parameter_set.startswith('C') or parameter_set.startswith('D'):
            variable = 'caConc'
            description = '[Ca2+]'

        xvals = []
        yvals = []
        labels = []

        info = '%s of %i neurons (%s %s)'%(description, len(cells),config,parameter_set)
        for cell in cells:
            a = lems_results[template.format(cell,variable)]
            
            xvals.append(times)
            yvals.append(a)
            labels.append(cell)
            
            if cell==cells[0]:
                activities_n = np.array([a])
            else:
                activities_n = np.append(activities_n,[a],axis=0)

        plots(activities_n, info, cells, dt)

        if save:
            f = save_fig_path%('neuron_activity_%s_%s.png'%(parameter_set,config))
            c302.print_("Saving figure to: %s"%os.path.abspath(f))
            plt.savefig(f,bbox_inches='tight')

        generate_traces_plot(config,
                             parameter_set,
                             xvals,
                             yvals,
                             info,
                             labels,
                             save=save,
                             save_fig_path=save_fig_path,
                             voltage=False,
                             muscles=False)
    
    ################################################
    ## Plot activity/[Ca2+] in muscles
    
    if plot_ca and parameter_set!='A' and len(muscles)>0:
        
        c302.print_("Plotting muscle activities ([Ca2+])")
        variable = 'activity'
        description = 'Activity'
            
        if parameter_set.startswith('C') or parameter_set.startswith('D'):
            variable = 'caConc'
            description = '[Ca2+]'
            
        xvals = []
        yvals = []
        labels = []

        info = '%s of %i muscles (%s %s)'%(description, len(muscles),config,parameter_set)
        for m in muscles:
            a = lems_results[template_m.format(m,variable)]
            
            xvals.append(times)
            yvals.append(a)
            labels.append(m)
            
            if m==muscles[0]:
                activities_n = np.array([a])
            else:
                activities_n = np.append(activities_n,[a],axis=0)

        plots(activities_n, info, muscles, dt)
    
        if save:
            f = save_fig_path%('muscle_activity_%s_%s.png'%(parameter_set,config))
            c302.print_("Saving figure to: %s"%os.path.abspath(f))
            plt.savefig(f,bbox_inches='tight')

        generate_traces_plot(config,
                             parameter_set,
                             xvals,
                             yvals,
                             info,
                             labels,
                             save=save,
                             save_fig_path=save_fig_path,
                             voltage=False,
                             muscles=True)
    

    if show_plot_already:
        try:
            plt.show()
        except KeyboardInterrupt:
            c302.print_("Interrupt received, stopping...")
    else:
        plt.close("all")
        
        
def _show_conn_matrix(data, t, all_info_pre,all_info_post, type, save_figure_to=False):
    
    
    if data.shape[0]>0 and data.shape[1]>0 and np.amax(data)>0:
        ##norm = matplotlib.colors.LogNorm(vmin=1, vmax=np.amax(data))
        maxn = int(np.amax(data))
    else:
        ##norm = None
        maxn = 0
        
    c302.print_("Plotting data of size %s, max %s: %s"%(str(data.shape),maxn, t))
    
    if maxn==0:
        c302.print_("No connections!!")
        return
    
    fig, ax = plt.subplots()
    title = '%s: %s'%(type,t)
    plt.title(title)
    fig.canvas.set_window_title(title)
    import matplotlib
    cm = matplotlib.cm.get_cmap('gist_stern_r')
    
    
    im = plt.imshow(data, cmap=cm, interpolation='nearest',norm=None)
    
    ax = plt.gca();
    # Gridlines based on minor ticks
    if data.shape[0]<40:
        ax.grid(which='minor', color='grey', linestyle='-', linewidth=.3)
    
    xt = np.arange(data.shape[1]) + 0
    ax.set_xticks(xt)
    ax.set_xticks(xt[:-1]+0.5,minor=True)
    ax.set_yticks(np.arange(data.shape[0]) + 0)
    ax.set_yticks(np.arange(data.shape[0]) + 0.5,minor=True)
    
    
    ax.set_yticklabels([all_info_pre[k][4] for k in all_info_pre])
    ax.set_xticklabels([all_info_post[k][4] for k in all_info_post])
    ax.set_ylabel('presynaptic')
    tick_size = 10 if data.shape[0]<20 else (8 if data.shape[0]<40 else 6)
    ax.tick_params(axis='y', labelsize=tick_size)
    ax.set_xlabel('postsynaptic')
    ax.tick_params(axis='x', labelsize=tick_size)
    fig.autofmt_xdate()
    
    
    #heatmap = ax.pcolor(data, cmap='gist_stern')
    cbar = plt.colorbar(im, ticks=range(maxn+1))
    cbar.set_ticklabels(range(maxn+1))
    if save_figure_to:
        c302.print_("Saving connectivity figure to: %s"%save_figure_to)
        plt.savefig(save_figure_to,bbox_inches='tight')

def generate_conn_matrix(nml_doc, save_fig_dir=None, verbose=False):
    
    net = nml_doc.networks[0]
    
    cc_exc_conns = {}
    cc_inh_conns = {}
    all_cells = []
    
    for cp in net.continuous_projections:
        if not cp.presynaptic_population in cc_exc_conns.keys():
            cc_exc_conns[cp.presynaptic_population] = {}
        if not cp.presynaptic_population in cc_inh_conns.keys():
            cc_inh_conns[cp.presynaptic_population] = {}
            
        if not cp.presynaptic_population in all_cells:
            all_cells.append(cp.presynaptic_population)
        if not cp.postsynaptic_population in all_cells:
            all_cells.append(cp.postsynaptic_population)
        
        for c in cp.continuous_connection_instance_ws:
            if 'inh' in c.post_component:
                cc_inh_conns[cp.presynaptic_population][cp.postsynaptic_population] = float(c.weight)
            else:
                cc_exc_conns[cp.presynaptic_population][cp.postsynaptic_population] = float(c.weight)
                
    
    gj_conns = {}
    for ep in net.electrical_projections:
        if not ep.presynaptic_population in gj_conns.keys():
            gj_conns[ep.presynaptic_population] = {}
            
        if not ep.presynaptic_population in all_cells:
            all_cells.append(ep.presynaptic_population)
        if not ep.postsynaptic_population in all_cells:
            all_cells.append(ep.postsynaptic_population)
        
        for e in ep.electrical_connection_instance_ws:
            gj_conns[ep.presynaptic_population][ep.postsynaptic_population] = float(e.weight)
            
            
    all_cells = sorted(all_cells)
    
    all_neuron_info, all_muscle_info = c302._get_cell_info(all_cells)
    all_neurons = [] 
    all_muscles = []
    for c in all_cells:
        if c302.is_muscle(c):
            all_muscles.append(c)
        else:
            all_neurons.append(c)
        
    
    data_exc_n = np.zeros((len(all_neurons),len(all_neurons)))
    data_exc_m = np.zeros((len(all_neurons),len(all_muscles)))
    
    data_inh_n = np.zeros((len(all_neurons),len(all_neurons)))
    data_inh_m = np.zeros((len(all_neurons),len(all_muscles)))
    
    for pre in cc_exc_conns.keys():
        for post in cc_exc_conns[pre].keys():
            c302.print_("Exc Conn %s -> %s: %s"%(pre,post,cc_exc_conns[pre][post]), verbose)
            if post in all_neurons:
                data_exc_n[all_neurons.index(pre),all_neurons.index(post)] = cc_exc_conns[pre][post]
            else:
                data_exc_m[all_neurons.index(pre),all_muscles.index(post)] = cc_exc_conns[pre][post]
            if pre in all_muscles:
                raise Exception("Unexpected...")
                
    for pre in cc_inh_conns.keys():
        for post in cc_inh_conns[pre].keys():
            c302.print_("Inh Conn %s -> %s: %s"%(pre,post,cc_inh_conns[pre][post]), verbose)
            if post in all_neurons:
                data_inh_n[all_neurons.index(pre),all_neurons.index(post)] = cc_inh_conns[pre][post]
            else:
                data_inh_m[all_neurons.index(pre),all_muscles.index(post)] = cc_inh_conns[pre][post]
            if pre in all_muscles:
                raise Exception("Unexpected...")
                
    
    _show_conn_matrix(data_exc_n, 'Excitatory (non GABA) conns to neurons',all_neuron_info,all_neuron_info, 
                      net.id, save_figure_to='%s/%s_exc_to_neurons.png'%(save_fig_dir,net.id) if save_fig_dir else None)
                      
    _show_conn_matrix(data_exc_m, 'Excitatory (non GABA) conns to muscles',all_neuron_info,all_muscle_info, 
                      net.id, save_figure_to='%s/%s_exc_to_muscles.png'%(save_fig_dir,net.id) if save_fig_dir else None)
    
    _show_conn_matrix(data_inh_n, 'Inhibitory (GABA) conns to neurons',all_neuron_info,all_neuron_info, 
                      net.id, save_figure_to='%s/%s_inh_to_neurons.png'%(save_fig_dir,net.id) if save_fig_dir else None)
    _show_conn_matrix(data_inh_m, 'Inhibitory (GABA) conns to muscles',all_neuron_info,all_muscle_info, 
                      net.id, save_figure_to='%s/%s_inh_to_muscles.png'%(save_fig_dir,net.id) if save_fig_dir else None)
    
    
    data_n = np.zeros((len(all_neurons),len(all_neurons)))
    data_n_m = np.zeros((len(all_neurons),len(all_muscles)))
    data_m_m = np.zeros((len(all_muscles), len(all_muscles)))

    neuron_muscle = False
    muscle_muscle = False

    for pre in gj_conns.keys():
        for post in gj_conns[pre].keys():
            c302.print_("Elect Conn %s -> %s: %s"%(pre,post,gj_conns[pre][post]), verbose)
            
            if pre in all_neurons and post in all_neurons:
                data_n[all_neurons.index(pre),all_neurons.index(post)] = gj_conns[pre][post]
            elif pre in all_neurons and post in all_muscles or pre in all_muscles and post in all_neurons:
                if pre in all_neurons:
                    data_n_m[all_neurons.index(pre), all_muscles.index(post)] = gj_conns[pre][post]
                else:
                    data_n_m[all_muscles.index(pre), all_neurons.index(post)] = gj_conns[pre][post]
                neuron_muscle = True
            elif pre in all_muscles and post in all_muscles:
                muscle_muscle = True
                data_m_m[all_muscles.index(pre), all_muscles.index(post)] = gj_conns[pre][post]
            else:
                raise Exception("Unexpected...")
        
    
    _show_conn_matrix(data_n, 'Electrical (gap junction) conns to neurons',all_neuron_info,all_neuron_info, 
                      net.id, save_figure_to='%s/%s_elec_neurons_neurons.png'%(save_fig_dir,net.id) if save_fig_dir else None)

    if neuron_muscle:
        _show_conn_matrix(data_n_m, 'Electrical (gap junction) conns between neurons and muscles', all_neuron_info, all_muscle_info,
                          net.id,
                          save_figure_to='%s/%s_elec_neurons_muscles.png' % (save_fig_dir, net.id) if save_fig_dir else None)

    if muscle_muscle:
        _show_conn_matrix(data_m_m, 'Electrical (gap junction) conns between muscles', all_muscle_info,
                          all_muscle_info,
                          net.id,
                          save_figure_to='%s/%s_elec_muscles_muscles.png' % (
                          save_fig_dir, net.id) if save_fig_dir else None)
    #_show_conn_matrix(data_m, 'Electrical (gap junction) conns to muscles',all_neuron_info,all_muscle_info, net.id)
        

            
if __name__ == '__main__':

    from neuroml.loaders import read_neuroml2_file
    
    configs = ['c302_C0_Syns.net.nml', 'c302_C0_Social.net.nml','c302_C0_Muscles.net.nml','c302_C0_Pharyngeal.net.nml','c302_C0_Oscillator.net.nml','c302_C0_Full.net.nml']
    configs = ['c302_C0_Syns.net.nml', 'c302_C0_Social.net.nml']
    #configs = ['c302_C0_Syns.net.nml']
    configs = ['c302_C0_Muscles.net.nml']
    #configs = ['c302_C0_Oscillator.net.nml']
    
    if '-phar' in sys.argv:
        
        configs = ['c302_C0_Pharyngeal.net.nml']
    
    for c in configs:

        nml_doc = read_neuroml2_file('examples/%s'%c)

        generate_conn_matrix(nml_doc, save_fig_dir='./examples/summary/')
    
    if not '-nogui' in sys.argv:
        plt.show()