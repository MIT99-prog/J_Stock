import pandas as pd
import datetime as dt

a = pd.Series([0, 0, 0], index=[dt.datetime(2020, 11, 1), dt.datetime(2020, 11, 2), dt.datetime(2020, 11, 3)])
b = pd.Series([1, 1, 1],index=[dt.datetime(2020, 11, 1),dt.datetime(2020, 11, 4),dt.datetime(2020, 11, 5)])
mylist = a.index.append(b.index)
mylist = set(mylist)
print(mylist)
x = pd.DataFrame(index=mylist)
x.insert(0, '1300.T', a)
x.insert(1, '1301.T', b)
print(x)



