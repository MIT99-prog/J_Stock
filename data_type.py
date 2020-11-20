#
import pandas as pd
import yfinance as yf

from analyze_bs_data import Analysis_BS
from analyze_income_data import Analysis_Income
from analyze_info_data import Analysis_Info
from analyze_stock_data import Analysis_Stock
from balance_sheet import BSes_Write
from income_statement import Incomes_Write
from infomation import Infos_Write
from stocks import Stocks_Write


class DataTypeDispatcher:
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
            ifw = Infos_Write()
            number_record = ifw.get_data(self.tickers)
            return number_record
        elif data_type == 'income':  # Income Statement
            iw = Incomes_Write()
            number_record = iw.get_data(self.tickers)
            return number_record
        elif data_type == 'balance':  # Balance Sheet
            bs = BSes_Write()
            number_record = bs.get_data(self.tickers)
            return number_record
        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            stw = Stocks_Write()
            number_record = stw.get_data(self.tickers)
            return number_record
    '''
    def read_data(self, data_type) -> int:
        # dispatch data by type
        if data_type == 'info':  # Company Information
            ifo = Infos_Read()
            self.number_record = ifo.data_read()
        elif data_type == 'income':  # Income Statement
            ir = Incomes_Read()  # initialize Income_Read class
            self.number_record = ir.data_read()  # set Income Statements Data
            return self.number_record
        elif data_type == 'balance':  # Balance Sheet
            bs = BSes_Read()
            self.number_record = bs.data_read()
            return self.number_record
        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            sr = Stocks_Read()
            self.number_record = sr.data_read()
            return self.number_record
    '''
    @staticmethod
    def exec_inquiry(data_type, company) -> pd.DataFrame:

        # dispatch data by type
        if data_type == 'info':  # Company Information
            aif = Analysis_Info('Base')
            result = aif.inquiry(company)
            return result
        elif data_type == 'income':  # Income Statement
            ai = Analysis_Income('Base')
            result = ai.inquiry(company)
            return result

        elif data_type == 'balance':  # Balance Sheet
            ab = Analysis_BS('Base')  # Base / Extend
            result = ab.inquiry(company)
            return result

        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            ast = Analysis_Stock('Base')
            result = ast.inquiry(company)
            return result

    @staticmethod
    def exec_analysis_graph(company):
        ai = Analysis_Income('Base')
        ai.profit_graph(company)

    @staticmethod
    def exec_ranking(data_type):

        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            ai = Analysis_Income('Extend')
            ai.Ranking()

        elif data_type == 'balance':  # Balance Sheet
            pass
        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            ast = Analysis_Stock('Extend')
            ast.generate_ranking()
