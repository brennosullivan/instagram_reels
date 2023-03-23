



import datetime as dt
from pandas_datareader import data as pdr
import seaborn as sns
import matplotlib.pyplot as plt

data_final = dt.datetime.now()
data_inicial = data_final - dt.timedelta(days=300)

precos = pdr.get_data_yahoo(
        ["PETR4.SA", "VALE3.SA", "WEGE3.SA", "LREN3.SA"], 
        data_inicial, data_final)['Adj Close']

retornos = precos.pct_change().dropna()

correlacao = retornos.corr()

plot = sns.heatmap(correlacao, annot=True, fmt=".2f", linewidths=.6)

plt.show()









