#

from dir_stock.stock import StockWrite
from market import Jasdaq

if __name__ == '__main__':
    # Get companies code of Jasdaq from jasdaq.txt file
    jasdaq = Jasdaq()

    # Get stock collection data and save stock file
    st = StockWrite()
    st.get_stocks(jasdaq)
