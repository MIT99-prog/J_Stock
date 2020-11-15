#
import pandas as pd
import yfinance as yf

from income_statement import Incomes_Write


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
    iw = Incomes_Write()
    iw.get_incomes(jasdaq)
