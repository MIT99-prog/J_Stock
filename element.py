#
import pandas as pd


class Element:
    def __init__(self, code: str, data: pd.DataFrame):
        self.company = code
        self.data = data

    def get_open(self) -> pd.Series:
        open_price = self.data['Open']
        return open_price

    def get_close(self) -> pd.Series:
        close_price = self.data['Close']
        return close_price
