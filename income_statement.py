#
import numpy as np
import pandas as pd
from element import Income_Element
from serialize import Data
from error_handler import Error_Handler, Error

class Incomes:
    def __init__(self):
        self.incomes = []
        # self.incomes = dict()

    def __getitem__(self, i):
        return self.incomes[i]

    def __len__(self):
        return self.incomes.__len__()


class Incomes_Write(Incomes):

    def __init__(self):
        super().__init__()

    def get_incomes(self, tickers) -> int:

        for i in range(len(tickers.tickers)):
            try:
                elt = Income_Element(tickers.tickers[i].ticker, tickers.tickers[i].financials)
                self.incomes.append(elt)
                print(" i= " + str(i))
                # self.incomes[tickers.tickers[i].ticker] = tickers.tickers[i].financials

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Income Data Error!')
                erh = Error_Handler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        data.save_data('income', self.incomes)  # Save data to stock file
        return self.__len__()


class Incomes_Read(Incomes):
    def __init__(self):
        super().__init__()

        # initialize values
        self.ie_dict = dict()  # Income Statement Dictionary
        self.total_revenues = pd.DataFrame()  # 売上高
        self.operating_incomes = pd.DataFrame()  # 営業利益
        self.net_incomes = pd.DataFrame()  # 当期純利益

        self.data_read()

    def data_read(self) -> int:
        # Deserialize Income-statement data
        filename = "income"  # data file name
        data = Data()

        self.incomes = data.load_data(filename)

        # Create dictionary of income statement
        ie = Income_Element()
        for i in range(self.__len__()):
            ie.company = self.__getitem__(i).company
            ie.data = self.__getitem__(i).data
            self.ie_dict[ie.company] = ie.data

        # create index
        # index = self.incomes[0].data.T.index
        index = self.__getitem__(0).data.T.index
        for i in range(self.__len__()):
            # for i in range(len(self.incomes)):
            index = index.append(self.__getitem__(i).data.T.index)

        index = set(index)
        # create data
        self.total_revenues = pd.DataFrame(index=index)
        self.operating_incomes = pd.DataFrame(index=index)
        self.net_incomes = pd.DataFrame(index=index)

        for i in range(self.__len__()):
            elt = self.__getitem__(i)

            self.total_revenues.insert(loc=i, column=elt.company, value=elt.get_total_revenue(),
                                       allow_duplicates=False)
            self.operating_incomes.insert(loc=i, column=elt.company, value=elt.get_operating_income(),
                                          allow_duplicates=False)
            self.net_incomes.insert(loc=i, column=elt.company, value=elt.get_net_income(),
                                    allow_duplicates=False)

        # 欠損データの補完
        self.total_revenues = self.total_revenues.ffill()
        self.operating_incomes = self.operating_incomes.ffill()
        self.net_incomes = self.net_incomes.ffill()

        print(" *** Total Revenue *** ")
        print(self.total_revenues)
        print(" *** Operating Income *** ")
        print(self.operating_incomes)
        print(" *** Net Income *** ")
        print(self.net_incomes)
        # return self.__len__()

