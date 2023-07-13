import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import mplcyberpunk
from bcb import sgs

#plt.style.use('cyberpunk')

selic = sgs.get({'selic' :11})

selic['selic'] = selic['selic']/100

selic = selic[selic.index > "2010-01-01"]

selic['cota'] = (1 + selic['selic']).cumprod() - 1

selic = selic.drop('selic', axis = 1)

print(selic)

acoes = ['ABEV3', 'CIEL3', 'CPFE3', 'ITUB4', 'BBDC4', 'LREN3', 'WEGE3', 'EQTL3']

acoes = [x + '.SA' for x in acoes]

acoes.append("^BVSP")

dados = yf.download(acoes, start='2009-12-30')['Adj Close']

dados.index = (pd.to_datetime(dados.index))

dados = dados.sort_index(ascending=True)

dados = dados.pct_change()

dados = (dados + 1).cumprod() - 1

dados = dados.dropna()

dados = pd.merge(dados, selic, left_index=True, right_index=True, how='left')

print(dados)

dados.plot()

plt.show()
