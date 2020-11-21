#
from error_handler import Error_Handler, Error, ErrorList
from serialize import Data
from widget_helper import Result


class Infomation:
    def __init__(self):
        self.e_list = ErrorList()
        self.infos = dict()
        self.result = Result()

    def __getitem__(self, i):
        keys = self.infos.keys()
        key = list(keys)[i]
        return self.infos.get(key)

    def __len__(self):
        return self.infos.__len__()


class InfosWrite(Infomation):

    def __init__(self):
        super().__init__()

    def get_data(self, tickers) -> Result:

        for i in range(len(tickers.tickers)):
            try:
                self.infos[tickers.tickers[i].ticker] = tickers.tickers[i].info

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Info Data Error!')
                self.e_list.add_list(er)
                erh = Error_Handler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        self.result = data.save_data('info', self.infos)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = 'Get Company Information Data'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass
        return self.result


class InfosRead(Infomation):
    def __init__(self, read_type):
        super().__init__()

        # initialize values

        self.result = self.data_read(read_type)

    def data_read(self, read_type) -> Result:
        filename = "info"  # data file name
        data = Data()

        self.result = data.load_data(filename)
        if self.result.exec_continue:
            self.infos = self.result.result_data
        else:
            pass

        # generate values
        if read_type == 'Extend':
            pass

        return self.result
