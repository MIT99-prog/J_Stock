#

import joblib
from errorhandler import Error, ErrorList
from widget_helper import Result


class FileName:
    def __init__(self):
        self.market = ''
        self.data_type = ''

    def get_file_name(self) -> str:
        return './' + self.data_type + '_' + self.market


class Data:
    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def save_data(filename: FileName, value) -> Result:
        result = Result()
        result.action_name = 'save_data'

        try:
            with open(filename.get_file_name(), "wb") as f:
                joblib.dump(value, f, compress=3)
                result.result_type = 'dict'
                result.result_data = value

        except:
            er = Error(BaseException, filename.get_file_name(), 'File serialize error!')
            e_list = ErrorList()
            e_list.add_list(er)
            result.error_list = e_list
            result.exec_continue = False

        return result

    @staticmethod
    def load_data(filename: FileName) -> Result:
        result = Result()
        result.action_name = 'load_data'

        try:
            with open(filename.get_file_name(), "rb") as f:
                result.result_data = joblib.load(f)
                result.result_type = 'dict'
                # return value

        except FileNotFoundError:
            er = Error(FileNotFoundError, filename.get_file_name(), 'File not found!')
            e_list = ErrorList()
            e_list.add_list(er)
            result.error_list = e_list
            result.exec_continue = False
        return result
