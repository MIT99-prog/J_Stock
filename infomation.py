#
from error_handler import Error_Handler, Error
from serialize import Data


class Infomation:
    def __init__(self):
        # self.stocks = []
        self.infos = dict()

    def __getitem__(self, i):
        keys = self.infos.keys()
        key = list(keys)[i]
        return self.infos.get(key)

    def __len__(self):
        return self.infos.__len__()


class Infos_Write(Infomation):

    def __init__(self):
        super().__init__()

    def get_data(self, tickers) -> int:

        for i in range(len(tickers.tickers)):
            try:
                self.infos[tickers.tickers[i].ticker] = tickers.tickers[i].info
            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Info Data Error!')
                erh = Error_Handler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        data.save_data('info', self.infos)  # Save data to stock file
        return self.__len__()


class Infos_Read(Infomation):
    def __init__(self, read_type):
        super().__init__()

        # initialize values

        self.data_read(read_type)

    def data_read(self, read_type):
        filename = "info"  # data file name
        data = Data()

        self.infos = data.load_data(filename)

        # Create dictionary of income statement

        # generate values
        if read_type == 'Extend':
            pass