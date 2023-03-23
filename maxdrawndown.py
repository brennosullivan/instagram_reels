


import yfinance as yf
import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.ticker as mtick
import matplotlib.dates as mdate


data_final = dt.datetime.now()
data_inicial = data_final - dt.timedelta(days=1500)
ativo = "PETR4.SA"
precos = yf.download(ativo, 
                        data_inicial, data_final)['Adj Close']


precos_max = precos.cummax()
drawdowns = (precos - precos_max)/precos_max
drawndown_maximo = drawdowns.min()
print(drawndown_maximo)

fig, ax = plt.subplots()
ax.plot(drawdowns.index, drawdowns)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.xaxis.set_major_locator(mdate.YearLocator(1))
plt.show()


