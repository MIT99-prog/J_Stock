#
from errorhandler import ErrorHandler, Error, ErrorList
from serialize import Data, FileName
from widget_helper import Result, DisplayInfo


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

    def __init__(self, di: DisplayInfo):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)

    def get_data(self, tickers) -> Result:

        for i in range(len(tickers.tickers)):
            try:
                self.infos[tickers.tickers[i].ticker] = tickers.tickers[i].info

            except:
                er = Error(self, str(tickers.tickers[i].ticker.__repr__()), 'Get Info Data Error!')
                self.e_list.add_list(er)
                erh = ErrorHandler(er)
                erh.print_error()

        data = Data()  # Create Data class of serialize.py
        self.result = data.save_data(self.filename, self.infos)  # Save data to stock file
        if self.result.exec_continue:
            self.result.action_name = 'Get Company Information Data'
            self.result.result_type = 'number'
            self.result.result_data = self.__len__()
            self.result.error_list = self.e_list
        else:
            pass
        return self.result


class InfosRead(Infomation):
    def __init__(self, di: DisplayInfo, read_type: str):
        super().__init__()
        self.filename = FileName(di.market, di.data_type)
        self.read_type = read_type

        # initialize values

        self.result = self.data_read()

    def data_read(self) -> Result:
        data = Data()

        self.result = data.load_data(self.filename)
        if self.result.exec_continue:
            self.infos = self.result.result_data
        else:
            pass

        # generate values
        if self.read_type == 'Extend':
            pass

        return self.result
