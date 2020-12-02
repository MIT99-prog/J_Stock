#
import pandas as pd

from collection import CollectionRead, ConfigDataRead
from errorhandler import Error, ErrorList
from analysis_methods import AnalysisFinancials, AnalysisBalanceSheet, AnalysisHistory, AnalysisCashFlow
from widget_helper import Result, Graph, DisplayInfo
from formula import CalcRatioPer


class AnalysisStatement:
    def __init__(self, market: str):

        # Get Collection data
        self.collection_read = CollectionRead(market)

        if self.collection_read.result.exec_continue and self.collection_read.collection is not None:
            collection_number = str(len(self.collection_read.collection))
            print('Get ' + market + ' Collection Data (' + collection_number + ') Companies!')
            pass
        else:
            print('Get ' + market + ' Collection Data error!')

        print('Complete Collection Data Process!')

    # class Inquiry:
    def inquiry(self, di: DisplayInfo) -> Result:
        result = Result()
        result.action_name = self.__str__()

        try:
            # select company data
            statement = self.collection_read.collection.get(di.company + '.T')

            # Select data type
            if di.data_type == 'actions':
                statement = statement.actions
            elif di.data_type == 'balance_sheet':
                statement = statement.balance_sheet
            elif di.data_type == 'calendar':
                statement = statement.calendar
            elif di.data_type == 'cashflow':
                statement = statement.cashflow
            elif di.data_type == 'dividends':
                statement = statement.dividends
            elif di.data_type == 'earnings':
                statement = statement.earnings
            elif di.data_type == 'financials':
                statement = statement.financials
            elif di.data_type == 'history':
                statement = statement.history(period='1y')
            elif di.data_type == 'info':
                statement = statement.info
            elif di.data_type == 'major_holders':
                statement = statement.major_holders
            elif di.data_type == 'options':
                statement = statement.options
            elif di.data_type == 'quarterly_balance_sheet':
                statement = statement.quarterly_balance_sheet
            elif di.data_type == 'quarterly_cashflow':
                statement = statement.quarterly_cashflow
            elif di.data_type == 'quarterly_earnings':
                statement = statement.quarterly_earnings
            elif di.data_type == 'quarterly_financials':
                statement = statement.quarterly_financials
            elif di.data_type == 'splits':
                statement = statement.splits
            elif di.data_type == 'ticker':
                statement = statement.ticker

            if di.data_type == 'dividends' or di.data_type == 'splits':
                result.result_type = 'series'
            elif di.data_type == 'options' or di.data_type == 'ticker':
                result.result_type = 'strings'
            elif di.data_type == 'info':
                result.result_type = 'dictionary'
            else:
                result.result_type = 'dataframe'

            result.result_data = statement

        except KeyError:
            er = Error(KeyError, di.company, 'Hit No Data')
            e_list = ErrorList()
            e_list.add_list(er)
            result.error_list = e_list
            result.exec_continue = False

        return result

    # class Graph:
    def analysis_graph(self, di: DisplayInfo) -> Result:
        # initialize values
        result = Result()
        result.action_name = self.__str__()
        asd = object()

        # Get Income Statement from Collection
        statement = self.collection_read.collection.get(di.company + '.T')
        if self.collection_read.result.exec_continue is True:
            if di.data_type == 'financials':
                asd = AnalysisFinancials()
            if di.data_type == 'balance_sheet':
                asd = AnalysisBalanceSheet()
            if di.data_type == 'history':
                asd = AnalysisHistory()
            if di.data_type == 'cashflow':
                asd = AnalysisCashFlow()

            g = asd.get_graph_data(statement)
            result.result_data = g
            result.result_type = g.graph_type
        else:
            er = Error(KeyError, di.company, 'Hit No Statement Data')
            e_list = ErrorList()
            e_list.add_list(er)
            result.error_list = e_list

        return result


class AnalysisCrossData:
    def __init__(self, market):
        # Get Collection data
        self.collection_read = ConfigDataRead(market)

        if self.collection_read.result.exec_continue and self.collection_read.collection_list is not None:
            collection_number = str(len(self.collection_read.collection_list))
            print('Get ' + market + ' Collection Data (' + collection_number + ') Statements!')
            pass
        else:
            print('Get ' + market + ' Collection Data error!')

        print('Complete Collection Data Process!')

    def generate_ranking(self, di: DisplayInfo) -> Result:
        # initialize values
        result = Result()
        result.action_name = self.__str__()
        result.exec_continue = True

        # get collection data
        collection_list = self.collection_read.collection_list
        if di.data_type == 'balance_sheet':
            # BS Ranking
            collection = collection_list.get('balance_sheet')
            asd = AnalysisBalanceSheet()
            g = asd.get_rank_data(collection)
            # Generate Result Class
            result.result_type = g.graph_type
            result.result_data = g
        elif di.data_type == 'history':
            # Stock Ranking
            collection = collection_list.get('history')
            asd = AnalysisHistory()
            g = asd.get_rank_data(collection)
            # Generate Result Class
            result.result_type = g.graph_type
            result.result_data = g
        elif di.data_type == 'financials':
            # Stock Ranking
            collection = collection_list.get('financials')
            asd = AnalysisFinancials()
            g = asd.get_rank_data(collection)
            # Generate Result Class
            result.result_type = g.graph_type
            result.result_data = g
        else:
            er = Error(self, 'Function Error', 'Ranking for ' + di.data_type + ' does not exist!')
            e_list = ErrorList()
            e_list.add_list(er)
            result.error_list = e_list
            result.exec_continue = False

        return result


if __name__ == '__main__':
    # ai = AnalysisStatement('Extend')
    # company_code = input('Company_Code? = ')
    # ai.inquiry(company_code)
    # ai.profit_graph(company_code)
    # ai.generate_ranking()
    pass
