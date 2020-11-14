#
import pandas as pd
from serialize import Data
from get_stock_data import Element


class Ranking:
    def __init__(self):
        self.stocks = []
        self.open_price = pd.DataFrame()
        self.close_price = pd.DataFrame()
        self.data = Data()

        self.data_read()
        self.generate_ranking()

    def data_read(self):
        filename = "stock"

        self.stocks = self.data.load_data(filename)

        for i in range(len(self.stocks)):
            elt = self.stocks[i]

            self.open_price.insert(loc=i, column=elt.company, value=elt.get_open())
            self.close_price.insert(loc=i, column=elt.company, value=elt.get_close())

    def generate_ranking(self):
        # open_frame = pd.DataFrame(open_price).T  # DataFrame化
        # open_frame.columns = stocks  # カラム名の設定
        open_frame = self.open_price.ffill()  # 欠損データの補完

        # close_frame = pd.DataFrame(close_price).T  # DataFrame化
        # close_frame.columns = stocks  # カラム名の設定
        close_frame = self.close_price.ffill()  # 欠損データの補完
        print(" *** open *** ")
        print(open_frame)
        print(" *** close *** ")
        print(close_frame)

        # Calc Balance from Open Price to Close price
        balance = close_frame - open_frame
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
