#
import pandas as pd
import yfinance as yf

class Jasdaq:
    def __init__(self):
        jasdaq_code = pd.read_csv("jasdaq-test.txt")
        company_codes = [str(s) + ".T" for s in jasdaq_code.code]
        # stocks.append("^JASDAQ")  #JASDAQ Index
        self.tickers = yf.Tickers(" ".join(company_codes))
        print(" *** tickers *** ")
        print(self.tickers)