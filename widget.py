# This Python file uses the following encoding: utf-8
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QHeaderView, QTableWidget
from PyQt5 import QtCore

from analyze_income_data import Analysis_Income
from data_type import Data_Type_Dispatcher


class Financial_Analysis(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # Set initial data for these QComboBoxes of the widget
        # Start Date and End Date for Get Data
        # end_date = dt.today()
        # differ = delta(days=365)
        # start_date = end_date - differ
        self.dtd = Data_Type_Dispatcher()
        self.data_type = ''
        # market and company
        market_items = ['JASDAQ']
        company_items = ['1381.T']

        # Load form file(.ui)
        uic.loadUi('fa.ui', self)

        # Set items to these QComboBoxes
        for i in range(len(market_items)):
            self.market.addItem(market_items[i])

        for i in range(len(company_items)):
            self.company.addItem(company_items[i])

        # construct DataInfo, Stock Classes
        # self.wdi = DataInfo()
        # self.st = Stock(self.wdi)

        self.getData.clicked.connect(self.on_getdata)
        self.inquiry.clicked.connect(self.on_inquiry)
        self.rank.clicked.connect(self.on_rank)

    def on_getdata(self):
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

        number_record = self.dtd.write_data(self.data_type)

        self.message.setText(self.data_type + "データが " + str(number_record) + "件　取得できました！")

        print("GetData process is completed!")

    def on_inquiry(self):
        # Market

        # Data_type ( Read data for inquiry)

        # Company
        company_code = self.company.currentText()

        # Inquiry
        result = self.dtd.exec_inquiry(self.check_data_type(), company_code)
        # Display Income Statement
        ddf = Disp_DataFrame()
        ddf.show_dataframe(result)

        print("Inquiry Button was clicked!")

    def on_rank(self):
        # Data_type
        # number_record = self.dtd.read_data(self.check_data_type())
        # print('Read ' + str(number_record) + ' Records')
        self.dtd.exec_ranking(self.check_data_type())

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


class Disp_DataFrame(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.sub_widget = uic.loadUi('table.ui', self)

    def show_dataframe(self, df):
        sub_widget = Disp_DataFrame()
        sub_widget.tableWidget.setRowCount(df.shape[0])
        sub_widget.tableWidget.setColumnCount(df.shape[1])
        # Set Data from DataFrame
        # Set Headers
        vheader = QHeaderView(QtCore.Qt.Vertical)
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        sub_widget.tableWidget.setVerticalHeader(vheader)
        sub_widget.tableWidget.setVerticalHeaderLabels(df.index.values)
        hheader = QHeaderView(QtCore.Qt.Horizontal)
        hheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        sub_widget.tableWidget.setHorizontalHeader(hheader)
        xlabel = []
        for i in range(df.columns.__len__()):
            xlabel.append(str(df.columns.values[i]))
        sub_widget.tableWidget.setHorizontalHeaderLabels(xlabel)

        # Set Data
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.values[i][j]))
                sub_widget.tableWidget.setItem(i, j, item)
        sub_widget.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Display Widget
    widget = Financial_Analysis()
    widget.show()

    # print("Process was finished without exception!")
    sys.exit(app.exec_())
