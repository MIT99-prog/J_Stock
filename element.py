#
import pandas as pd
import datetime as dt


class Element:
    def __init__(self, code, data):
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


class Income_Element(Element):
    def __init__(self, code='', data=pd.DataFrame()):
        super().__init__(code, data)

    def get_company(self):
        return self.company

    def get_income(self):
        return self.data

    def get_data_index(self):
        return self.data.index


    def get_total_revenue(self) -> pd.Series:  # 売上高
        total_revenue = self.data.T['Total Revenue']
        # total_revenue.index = total_revenue.index.year
        return total_revenue

    def get_operating_income(self) -> pd.Series:  # 営業利益
        operating_income = self.data.T['Operating Income']
        # operating_income.index = operating_income.index.year
        return operating_income

    def get_net_income(self) -> pd.Series:  # 当期純利益
        net_income = self.data.T['Net Income']
        # net_income.index = net_income.index.year
        return net_income
