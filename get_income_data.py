#

from dir_income_statement.income_statement import IncomesWrite
from market import Jasdaq

if __name__ == '__main__':
    # Get companies code of Jasdaq from jasdaq.txt file
    jasdaq = Jasdaq()

    # Get stock collection data and save stock file
    iw = IncomesWrite()
    iw.get_incomes(jasdaq)
