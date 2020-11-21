#
import yfinance as yf

from analyze_bs_data import AnalysisBS
from analyze_income_data import AnalysisIncome
from analyze_info_data import Analysis_Info
from analyze_stock_data import AnalysisStock
from balance_sheet import BSesWrite
from income_statement import IncomesWrite
from information import InfosWrite
from stocks import Stocks_Write
from widget_helper import Result


class DataTypeDispatcher:
    def __init__(self):
        self.tickers = object
        self.result = Result()
        self.number_record = 0

    def write_data(self, companies, data_type) -> Result:
        # create Tickers
        companies_t = [str(s) + ".T" for s in companies]
        # get tickers from yahoo finance
        self.tickers = yf.Tickers(" ".join(companies_t))
        # print(" *** tickers *** ")
        # print(self.tickers)

        # dispatch data by type
        if data_type == 'info':  # Company Information
            ifw = InfosWrite()
            self.result = ifw.get_data(self.tickers)

        elif data_type == 'income':  # Income Statement
            iw = IncomesWrite()
            self.result = iw.get_data(self.tickers)

        elif data_type == 'balance':  # Balance Sheet
            bs = BSesWrite()
            self.result = bs.get_data(self.tickers)

        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            stw = Stocks_Write()
            self.result = stw.get_data(self.tickers)

        return self.result

    def exec_inquiry(self, data_type, company) -> Result:

        # dispatch data by type
        if data_type == 'info':  # Company Information
            aif = Analysis_Info('Base')
            if aif.info_collection.result.exec_continue:
                self.result = aif.inquiry(company)
            else:
                self.result = aif.info_collection.result

        elif data_type == 'income':  # Income Statement
            ai = AnalysisIncome('Base')
            if ai.income_collection.result.exec_continue:
                self.result = ai.inquiry(company)
            else:
                self.result = ai.income_collection.result

        elif data_type == 'balance':  # Balance Sheet
            ab = AnalysisBS('Base')  # Read BS Data (Base / Extend)
            if ab.bs_collection.result.exec_continue:
                self.result = ab.inquiry(company)
            else:
                self.result = ab.bs_collection.result

        elif data_type == 'cash':  # Cash Flow
            pass

        elif data_type == 'stock':  # Stock
            ast = AnalysisStock('Base')
            if ast.stock_collection.result.exec_continue:
                self.result = ast.inquiry(company)
            else:
                self.result = ast.stock_collection.result

        return self.result

    def exec_analysis_graph(self, data_type, company):
        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            ai = AnalysisIncome('Base')
            self.result = ai.profit_graph(company)

        elif data_type == 'balance':  # Balance Sheet
            pass

        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            pass

        return self.result

    def exec_ranking(self, data_type):

        # dispatch data by type
        if data_type == 'info':  # Company Information
            pass
        elif data_type == 'income':  # Income Statement
            ai = AnalysisIncome('Extend')
            self.result = ai.generate_ranking()

        elif data_type == 'balance':  # Balance Sheet
            ab = AnalysisBS('Extend')
            self.result = ab.generate_ranking()

        elif data_type == 'cash':  # Cash Flow
            pass
        elif data_type == 'stock':  # Stock
            ast = AnalysisStock('Extend')
            self.result = ast.generate_ranking()

        return self.result
