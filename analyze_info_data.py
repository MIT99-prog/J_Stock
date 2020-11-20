#

from infomation import Infos_Read
from serialize import Data
import pandas as pd


class Analysis_Info:
    def __init__(self, read_type):
        self.info_collection = []

        self.data = Data()

        # Get Stocks data
        self.info_collection = Infos_Read(read_type)
        print('Info Data set completed!')

    def inquiry(self, company_code):
        # pd.set_option('display.max_columns', None)
        result = self.info_collection.infos.get(company_code + '.T')
        result_df = pd.DataFrame(result.values(), index=result.keys())
        # result.to_excel('./test.xlsx')
        return result_df

    def generate_ranking(self):
        pass
