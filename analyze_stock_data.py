#
import matplotlib.pyplot as plt

from serialize import Data
from stocks import Stocks_Read


class Analysis_Stock:
    def __init__(self, read_type):
        self.stock_collection = []
        # self.open_price = pd.DataFrame()
        # self.close_price = pd.DataFrame()
        self.data = Data()

        # Get Stocks data
        self.stock_collection = Stocks_Read(read_type)
        print('Data set completed!')

    def inquiry(self, company_code):
        # pd.set_option('display.max_columns', None)
        result = self.stock_collection.stocks.get(company_code + '.T')
        # result.to_excel('./test.xlsx')
        return result

    def generate_ranking(self):
        # Calc Balance from Open Price to Close price
        balance = self.stock_collection.close_price - self.stock_collection.open_price
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

        point = point.head(10)
        x = point.index
        y = point.values
        fig, ax = plt.subplots()
        ax.set_title('Change Price Ranking Graph (Top10)')
        ax.set_xlabel('Company')
        ax.set_ylabel('Point Average + Variant * -1')

        ax.bar(x, y, label='Point')
        ax.legend()
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    pass
