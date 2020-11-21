#

import joblib
from error_handler import Error, ErrorList
from widget_helper import Result


class Data:
    def __init__(self):
        self.result = Result()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def save_data(self, filename: str, value) -> Result:
        self.result.action_name = 'save_data'
        filename = "./" + filename
        try:
            with open(filename, "wb") as f:
                joblib.dump(value, f, compress=3)
        except:
            pass
        return self.result

        # print("save data!")

    def load_data(self, filename: str) -> Result:
        self.result.action_name = 'load_data'
        filename = "./" + filename
        try:
            with open(filename, "rb") as f:
                self.result.result_data = joblib.load(f)
                self.result.result_type = 'dict'
                # return value

        except FileNotFoundError:
            er = Error(FileNotFoundError, filename, 'File not found!')
            e_list = ErrorList()
            e_list.add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False
        return self.result
