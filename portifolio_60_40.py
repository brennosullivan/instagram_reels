import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
import yfinance as yf
import quandl
from datetime import date 
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

ibov_retorno_mensal = ibov_cumulative_return.resample("M").last().pct_change().dropna()
cdi_retorno_mensal = cdi_cumulative_return.resample("M").last().pct_change()

datas = cdi_retorno_mensal.index

cdi_retorno_mensal = cdi_retorno_mensal.dropna()

df_valores = pd.DataFrame(data = {'ibov': 600, 'cdi': 400, 'Carteira 60/40': 1000, 'Rent 60/40': 0}, index = datas)

aporte_mensal = 200

for i, data in enumerate(ibov_retorno_mensal.index):

    rent_ibov = ibov_retorno_mensal.loc[data]
    rent_cdi = cdi_retorno_mensal.loc[data]

    novo_valor_ibov = df_valores.iloc[i, 0] * (1 + rent_ibov)
    novo_valor_cdi = df_valores.iloc[i, 1] * (1 + rent_cdi)

    rent_ibov_port = (novo_valor_ibov - df_valores.iloc[i, 0])/df_valores.iloc[i, 2]
    rent_cdi_port = (novo_valor_cdi - df_valores.iloc[i, 1])/df_valores.iloc[i, 2]

    total = novo_valor_ibov + novo_valor_cdi
    rent_total = rent_ibov_port + rent_cdi_port

    if (novo_valor_cdi/total) > 0.4:

        novo_valor_ibov = novo_valor_ibov + aporte_mensal

    else:

        novo_valor_cdi = novo_valor_cdi + aporte_mensal

    total = novo_valor_ibov + novo_valor_cdi

    df_valores.loc[data, 'ibov'] = novo_valor_ibov
    df_valores.loc[data, 'cdi'] = novo_valor_cdi  
    df_valores.loc[data, 'Carteira 60/40'] = total
    df_valores.loc[data, 'Rent 60/40'] = rent_total

df_valores = df_valores[['Carteira 60/40', 'Rent 60/40']] 

#CDI


df_valores_cdi = pd.DataFrame(data = {'CDI': 1000, 'Rent CDI': 0}, index = datas)

aporte_mensal = 200

for i, data in enumerate(cdi_retorno_mensal.index):

    rent_cdi = cdi_retorno_mensal.loc[data]

    novo_valor_cdi = (df_valores_cdi.iloc[i, 0] * (1 + rent_cdi)) + aporte_mensal    

    df_valores_cdi.loc[data, 'CDI'] = novo_valor_cdi
    df_valores_cdi.loc[data, 'Rent CDI'] = rent_cdi
     

#IBOV

df_valores_ibov = pd.DataFrame(data = {'IBOV': 1000, 'Rent IBOV': 0}, index = datas)

aporte_mensal = 200

for i, data in enumerate(ibov_retorno_mensal.index):

    rent_ibov = ibov_retorno_mensal.loc[data]

    novo_valor_ibov = (df_valores_ibov.iloc[i, 0] * (1 + rent_ibov)) + aporte_mensal    

    df_valores_ibov.loc[data, 'IBOV'] = novo_valor_ibov
    df_valores_ibov.loc[data, 'Rent IBOV'] = rent_ibov
     


df_valores = (df_valores.join(df_valores_ibov)).join(df_valores_cdi)

df_valores_dinheiro = df_valores[['Carteira 60/40', 'IBOV', 'CDI']]
df_valores_rent = df_valores[['Rent 60/40', 'Rent IBOV', 'Rent CDI']]

print(df_valores_rent.std())

df_valores_dinheiro.plot()
plt.legend()

plt.title('Comparação entre carteiras')
plt.savefig('6040.png')
plt.show()


















