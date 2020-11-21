#

from information import InfosRead
from serialize import Data
import pandas as pd

from error_handler import Error, ErrorList
from widget_helper import Result

class Analysis_Info:
    def __init__(self, read_type):
        self.info_collection = []

        # Get Company Information data
        self.info_collection = InfosRead(read_type)
        if self.info_collection.result.exec_continue:
            print('Company Information Data (' + str(len(self.info_collection.result.result_data)) + ') set completed!')
            # Prepare Result Class
            self.result = Result()
        else:
            pass

    # class Inquiry
    def inquiry(self, company) -> Result:
        self.result.action_name = 'Inquiry Company Information'
        self.result.result_type = 'dataframe'
        self.result.result_data = self.info_collection.infos.get(company + '.T')
        if self.result.exec_continue is False:
            er = Error(ValueError, company, 'Hit No Data')
            e_list = ErrorList().add_list(er)
            self.result.error_list = e_list
            self.result.exec_continue = False
        else:
            # Dictionary to DataFrame
            self.result.result_data = pd.DataFrame(self.result.result_data.values(),
                                                   index=self.result.result_data.keys())

        # result.to_excel('./test.xlsx')
        return self.result

    def generate_ranking(self):
        pass
