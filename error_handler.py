#

class Error_Handler:
    def __init__(self, error):
        self.error = error

    def print_error(self):
        print('Error! Type = ' + str(self.error.type)
              + ' / name = ' + self.error.name
              + ' / message = ' + self.error.message)

class Error(Exception):
    def __init__(self, type=object, name='', message=''):
        super().__init__()
        self.type = type
        self.name = name
        self.message = message

class Error_list:
    def __init__(self):
        self.error_list = []

    def addlist(self, error: Error):
        self.error_list.append(error)

    def get_length(self):
        return self.error_list.__len__()

