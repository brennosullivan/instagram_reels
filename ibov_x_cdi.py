import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import yfinance as yf
import quandl

plt.style.use("cyberpunk")


cdi_data = quandl.get('BCB/11', start_date='1994-06-01')
dados = yf.download('^BVSP', start='1994-06-01')['Adj Close']
dados.index = (pd.to_datetime(dados.index))
dados = dados.sort_index(ascending=True)
dados = dados.pct_change()

cdi_returns = cdi_data['Value']/100

# calcula o retorno acumulado
ibov_cumulative_return = (1 + dados).cumprod() 
cdi_cumulative_return = (1 + cdi_returns).cumprod() 

# plota o gráfico comparando os retornos acumulados
plt.plot(ibov_cumulative_return, label='IBOV')
plt.plot(cdi_cumulative_return, label='CDI')
plt.legend()
plt.title('IBOV X CDI desde 1994')
plt.savefig('IBOV_CDI.png')
plt.show()