#
import joblib
import pandas as pd
from get_stock_data import Element

# elt = Element('', pd.DataFrame())
open_price = pd.DataFrame()
close_price = pd.DataFrame()

filename = "./pydata"
with open(filename, "rb") as f:
    stocks = joblib.load(f)

for i in range(len(stocks)):
    elt = stocks[i]

    open_price.insert(loc=i, column=elt.company, value=elt.get_open())
    close_price.insert(loc=i, column=elt.company, value=elt.get_close())

# open_frame = pd.DataFrame(open_price).T  # DataFrame化
# open_frame.columns = stocks  # カラム名の設定
open_frame = open_price.ffill()  # 欠損データの補完

# close_frame = pd.DataFrame(close_price).T  # DataFrame化
# close_frame.columns = stocks  # カラム名の設定
close_frame = close_price.ffill()  # 欠損データの補完
print(" *** open *** ")
print(open_frame)
print(" *** close *** ")
print(close_frame)

balance = close_frame - open_frame
print(" *** balance *** ")
print(balance)

mu = balance.mean()
mu_mean = mu.mean()
mu_std = mu.std()
mu_point = (mu - mu_mean) / mu_std

print(" *** mu *** ")
print(mu)
print(mu_mean, mu_std)

sigma2 = balance.var()
sigma2_mean = sigma2.mean()
sigma2_std = sigma2.std()

sigma2_point = (sigma2 - sigma2_mean) / sigma2_std
print(" *** sigma2 *** ")
print(sigma2)
print(sigma2_mean, sigma2_std)

print(" *** point *** ")
print(mu_point)
print(sigma2_point)

point = mu_point + sigma2_point * -1
point = point.sort_values(ascending=False)
print("Ranking")
print(point)
