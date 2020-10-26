import numpy as py
import statistics as stat
import math as math


class DataProcess(object):
    def __init__(self):
        self.result = []
        self.history = []

        self.extra_result1 = []
        self.extra_result2 = []
        self.extra_result3 = []
        self.extra_result4 = []

    def sma(self, period, data_in):
        # Simple moving average calculation
        self.__init__()
        for each_element in data_in:
            self.history.append(each_element)
            if len(self.history) > period:
                del (self.history[0])

            sma_value = stat.mean(self.history)
            self.result.append(sma_value)

            variance = 0
            for price in self.history:
                variance = variance + ((price - sma_value) ** 2)

            stddev = math.sqrt(variance / len(self.history))
            self.extra_result1.append(stddev)

        return self.result

    def ema(self, period, data_in):
        # Exponential moving average calculation
        self.__init__()
        mu = 2 / (period + 1)
        temp = 0
        for each_element in data_in:
            if temp == 0:
                temp = each_element
            else:
                temp = (each_element - temp) * mu + temp

            self.result.append(temp)

        return self.result

    def apo(self, short_period, long_period, data_in):
        # Absolute price oscillator calculation
        self.__init__()
        temp1 = self.ema(short_period, data_in)
        temp2 = self.ema(long_period, data_in)
        self.result = py.subtract(temp1, temp2)
        self.extra_result1 = temp1
        self.extra_result2 = temp2

        return self.result

    def macd(self, short_period, long_period, macd_period, data_in):
        # Moving average convergence divergence calculation
        self.__init__()
        k_macd = 2 / (macd_period + 1)
        ema_macd = 0

        self.result = self.apo(short_period, long_period, data_in)
        for each_element in self.result:
            if ema_macd == 0:
                ema_macd = each_element
            else:
                ema_macd = (each_element - ema_macd) * k_macd + ema_macd

            self.extra_result3.append(ema_macd)  # signal data
            self.extra_result4.append(each_element - ema_macd)  # macd histogram

        return self.result

    def bb(self, period, stddev_factor, data_in):
        # Bollinger bands calculation
        self.__init__()
        self.result = self.sma(period, data_in)
        temp = [i * stddev_factor for i in self.extra_result1]
        self.extra_result1 = py.subtract(self.result, temp)
        self.extra_result2 = py.add(self.result, temp)

        return self.result

    def rsi(self, period, data_in):
        # Relative strength indicator calculation
        self.__init__()
        gain_history = []
        loss_history = []
        avg_gain_values = []
        avg_loss_values = []
        last_price = 0

        for each_element in data_in:
            if last_price == 0:
                last_price = each_element

            gain_history.append(max(0, each_element - last_price))
            loss_history.append(max(0, last_price - each_element))
            last_price = each_element

            if len(gain_history) > period:
                del (gain_history[0])
                del (loss_history[0])

            avg_gain = stat.mean(gain_history)
            avg_loss = stat.mean(loss_history)

            avg_gain_values.append(avg_gain)
            avg_loss_values.append(avg_loss)

            rs = 0
            if avg_loss > 0:
                rs = avg_gain / avg_loss

            rsi = 100 - (100 / (1 + rs))
            self.result.append(rsi)

        self.extra_result1 = avg_gain_values
        self.extra_result2 = avg_loss_values

        return self.result

    def sdv(self, period, data_in):
        # Standard deviation calculation
        self.__init__()
        self.sma(period, data_in)
        self.result = self.extra_result1

        return self.result

    def mom(self, period, data_in):
        # Momentum calculation
        self.__init__()
        for each_element in data_in:
            self.history.append(each_element)
            if len(self.history) > period:
                del (self.history[0])

            self.result.append(each_element - self.history[0])

        return self.result
