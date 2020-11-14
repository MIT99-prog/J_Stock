#
import pandas as pd
import yfinance as yf

from stocks import StocksWrite


class Jasdaq:
    def __init__(self):
        jasdaq_code = pd.read_csv("jasdaq-test.txt")
        company_codes = [str(s) + ".T" for s in jasdaq_code.code]
        # stocks.append("^JASDAQ")  #JASDAQ Index
        self.tickers = yf.Tickers(" ".join(company_codes))
        print(" *** tickers *** ")
        print(self.tickers)


if __name__ == '__main__':
    # Get companies code of Jasdaq from jasdaq.txt file
    jasdaq = Jasdaq()

    # Get stock collection data and save stock file
    st = StocksWrite()
    st.get_stocks(jasdaq)
