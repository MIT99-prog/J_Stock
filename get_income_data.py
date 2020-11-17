#
import pandas as pd
import yfinance as yf

from income_statement import Incomes_Write
from market import Jasdaq

if __name__ == '__main__':
    # Get companies code of Jasdaq from jasdaq.txt file
    jasdaq = Jasdaq()

    # Get stock collection data and save stock file
    iw = Incomes_Write()
    iw.get_incomes(jasdaq)
