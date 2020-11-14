#
import pandas as pd


class Element:
    def __init__(self, code: str, data: pd.DataFrame):
        self.company = code
        self.data = data


class Stock_Element(Element):
    def __init__(self, code: str, data: pd.DataFrame):
        super().__init__(code, data)

    def get_open(self) -> pd.Series:
        open_price = self.data['Open']
        return open_price

    def get_close(self) -> pd.Series:
        close_price = self.data['Close']
        return close_price

    def get_high(self) -> pd.Series:
        high_price = self.data['High']
        return high_price

    def get_low(self) -> pd.Series:
        low_price = self.data['Low']
        return low_price

    def get_volume(self) -> pd.Series:
        volume = self.data['Volume']
        return volume

    def get_dividends(self) -> pd.Series:
        dividends = self.data['Dividends']
        return dividends

    def get_stock_splits(self) -> pd.Series:
        stock_splits = self.data['Stock Splits']
        return stock_splits
