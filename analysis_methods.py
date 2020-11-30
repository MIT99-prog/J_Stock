#
import pandas as pd

from formula import CalcRatioPer
from widget_helper import Graph


class AnalysisFinancials:
    def __init__(self):
        pass

    @staticmethod
    def get_graph_data(statement) -> Graph:
        # extract financials
        statement = statement.financials

        # Calc Profit Ratio
        cp = CalcRatioPer(statement.T['Operating Income'], statement.T['Total Revenue'])
        if cp.result.exec_continue:
            profit_ratio_1 = cp.result.result_data
        else:
            profit_ratio_1 = None

        cp = CalcRatioPer(statement.T['Net Income'], statement.T['Total Revenue'])
        if cp.result.exec_continue:
            profit_ratio_2 = cp.result.result_data
        else:
            profit_ratio_2 = None

        # generate Graph Class
        g = Graph()
        g.graph_type = 'line graph'
        g.set_title('Profit Ratio Graph')
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

        return g


class AnalysisBalanceSheet:
    def __init__(self):
        pass

    @staticmethod
    def get_graph_data(statement) -> Graph:
        statement = statement.balance_sheet

        # Calc Profit Ratio
        cp = CalcRatioPer(statement.T['Total Stockholder Equity'], statement.T['Total Assets'])  # 自己資本比率
        if cp.result.exec_continue:
            profit_ratio_1 = cp.result.result_data
        else:
            profit_ratio_1 = None

        cp = CalcRatioPer(statement.T['Total Current Assets'], statement.T['Total Current Liabilities'])  # 流動比率
        if cp.result.exec_continue:
            profit_ratio_2 = cp.result.result_data
        else:
            profit_ratio_2 = None

        # Generate Graph
        g = Graph()
        g.graph_type = 'multi_line graph'
        g.set_title('Capital Adequacy & Current Ratio Graph')
        # line 1
        g.set_x_label('Date')
        g.set_y_label('Percentage')
        g.set_data_label('Capital adequacy ratio')
        if profit_ratio_1 is not None:
            g.set_data(profit_ratio_1)
        # line 2
        g.set_x_label('Date')
        g.set_y_label('Percentage')
        g.set_data_label('Current ratio')
        if profit_ratio_2 is not None:
            g.set_data(profit_ratio_2)

        return g


class AnalysisHistory:
    def __init__(self):
        pass

    @staticmethod
    def get_graph_data(statement) -> Graph:
        # extract financials
        statement = statement.history(period='1y')
        df = pd.DataFrame()
        df.insert(0, 'Open', statement['Open'])
        df.insert(1, 'Close', statement['Close'])
        df.insert(2, 'High', statement['High'])
        df.insert(3, 'Low', statement['Low'])
        df.insert(4, 'Volume', statement['Volume'])

        # Generate Graph
        g = Graph()
        g.graph_type = 'candle graph'
        g.set_title('Candle Graph')
        # line 1
        g.set_x_label('Date')
        g.set_y_label('Price')
        g.set_data_label('')
        if statement is not None:
            g.set_data(df)

        return g

class AnalysisCashFlow:
    def __init__(self):
        pass

    @staticmethod
    def get_graph_data(statement) -> Graph:
        # extract financials
        statement = statement.cashflow
        df = pd.DataFrame()
        df_var = statement.T['Total Cash From Operating Activities']
        df.insert(loc=0, column='Total Cash From Operating Activities', value=df_var)
        # Operating Collection
        df_var = statement.T['Total Cash From Financing Activities']
        df.insert(loc=1, column='Total Cash From Financing Activities', value=df_var)
        # Net Collection
        df_var = statement.T['Total Cashflows From Investing Activities']
        df.insert(loc=2, column='Total Cashflows From Investing Activities', value=df_var)

        # Generate Graph
        g = Graph()
        # g.graph_type = 'stacked_bar graph'
        g.graph_type = 'line graph'
        g.set_title('Line Graph')
        # line 1
        g.set_x_label('Date')
        g.set_y_label('Amount')
        g.set_data_label('Total Cash From Operating Activities')
        if statement is not None:
            g.set_data(df['Total Cash From Operating Activities'])
        # line 2
        g.set_x_label('Date')
        g.set_y_label('Amount')
        g.set_data_label('Total Cash From Financing Activities')
        if statement is not None:
            g.set_data(df['Total Cash From Financing Activities'])
        # line 3
        g.set_x_label('Date')
        g.set_y_label('Amount')
        g.set_data_label('Total Cashflows From Investing Activities')
        if statement is not None:
            g.set_data(df['Total Cashflows From Investing Activities'])

        return g