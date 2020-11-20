#
import pandas as pd

from error_handler import Error_Handler, Error
from serialize import Data


class Stocks:
    def __init__(self):
        # self.stocks = []
        self.stocks = dict()

    def __getitem__(self, i):
        keys = self.stocks.keys()
        key = list(keys)[i]
        return self.stocks.get(key)

    def __len__(self):
        return self.stocks.__len__()

class Stocks_Write(Stocks):

    def __init__(self):
        super().__init__()

    def get_data(self, tickers) -> int:

        for i in range(len(tickers.tickers)):
            try:
                # elt = Stock_Element(tickers.tickers[i].ticker, tickers.tickers[i].history(period="1mo"))
                # self.stocks.append(elt)
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                self.stocks[tickers.tickers[i].ticker] = tickers.tickers[i].history(period='1mo')

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Stock Data Error!')
                erh = Error_Handler(er)
                erh.print_error()

        # self.stocks = yf.download(self.tickers, period="1mo")  動かない！

        data = Data()  # Create Data class of serialize.py
        data.save_data('stock', self.stocks)  # Save data to stock file
        return self.__len__()

class Stocks_Read(Stocks):
    def __init__(self, read_type):
        super().__init__()

        # initialize values
        # self.se_dict = dict()  # Stock Dictionary
        self.open_price = pd.DataFrame()  # 始値
        self.close_price = pd.DataFrame()  # 終値
        self.high_price = pd.DataFrame()  # 高値
        self.low_price = pd.DataFrame()  # 安値
        self.volume = pd.DataFrame()  # 出来高
        self.dividends = pd.DataFrame()  # 配当
        self.stock_splits = pd.DataFrame()  # 分割

        self.data_read(read_type)

    def data_read(self, read_type):
        filename = "stock"  # data file name
        data = Data()

        self.stocks = data.load_data(filename)



        # Create dictionary of income statement
        '''
        se = Stock_Element()
        for i in range(self.__len__()):
            se.company = self.__getitem__(i).company
            se.data = self.__getitem__(i).data
            self.se_dict[se.company] = se.data
        '''
        if read_type == 'Extend':
            # Dict to DataFrame
            df = pd.DataFrame(self.stocks.values(), index=self.stocks.keys()).T
            for i in range(len(df.keys())):
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

            # generate values
            '''
            for i in range(self.__len__()):
                elt = self.__getitem__(i)

                self.open_price.insert(loc=i, column=elt.company, value=elt.get_open())
                self.close_price.insert(loc=i, column=elt.company, value=elt.get_close())
                self.high_price.insert(loc=i, column=elt.company, value=elt.get_high())
                self.low_price.insert(loc=i, column=elt.company, value=elt.get_low())
                self.volume.insert(loc=i, column=elt.company, value=elt.get_volume())
                self.dividends.insert(loc=i, column=elt.company, value=elt.get_dividends())
                self.stock_splits.insert(loc=i, column=elt.company, value=elt.get_stock_splits())
            '''
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
