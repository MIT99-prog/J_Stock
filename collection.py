#
import pandas as pd
import xarray as xr
import yfinance as yf

from errorhandler import ErrorHandler, Error, ErrorList
from serialize import Data, FileName
from widget_helper import Result, DisplayInfo


class CollectionWrite:
    def __init__(self, di: DisplayInfo):
        # set initial Values
        self.di = di
        self.collection = dict()
        self.result = Result()
        self.e_list = ErrorList()
        self.filename = FileName()

        self.result.action_name = self.__str__()
        self.result.exec_continue = True

    def get_data(self) -> Result:
        # create Tickers
        companies_t = [str(s) + ".T" for s in self.di.companies]
        # get tks from yahoo finance
        tks = None
        try:

            tks = yf.Tickers(" ".join(companies_t))  # Get Data from Yahoo Finance
            for i in range(tks.symbols.__len__()):
                self.collection[tks.symbols[i]] = tks.tickers[i]

        except ConnectionError:
            Error(ConnectionError, tks, 'Cannot get data from Yahoo Finance!')

        data = Data()  # Create Data class of serialize.py
        self.filename.market = self.di.market
        self.result = data.save_data(self.filename, self.collection)  # Save data to stock file
        # self.result = data.save_data(self.filename, xr_array)  # Save data to stock file  # for xarray test
        if self.result.exec_continue:
            self.result.action_name = self.__str__()
            self.result.result_type = 'tickers'
            self.result.result_data = self.collection
            self.result.error_list = self.e_list
        else:
            pass
        return self.result


