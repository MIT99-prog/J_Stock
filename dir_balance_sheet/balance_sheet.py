#
import pandas as pd

from errorhandler import ErrorHandler, Error, ErrorList
from serialize import Data, FileName
from widget_helper import Result, DisplayInfo

class BSes:
    def __init__(self):
        self.e_list = ErrorList()
        self.bses = dict()
        self.result = Result()

    def __getitem__(self, i):
        keys = self.bses.keys()
        key = list(keys)[i]
        return self.bses.get(key)

    def __len__(self):
        return self.bses.__len__()

class BSesWrite(BSes):

    def __init__(self, di: DisplayInfo):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)

    def get_data(self, tickers) -> Result:

        for i in range(len(tickers.tickers)):
            try:
                self.bses[tickers.tickers[i].ticker] = tickers.tickers[i].balance_sheet

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get BS Data Error!')
                self.e_list.add_list(er)
                erh = ErrorHandler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        self.result = data.save_data(self.filename, self.bses)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = 'Get Balance Sheet Data'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass
        return self.result

class BSesRead(BSes):
    def __init__(self, di: DisplayInfo, read_type: str):
        super().__init__()
        self.filename = FileName()
        self.filename.market = di.market

        # initialize values
        self.total_assets = pd.DataFrame()  # 資産
        self.total_liab = pd.DataFrame()  # 負債
        self.total_stockholder_equity = pd.DataFrame()  # 自己資本
        self.total_current_assets = pd.DataFrame()  # 流動資産
        self.total_current_liabilities = pd.DataFrame()  # 流動負債

        self.result = self.data_read(read_type)

    def data_read(self, read_type) -> Result:
        # Deserialize Balance Sheet data
        data = Data()
        self.result = data.load_data(self.filename)
        if self.result.exec_continue:
            self.bses = self.result.result_data
            self.result.action_name = 'Read Balance Sheet Data Base Mode'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass

        # Extend mode
        if read_type == 'Extend':
            # initialize index
            bs = pd.DataFrame()
            index = bs.index

            for i in range(self.__len__()):
                bs = self.__getitem__(i)
                index = index.append(bs.T.index)

            index = set(index)
            # create dataframes
            self.total_assets = pd.DataFrame(index=index)
            self.total_liab = pd.DataFrame(index=index)
            self.total_stockholder_equity = pd.DataFrame(index=index)
            self.total_current_liabilities = pd.DataFrame(index=index)
            self.total_current_assets = pd.DataFrame(index=index)

            # Dict to DataFrame
            df = pd.DataFrame(self.bses.values(), index=self.bses.keys()).T
            for i in range(len(df.keys())):
                try:
                    # Total Assets
                    df_var = df.values[0][i].T['Total Assets']
                    self.total_assets.insert(loc=i, column=df.columns[i], value=df_var)
                    # Total Liabilities
                    df_var = df.values[0][i].T['Total Liab']
                    self.total_liab.insert(loc=i, column=df.columns[i], value=df_var)
                    # Total Stockholder Equity
                    df_var = df.values[0][i].T['Total Stockholder Equity']
                    self.total_stockholder_equity.insert(loc=i, column=df.columns[i], value=df_var)
                    # Total Current Liabilities
                    df_var = df.values[0][i].T['Total Current Liabilities']
                    self.total_current_liabilities.insert(loc=i, column=df.columns[i], value=df_var)
                    # Total Current Assets
                    df_var = df.values[0][i].T['Total Current Assets']
                    self.total_current_assets.insert(loc=i, column=df.columns[i], value=df_var)
                except KeyError:
                    er = Error(KeyError, df.keys()[i], 'missing data error in Balance Sheet')
                    self.e_list.add_list(er)
                    erh = ErrorHandler(er)
                    erh.print_error()
                    # Recover missing data
                    self.total_assets.insert(loc=i, column=df.columns[i], value=None)
                    self.total_liab.insert(loc=i, column=df.columns[i], value=None)
                    self.total_stockholder_equity.insert(loc=i, column=df.columns[i], value=None)
                    self.total_current_liabilities.insert(loc=i, column=df.columns[i], value=None)
                    self.total_current_assets.insert(loc=i, column=df.columns[i], value=None)

                    continue

            # 欠損データの補完
            self.total_assets = self.total_assets.ffill()
            self.total_liab = self.total_liab.ffill()
            self.total_stockholder_equity = self.total_stockholder_equity.ffill()
            self.total_current_liabilities = self.total_current_liabilities.ffill()
            self.total_current_assets = self.total_current_assets.ffill()

            self.result.action_name = 'Read Balance Sheet Data Extend Mode'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
            if self.result.result_data == 0:
                self.result.exec_continue = False

        return self.result

if __name__ == '__main__':
    di = DisplayInfo('mothers', 'info', [1401, 1431, 1436], '1401')
    # cw = CollectionWrite(di)
    # rslt = cw.get_data()
    # cr = CollectionRead(di, 'Base')
    cr = BSesRead(di, 'Extend')
    print('end')
