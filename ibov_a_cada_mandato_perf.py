import pandas as pd
import os
import yfinance as yf

os.chdir('/home/brenno/Documentos/instagram_reels/dados')

dados_ibov = pd.read_csv("dados_ibovespa.csv")

dados_ibov = dados_ibov.drop("cod", axis = 1)

dados_ibov['date'] = pd.to_datetime(dados_ibov['date'])

dados_ibov = dados_ibov.set_index("date")

dados_ibov = dados_ibov['value_price']

dados_ibov_att = yf.download("^BVSP", "1994-12-20", "2023-03-20")['Adj Close']

#dados_ibov = dados_ibov.append(dados_ibov_att)

dados_ibov = dados_ibov_att

dados_ibov = dados_ibov.to_frame()

dados_ibov.columns = ['value_price']

dados_ibov = dados_ibov.resample("M").last()

dados_ibov = dados_ibov.pct_change().dropna()

dados_ibov['presidente'] = pd.NA

# dados_ibov.loc[dados_ibov.index < "1999-01-01", 'presidente'] = "Mandato FHC 1"

# dados_ibov.loc[(dados_ibov.index > "1998-12-31") & (dados_ibov.index < "2003-01-01"), 'presidente'] = "Mandato FHC 2"

# dados_ibov.loc[(dados_ibov.index > "2002-12-31") & (dados_ibov.index < "2007-01-01"), 'presidente'] = "Mandato Lula 1"

# dados_ibov.loc[(dados_ibov.index > "2006-12-31") & (dados_ibov.index < "2011-01-01"), 'presidente'] = "Mandato Lula 2"

# dados_ibov.loc[(dados_ibov.index > "2010-12-31") & (dados_ibov.index < "2015-01-01"), 'presidente'] = "Mandato Dilma 1"

# dados_ibov.loc[(dados_ibov.index > "2014-12-31") & (dados_ibov.index < "2016-09-01"), 'presidente'] = "Mandato Dilma 2"

# dados_ibov.loc[(dados_ibov.index > "2016-08-31") & (dados_ibov.index < "2018-01-01"), 'presidente'] = "Mandato Temer"

# dados_ibov.loc[dados_ibov.index > "2017-12-31", 'presidente'] = "Mandato Bolsonaro"

dados_ibov.loc[dados_ibov.index < "2003-01-01", 'presidente'] = "Mandato FHC"

dados_ibov.loc[(dados_ibov.index > "2002-12-31") & (dados_ibov.index < "2011-01-01"), 'presidente'] = "Mandato Lula"

dados_ibov.loc[(dados_ibov.index > "2010-12-31") & (dados_ibov.index < "2016-09-01"), 'presidente'] = "Mandato Dilma"

dados_ibov.loc[(dados_ibov.index > "2016-08-31") & (dados_ibov.index < "2018-01-01"), 'presidente'] = "Mandato Temer"

dados_ibov.loc[(dados_ibov.index > "2017-12-31") & (dados_ibov.index < "2023-01-01"), 'presidente'] = "Mandato Bolsonaro"

dados_ibov.loc[dados_ibov.index > "2023-01-01", 'presidente'] = "Mandato Lula 3"

print(dados_ibov)

dados_ibov['retornos'] = dados_ibov['value_price'] + 1

dados_ibov = dados_ibov.drop("value_price", axis = 1)

#print(dados_ibov)

dados_ibov["retorno_acumulado_ibovespa"] = dados_ibov.groupby('presidente')['retornos'].cumprod() - 1

dados_ibov['retorno_acumulado_ibovespa'] = pd.Series([round(val, 2) for val in dados_ibov['retorno_acumulado_ibovespa']], index = dados_ibov.index)
dados_ibov['retorno_acumulado_ibovespa'] = pd.Series(["{0:.2f}%".format(val * 100) for val in dados_ibov['retorno_acumulado_ibovespa']], index = dados_ibov.index)

dados_ibov.to_csv("dados_mandatos.csv")

dados_ibov = (dados_ibov.groupby(['presidente']).tail(1))[['presidente', 'retorno_acumulado_ibovespa']]

print(dados_ibov)

