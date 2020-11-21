#
import pandas as pd

from errorhandler import ErrorHandler, Error, ErrorList
from serialize import Data, FileName
from widget_helper import Result, DisplayInfo


class Statements:
    def __init__(self):
        self.statements = dict()
        self.e_list = ErrorList()
        self.result = Result()

    def __getitem__(self, i):
        keys = self.statements.keys()
        key = list(keys)[i]
        return self.statements.get(key)

    def __len__(self):
        return self.statements.__len__()


class StatementsWrite(Statements):

    def __init__(self, di: DisplayInfo):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)

    def get_data(self, tickers) -> Result:

        for i in range(len(tickers.tickers)):
            try:

                self.statements[tickers.tickers[i].ticker] = tickers.tickers[i].cashflow

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Cash Flow Error!')
                erh = ErrorHandler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        self.result = data.save_data(self.filename, self.statements)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = 'Get Cash Flow Data'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass
        return self.result


class StatementsRead(Statements):
    def __init__(self, di: DisplayInfo, read_type: str):
        super().__init__()
        self.read_type = read_type
        self.filename = FileName(di.market, di.data_type)
        # initialize values
        self.total_cashflows_from_operating_activities = pd.DataFrame()  # 営業キャッシュフロー
        self.total_cashflows_from_financing_activities = pd.DataFrame()  # 財務キャッシュフロー
        self.total_cashflows_from_investing_activities = pd.DataFrame()  # 投資キャッシュフロー

        self.data_read()

    def data_read(self) -> Result:
        # Deserialize Cash Flow data
        data = Data()
        self.result = data.load_data(self.filename)
        if self.result.exec_continue:
            self.statements = self.result.result_data
            self.result.action_name = 'Read Cash Flow Data Base Mode'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass

        # Extended Data Read
        if self.read_type == 'Extend':
            # initialize index
            statement = pd.DataFrame()
            index = statement.index

            for i in range(self.__len__()):
                statement = self.__getitem__(i)
                index = index.append(statement.T.index)

            index = set(index)
            # create dataframes
            self.total_cashflows_from_operating_activities = pd.DataFrame(index=index)
            self.total_cashflows_from_financing_activities = pd.DataFrame(index=index)
            self.total_cashflows_from_investing_activities = pd.DataFrame(index=index)

            # Dictionary to DataFrame
            df = pd.DataFrame(self.statements.values(), index=self.statements.keys()).T
            for i in range(len(df.keys())):
                # Total Revenues
                df_var = df.values[0][i].T['Total Cashflows From Operating Activities']
                self.total_cashflows_from_operating_activities.insert(loc=i, column=df.columns[i], value=df_var)
                # Operating Incomes
                df_var = df.values[0][i].T['Total Cashflows From Financing Activities']
                self.total_cashflows_from_financing_activities.insert(loc=i, column=df.columns[i], value=df_var)
                # Net Incomes
                df_var = df.values[0][i].T['Total Cashflows From Investing Activities']
                self.total_cashflows_from_investing_activities.insert(loc=i, column=df.columns[i], value=df_var)

            # 欠損データの補完
            self.total_cashflows_from_operating_activities = self.total_cashflows_from_operating_activities.ffill()
            self.total_cashflows_from_financing_activities = self.total_cashflows_from_financing_activities.ffill()
            self.total_cashflows_from_investing_activities = self.total_cashflows_from_investing_activities.ffill()

            self.result.action_name = 'Read Cash Flow Data Extend Mode'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
            if self.result.result_data == 0:
                self.result.exec_continue = False

        return self.result
