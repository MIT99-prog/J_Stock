#
import urllib.error

import pandas as pd
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
        self.filename.data_type = 'tickers'
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
    def __init__(self, market: str):
        # set initial Values
        self.result = Result()
        self.e_list = ErrorList()
        self.collection = dict()

        # Create FileName Object as filename
        self.filename = FileName()
        self.data_read(market)

    def __getitem__(self, i):
        keys = self.collection.keys()
        key = list(keys)[i]
        return self.collection.get(key)

    def data_read(self, market: str):
        # internal function called by constructor
        # Set market data
        self.filename.market = market
        self.filename.data_type = 'tickers'
        # Deserialize Income-statement data
        data = Data()
        result = data.load_data(self.filename)
        if result.exec_continue:
            self.collection = result.result_data  # As Dictionary

        else:
            self.result = result

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


class ConfigDataWrite:
    def __init__(self, market: str):
        # Set market data
        filename = FileName()
        filename.market = market

        # Deserialize Income-statement data
        filename.data_type = 'tickers'
        data = Data()
        result = data.load_data(filename)
        collection = dict()
        if result.exec_continue:
            collection = result.result_data  # As Dictionary

        print('Get Data ' + str(collection.__len__()) + ' companies 1/4')

        # initialize for read extend mode
        collection_actions = pd.DataFrame()
        collection_balance_sheet = pd.DataFrame()
        # collection_calendar = pd.DataFrame()
        collection_cashflow = pd.DataFrame()
        collection_dividends = pd.DataFrame()
        collection_earnings = pd.DataFrame()
        collection_financials = pd.DataFrame()
        collection_history = pd.DataFrame()
        collection_info = pd.DataFrame()
        collection_major_holders = pd.DataFrame()
        # collection_options = pd.DataFrame()
        collection_quarterly_balance_sheet = pd.DataFrame()
        collection_quarterly_cashflow = pd.DataFrame()
        collection_quarterly_earnings = pd.DataFrame()
        collection_quarterly_financials = pd.DataFrame()
        collection_splits = pd.DataFrame()
        # collection_ticker = pd.DataFrame()
        print('Create collection_xxx 2/4')
        i = 0
        e_list = ErrorList()
        for k, v in collection.items():
            try:
                collection_actions.insert(i, k, v.actions.mean(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / action', k)
                e_list.add_list(er)
                collection_actions.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / action', k)
                e_list.add_list(er)
                collection_actions.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / action', k)
                e_list.add_list(er)
                collection_actions.insert(i, k, None)
            try:
                collection_balance_sheet.insert(i, k, v.balance_sheet.mean(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / bs', k)
                e_list.add_list(er)
                collection_balance_sheet.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / bs', k)
                e_list.add_list(er)
                collection_balance_sheet.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / bs', k)
                e_list.add_list(er)
                collection_balance_sheet.insert(i, k, None)
                # collection_calendar.insert(i, k, v.calendar.mean(1))
            try:
                collection_cashflow.insert(i, k, v.cashflow.mean(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / cashflow', k)
                e_list.add_list(er)
                collection_cashflow.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / cashflow', k)
                e_list.add_list(er)
                collection_cashflow.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / cashflow', k)
                e_list.add_list(er)
                collection_cashflow.insert(i, k, None)
            try:
                collection_dividends.insert(i, k, v.dividends.mean(0))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / dividends', k)
                e_list.add_list(er)
                collection_dividends.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / dividends', k)
                e_list.add_list(er)
                collection_dividends.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / dividends', k)
                e_list.add_list(er)
                collection_dividends.insert(i, k, None)
            try:
                collection_earnings.insert(i, k, v.earnings.mean(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / earnings', k)
                e_list.add_list(er)
                collection_earnings.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / earnings', k)
                e_list.add_list(er)
                collection_earnings.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / earnings', k)
                e_list.add_list(er)
                collection_earnings.insert(i, k, None)
            try:
                collection_financials.insert(i, k, v.financials.sum(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / financials', k)
                e_list.add_list(er)
                collection_financials.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / financials', k)
                e_list.add_list(er)
                collection_financials.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / financials', k)
                e_list.add_list(er)
                collection_financials.insert(i, k, None)
            try:
                collection_history.insert(i, k, v.history(period='1mo').mean(0))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / history', k)
                e_list.add_list(er)
                collection_history.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / history', k)
                e_list.add_list(er)
                collection_history.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / history', k)
                e_list.add_list(er)
                collection_history.insert(i, k, None)
            try:
                collection_info.insert(i, k, v.info.values)
            except KeyError:
                er = Error(KeyError, 'get_rank_data / info', k)
                e_list.add_list(er)
                collection_info.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / info', k)
                e_list.add_list(er)
                collection_info.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / info', k)
                e_list.add_list(er)
                collection_info.insert(i, k, None)
            try:
                collection_major_holders.insert(i, k, v.major_holders.mean(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / m_holders', k)
                e_list.add_list(er)
                collection_major_holders.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / m_holders', k)
                e_list.add_list(er)
                collection_major_holders.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / m_holders', k)
                e_list.add_list(er)
                collection_major_holders.insert(i, k, None)
                # collection_options.insert(i, k, v.options)
            try:
                collection_quarterly_balance_sheet.insert(i, k, v.quarterly_balance_sheet.mean(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / q_bs', k)
                e_list.add_list(er)
                collection_quarterly_balance_sheet.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / q_bs', k)
                e_list.add_list(er)
                collection_quarterly_balance_sheet.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / q_bs', k)
                e_list.add_list(er)
                collection_quarterly_balance_sheet.insert(i, k, None)
            try:
                collection_quarterly_cashflow.insert(i, k, v.quarterly_cashflow.sum(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / q_cashflow', k)
                e_list.add_list(er)
                collection_quarterly_cashflow.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / q_cashflow', k)
                e_list.add_list(er)
                collection_quarterly_cashflow.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / q_cashflow', k)
                e_list.add_list(er)
                collection_quarterly_cashflow.insert(i, k, None)
            try:
                collection_quarterly_earnings.insert(i, k, v.quarterly_earnings.sum(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / q_earnings', k)
                e_list.add_list(er)
                collection_quarterly_earnings.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / q_earnings', k)
                e_list.add_list(er)
                collection_quarterly_earnings.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / q_earnings', k)
                e_list.add_list(er)
                collection_quarterly_earnings.insert(i, k, None)
            try:
                collection_quarterly_financials.insert(i, k, v.quarterly_financials.sum(1))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / q_financials', k)
                e_list.add_list(er)
                collection_quarterly_financials.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / q_financials', k)
                e_list.add_list(er)
                collection_quarterly_financials.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / q_financials', k)
                e_list.add_list(er)
                collection_quarterly_financials.insert(i, k, None)
            try:
                collection_splits.insert(i, k, v.splits.sum(0))
            except KeyError:
                er = Error(KeyError, 'get_rank_data / splits', k)
                e_list.add_list(er)
                collection_splits.insert(i, k, None)
            except ValueError:
                er = Error(ValueError, 'get_rank_data / splits', k)
                e_list.add_list(er)
                collection_splits.insert(i, k, None)
            except urllib.error.HTTPError:
                er = Error(urllib.error.HTTPError, 'get_rank_data / splits', k)
                e_list.add_list(er)
                collection_splits.insert(i, k, None)

            i = i + 1
            print(str(i) + ' : key = ' + k)

        for i in range(e_list.get_length()):
            ErrorHandler(e_list.error_list[i]).print_error()

        print('Create collection 3/4')
        # Create collection (dictionary)
        collection = dict()
        collection['actions'] = collection_actions
        collection['balance_sheet'] = collection_balance_sheet
        # collection['calendar'] = collection_calendar
        collection['cashflow'] = collection_cashflow
        collection['dividends'] = collection_dividends
        collection['earnings'] = collection_earnings
        collection['financials'] = collection_financials
        collection['history'] = collection_history
        collection['info'] = collection_info
        collection['major_holders'] = collection_major_holders
        # collection['options'] = collection_options
        collection['quarterly_balance_sheet'] = collection_quarterly_balance_sheet
        collection['quarterly_cashflow'] = collection_quarterly_cashflow
        collection['quarterly_earnings'] = collection_quarterly_earnings
        collection['quarterly_financials'] = collection_quarterly_financials
        collection['splits'] = collection_splits
        # collection['ticker'] = collection_ticker
        print('Save data as a file 4/4')
        data = Data()  # Create Data class of serialize.py
        filename.data_type = 'config'
        self.result = data.save_data(filename, collection)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = self.__str__()
            self.result.result_type = 'dictionary'
            self.result.result_data = collection
            # self.result.error_list = self.e_list
        else:
            self.result.exec_continue = False


class ConfigDataRead:
    def __init__(self, market: str):
        # set initial Values
        self.result = Result()
        self.e_list = ErrorList()
        self.collection_list = dict()

        # Create FileName Object as filename
        self.filename = FileName()
        self.data_read(market)

    def data_read(self, market: str):
        # internal function called by constructor
        # Set market data
        self.filename.market = market
        self.filename.data_type = 'config'
        # Deserialize Income-statement data
        data = Data()
        result = data.load_data(self.filename)
        if result.exec_continue:
            self.collection_list = result.result_data  # As Dictionary
        else:
            self.result = result


if __name__ == '__main__':
    # di = DisplayInfo('mothers', 'info', [1401, 1431, 1436], '1401')
    # cw = CollectionWrite(di)
    # rslt = cw.get_data()
    # cr = CollectionRead(di.market)
    # cr = CollectionRead(di, 'Extend')
    # ConfigDataWrite('mothers')
    ConfigDataRead('mothers')
    print('end')
