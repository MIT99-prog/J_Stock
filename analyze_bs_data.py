#
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from balance_sheet import BSes_Read


class Analysis_BS:
    def __init__(self, read_type):
        self.bs_collection = []

        # Get Income data
        self.bs_collection = BSes_Read(read_type)

        print('Data set completed!')

    # class Inquiry:
    def inquiry(self, company_code):
        result = self.bs_collection.bses.get(company_code + '.T')
        # result.to_excel('./test.xlsx')
        return result

    # class Graph:
    def ratio_graph(self, company_code):

        bs = self.bs_collection.bses.get(company_code + '.T')

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

    def Ranking(self):
        ratios_1 = self.bs_collection.total_stockholder_equity / \
                          self.bs_collection.total_assets * 100  # 自己資本比率
        ratios_2 = self.bs_collection.total_current_assets / \
                          self.bs_collection.total_current_liabilities * 100  # 流動比率

        average_pr1 = ratios_1.mean(numeric_only=True)
        average_pr2 = ratios_2.mean(numeric_only=True)
        average_pr = pd.DataFrame()
        average_pr.insert(0, 'Capital adequacy ratio', average_pr1)
        average_pr.insert(1, 'Current Ratio', average_pr2)
        average_pr = average_pr.sort_values('Capital adequacy ratio', ascending=False)
        average_pr = average_pr.head(10)

        print('Capital adequacy ratio & Current ratio')
        print(average_pr)

        x_1 = average_pr.index

        y_1 = average_pr['Capital adequacy ratio'].values
        y_2 = average_pr['Current ratio'].values
        x = np.arange(len(x_1))
        width = 0.35

        fig, ax = plt.subplots()
        ax.set_title('Capital adequacy ratio Ranking Graph (Top10)')
        ax.set_xlabel('Company')
        ax.set_ylabel('Average %')
        ax.set_xticks(x)
        ax.set_xticklabels(x_1)
        ax.bar(x + width / 2, y_1, label='Capital adequacy ratio')
        ax.bar(x - width / 2, y_2, label='Current ratio')
        ax.legend()
        plt.tight_layout()
        plt.show()