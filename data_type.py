#
import pandas as pd
import yfinance as yf

from analyze_income_data import Analysis_Income
from analyze_stock_data import Analysis_Stock
from income_statement import Incomes_Write, Incomes_Read
from stocks import Stocks_Write, Stocks_Read


class Data_Type_Dispatcher:
    def __init__(self):
        self.tickers = object
        self.number_record = 0

    def write_data(self, companies, data_type) -> int:
        # create Tickers
        companies_t = [str(s) + ".T" for s in companies]
        # get tickers from yahoo finance
        self.tickers = yf.Tickers(" ".join(companies_t))
        print(" *** tickers *** ")
        print(self.tickers)

        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            iw = Incomes_Write()
            number_record = iw.get_incomes(self.tickers)
            return number_record
        elif data_type == 'Balance':  # Balance Sheet
            pass
        elif data_type == 'Cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            stw = Stocks_Write()
            number_record = stw.get_stocks(self.tickers)
            return number_record

    def read_data(self, data_type) -> int:
        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            ir = Incomes_Read()  # initialize Income_Read class
            self.number_record = ir.data_read()  # set Income Statements Data
            return self.number_record
        elif data_type == 'Balance':  # Balance Sheet
            pass
        elif data_type == 'Cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            sr = Stocks_Read()
            self.number_record = sr.data_read()
            return self.number_record

    @staticmethod
    def exec_inquiry(data_type, company) -> pd.DataFrame:
        # Set data for inquiry
        # number_record = self.read_data(data_type)
        # print('Read ' + str(number_record) + ' Records')

        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            ai = Analysis_Income()
            result = ai.inquiry(company)
            # ai.profit_graph(company)
            return result

        elif data_type == 'Balance':  # Balance Sheet
            pass
        elif data_type == 'Cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            ast = Analysis_Stock()
            result = ast.inquiry(company)
            return result

    def exec_analysis_graph(self, company):
        ai = Analysis_Income()
        ai.profit_graph(company)

    @staticmethod
    def exec_ranking(data_type):
        # Set data for inquiry
        # number_record = self.read_data(data_type)
        # print('Read ' + str(number_record) + ' Records')

        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            ai = Analysis_Income()
            ai.Ranking()

        elif data_type == 'Balance':  # Balance Sheet
            pass
        elif data_type == 'Cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            ast = Analysis_Stock()
            ast.generate_ranking()
