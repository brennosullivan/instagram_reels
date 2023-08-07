
import pandas as pd
import numpy as np
from  bcb import sgs
from datetime import date

init_date = date(2000, 1, 1)
end_date = date(2022, 3, 31)
capital = 1000

selic = sgs.get({"SELIC":11}, start=init_date, end=end_date )/100

windows = ((1 + selic).rolling(window=500).apply(np.prod) - 1)
windows.plot()
windows = windows.reset_index()
windows.columns = ["end_date","returns"]
windows.insert(0,"init_date",0)
windows["init_date"] = windows["end_date"].shift(499)
windows.dropna(inplace=True)
print(windows)

id_row = windows["returns"].idxmax()
row = windows.loc[id_row]
initial_return_date = row[0]
final_return_date  = row[1]
selic_range = selic[(selic.index >= initial_return_date) & (selic.index <= final_return_date)]
acum_return_range = (selic_range + 1).cumprod() - 1
acum_return_range.plot()

acum_return_range["won"] = acum_return_range * capital
total = acum_return_range.iloc[-1] * capital
print(total)