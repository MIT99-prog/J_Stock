# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

from data_type import DataTypeDispatcher
from error_handler import Error_Handler, Error
from market import Tosho1, Tosho2, Mothers, Jasdaq
from widget_helper import DispDataFrame, Result, WidgetHelper


class FinancialAnalysis(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Set initial data for the widget
        # Data Type (Information / Income Statement / Balance Sheet / Cash Flow / Stock)
        self.dtd = DataTypeDispatcher()
        self.data_type = ''

        # market and company
        self.market_items = ['市場第一部', '市場第二部', 'マザーズ', 'JASDAQ']
        self.companies = []

        # Load form file(.ui)
        uic.loadUi('fa.ui', self)

        # Set items to these QComboBoxes
        for i in range(len(self.market_items)):
            self.market.addItem(self.market_items[i])

        # sign connect to slot
        self.getData.clicked.connect(self.on_get_data)
        self.inquiry.clicked.connect(self.on_inquiry)
        self.rank.clicked.connect(self.on_rank)
        self.market.activated.connect(self.create_companies)
        self.analysisGraph.clicked.connect(self.on_analysis_graph)

        # Prepare Result Class
        self.result = Result()

    # Slots
    def on_get_data(self):
        # Get info from screen widget
        # Market
        # if self.market.currentText() == 'JASDAQ':
        #    jasdaq = Jasdaq()

        # Data_type

        if self.info.isChecked():  # Company Information
            self.data_type = 'info'

        elif self.pl.isChecked():  # Income Statement
            self.data_type = 'income'

        elif self.bs.isChecked():  # Balance Sheet
            self.data_type = 'balance'

        elif self.cf.isChecked():  # Cash Flow
            self.data_type = 'cash'

        elif self.stock.isChecked():  # Stock
            self.data_type = 'stock'

        self.result = self.dtd.write_data(self.companies, self.data_type)

        self.message.setText(self.data_type + "データが " + str(self.result.result_data) + "件　取得できました！")

        print("GetData process is completed!")

    def on_inquiry(self):
        # Market
        # Need a program in widget_helper
        # Data_type ( Read data for inquiry)
        data_type = self.check_data_type()
        # Company
        company = self.company.currentText()

        # Inquiry
        self.result = self.dtd.exec_inquiry(data_type, company)
        # Check the value of result
        wh = WidgetHelper()
        wh.parse_result(self.result)

        print("Inquiry Button was clicked!")

    def on_analysis_graph(self):
        # Company
        company = self.company.currentText()
        self.result = self.dtd.exec_analysis_graph(self.check_data_type(), company)
        wh = WidgetHelper()
        wh.parse_result(self.result)


    def on_rank(self):
        # Data_type
        # number_record = self.dtd.read_data(self.check_data_type())
        # print('Read ' + str(number_record) + ' Records')
        self.result = self.dtd.exec_ranking(self.check_data_type())
        wh = WidgetHelper()
        wh.parse_result(self.result)


    # -----------
    def create_companies(self):  # Create Company List by Market
        # initialize mk market object
        mk = object
        # set market object
        if self.market.currentText() == '市場第一部':
            mk = Tosho1()

        elif self.market.currentText() == '市場第二部':
            mk = Tosho2()

        elif self.market.currentText() == 'マザーズ':
            mk = Mothers()

        elif self.market.currentText() == 'JASDAQ':
            mk = Jasdaq()

        # set companies by market
        self.companies = mk.companies
        self.company.clear()
        for i in range(len(self.companies)):
            self.company.addItem(str(self.companies[i]))

    def check_data_type(self) -> str:
        # Data_type
        self.data_type = ''
        if self.info.isChecked():  # Company Information
            self.data_type = 'info'
            return self.data_type

        elif self.pl.isChecked():  # Income Statement
            self.data_type = 'income'
            return self.data_type

        elif self.bs.isChecked():  # Balance Sheet
            self.data_type = 'balance'
            return self.data_type

        elif self.cf.isChecked():  # Cash Flow
            self.data_type = 'cash'
            return self.data_type

        elif self.stock.isChecked():  # Stock
            self.data_type = 'stock'
            return self.data_type


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Display Widget
    widget = FinancialAnalysis()
    widget.show()

    # print("Process was finished without exception!")
    sys.exit(app.exec_())
