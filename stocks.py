#
import pandas as pd
from element import Stock_Element
from serialize import Data


class Stocks:
    def __init__(self):
        self.stocks = []

    def __getitem__(self, i):
        return self.stocks[i]

    def __len__(self):
        return self.stocks.__len__()

class Stocks_Write(Stocks):

    def __init__(self):
        super().__init__()

    def get_stocks(self, tickers) -> int:

        for i in range(len(tickers.tickers)):
            elt = Stock_Element(tickers.tickers[i].ticker, tickers.tickers[i].history(period="1mo"))
            self.stocks.append(elt)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

        # self.stocks = yf.download(self.tickers, period="1mo")  動かない！

        data = Data()  # Create Data class of serialize.py
        data.save_data('stock', self.stocks)  # Save data to stock file
        return self.__len__()

class Stocks_Read(Stocks):
    def __init__(self):
        super().__init__()

        # initialize values
        self.open_price = pd.DataFrame()  # 始値
        self.close_price = pd.DataFrame()  # 終値
        self.high_price = pd.DataFrame()  # 高値
        self.low_price = pd.DataFrame()  # 安値
        self.volume = pd.DataFrame()  # 出来高
        self.dividends = pd.DataFrame()  # 配当
        self.stock_splits = pd.DataFrame()  # 分割

        self.data_read()

    def data_read(self):
        filename = "stock"  # data file name
        data = Data()

        self.stocks = data.load_data(filename)

        for i in range(self.__len__()):
            elt = self.__getitem__(i)

            self.open_price.insert(loc=i, column=elt.company, value=elt.get_open())
            self.close_price.insert(loc=i, column=elt.company, value=elt.get_close())
            self.high_price.insert(loc=i, column=elt.company, value=elt.get_high())
            self.low_price.insert(loc=i, column=elt.company, value=elt.get_low())
            self.volume.insert(loc=i, column=elt.company, value=elt.get_volume())
            self.dividends.insert(loc=i, column=elt.company, value=elt.get_dividends())
            self.stock_splits.insert(loc=i, column=elt.company, value=elt.get_stock_splits())

        # 欠損データの補完
        self.open_price = self.open_price.ffill()
        self.close_price = self.close_price.ffill()
        self.high_price = self.high_price.ffill()
        self.low_price = self.low_price.ffill()
        self.volume = self.volume.ffill()
        self.dividends = self.dividends.ffill()
        self.stock_splits = self.stock_splits.ffill()

        print(" *** open *** ")
        print(self.open_price.shape)
        print(" *** close *** ")
        print(self.close_price.shape)
