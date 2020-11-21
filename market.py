#
import pandas as pd


class Market:
    def __init__(self):
        self.company_list = pd.read_excel('data_j.xls')
        self.market_list = pd.DataFrame()
        self.companies = []
        # self.market_code_t = []
        self.tickers = object
        # print(self.company_list.head(10))

    def select_companies(self, market):
        # select company codes from company_list in Market
        self.market_list = self.company_list[self.company_list['市場・商品区分'].str.contains(market)]
        # select code
        self.companies = self.market_list['コード'].values


class Jasdaq(Market):
    def __init__(self):
        super(Jasdaq, self).__init__()

        self.select_companies("JASDAQ")


class Tosho1(Market):
    def __init__(self):
        super(Tosho1, self).__init__()
        self.select_companies("市場第一部")


class Tosho2(Market):
    def __init__(self):
        super(Tosho2, self).__init__()
        self.select_companies("市場第二部")


class Mothers(Market):
    def __init__(self):
        super(Mothers, self).__init__()
        self.select_companies("マザーズ")


if __name__ == '__main__':
    # Jasdaq()
    # Tosho1()
    # Tosho2()
    # Mothers()
    pass
