import pandas as pd
import os

os.chdir('/home/brenno/Documentos/Instagram/dados')

dados_dolar = pd.read_csv("dados_dolar.csv")

dados_dolar = dados_dolar.drop("cod", axis = 1)

dados_dolar['date'] = pd.to_datetime(dados_dolar['date'])

dados_dolar = dados_dolar.set_index("date")

dados_dolar = dados_dolar.resample("M").last()

dados_dolar = dados_dolar.pct_change().dropna()

dados_dolar['presidente'] = pd.NA

# dados_dolar.loc[dados_dolar.index < "1999-01-01", 'presidente'] = "Mandato FHC 1"

# dados_dolar.loc[(dados_dolar.index > "1998-12-31") & (dados_dolar.index < "2003-01-01"), 'presidente'] = "Mandato FHC 2"

# dados_dolar.loc[(dados_dolar.index > "2002-12-31") & (dados_dolar.index < "2007-01-01"), 'presidente'] = "Mandato Lula 1"

# dados_dolar.loc[(dados_dolar.index > "2006-12-31") & (dados_dolar.index < "2011-01-01"), 'presidente'] = "Mandato Lula 2"

# dados_dolar.loc[(dados_dolar.index > "2010-12-31") & (dados_dolar.index < "2015-01-01"), 'presidente'] = "Mandato Dilma 1"

# dados_dolar.loc[(dados_dolar.index > "2014-12-31") & (dados_dolar.index < "2016-09-01"), 'presidente'] = "Mandato Dilma 2"

# dados_dolar.loc[(dados_dolar.index > "2016-08-31") & (dados_dolar.index < "2018-01-01"), 'presidente'] = "Mandato Temer"

# dados_dolar.loc[dados_dolar.index > "2017-12-31", 'presidente'] = "Mandato Bolsonaro"

dados_dolar.loc[dados_dolar.index < "2003-01-01", 'presidente'] = "Mandato FHC"

dados_dolar.loc[(dados_dolar.index > "2002-12-31") & (dados_dolar.index < "2011-01-01"), 'presidente'] = "Mandato Lula"

dados_dolar.loc[(dados_dolar.index > "2010-12-31") & (dados_dolar.index < "2016-09-01"), 'presidente'] = "Mandato Dilma"

dados_dolar.loc[(dados_dolar.index > "2016-08-31") & (dados_dolar.index < "2018-01-01"), 'presidente'] = "Mandato Temer"

dados_dolar.loc[dados_dolar.index > "2017-12-31", 'presidente'] = "Mandato Bolsonaro"

dados_dolar['retornos'] = dados_dolar['value_price'] + 1

dados_dolar = dados_dolar.drop("value_price", axis = 1)

dados_dolar["retorno_acumulado_dolar"] = dados_dolar.groupby('presidente')['retornos'].cumprod() - 1

dados_dolar['retorno_acumulado_dolar'] = pd.Series([round(val, 2) for val in dados_dolar['retorno_acumulado_dolar']], index = dados_dolar.index)
dados_dolar['retorno_acumulado_dolar'] = pd.Series(["{0:.2f}%".format(val * 100) for val in dados_dolar['retorno_acumulado_dolar']], index = dados_dolar.index)

dados_dolar.to_csv("dados_mandatos_dolar.csv")

dados_dolar = (dados_dolar.groupby(['presidente']).tail(1))[['presidente', 'retorno_acumulado_dolar']]

print(dados_dolar)