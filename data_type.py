#
import yfinance as yf

from dir_balance_sheet.analyze_bs_data import AnalysisBS
from dir_income_statement.analyze_income_data import AnalysisIncome
from dir_information.analyze_info_data import Analysis_Info
from dir_stock.analyze_stock_data import AnalysisStock
from dir_balance_sheet.balance_sheet import BSesWrite
from dir_cash_flow.analyze_cash_flow_data import AnalysisCashFlow
from dir_cash_flow.cash_flow import StatementsWrite
from dir_income_statement.income_statement import IncomesWrite
from dir_information.information import InfosWrite
from dir_stock.stock import StockWrite
from widget_helper import Result, DisplayInfo


class DataTypeDispatcher:
    def __init__(self):
        self.tickers = object
        self.result = Result()
        self.number_record = 0

    def write_data(self, di: DisplayInfo) -> Result:
        # create Tickers
        companies_t = [str(s) + ".T" for s in di.companies]
        # get tickers from yahoo finance
        self.tickers = yf.Tickers(" ".join(companies_t))

        # dispatch data by type
        if di.data_type == 'info':  # Company Information
            ifw = InfosWrite(di)
            self.result = ifw.get_data(self.tickers)

        elif di.data_type == 'income':  # Income Statement
            iw = IncomesWrite(di)
            self.result = iw.get_data(self.tickers)

        elif di.data_type == 'balance':  # Balance Sheet
            bs = BSesWrite(di)
            self.result = bs.get_data(self.tickers)

        elif di.data_type == 'cash':  # Cash Flow
            cf = StatementsWrite(di)
            self.result = cf.get_data(self.tickers)
        elif di.data_type == 'stock':  # Stock
            stw = StockWrite(di)
            self.result = stw.get_data(self.tickers)

        return self.result

    def exec_inquiry(self, di: DisplayInfo) -> Result:

        # dispatch data by type
        if di.data_type == 'info':  # Company Information
            aif = Analysis_Info(di, 'Base')
            if aif.info_collection.result.exec_continue:
                self.result = aif.inquiry()
            else:
                self.result = aif.info_collection.result

        elif di.data_type == 'income':  # Income Statement
            ai = AnalysisIncome(di, 'Base')
            if ai.income_collection.result.exec_continue:
                self.result = ai.inquiry()
            else:
                self.result = ai.income_collection.result

        elif di.data_type == 'balance':  # Balance Sheet
            ab = AnalysisBS(di, 'Base')  # Read BS Data (Base / Extend)
            if ab.bs_collection.result.exec_continue:
                self.result = ab.inquiry()
            else:
                self.result = ab.bs_collection.result

        elif di.data_type == 'cash':  # Cash Flow
            stm = AnalysisCashFlow(di, 'Base')
            if stm.stm_collection.result.exec_continue:
                self.result = stm.inquiry()
            else:
                self.result = stm.stm_collection.result

        elif di.data_type == 'stock':  # Stock
            ast = AnalysisStock(di, 'Base')
            if ast.stock_collection.result.exec_continue:
                self.result = ast.inquiry()
            else:
                self.result = ast.stock_collection.result

        return self.result

    def exec_analysis_graph(self, di: DisplayInfo) -> Result:
        # dispatch data by type
        if di.data_type == 'info':  # Company Information
            pass
        elif di.data_type == 'income':  # Income Statement
            ai = AnalysisIncome(di, 'Base')
            self.result = ai.analysis_graph()

        elif di.data_type == 'balance':  # Balance Sheet
            pass

        elif di.data_type == 'cash':  # Cash Flow
            pass
        elif di.data_type == 'stock':  # Stock
            pass

        return self.result

    def exec_ranking(self, di: DisplayInfo) -> Result:

        # dispatch data by type
        if di.data_type == 'info':  # Company Information
            pass
        elif di.data_type == 'income':  # Income Statement
            ai = AnalysisIncome(di, 'Extend')
            self.result = ai.generate_ranking()

        elif di.data_type == 'balance':  # Balance Sheet
            ab = AnalysisBS(di, 'Extend')
            self.result = ab.generate_ranking()

        elif di.data_type == 'cash':  # Cash Flow
            pass
        elif di.data_type == 'stock':  # Stock
            ast = AnalysisStock(di, 'Extend')
            self.result = ast.generate_ranking()

        return self.result
