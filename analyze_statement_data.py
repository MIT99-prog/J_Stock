#
import pandas as pd

from collection import CollectionRead
from errorhandler import Error, ErrorList
from formula import CalcProfitRatio, CalcProfitMean
from widget_helper import Result, Graph, DisplayInfo


class AnalysisStatement:
    def __init__(self, market: str, read_type: str):

        # Get Collection data
        self.collection_read = CollectionRead(market, read_type)

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
                statement = statement.history()
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
            e_list = ErrorList().add_list(er)
            result.error_list = e_list
            result.exec_continue = False

        return result

    # class Graph:
    def analysis_graph(self, di) -> Result:
        # initialize values
        result = Result()
        result.action_name = self.__str__()
        result.result_type = 'line graph'

        # Get Income Statement from Collection
        statement = self.collection_read.collection.get(di.company + '.T')
        if self.collection_read.result.exec_continue is True:

            # Calc Profit Ratio
            cp = CalcProfitRatio(statement.T['Operating Income'], statement.T['Total Revenue'])
            if cp.result.exec_continue:
                profit_ratio_1 = cp.result.result_data
            else:
                profit_ratio_1 = None

            cp = CalcProfitRatio(statement.T['Net Income'], statement.T['Total Revenue'])
            if cp.result.exec_continue:
                profit_ratio_2 = cp.result.result_data
            else:
                profit_ratio_2 = None

            # generate Graph Class
            g = Graph()
            g.set_title('Profit Rate Graph')
            # line 1
            g.set_x_label('Date')
            g.set_y_label('Profit Rate')
            g.set_data_label('Operating Income')
            if profit_ratio_1 is not None:
                g.set_data(profit_ratio_1)
            # line 2
            g.set_x_label('Date')
            g.set_y_label('Profit Rate')
            g.set_data_label('Net Income')
            if profit_ratio_2 is not None:
                g.set_data(profit_ratio_2)

            result.result_data = g
        else:
            er = Error(ValueError, self.di.company, 'Hit No Statement Data')
            e_list = ErrorList().add_list(er)
            result.error_list = e_list

        return result

    def generate_ranking(self) -> Result:
        result = Result()
        result.action_name = self.__str__()
        result.result_type = 'line graph'
        # Calc Profit Ratio
        '''
        profit_ratios_1 = self.collection.operating_incomes / \
                          self.collection.total_revenues * 100  # Operating Income
        profit_ratios_2 = self.collection.net_incomes / \
                          self.collection.total_revenues * 100  # Net Income

        average_pr1 = profit_ratios_1.mean(numeric_only=True)
        average_pr2 = profit_ratios_2.mean(numeric_only=True)
        '''
        average_pr1 = CalcProfitMean(self.collection_read.collection.operating_incomes,
                                     self.collection_read.collection.total_revenues)
        average_pr2 = CalcProfitMean(self.collection_read.collection.net_incomes,
                                     self.collection_read.collection.total_revenues)
        average_pr = pd.DataFrame()
        average_pr.insert(0, 'By Net Income', average_pr2)
        average_pr.insert(1, 'By Operating Income', average_pr1)
        average_pr = average_pr.sort_values('By Net Income', ascending=False)
        average_pr = average_pr.head(10)

        # generate Graph Object
        g = Graph()
        g.set_title('Profit Ratio Ranking Graph (Top10)')
        # bar1
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('Calc by Net Income')
        g.set_data(average_pr['By Net Income'])
        # bar2
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('Calc by Operating Income')
        g.set_data(average_pr['By Operating Income'])

        # Generate Result Class
        self.result.action_name = 'generate Profitability ranking'
        self.result.result_type = 'bar graph'
        self.result.result_data = g
        self.result.exec_continue = True
        return self.result


if __name__ == '__main__':
    # ai = AnalysisStatement('Extend')
    # company_code = input('Company_Code? = ')
    # ai.inquiry(company_code)
    # ai.profit_graph(company_code)
    # ai.generate_ranking()
    pass
