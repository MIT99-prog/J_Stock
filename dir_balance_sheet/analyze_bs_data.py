#
import matplotlib.pyplot as plt
import pandas as pd

from dir_balance_sheet.balance_sheet import BSesRead
from errorhandler import Error, ErrorList
from widget_helper import Result, Graph, DisplayInfo


class AnalysisBS:
    def __init__(self, di: DisplayInfo, read_type: str):
        self.result = Result()
        self.di = di
        # Get Balance Sheet data
        self.bs_collection = BSesRead(di, read_type)
        if self.bs_collection.result.exec_continue:
            print('Balance Sheet Data (' + str(self.bs_collection.result.result_data) + ') set completed!')
            # Prepare Result Class
            self.result = Result()
        else:
            pass

    # class Inquiry:
    def inquiry(self) -> Result:
        self.result.action_name = 'Inquiry Balance Sheet'
        self.result.result_type = 'dataframe'
        self.result.result_data = self.bs_collection.bses.get(self.di.company + '.T')
        if self.result.exec_continue is False:
            er = Error(ValueError, self.di.company, 'Hit No Data')
            e_list = ErrorList().add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False
        # result.to_excel('./test.xlsx')
        return self.result

    # class Graph:
    def analysis_graph(self, di):
        bs = self.bs_collection.bses.get(di.company + '.T')

        # Calc Profit Ratio
        ratio_1 = bs.T['Total Stockholder Equity'] / bs.T['Total Assets'] * 100  # 自己資本比率
        ratio_2 = bs.T['Total Current Assets'] / bs.T['Total Current Liabilities'] * 100  # 流動比率

        print("Ratio 1")
        print(ratio_1)
        print('Ratio 2')
        print(ratio_2)

        # Generate Graph
        x = ratio_1.index
        y_1 = ratio_1.values
        y_2 = ratio_2.values

        fig, ax = plt.subplots()
        ax.set_title('Ratio Graph')
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage')
        ax.plot(x, y_1, label='Capital adequacy ratio')
        ax.plot(x, y_2, label='Current ratio')
        ax.legend()
        plt.show()

    def generate_ranking(self):
        ratios_1 = self.bs_collection.total_stockholder_equity / \
                   self.bs_collection.total_assets * 100  # 自己資本比率
        ratios_2 = self.bs_collection.total_current_assets / \
                   self.bs_collection.total_current_liabilities  # 流動比率

        average_pr1 = ratios_1.mean(numeric_only=True)
        average_pr2 = ratios_2.mean(numeric_only=True)
        average_pr = pd.DataFrame()
        average_pr.insert(0, 'Capital adequacy ratio', average_pr1)
        average_pr.insert(1, 'Current Ratio', average_pr2)
        average_pr = average_pr.sort_values('Capital adequacy ratio', ascending=False)
        average_pr = average_pr.head(10)

        print(average_pr)

        # generate Graph Object
        g = Graph()
        g.set_title('Capital Adequacy Ratio Ranking Graph (Top10)')
        # bar1
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('Capital adequacy ratio')
        g.set_data(average_pr['Capital adequacy ratio'])
        # bar2
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('Current Ratio (1/100)')
        g.set_data(average_pr['Current Ratio'])

        # Generate Result Class
        self.result.action_name = 'generate Capital Adequacy Ratio ranking'
        self.result.result_type = 'bar graph'
        self.result.result_data = g
        self.result.exec_continue = True
        return self.result
