#

from dir_balance_sheet.analyze_bs_data import AnalysisBS
from analyze_statement_data import AnalysisStatement
from dir_stock.analyze_stock_data import AnalysisStock
from collection import CollectionWrite
from widget_helper import Result, DisplayInfo


class DataTypeDispatcher:
    def __init__(self):
        self.tickers = object
        self.result = Result()
        self.number_record = 0

    def write_data(self, di: DisplayInfo) -> Result:

        # Get Data by Market
        cw = CollectionWrite(di)
        self.result = cw.get_data()

        return self.result

    def exec_inquiry(self, di: DisplayInfo) -> Result:

        # Get inquiry data
        ast = AnalysisStatement(di.market, 'Base')
        if ast.collection_read.result.exec_continue:
            self.result = ast.inquiry(di)
        else:
            self.result = ast.collection_read.result

        return self.result

    def exec_analysis_graph(self, di: DisplayInfo) -> Result:
        # dispatch data by type
        if di.data_type == 'info':  # Company Information
            pass
        elif di.data_type == 'income':  # Income Statement
            ai = AnalysisStatement(di, 'Base')
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
            ai = AnalysisStatement(di, 'Extend')
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
