#
import pandas as pd

from errorhandler import ErrorHandler, Error, ErrorList
from serialize import Data, FileName
from widget_helper import Result, DisplayInfo


class Incomes:
    def __init__(self):
        self.e_list = ErrorList()
        self.incomes = dict()
        self.result = Result()

    def __getitem__(self, i):
        keys = self.incomes.keys()
        key = list(keys)[i]
        return self.incomes.get(key)

    def __len__(self):
        return self.incomes.__len__()


class IncomesWrite(Incomes):

    def __init__(self, di: DisplayInfo):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)

    def get_data(self, tickers) -> Result:

        for i in range(len(tickers.tickers)):
            try:

                self.incomes[tickers.tickers[i].ticker] = tickers.tickers[i].financials

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Income Data Error!')
                erh = ErrorHandler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        self.result = data.save_data(self.filename, self.incomes)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = 'Get Balance Sheet Data'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass
        return self.result


class IncomesRead(Incomes):
    def __init__(self, di: DisplayInfo, read_type: str):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)
        # initialize values
        # self.ie_dict = dict()  # Income Statement Dictionary
        self.total_revenues = pd.DataFrame()  # 売上高
        self.operating_incomes = pd.DataFrame()  # 営業利益
        self.net_incomes = pd.DataFrame()  # 当期純利益

        self.result = self.data_read(read_type)

    def data_read(self, read_type) -> Result:
        # Deserialize Income-statement data
        data = Data()
        self.result = data.load_data(self.filename)
        if self.result.exec_continue:
            self.incomes = self.result.result_data
            self.result.action_name = 'Read Income Statement Data Base Mode'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass

        # Extended Data Read
        if read_type == 'Extend':
            # initialize index
            income = pd.DataFrame()
            index = income.index

            for i in range(self.__len__()):

                income = self.__getitem__(i)
                index = index.append(income.T.index)

            index = set(index)
            # create dataframes
            self.total_revenues = pd.DataFrame(index=index)
            self.operating_incomes = pd.DataFrame(index=index)
            self.net_incomes = pd.DataFrame(index=index)

            # Dict to DataFrame
            df = pd.DataFrame(self.incomes.values(), index=self.incomes.keys()).T
            for i in range(len(df.keys())):
                # Total Revenues
                df_var = df.values[0][i].T['Total Revenue']
                self.total_revenues.insert(loc=i, column=df.columns[i], value=df_var)
                # Operating Incomes
                df_var = df.values[0][i].T['Operating Income']
                self.operating_incomes.insert(loc=i, column=df.columns[i], value=df_var)
                # Net Incomes
                df_var = df.values[0][i].T['Net Income']
                self.net_incomes.insert(loc=i, column=df.columns[i], value=df_var)

            # 欠損データの補完
            self.total_revenues = self.total_revenues.ffill()
            self.operating_incomes = self.operating_incomes.ffill()
            self.net_incomes = self.net_incomes.ffill()

            self.result.action_name = 'Read Income Statement Data Extend Mode'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
            if self.result.result_data == 0:
                self.result.exec_continue = False

        return self.result
