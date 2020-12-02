#
import pandas as pd

from formula import CalcRatioPer, CalcBalance
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

    @staticmethod
    def get_rank_data(collection: pd.DataFrame) -> Graph:
        # get data from collection
        total_revenue = collection.T['Total Revenue']
        operating_income = collection.T['Operating Income']
        net_income = collection.T['Net Income']


        # Calc Capital Adequacy Ratio & Current Ratio
        average_pr1 = CalcRatioPer(operating_income, total_revenue)
        average_pr2 = CalcRatioPer(net_income, total_revenue)
        average_1 = pd.Series.sort_values(average_pr1.result.result_data, ascending=False)
        average_1 = average_1.head(15)
        average_2 = pd.Series.sort_values(average_pr2.result.result_data, ascending=False)
        average_2 = average_2.head(15)

        # generate Graph Object
        g = Graph()
        g.graph_type = 'multi_bar graph'
        g.set_title('Profit Ratio Ranking Graph (Top15)')
        # bar1
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('By Operating Income')
        g.set_data(average_1)
        # bar2
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('By Net Income')
        g.set_data(average_2)

        # print(g)
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

    @staticmethod
    def get_rank_data(collection: pd.DataFrame) -> Graph:
        # get data from collection
        total_stockholder_equity = collection.T['Total Stockholder Equity']
        total_assets = collection.T['Total Assets']
        total_current_assets = collection.T['Total Current Assets']
        total_current_liabilities = collection.T['Total Current Liabilities']

        # Calc Capital Adequacy Ratio & Current Ratio
        average_pr1 = CalcRatioPer(total_stockholder_equity, total_assets)
        average_pr2 = CalcRatioPer(total_current_assets, total_current_liabilities)
        average_1 = pd.Series.sort_values(average_pr1.result.result_data, ascending=False)
        average_1 = average_1.head(15)
        average_2 = pd.Series.sort_values(average_pr2.result.result_data, ascending=False)
        average_2 = average_2.head(15)

        # generate Graph Object
        g = Graph()
        g.graph_type = 'multi_bar graph'
        g.set_title('Capital Adequacy Ratio Ranking Graph (Top10)')
        # bar1
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('Capital Adequacy Ratio')
        g.set_data(average_1)
        # bar2
        g.set_x_label('Company')
        g.set_y_label('Average %')
        g.set_data_label('Current Ratio')
        g.set_data(average_2)

        # print(g)
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

    @staticmethod
    def get_rank_data(collection: pd.DataFrame) -> Graph:
        # get data from collection
        open_price = collection.T['Open']
        close_price = collection.T['Close']
        volume = collection.T['Volume']

        # Calc Capital Adequacy Ratio & Current Ratio
        balance = CalcBalance(open_price, close_price)
        calc_data = pd.DataFrame()
        calc_data.insert(0, 'Balance', balance.result.result_data)
        calc_data.insert(1, 'Volume', volume)
        calc_data = calc_data.sort_values('Balance', ascending=False)
        calc_data = calc_data.head(15)


        # generate Graph Object
        g = Graph()
        g.graph_type = 'multi_bar graph'
        g.set_title('Price Change Average Ranking Graph (Top10)')
        # bar1
        g.set_x_label('Company')
        g.set_y_label('Currency')
        g.set_data_label('Balance')
        g.set_data(calc_data['Balance'])
        # bar2
        g.set_x_label('Company')
        g.set_y_label('unit')
        g.set_data_label('Volume')
        g.set_data(calc_data['Volume'])

        # print(g)
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
