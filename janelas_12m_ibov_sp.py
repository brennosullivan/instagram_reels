import pandas as pd
from datetime import datetime
import quandl


dados = pd.read_excel('/home/brenno/Downloads/ibov_sp.xlsx', na_values="-")
cdi_data = quandl.get('BCB/11', start_date='1994-06-01')
cdi_data['Value'] = cdi_data['Value']/100
cdi_data['cota'] = (1 + cdi_data['Value']).cumprod() 
cdi_data = cdi_data[['cota']]
dados['Data'] = pd.to_datetime(dados['Data']).dt.date
dados = dados.set_index('Data')

dados = pd.merge(dados, cdi_data, left_index=True, right_index=True)


dados = dados.dropna()

dados = dados[dados.index > datetime(1999, 12, 31, 0, 0, 0)]

dados = dados.pct_change(periods=(252 * 10))

dados = dados.dropna()

print('% janelas', sum(dados['ibov'] > dados['cota'])/len(dados))
print("Periodos positivos ibov:", sum(dados['ibov'] > 0)/len(dados))
print("Periodos positivos sp:", sum(dados['sp'] > 0)/len(dados))
print('Media retornos', dados.mean())

dados.to_excel('/home/brenno/Downloads/dados_120m_ibov_sp.xlsx')
