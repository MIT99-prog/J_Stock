#
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QHeaderView
from PyQt5 import uic
from PyQt5 import QtCore
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from error_handler import Error_Handler


class Result:
    def __init__(self):
        self.action_name = ''
        self.result_type = ''  # 'number' / 'dataframe' / 'graph'
        self.result_data = object  # data object
        self.error_list = object  # 'Errorlist' object
        self.exec_continue = True  # Bool value


class DispDataFrame(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.sub_widget = uic.loadUi('table.ui', self)

    def show_dataframe(self, df: pd.DataFrame):
        # sub_widget = Disp_DataFrame()
        self.sub_widget.tableWidget.setRowCount(df.shape[0])
        self.sub_widget.tableWidget.setColumnCount(df.shape[1])
        # Set Data from DataFrame
        # Set Headers
        vheader = QHeaderView(QtCore.Qt.Vertical)
        vheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.sub_widget.tableWidget.setVerticalHeader(vheader)
        # parse y_label to String
        ylabel = []
        for i in range(df.index.__len__()):
            ylabel.append(str(df.index.values[i]))
        self.sub_widget.tableWidget.setVerticalHeaderLabels(ylabel)
        hheader = QHeaderView(QtCore.Qt.Horizontal)
        hheader.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.sub_widget.tableWidget.setHorizontalHeader(hheader)
        # parse x_label to String
        xlabel = []
        for i in range(df.columns.__len__()):
            xlabel.append(str(df.columns.values[i]))
        self.sub_widget.tableWidget.setHorizontalHeaderLabels(xlabel)

        # Set Data
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.values[i][j]))
                self.sub_widget.tableWidget.setItem(i, j, item)
        self.sub_widget.show()


class Graph:
    def __init__(self):
        self.title = ''
        self.x_label = []
        self.y_label = []
        self.data = []
        self.data_label = []

    def set_title(self, title: str):
        self.title = title

    def set_x_label(self, x_label: str):
        self.x_label.append(x_label)

    def set_y_label(self, y_label: str):
        self.y_label.append(y_label)

    def set_data(self, data):
        self.data.append(data)

    def set_data_label(self, data_label: str):
        self.data_label.append(data_label)


class GenerateGraph:
    def __init__(self):
        pass

    def line_graph(self, graph_object: Graph):
        # initialize values
        x = []
        y = []

        # set graph data
        fig, ax = plt.subplots()
        ax.set_title(graph_object.title)
        for i in range(graph_object.data.__len__()):
            # Generate Graph
            ax.set_xlabel(graph_object.x_label[i])
            ax.set_ylabel(graph_object.y_label[i])
            x.append(graph_object.data[i].index)
            y.append(graph_object.data[i].values)
            ax.plot(x[i], y[i], label=graph_object.data_label[i])

        # Display Graph
        ax.legend()
        plt.show()

    def bar_graph(self, graph_object: Graph):
        x = []
        y = []

        fig, ax = plt.subplots()
        ax.set_title(graph_object.title)
        width = 0.5
        graph_number = len(graph_object.data)
        if graph_number > 1:
            width = 1 / graph_number - 0.1

        for i in range(graph_number):

            ax.set_xlabel(graph_object.x_label[i])
            ax.set_ylabel(graph_object.y_label[i])
            x.append(graph_object.data[i].index)
            y.append(graph_object.data[i].values)
            x_number = np.arange(len(x[i]))
            ax.set_xticks(x_number)
            ax.set_xticklabels(x[i])
            if i % 2 == 0:
                ax.bar(x_number - width / 2, y[i], width, label=graph_object.data_label[i])
            else:
                ax.bar(x_number + width / 2, y[i], width, label=graph_object.data_label[i])

        ax.legend()
        plt.tight_layout()
        plt.show()


class WidgetHelper:
    def __init__(self):
        pass

    def parse_result(self, r: Result):
        if r.exec_continue:
            if r.result_type == 'dataframe':
                ddf = DispDataFrame()
                ddf.show_dataframe(r.result_data)

            elif r.result_type == 'line graph':
                gg = GenerateGraph()
                gg.line_graph(r.result_data)

            elif r.result_type == 'bar graph':
                gg = GenerateGraph()
                gg.bar_graph(r.result_data)
            else:
                print('result_type is out of barns')
                print('Type = ' + r.result_type)
        else:
            error_list = r.error_list
            for i in range(error_list.get_length):
                er = error_list.error_list[i]
                erh = Error_Handler(er)
                erh.print_error()

