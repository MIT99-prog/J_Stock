#

from dir_information.information import InfosRead
import pandas as pd

from errorhandler import Error, ErrorList
from widget_helper import Result, DisplayInfo

class Analysis_Info:
    def __init__(self, di: DisplayInfo, read_type: str):
        self.info_collection = []
        self.di = di
        # Get Company Information data
        self.info_collection = InfosRead(di, read_type)
        if self.info_collection.result.exec_continue:
            print('Company Information Data (' + str(len(self.info_collection.result.result_data)) + ') set completed!')
            # Prepare Result Class
            self.result = Result()
        else:
            pass

    # class Inquiry
    def inquiry(self) -> Result:
        self.result.action_name = 'Inquiry Company Information'
        self.result.result_type = 'dataframe'
        self.result.result_data = self.info_collection.infos.get(self.di.company + '.T')
        if self.result.exec_continue is False:
            er = Error(ValueError, self.di.company, 'Hit No Data')
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
