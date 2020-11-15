#
import pandas as pd
import numpy as np
from element import Income_Element
from income_statement import Incomes_Read
from serialize import Data
import matplotlib.pyplot as plt


class Analysis_Income:
    def __init__(self):
        self.income_collection = []
        self.total_revenue = pd.DataFrame()
        self.operating_income = pd.DataFrame()
        self.net_income = pd.DataFrame()
        self.data = Data()

        # Get Income data
        self.income_collection = Incomes_Read()

        print('Data set completed!')

    # class Inquiry:
    def inquiry(self, company_code):
        pd.set_option('display.max_columns', None)
        print(self.income_collection.ie_dict.get(company_code))

    # class Graph:
    def profit_graph(self, company_code):
        company_element = Income_Element(company_code, self.income_collection.ie_dict.get(company_code))

        profit_ratio_1 = company_element.get_operating_income() / company_element.get_total_revenue() * 100
        profit_ratio_2 = company_element.get_net_income() / company_element.get_total_revenue() * 100

        # profit_ratio_1 = profit_ratio_1.sort_index()

        print("Ratio 1")
        print(profit_ratio_1)
        print('Ratio 2')
        print(profit_ratio_2)

        x = profit_ratio_1.index
        y_1 = profit_ratio_1.values
        y_2 = profit_ratio_2.values

        fig, ax = plt.subplots()
        ax.set_title('Profit Ratio Graph')
        ax.set_xlabel('Date')
        ax.set_ylabel('Percentage')
        ax.plot(x, y_1, label='Calc by Operating Income')
        ax.plot(x, y_2, label='Calc by Net Income')
        ax.legend()
        plt.show()

    def Ranking(self):
        profit_ratios_1 = self.income_collection.operating_incomes / self.income_collection.total_revenues * 100
        profit_ratios_2 = self.income_collection.net_incomes / self.income_collection.total_revenues * 100
        average_pr1 = profit_ratios_1.mean(numeric_only=True)
        average_pr2 = profit_ratios_2.mean(numeric_only=True)
        average_pr = pd.DataFrame()
        average_pr.insert(0, 'By Operating Income', average_pr1)
        average_pr.insert(1, 'By Net Income', average_pr2)
        average_pr = average_pr.sort_values('By Operating Income', ascending=False)
        average_pr = average_pr.head(10)

        print('Average Profit Ratio')
        print(average_pr)

        x_1 = average_pr.index

        y_1 = average_pr['By Operating Income'].values
        y_2 = average_pr['By Net Income'].values
        x = np.arange(len(x_1))
        width = 0.35

        fig, ax = plt.subplots()
        ax.set_title('Profit Ratio Ranking Graph (Top10)')
        ax.set_xlabel('Company')
        ax.set_ylabel('Average %')
        ax.set_xticks(x)
        ax.set_xticklabels(x_1)
        ax.bar(x - width / 2, y_1, label='Calc by Operating Income')
        ax.bar(x + width / 2, y_2, label='Calc by Net Income')
        ax.legend()
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    ai = Analysis_Income()
    # company_code = input('Company_Code? = ')
    # ai.inquiry(company_code)
    # ai.profit_graph(company_code)
    ai.Ranking()
