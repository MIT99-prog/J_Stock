import pandas as pd
import yfinance as yf
from element import Stock_Element
from serialize import Data


class Stocks:
    def __init__(self):
        self.stocks = []
        self.tickers = yf.Tickers("")

        self.read_jasdaq()

        self.get_stocks()

    def read_jasdaq(self):
        jasdaq_code = pd.read_csv("jasdaq.txt")
        company_codes = [str(s) + ".T" for s in jasdaq_code.code]
        # stocks.append("^JASDAQ")  #JASDAQ Index
        self.tickers = yf.Tickers(" ".join(company_codes))
        print(" *** tickers *** ")
        print(self.tickers)

    def get_stocks(self):
        # open_price = []  # 始値
        # close_price = []  # 終値

        for i in range(len(self.tickers.tickers)):
            # open_price.append(tickers.tickers[i].history(period="1mo").Open)
            # close_price.append(tickers.tickers[i].history(period="1mo").Close)
            elt = Stock_Element(self.tickers.tickers[i].ticker, self.tickers.tickers[i].history(period="1mo"))
            self.stocks.append(elt)
            # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo

        # self.stocks = yf.download(self.tickers, period="1mo")

        data_save = Data()  # Create Data class of serialize.py
        data_save.save_data('stock', self.stocks)  # Save data to stock file


if __name__ == '__main__':
    Stocks()
