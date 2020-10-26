import analysis as ana
import downloader as dw
import pandas as pd
import plotter as pt
import tkinter as tk

tech_meth = [
    ("Absolute Price Oscillator", 1),
    ("Bollinger Bands", 2),
    ("Exponential Moving Average", 3),
    ("Momentum", 4),
    ("Moving Average Convergence Divergence", 5),
    ("Relative Strength Indicator", 6),
    ("Simple Moving Average", 7),
    ("Standard Deviation", 8)]

stock_name = 'GOOG'
start_date = '2014-01-01'
end_date = '2018-01-01'


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Add widgets to a frame
        self.choice = tk.IntVar()
        self.choice.set(1)

        self.group_radio = tk.LabelFrame(self, padx=10, pady=20, text="Technical analysis")
        self.create_radio(self.group_radio, tech_meth)
        self.disable_radio()

        self.btn_get = tk.Button(self, text="Get DATA", command=self.calculate)

        # Put the plot in a frame
        self.group_plot = tk.LabelFrame(self, width=805, height=520, padx=0, pady=0, text="DATA plot")
        self.plotter = pt.PlotData((8, 5), 8)
        self.canvas = self.plotter.set_gui(self)
        self.canvas.draw()

        # Arrange the widgets by using grid
        self.opts = {'ipadx': 0, 'ipady': 0, 'sticky': 'nswe'}
        self.group_radio.grid(row=0, column=0, rowspan=5, **self.opts)
        self.btn_get.grid(row=5, column=0, **self.opts)
        self.group_plot.grid(row=0, column=2, rowspan=6, columnspan=3, **self.opts)
        self.canvas.get_tk_widget().place(in_=self.group_plot)

        # Prepare variables
        self.fetcher = dw.Taker()
        self.stock_data = pd.DataFrame([])
        self.tech = ana.DataProcess()

    def enable_radio(self):
        for child in self.group_radio.winfo_children():
            child.configure(state='normal')

    def disable_radio(self):
        for child in self.group_radio.winfo_children():
            child.configure(state='disabled')

    def create_radio(self, master_option, list_input):
        for technique, val in list_input:
            tk.Radiobutton(master_option, text=technique,
                           variable=self.choice, value=val, command=self.plotting).pack(anchor=tk.W, pady=10)

    def quit_window(self):
        self.quit()
        self.destroy()

    def calculate(self):
        # import data
        if self.fetcher.read_data():
            self.stock_data = self.fetcher.data_source
            if (self.stock_data.stock_name != stock_name) or (self.stock_data.start_date != start_date) \
               or (self.stock_data.end_date != end_date):
                self.fetcher.get_data(stock_name, start_date, end_date)
                self.stock_data = self.fetcher.data_source

            self.enable_radio()
        else:
            if self.fetcher.get_data(stock_name, start_date, end_date):
                self.stock_data = self.fetcher.data_source
            else:
                print('Data taking failure')

        # technical analysis calculations start here
        self.stock_data = self.stock_data.tail(620)  # this operation removes extra attributes of stock_data
        close_price = self.stock_data['Close']

        result = self.tech.apo(10, 40, close_price)  # apo calculation
        self.stock_data = self.stock_data.assign(apoCalc=pd.Series(result, index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(apoShort=pd.Series(self.tech.extra_result1,
                                                                    index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(apoLong=pd.Series(self.tech.extra_result2,
                                                                   index=self.stock_data.index))

        result = self.tech.bb(20, 2, close_price)  # Bollinger bands calculation
        self.stock_data = self.stock_data.assign(bbCalc=pd.Series(result, index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(bbLow=pd.Series(self.tech.extra_result1,
                                                                 index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(bbHigh=pd.Series(self.tech.extra_result2,
                                                                  index=self.stock_data.index))

        result = self.tech.ema(20, close_price)  # ema calculation
        self.stock_data = self.stock_data.assign(emaCalc=pd.Series(result, index=self.stock_data.index))

        result = self.tech.mom(20, close_price)  # Momentum calculation
        self.stock_data = self.stock_data.assign(momCalc=pd.Series(result, index=self.stock_data.index))

        result = self.tech.macd(10, 40, 20, close_price)  # macd calculation
        self.stock_data = self.stock_data.assign(macdCalc=pd.Series(result, index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(macdShort=pd.Series(self.tech.extra_result1,
                                                                     index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(macdLong=pd.Series(self.tech.extra_result2,
                                                                    index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(macdEma=pd.Series(self.tech.extra_result3,
                                                                   index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(macdHist=pd.Series(self.tech.extra_result4,
                                                                    index=self.stock_data.index))

        result = self.tech.rsi(20, close_price)  # rsi calculation
        self.stock_data = self.stock_data.assign(rsiCalc=pd.Series(result, index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(rsiGain=pd.Series(self.tech.extra_result1,
                                                                   index=self.stock_data.index))
        self.stock_data = self.stock_data.assign(rsiLoss=pd.Series(self.tech.extra_result2,
                                                                   index=self.stock_data.index))

        result = self.tech.sma(20, close_price)  # sma calculation
        self.stock_data = self.stock_data.assign(smaCalc=pd.Series(result, index=self.stock_data.index))

        result = self.tech.sdv(20, close_price)  # Standard deviation calculation
        self.stock_data = self.stock_data.assign(sdvCalc=pd.Series(result, index=self.stock_data.index))

        self.plotting()

    def plotting(self):
        select = self.choice.get()
        self.plotter.clear_figure()
        if select == 1:  # Absolute price oscillator plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.set_plot(211, stock_name + ' price in $', 'l')
            self.plotter.push_data('Absolute price oscillator', self.stock_data['apoCalc'])
            self.plotter.set_plot(212, 'APO', 'l')

        elif select == 2:  # Bollinger bands plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.push_data('Middle band of 20 days', self.stock_data['bbCalc'])
            self.plotter.push_data('Lower band of 20 days', self.stock_data['bbLow'])
            self.plotter.push_data('Upper band of 20 days', self.stock_data['bbHigh'])
            self.plotter.set_plot(111, stock_name + ' price in $', 'l')

        elif select == 3:  # Exponential moving average plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.push_data('EMA of 20 days', self.stock_data['emaCalc'])
            self.plotter.set_plot(111, stock_name + ' price in $', 'l')

        elif select == 4:  # Momentum plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.set_plot(211, stock_name + ' price in $', 'l')
            self.plotter.push_data('Momentum of 20 days', self.stock_data['momCalc'])
            self.plotter.set_plot(212, 'Momentum in $', 'l')

        elif select == 5:  # Moving average convergence divergence plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.push_data('Ema of 10 days', self.stock_data['macdShort'])
            self.plotter.push_data('Ema of 40 days', self.stock_data['macdLong'])
            self.plotter.set_plot(311, stock_name + ' price in $', 'l')
            self.plotter.push_data('MACD histogram', self.stock_data['macdHist'])
            self.plotter.set_plot(312, 'MACD', 'b')
            self.plotter.push_data('MACD', self.stock_data['macdCalc'])
            self.plotter.push_data('Ema MACD of 20 days', self.stock_data['macdEma'])
            self.plotter.set_plot(313, 'MACD', 'l')

        elif select == 6:  # Relative strength indicator plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.set_plot(311, stock_name + ' price in $', 'l')
            self.plotter.push_data('Gain of 20 days', self.stock_data['rsiGain'])
            self.plotter.push_data('Loss of 20 days', self.stock_data['rsiLoss'])
            self.plotter.set_plot(312, 'RS', 'l')
            self.plotter.push_data('Relative strength indicator of 20 days', self.stock_data['rsiCalc'])
            self.plotter.set_plot(313, 'RSI', 'l')

        elif select == 7:  # Simple moving average plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.push_data('SMA of 20 days', self.stock_data['smaCalc'])
            self.plotter.set_plot(111, stock_name + ' price in $', 'l')

        elif select == 8:  # Standard deviation plot
            self.plotter.push_data('Close price', self.stock_data['Close'])
            self.plotter.set_plot(211, stock_name + ' price in $', 'l')
            self.plotter.push_data('Standard deviation of 20 days', self.stock_data['sdvCalc'])
            self.plotter.set_plot(212, 'StdDev in $', 'l')

        self.canvas.draw()


if __name__ == "__main__":
    app = App()
    app.title("Stock DATA technical analysis")
    app.attributes('-toolwindow', 'true')
    app.protocol('WM_DELETE_WINDOW', app.quit_window)
    app.mainloop()
