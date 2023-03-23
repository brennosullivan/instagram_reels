from pandas_datareader import data as pdr
import pandas as pd
from datetime import datetime
import requests
import os
import zipfile
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap



tickers = pd.read_excel("composicao_ibov_v2.xlsx")

intervalo_tempo = range(2014, 2022)

lista_tickers = []

for ano in intervalo_tempo:

    tickers_no_ano = tickers[ano]

    tickers_no_ano = tickers_no_ano.dropna()

    tickers_no_ano = tickers_no_ano.apply(lambda x: x + ".SA")

    lista_tickers.append(tickers_no_ano)


lista_tickers_finais = pd.concat(lista_tickers)

lista_tickers_finais = list(lista_tickers_finais)


dados_cotacoes = pdr.get_data_yahoo(symbols = lista_tickers_finais, start="2014-12-30", end= "2022-08-09" )['Adj Close']

ultima_linha = dados_cotacoes.iloc[-1:]

dados_cotacoes_anual = dados_cotacoes.resample("Y").last()
dados_cotacoes_anual = dados_cotacoes_anual.append(ultima_linha)
dados_cotacoes_anual = dados_cotacoes_anual.drop("2022-12-31", axis = 0)

datas_carteiras = list(dados_cotacoes_anual.index)[1:]


dados_cotacoes_anual = dados_cotacoes_anual.fillna(0)

for i, nome_empresa in enumerate(dados_cotacoes_anual.columns):

    if i == 0:

      retornos = dados_cotacoes_anual[nome_empresa].pct_change()

      retornos = retornos.replace([np.inf, -np.inf, -1], 0)

      df_retornos = pd.DataFrame(data = {nome_empresa: retornos}, index = dados_cotacoes_anual.index)

    else:
    
      df_retornos[nome_empresa] = dados_cotacoes_anual[nome_empresa].pct_change().replace([np.inf, -np.inf, -1], 0)


df_retornos


df_retornos = df_retornos.drop("2014-12-31", axis = 0)

dados_cotacoes_anual = dados_cotacoes_anual.reset_index()

df_retornos = df_retornos.reset_index()


dados_cotacoes_anual = pd.melt(dados_cotacoes_anual, id_vars= "Date", var_name= "cod", value_name= "cotacao")
df_retornos = pd.melt(df_retornos, id_vars= "Date", var_name= "cod", value_name= "retorno_12m")



dados_cotacoes_anual = dados_cotacoes_anual.dropna()
df_retornos = df_retornos.dropna()


anos_modelo = range(2015, 2023)

lista_retornos = []

df_retornos['Date'] = pd.to_datetime(df_retornos['Date'])

for indice, ano in enumerate(datas_carteiras):

    #pegando empresas

    empresas_ibov = tickers[anos_modelo[indice]]

    empresas_ibov = list(empresas_ibov.dropna().values) 

    empresas_ibov = [empresa + ".SA" for empresa in empresas_ibov]

    #pegando retornos pra criar o ranking

    retornos_empresas_ibov_esse_ano = df_retornos[(df_retornos["cod"].isin(empresas_ibov)) & (df_retornos['Date'] == ano)]

    #pegando os 10 maiores retornos

    dez_maiores_retornos = retornos_empresas_ibov_esse_ano.sort_values(by = "retorno_12m", ascending = False).head(10)

    tickers_dez_maiores_retornos = dez_maiores_retornos["cod"].to_list()

    #calculando retorno da carteira 

    if indice != (len(datas_carteiras) - 1):

      retornos_12m_seguintes = df_retornos[(df_retornos["cod"].isin(tickers_dez_maiores_retornos)) & (df_retornos['Date'] == datas_carteiras[indice + 1])]

      retorno_no_ano = np.mean(retornos_12m_seguintes['retorno_12m'])

      df_retorno_modelo = pd.DataFrame(data = {"retorno": retorno_no_ano}, index = [ano.year + 1])

      lista_retornos.append(df_retorno_modelo)


retornos_modelo = pd.concat(lista_retornos)

retornos_modelo


ibovespa = pdr.get_data_yahoo(symbols = '^BVSP', start="2015-12-30", end= "2022-08-09" )['Adj Close']

retornos_ibovespa = ibovespa.resample("Y").last().pct_change().dropna()

retornos_ibovespa

retornos_modelo['ibovespa'] = retornos_ibovespa.values

retornos_modelo['bateu_mercado'] = retornos_modelo['retorno'] > retornos_modelo['ibovespa']


retornos_modelo.style.format({
    'retorno': '{:,.2%}'.format,
    'ibovespa': '{:,.2%}'.format
})



cumulative_ret_modelo = (retornos_modelo.retorno + 1).cumprod() - 1

cumulative_ret_modelo[2015] = 0

cumulative_ret_modelo = cumulative_ret_modelo.sort_index()

cumulative_ret_ibov = (retornos_modelo.ibovespa + 1).cumprod() - 1

cumulative_ret_ibov[2015] = 0

cumulative_ret_ibov = cumulative_ret_ibov.sort_index()

df_acumulado = pd.DataFrame(data = {"retorno_acum_modelo": cumulative_ret_modelo, "retorno_acum_ibov" : cumulative_ret_ibov }, index = cumulative_ret_ibov.index)

df_acumulado.style.format({
    'retorno_acum_modelo': '{:,.2%}'.format,
    'retorno_acum_ibov': '{:,.2%}'.format
})


df_acumulado.plot()