class CollectionRead:
    def __init__(self, market: str, read_type: str):
        # set initial Values
        self.result = Result()
        self.e_list = ErrorList()
        self.collection = dict()

        # initialize for read extend mode
        self.collection_actions = dict()
        self.collection_balance_sheet = dict()
        self.collection_calendar = dict()
        self.collection_cashflow = dict()
        self.collection_dividends = dict()
        self.collection_earnings = dict()
        self.collection_financials = dict()
        self.collection_history = dict()
        self.collection_info = dict()
        self.collection_major_holders = dict()
        self.collection_options = dict()
        self.collection_quarterly_balance_sheet = dict()
        self.collection_quarterly_cashflow = dict()
        self.collection_quarterly_earnings = dict()
        self.collection_quarterly_financials = dict()
        self.collection_splits = dict()
        self.collection_ticker = dict()

        # Create FileName Object as filename
        self.filename = FileName()
        self.data_read(market, read_type)

    def __getitem__(self, i):
        keys = self.collection.keys()
        key = list(keys)[i]
        return self.collection.get(key)

    def data_read(self, market: str, read_type: str):
        # internal function called by constructor
        # Set market data
        self.filename.market = market
        # Deserialize Income-statement data
        data = Data()
        result = data.load_data(self.filename)
        if result.exec_continue:
            self.collection = result.result_data  # As Dictionary
            # Base Data Read (Dictionary)
            # if read_type == 'Base':
            # self.read_base(di)

            # Extended Data Read (List)
            if read_type == 'Extend':
                self.read_extend()
        else:
            self.result = result

    def read_base(self, di: DisplayInfo):
        # initialize
        collection_list = dict()

        keys = self.collection.keys()
        key = ''
        for i in range(len(self.collection)):
            try:
                key = list(keys)[i]
                if di.data_type == 'actions':
                    self.collection_actions[key] = self.collection.get(key).actions
                if di.data_type == 'balance_sheet':
                    self.collection_balance_sheet[key] = self.collection.get(key).balance_sheet
                if di.data_type == 'calendar':
                    self.collection_calendar[key] = self.collection.get(key).calendar
                if di.data_type == 'cashflow':
                    self.collection_cashflow[key] = self.collection.get(key).cashflow
                if di.data_type == 'dividends':
                    self.collection_dividends[key] = self.collection.get(key).dividends
                if di.data_type == 'earnings':
                    self.collection_earnings[key] = self.collection.get(key).earnings
                if di.data_type == 'financials':
                    self.collection_financials[key] = self.collection.get(key).financials
                if di.data_type == 'history':
                    self.collection_history[key] = self.collection.get(key).history(period='max')
                if di.data_type == 'info':
                    self.collection_info[key] = self.collection.get(key).info
                if di.data_type == 'major_holders':
                    self.collection_major_holders[key] = self.collection.get(key).major_holders
                if di.data_type == 'options':
                    self.collection_options[key] = self.collection.get(key).options
                if di.data_type == 'quarterly_balance_sheet':
                    self.collection_quarterly_balance_sheet[key] = self.collection.get(key).quarterly_balance_sheet
                if di.data_type == 'quarterly_cashflow':
                    self.collection_quarterly_cashflow[key] = self.collection.get(key).quarterly_cashflow
                if di.data_type == 'quarterly_earnings':
                    self.collection_quarterly_earnings[key] = self.collection.get(key).quarterly_earnings
                if di.data_type == 'quarterly_financials':
                    self.collection_quarterly_financials[key] = self.collection.get(key).quarterly_financials
                if di.data_type == 'splits':
                    self.collection_splits[key] = self.collection.get(key).splits
                if di.data_type == 'ticker':
                    self.collection_ticker[key] = self.collection.get(key).ticker

            except KeyError:
                er = Error(KeyError, key, 'Not exist!')
                erh = ErrorHandler(er)
                erh.print_error()
            except IndexError:
                er = Error(IndexError, key, 'Index not exist!')
                erh = ErrorHandler(er)
                erh.print_error()

        # Create collection_list (dictionary)
        collection_list['actions'] = self.collection_actions
        collection_list['balance_sheet'] = self.collection_balance_sheet
        collection_list['calendar'] = self.collection_calendar
        collection_list['cashflow'] = self.collection_cashflow
        collection_list['dividends'] = self.collection_dividends
        collection_list['earnings'] = self.collection_earnings
        collection_list['financials'] = self.collection_financials
        collection_list['history'] = self.collection_history
        collection_list['info'] = self.collection_info
        collection_list['major_holders'] = self.collection_major_holders
        collection_list['options'] = self.collection_options
        collection_list['quarterly_balance_sheet'] = self.collection_quarterly_balance_sheet
        collection_list['quarterly_cashflow'] = self.collection_quarterly_cashflow
        collection_list['quarterly_earnings'] = self.collection_quarterly_earnings
        collection_list['quarterly_financials'] = self.collection_quarterly_financials
        collection_list['splits'] = self.collection_splits
        collection_list['ticker'] = self.collection_ticker

        # Set data to result object
        self.result.action_name = self.__str__()
        self.result.result_type = 'collection'
        self.result.result_data = collection_list
        self.result.error_list = self.e_list

    def read_extend(self):
        # initialize indicator values for Extend Mode

        # Income Statement
        total_revenues = pd.DataFrame()  # 売上高
        operating_incomes = pd.DataFrame()  # 営業利益
        net_incomes = pd.DataFrame()  # 当期純利益

        # initialize index
        index = self.generate_index(self.collection_financials)

        # create dataframes
        total_revenues = pd.DataFrame(index=index)
        operating_incomes = pd.DataFrame(index=index)
        net_incomes = pd.DataFrame(index=index)

        # Dict to DataFrame
        # df = pd.DataFrame(self.collection_financials.values(), index=self.collection_financials.keys()).T
        keys = self.collection_financials.keys()
        for i in range(len(keys)):
            try:
                key = list(keys)[i]
                df = self.collection_financials.get(key)
                # Total Revenues
                series_var = df.T['Total Revenue']
                total_revenues.insert(loc=i, column=key, value=series_var)
                # Operating Collection
                series_var = df.T['Operating Income']
                operating_incomes.insert(loc=i, column=key, value=series_var)
                # Net Collection
                series_var = df.T['Net Income']
                net_incomes.insert(loc=i, column=key, value=series_var)

            except KeyError:
                er = Error(KeyError, key, 'missing data error in Income Statement')
                self.e_list.add_list(er)
                erh = ErrorHandler(er)
                erh.print_error()
                # Recover missing data
                total_revenues.insert(loc=i, column=key, value=None)
                operating_incomes.insert(loc=i, column=key, value=None)
                net_incomes.insert(loc=i, column=key, value=None)

            continue

        # 欠損データの補完
        total_revenues = total_revenues.ffill()
        operating_incomes = operating_incomes.ffill()
        net_incomes = net_incomes.ffill()
        collection_list = {'Total Revenue': total_revenues, 'Operating Income': operating_incomes,
                           'Net Income': net_incomes}

        # ser result
        self.result.action_name = 'Read Income Statement Data Extend Mode'
        self.result.result_type = 'dataframe'
        self.result.result_data = collection_list
        self.result.error_list = self.e_list
        if total_revenues.__len__() == 0:
            self.result.exec_continue = False

    def read_cube(self):
        # TODO: compress the dimension of datetime

        # set data to xarray
        df_info = pd.DataFrame(self.collection_info.values(), index=self.collection_info.keys()).T
        xr_array = xr.DataArray(df_info.values, coords=[df_info.index, df_info.columns],
                                dims=['items', 'companies'])

    @staticmethod
    def generate_index(collection_p: dict) -> pd.DataFrame.index:
        # initialize index
        statement = pd.DataFrame()
        index = statement.index

        for i in range(collection_p.__len__()):
            keys = collection_p.keys()
            key = list(keys)[i]
            statement = collection_p.get(key)
            index = index.append(statement.T.index)

        index = set(index)

        return index


if __name__ == '__main__':
    di = DisplayInfo('mothers', 'info', [1401, 1431, 1436], '1401')
    # cw = CollectionWrite(di)
    # rslt = cw.get_data()
    cr = CollectionRead(di, 'Base')
    # cr = CollectionRead(di, 'Extend')
    print('end')
