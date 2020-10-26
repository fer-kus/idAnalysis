import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class PlotData(object):  # Plotting class
    def __init__(self, plot_size, font_size):
        self.plot = plt
        self.plot.rcParams.update({'font.size': font_size})
        self.fig = self.plot.figure(figsize=plot_size)
        self.data = pd.DataFrame([])
        self.line_color = ['k', 'b', 'g', 'r', 'c', 'm', 'y']

    def clear_figure(self):
        self.plot.clf()

    def push_data(self, data_title, data_in):
        self.data = self.data.assign(temp_title=pd.Series(data_in))
        self.data.columns = [*self.data.columns[:-1], data_title]
        return 1

    def pop_data(self):
        if len(self.data.columns) > 0:
            self.data = self.data.iloc[:, :-1]
            return 1
        else:
            return 0

    def set_plot(self, config, y_title, plot_type):
        if (len(self.data.columns) > 0) and (len(self.data.columns) <= len(self.line_color)):
            count = 0
            axis = self.fig.add_subplot(config)
            placement = [int(i) for i in str(config)]
            for each_element in self.data.columns:
                y_axis = self.data.iloc[:, count]
                if plot_type == 'l':
                    y_axis.plot(ax=axis, color=self.line_color[count], lw=1, legend=True)
                else:
                    y_axis.plot(ax=axis, color='r', kind='bar', legend=True,
                                use_index=False)

                count += 1

            if placement[0] != placement[2]:
                axis.get_xaxis().set_visible(False)

            axis.set_ylabel(y_title)
            self.fig.tight_layout()
            self.data = pd.DataFrame([])
            return 1
        else:
            return 0

    def set_gui(self, master_mode):
        return FigureCanvasTkAgg(self.fig, master=master_mode)
