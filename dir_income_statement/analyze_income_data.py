#
import pandas as pd

from errorhandler import Error, ErrorList
from dir_income_statement.income_statement import IncomesRead
from serialize import Data
from widget_helper import Result, Graph, DisplayInfo


class AnalysisIncome:
    def __init__(self, di: DisplayInfo, read_type: str):
        self.income_collection = []
        self.di = di
        self.data = Data()

        # Get Income data
        self.income_collection = IncomesRead(di, read_type)
        if self.income_collection.result.exec_continue:
            print('Income Statement Data (' + str(self.income_collection.result.result_data) + ') set completed!')
            # Prepare Result Class
            self.result = Result()
        else:
            pass
        print('Income Statement Data set completed!')

    # class Inquiry:
    def inquiry(self):
        self.result.action_name = 'Inquiry Income Statement'
        self.result.result_type = 'dataframe'
        self.result.result_data = self.income_collection.incomes.get(self.di.company + '.T')
        if self.result.exec_continue is False:
            er = Error(ValueError, self.di.company, 'Hit No Data')
            e_list = ErrorList().add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False
        # result.to_excel('./test.xlsx')
        return self.result

    # class Graph:
    def analysis_graph(self):

        self.result.action_name = 'profit_graph of Income Statement'
        self.result.result_type = 'line graph'
        income = self.income_collection.incomes.get(self.di.company + '.T')
        if self.result.exec_continue is False:
            er = Error(ValueError, self.di.company, 'Hit No Data')
            e_list = ErrorList().add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False

        # Calc Profit Ratio
        profit_ratio_1 = income.T['Operating Income'] / income.T['Total Revenue'] * 100
        profit_ratio_2 = income.T['Net Income'] / income.T['Total Revenue'] * 100

        # generate Graph Class
        g = Graph()
        g.set_title('Profit Rate Graph')
        # line 1
        g.set_x_label('Date')
        g.set_y_label('Profit Rate')
        g.set_data_label('Operating Income')
        g.set_data(profit_ratio_1)
        # line 2
        g.set_x_label('Date')
        g.set_y_label('Profit Rate')
        g.set_data_label('Net Income')
        g.set_data(profit_ratio_2)

        self.result.result_data = g
        return self.result

    def generate_ranking(self) -> Result:
        profit_ratios_1 = self.income_collection.operating_incomes / \
                          self.income_collection.total_revenues * 100  # Operating Income
        profit_ratios_2 = self.income_collection.net_incomes / \
                          self.income_collection.total_revenues * 100  # Net Income

        average_pr1 = profit_ratios_1.mean(numeric_only=True)
        average_pr2 = profit_ratios_2.mean(numeric_only=True)
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
    # ai = AnalysisIncome('Extend')
    # company_code = input('Company_Code? = ')
    # ai.inquiry(company_code)
    # ai.profit_graph(company_code)
    # ai.generate_ranking()
    pass
