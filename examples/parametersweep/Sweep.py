from GenerateExamples import colors

from neuromllite.sweep.ParameterSweep import ParameterSweep
from neuromllite.sweep.ParameterSweep import NeuroMLliteRunner

import sys

import pprint

pp = pprint.PrettyPrinter(depth=6)


if __name__ == "__main__":
    heatmap_lims = [-110, 20]

    standard_stim_amps = ["%spA" % (i / 10.0) for i in range(-5, 70, 1)]

    if "-all" in sys.argv:
        print("Generating all plots")
        save_fig_dir = "./"
        html = "<table>\n"

        fixed = {"dt": 0.025, "duration": 3000}

        vary = {"stim_amp": standard_stim_amps}
        # vary = {'stim_amp':['%spA'%(i/10.0) for i in range(-10,20,5)]}
        # vary = {'stim_amp':['-100pA','0pA','100pA','200pA','300pA','400pA']}

        cells = colors.keys()

        for type in cells:
            if type != "ec" and type != "ca3":
                run = True
                # run = False

                if run:
                    nmllr = NeuroMLliteRunner(
                        "Sim_IClamp_%s.json" % type, simulator="jNeuroML_NEURON"
                    )
                    ps = ParameterSweep(
                        nmllr,
                        vary,
                        fixed,
                        num_parallel_runs=6,
                        save_plot_all_to="firing_rates_%s.png" % type,
                        heatmap_all=True,
                        save_heatmap_to="heatmap_%s.png" % type,
                        heatmap_lims=heatmap_lims,
                        plot_all=True,
                        show_plot_already=False,
                    )

                    report = ps.run()

                    # ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
                    ps.plotLines(
                        "stim_amp",
                        "mean_spike_frequency",
                        save_figure_to="mean_spike_frequency_%s.png" % type,
                    )

                height = "160"
                html += "<tr>\n"
                html += "  <td width=30><b>" + type + "</b></td>\n"
                html += '  <td><a href="mean_spike_frequency_%s.png' % type + '">\n'
                html += (
                    '    <img alt="?" src="mean_spike_frequency_%s.png' % type
                    + '" height="'
                    + height
                    + '"/></a>\n'
                )
                html += "  </td>\n"
                html += '  <td><a href="firing_rates_%s.png' % type + '">\n'
                html += (
                    '    <img alt="?" src="firing_rates_%s.png' % type
                    + '" height="'
                    + height
                    + '"/></a>\n'
                )
                html += "  </td>\n"
                html += '  <td><a href="heatmap_%s.png' % type + '">\n'
                html += (
                    '    <img alt="?" src="heatmap_%s.png' % type
                    + '" height="'
                    + height
                    + '"/></a>\n'
                )
                html += "  </td>\n"
                html += '  <td><a href="dt_traces_%s.png' % type + '">\n'
                html += (
                    '    <img alt="?" src="dt_traces_%s.png' % type
                    + '" height="'
                    + height
                    + '"/></a>\n'
                )
                html += "  </td>\n"
                html += '  <td><a href="heatmap_dt_%s.png' % type + '">\n'
                html += (
                    '    <img alt="?" src="heatmap_dt_%s.png' % type
                    + '" height="'
                    + height
                    + '"/></a>\n'
                )
                html += "  </td>\n"
                html += '  <td><a href="mean_spike_frequency_dt_%s.png' % type + '">\n'
                html += (
                    '    <img alt="?" src="mean_spike_frequency_dt_%s.png' % type
                    + '" height="'
                    + height
                    + '"/></a>\n'
                )
                html += "  </td>\n"
                html += "<tr>\n"

        import matplotlib.pyplot as plt

        if "-nogui" not in sys.argv:
            print("Showing plots")
            plt.show()

        with open(save_fig_dir + "info.html", "w") as f:
            f.write("<html><body>\n%s\n</body></html>" % html)
        with open(save_fig_dir + "README.md", "w") as f2:
            f2.write("### c302 cell summary \n%s" % (html.replace(".html", ".md")))

    elif "-dt" in sys.argv:
        optimal_stim = {
            "cADpyr229_L23_PC_c292d67a2e_0_0": "500",
            "cNAC187_L23_NBC_9d37c4b1f8_0_0": "30",
        }

        vary = {
            "dt": [
                0.1,
                0.05,
                0.025,
                0.01,
                0.005,
                0.0025,
                0.001,
                0.0005,
                0.00025,
                0.0001,
            ]
        }
        vary = {"dt": [0.1, 0.05, 0.025, 0.01, 0.005, 0.0025, 0.001]}
        vary = {"dt": [0.05, 0.025, 0.01, 0.005, 0.0025]}
        # vary = {'dt':[0.05,0.025,0.01,0.005]}
        # vary = {'dt':[0.05,0.025,0.01]}
        # vary = {'dt':[0.05,0.025,0.01]}

        for type in optimal_stim:
            if type != "ec" and type != "ca3":
                run = True

                if run:
                    fixed = {"duration": 3000, "stim_amp": "%spA" % optimal_stim[type]}

                    nmllr = NeuroMLliteRunner(
                        "Sim_IClamp_%s.json" % type, simulator="jNeuroML_NEURON"
                    )
                    ps = ParameterSweep(
                        nmllr,
                        vary,
                        fixed,
                        num_parallel_runs=16,
                        save_plot_all_to="dt_traces_%s.png" % type,
                        heatmap_all=True,
                        save_heatmap_to="heatmap_dt_%s.png" % type,
                        heatmap_lims=heatmap_lims,
                        plot_all=True,
                        show_plot_already=False,
                    )

                    report = ps.run()

                    # ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
                    ps.plotLines(
                        "dt",
                        "mean_spike_frequency",
                        save_figure_to="mean_spike_frequency_dt_%s.png" % type,
                        logx=True,
                    )

        import matplotlib.pyplot as plt

        if "-nogui" not in sys.argv:
            print("Showing plots")
            plt.show()

    elif "-iv" in sys.argv:
        fixed = {"dt": 0.025, "duration": 2000}

        quick = False
        # quick=True

        vary = {"stim_amp": standard_stim_amps}

        # vary = {'number_per_cell':[i for i in range(0,250,10)]}
        vary = {"stim_amp": ["-1pA", "0pA", "1.5pA", "2pA"]}
        vary = {"stim_amp": ["%spA" % (i / 10.0) for i in range(-20, 60, 5)]}

        type = "GenericMuscleCell"
        type = "GenericNeuronCell"
        # type='poolosyn'
        config = "IClamp"
        # config = 'PoissonFiringSynapse'

        nmllr = NeuroMLliteRunner(
            "Sim_%s_%s.json" % (config, type), simulator="jNeuroML_NEURON"
        )

        if quick:
            pass

        ps = ParameterSweep(
            nmllr,
            vary,
            fixed,
            num_parallel_runs=6,
            plot_all=True,
            save_plot_all_to="firing_rates_%s.png" % type,
            heatmap_all=True,
            save_heatmap_to="heatmap_%s.png" % type,
            heatmap_lims=heatmap_lims,
            show_plot_already=False,
        )

        report = ps.run()
        ps.print_report()

        ps.plotLines(
            "stim_amp",
            "average_last_1percent",
            save_figure_to="average_last_1percent_%s.png" % type,
        )
        ps.plotLines(
            "stim_amp",
            "mean_spike_frequency",
            save_figure_to="mean_spike_frequency_%s.png" % type,
        )
        # ps.plotLines('dt','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type, logx=True)
        # ps.plotLines('number_per_cell','mean_spike_frequency',save_figure_to='poisson_mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt

        if "-nogui" not in sys.argv:
            print("Showing plots")
            plt.show()

    elif "-w2d" in sys.argv:
        fixed = {
            "dt": 0.025,
            "duration": 8000,
            "stim_delay": "1000ms",
            "stim_duration": "5000ms",
        }

        quick = False
        # quick=True

        vary = {"stim_amp": ["%spA" % (i / 1) for i in range(-3, 6, 1)]}

        type = "GenericMuscleCell"
        type = "GenericNeuronCell"
        type = "GenericNeuronCellW2D"
        # type='poolosyn'
        config = "IClamp"
        # config = 'PoissonFiringSynapse'

        nmllr = NeuroMLliteRunner(
            "Sim_%s_%s.json" % (config, type), simulator="jNeuroML"
        )

        if quick:
            pass

        ps = ParameterSweep(
            nmllr,
            vary,
            fixed,
            num_parallel_runs=1,
            plot_all=True,
            save_plot_all_to="firing_rates_%s.png" % type,
            heatmap_all=True,
            save_heatmap_to="heatmap_%s.png" % type,
            heatmap_lims=heatmap_lims,
            show_plot_already=False,
        )

        report = ps.run()
        ps.print_report()

        ps.plotLines(
            "stim_amp",
            "average_last_1percent",
            save_figure_to="average_last_1percent_%s.png" % type,
        )

        # ps.plotLines('dt','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type, logx=True)
        # ps.plotLines('number_per_cell','mean_spike_frequency',save_figure_to='poisson_mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt

        if "-nogui" not in sys.argv:
            print("Showing plots")
            plt.show()

    else:
        fixed = {"dt": 0.025, "duration": 3000}

        quick = False
        # quick=True

        vary = {"stim_amp": standard_stim_amps}
        vary = {
            "dt": [
                0.1,
                0.05,
                0.025,
                0.01,
                0.005,
                0.0025,
                0.001,
                0.0005,
                0.00025,
                0.0001,
            ]
        }
        vary = {"dt": [0.1, 0.05, 0.025, 0.01, 0.005, 0.0025, 0.001]}
        vary = {"dt": [0.1, 0.05, 0.025, 0.01, 0.005]}

        # vary = {'number_per_cell':[i for i in range(0,250,10)]}
        # vary = {'stim_amp':['1pA','1.5pA','2pA']}
        vary = {"stim_amp": ["%spA" % (i / 10.0) for i in range(-3, 60, 1)]}

        type = "GenericMuscleCell"
        type = "GenericNeuronCell"
        type = "GenericNeuronCellW2D"
        # type='poolosyn'
        config = "IClamp"
        # config = 'PoissonFiringSynapse'

        nmllr = NeuroMLliteRunner(
            "Sim_%s_%s.json" % (config, type), simulator="jNeuroML_NEURON"
        )

        if quick:
            pass

        ps = ParameterSweep(
            nmllr,
            vary,
            fixed,
            num_parallel_runs=6,
            plot_all=True,
            save_plot_all_to="firing_rates_%s.png" % type,
            heatmap_all=True,
            save_heatmap_to="heatmap_%s.png" % type,
            heatmap_lims=heatmap_lims,
            show_plot_already=False,
        )

        report = ps.run()
        ps.print_report()

        # ps.plotLines('stim_amp','average_last_1percent',save_figure_to='average_last_1percent_%s.png'%type)
        ps.plotLines(
            "stim_amp",
            "mean_spike_frequency",
            save_figure_to="mean_spike_frequency_%s.png" % type,
        )
        # ps.plotLines('dt','mean_spike_frequency',save_figure_to='mean_spike_frequency_%s.png'%type, logx=True)
        # ps.plotLines('number_per_cell','mean_spike_frequency',save_figure_to='poisson_mean_spike_frequency_%s.png'%type)

        import matplotlib.pyplot as plt

        if "-nogui" not in sys.argv:
            print("Showing plots")
            plt.show()
