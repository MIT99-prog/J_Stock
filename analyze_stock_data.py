#
import pandas as pd
from stocks import Stocks_Read
from serialize import Data


class Ranking:
    def __init__(self):
        self.stocks = []
        self.open_price = pd.DataFrame()
        self.close_price = pd.DataFrame()
        self.data = Data()

        self.generate_ranking()

    def generate_ranking(self):
        # Get Stocks data
        self.stocks = Stocks_Read()

        # Calc Balance from Open Price to Close price
        balance = self.stocks.close_price - self.stocks.open_price
        print(" *** balance *** ")
        print(balance)

        # Calc average of the balance
        mu = balance.mean()
        mu_mean = mu.mean()
        mu_std = mu.std()
        mu_point = (mu - mu_mean) / mu_std

        print(" *** mu *** ")
        print(mu)
        print(mu_mean, mu_std)

        # Calc variance of the balance
        sigma2 = balance.var()
        sigma2_mean = sigma2.mean()
        sigma2_std = sigma2.std()
        sigma2_point = (sigma2 - sigma2_mean) / sigma2_std

        print(" *** sigma2 *** ")
        print(sigma2)
        print(sigma2_mean, sigma2_std)

        print(" *** point *** ")
        print(mu_point)
        print(sigma2_point)

        point = mu_point + sigma2_point * -1
        point = point.sort_values(ascending=False)

        filename = "rank"
        self.data.save_data(filename, point)

        print("Ranking")
        print(point)


if __name__ == '__main__':
    Ranking()
