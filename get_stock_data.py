#
import pandas as pd
import yfinance as yf

from stocks import Stocks_Write
from market import Jasdaq

if __name__ == '__main__':
    # Get companies code of Jasdaq from jasdaq.txt file
    jasdaq = Jasdaq()

    # Get stock collection data and save stock file
    st = Stocks_Write()
    st.get_stocks(jasdaq)
