#

from errorhandler import Error, ErrorList
from dir_stock.stock import StockRead
from widget_helper import Result, Graph, DisplayInfo


class AnalysisStock:
    def __init__(self, di: DisplayInfo, read_type: str):
        self.stock_collection = []
        self.di = di
        # Get Stocks data
        self.stock_collection = StockRead(di, read_type)
        if self.stock_collection.result.exec_continue:
            print('Stock History Data (' + str(self.stock_collection.result.result_data) + ') set completed!')
            # Prepare Result Class
            self.result = Result()
        else:
            pass

    def inquiry(self) -> Result:
        self.result.action_name = 'Inquiry Stock History'
        self.result.result_type = 'dataframe'
        self.result.result_data = self.stock_collection.stocks.get(self.di.company + '.T')
        if self.result.exec_continue is False:
            er = Error(ValueError, self.di.company, 'Hit No Data')
            e_list = ErrorList().add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False
        # result.to_excel('./test.xlsx')
        return self.result

    def generate_ranking(self) -> Result:
        # Calc Balance from Open Price to Close price
        change_value = self.stock_collection.close_price - self.stock_collection.open_price
        print(" *** change_value *** ")
        print(change_value)

        # Calc average of the balance
        mu = change_value.mean()
        mu_mean = mu.mean()
        mu_std = mu.std()
        mu_point = (mu - mu_mean) / mu_std

        print(" *** mu *** ")
        print(mu)
        print(mu_mean, mu_std)

        # Calc variance of the balance
        sigma2 = change_value.var()
        sigma2_mean = sigma2.mean()
        sigma2_std = sigma2.std()
        sigma2_point = (sigma2 - sigma2_mean) / sigma2_std

        print(" *** sigma2 *** ")
        print(sigma2)
        print(sigma2_mean, sigma2_std)

        print(" *** point *** ")
        print(mu_point)
        print(sigma2_point)

        point = mu_point + sigma2_point * -1
        point = point.sort_values(ascending=False)

        # filename = "rank"
        # self.data.save_data(filename, point)

        # print("Ranking")
        # print(point)

        point = point.head(10)
        # generate Graph Object
        g = Graph()
        g.set_title('Change Price Ranking Graph (Top10)')
        g.set_x_label('Company')
        g.set_y_label('Point : Average + Variant * -1')
        g.set_data_label('Point')
        g.set_data(point)

        # Generate Result Class
        self.result.action_name = 'generate stock ranking'
        self.result.result_type = 'bar graph'
        self.result.result_data = g
        self.result.exec_continue = True
        return self.result


if __name__ == '__main__':
    pass
