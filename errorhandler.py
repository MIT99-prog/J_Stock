#

class ErrorHandler:
    def __init__(self, error):
        self.error = error

    def print_error(self):
        print('Error! Type = ' + str(self.error.error_type)
              + ' / name = ' + self.error.error_name
              + ' / message = ' + self.error.error_message)


class Error(Exception):
    def __init__(self, error_type=object, name='', message=''):
        super().__init__()
        self.error_type = error_type
        self.error_name = name
        self.error_message = message


class ErrorList:
    def __init__(self):
        self.error_list = []

    def add_list(self, error: Error):
        self.error_list.append(error)

    def get_length(self):
        return self.error_list.__len__()
