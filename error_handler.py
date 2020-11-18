#

class Error_Handler:
    def __init__(self, error):
        self.error = error

    def print_error(self):
        print('Error is occurred! Type = ' + self.error.type.__str__()
              + ' / name = ' + self.error.name
              + ' / message = ' + self.error.message)

class Error:
    def __init__(self, type=object, name='', message=''):
        self.type = type
        self.name = name
        self.message = message
