import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError


class Taker(object):
    def __init__(self):
        self.data_filename = 'data.h5'
        self.data_source = pd.DataFrame([])
        self.data_source.stock_name = 'NONE'
        self.data_source.start_date = ''
        self.data_source.end_date = ''

    def read_data(self):
        store = pd.DataFrame([])
        try:
            store = pd.HDFStore(self.data_filename)
            self.data_source = store.get('df')
        except KeyError:
            store.close()
            self.data_source = pd.DataFrame([])
            return 0

        self.data_source.stock_name = store.get_storer('df').attrs.stock_name
        self.data_source.start_date = store.get_storer('df').attrs.start_date
        self.data_source.end_date = store.get_storer('df').attrs.end_date
        store.close()

        return 1

    def get_data(self, stock_name, start_date, end_date):
        try:
            self.data_source = data.DataReader(stock_name, 'yahoo', start_date, end_date)
        except RemoteDataError:
            return 0

        self.data_source.stock_name = stock_name
        self.data_source.start_date = start_date
        self.data_source.end_date = end_date

        store = pd.HDFStore(self.data_filename)
        store.put('df', self.data_source)
        store.get_storer('df').attrs.stock_name = self.data_source.stock_name
        store.get_storer('df').attrs.start_date = self.data_source.start_date
        store.get_storer('df').attrs.end_date = self.data_source.end_date
        store.close()

        return 1
