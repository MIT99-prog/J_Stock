#
import pandas as pd

from errorhandler import ErrorHandler, Error, ErrorList
from serialize import Data, FileName
from widget_helper import Result, DisplayInfo


class Stocks:
    def __init__(self):

        self.e_list = ErrorList()
        self.stocks = dict()
        self.result = Result()

    def __getitem__(self, i):
        keys = self.stocks.keys()
        key = list(keys)[i]
        return self.stocks.get(key)

    def __len__(self):
        return self.stocks.__len__()


class StockWrite(Stocks):

    def __init__(self, di: DisplayInfo):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)

    def get_data(self, tickers) -> Result:

        for i in range(len(tickers.tickers)):
            try:
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                self.stocks[tickers.tickers[i].ticker] = tickers.tickers[i].history(period='1mo')

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Stock Data Error!')
                self.e_list.add_list(er)
                erh = ErrorHandler(er)
                erh.print_error()

        # self.stocks = yf.download(self.tickers, period="1mo")  動かない！

        data = Data()  # Create Data class of serialize.py
        self.result = data.save_data(self.filename, self.stocks)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = 'Get Stock History Data'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass
        return self.result


class StockRead(Stocks):
    def __init__(self, di: DisplayInfo, read_type: str):
        super().__init__()
        self.di = di
        self.filename = FileName(di.market, di.data_type)
        # initialize values
        self.read_type = read_type
        self.open_price = pd.DataFrame()  # 始値
        self.close_price = pd.DataFrame()  # 終値
        self.high_price = pd.DataFrame()  # 高値
        self.low_price = pd.DataFrame()  # 安値
        self.volume = pd.DataFrame()  # 出来高
        self.dividends = pd.DataFrame()  # 配当
        self.stock_splits = pd.DataFrame()  # 分割

        self.result = self.data_read()

    def data_read(self):

        data = Data()
        self.result = data.load_data(self.filename)
        if self.result.exec_continue:
            self.stocks = self.result.result_data
        else:
            pass

        # Extend mode
        if self.read_type == 'Extend':
            # Dict to DataFrame
            df = pd.DataFrame(self.stocks.values(), index=self.stocks.keys()).T
            for i in range(len(df.keys())):
                try:
                    # Open Price
                    df_var = df.values[0][i]['Open']
                    self.open_price.insert(loc=i, column=df.columns[i], value=df_var)
                    # Clos Price
                    df_var = df.values[0][i]['Close']
                    self.close_price.insert(loc=i, column=df.columns[i], value=df_var)
                    # High Price
                    df_var = df.values[0][i]['High']
                    self.high_price.insert(loc=i, column=df.columns[i], value=df_var)
                    # Low Price
                    df_var = df.values[0][i]['Low']
                    self.low_price.insert(loc=i, column=df.columns[i], value=df_var)
                    # Volume
                    df_var = df.values[0][i]['Volume']
                    self.volume.insert(loc=i, column=df.columns[i], value=df_var)
                    # Dividends
                    df_var = df.values[0][i]['Dividends']
                    self.dividends.insert(loc=i, column=df.columns[i], value=df_var)
                    # Stock Splits
                    df_var = df.values[0][i]['Stock Splits']
                    self.stock_splits.insert(loc=i, column=df.columns[i], value=df_var)
                except KeyError:
                    er = Error(KeyError, df.keys()[i], 'missing data error in Balance Sheet')
                    self.e_list.add_list(er)
                    erh = ErrorHandler(er)
                    erh.print_error()
                    # Recover missing data
                    self.open_price.insert(loc=i, column=df.columns[i], value=None)
                    self.close_price.insert(loc=i, column=df.columns[i], value=None)
                    self.high_price.insert(loc=i, column=df.columns[i], value=None)
                    self.low_price.insert(loc=i, column=df.columns[i], value=None)
                    self.volume.insert(loc=i, column=df.columns[i], value=None)
                    self.dividends.insert(loc=i, column=df.columns[i], value=None)
                    self.stock_splits.insert(loc=i, column=df.columns[i], value=None)

                    continue

            # 欠損データの補完
            self.open_price = self.open_price.ffill()
            self.close_price = self.close_price.ffill()
            self.high_price = self.high_price.ffill()
            self.low_price = self.low_price.ffill()
            self.volume = self.volume.ffill()
            self.dividends = self.dividends.ffill()
            self.stock_splits = self.stock_splits.ffill()

            # print(" *** open *** ")
            # print(self.open_price.shape)
            # print(" *** close *** ")
            # print(self.close_price.shape)
        self.result.action_name = 'Read Stock History Data'
        self.result.result_type = 'number'
        self.result.result_data = self.__len__()
        self.result.error_list = self.e_list
        if self.result.result_data == 0:
            self.result.exec_continue = False

        return self.result
