#

import joblib
from errorhandler import Error, ErrorList
from widget_helper import Result

class FileName:
    def __init__(self, market: str, data_type: str):
        self.market = market
        self.data_type = data_type

    def get_file_name(self) -> str:
        return './' + self.data_type + '_' + self.market



class Data:
    def __init__(self):
        self.result = Result()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save_data(self, filename: FileName, value) -> Result:
        self.result.action_name = 'save_data'

        try:
            with open(filename.get_file_name(), "wb") as f:
                joblib.dump(value, f, compress=3)
        except:
            pass
        return self.result

        # print("save data!")

    def load_data(self, filename: FileName) -> Result:
        self.result.action_name = 'load_data'

        try:
            with open(filename.get_file_name(), "rb") as f:
                self.result.result_data = joblib.load(f)
                self.result.result_type = 'dict'
                # return value

        except FileNotFoundError:
            er = Error(FileNotFoundError, filename.get_file_name(), 'File not found!')
            e_list = ErrorList()
            e_list.add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False
        return self.result
