from cProfile import label
from curses import window
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from dateutil.relativedelta import relativedelta
from datetime import date
import seaborn as sns
import matplotlib.ticker as mtick

url = "https://www.comdinheiro.com.br/Clientes/API/EndPoint001.php"

querystring = {"code":"import_data"}

data = "18082000"

payload = "username=edufinance_&password=Research81%40Varos&URL=HistoricoCotacao002.php%3F%26x%3DCDI%2BATIVO_INDEXADO_TR%2818~08~2000%2C1%2C0.2466%29%2BIBGE_IPCA%2BVALE3%2BPETR4%2BIBOV%2B%26data_ini%3D18082000%26data_fim%3D29042022%26pagina%3D1%26d%3DMOEDA_ORIGINAL%26g%3D0%26m%3D0%26info_desejada%3Dretorno_acum%26retorno%3Ddiscreto%26tipo_data%3Ddu_br%26tipo_ajuste%3Dtodosajustes%26num_casas%3D2%26enviar_email%3D0%26ordem_legenda%3D1%26cabecalho_excel%3Dmodo1%26classes_ativos%3D4xdkkfek4xr%26ordem_data%3D0%26rent_acum%3Drent_acum%26minY%3D%26maxY%3D%26deltaY%3D%26preco_nd_ant%3D0%26base_num_indice%3D100%26flag_num_indice%3D0%26eixo_x%3DData%26startX%3D0%26max_list_size%3D20%26line_width%3D2%26titulo_grafico%3D%26legenda_eixoy%3D%26tipo_grafico%3Dline&format=json2"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

json_resposta = json.loads(response.text)

lista_dados = []

for inflacao in json_resposta['resposta']['tab-p1']['linha']:

    lista_dados.append(pd.DataFrame(data = inflacao, index=[0]))

df_dados = pd.concat(lista_dados, ignore_index=True)

df_dados['data'] = pd.to_datetime(df_dados['data'], format= '%d/%m/%Y')

df_dados.columns = ['data', 'CDI', 'FGTS', 'IBGE_IPCA', 'VALE3', 'PETR4', 'IBOV']

def tratando_dados_com_dinheiro(nome_coluna):
    
    df_dados[f'{nome_coluna}'] = list(map(lambda x: x.replace(",", "."), df_dados[f'{nome_coluna}']))
    df_dados[f'{nome_coluna}'] =df_dados[f'{nome_coluna}'].astype(float)
    df_dados[f'{nome_coluna}'] = list(map(lambda x: round(x, 2), df_dados[f'{nome_coluna}']))


tratando_dados_com_dinheiro('CDI')
tratando_dados_com_dinheiro('FGTS')
tratando_dados_com_dinheiro('IBGE_IPCA')
tratando_dados_com_dinheiro('VALE3')
tratando_dados_com_dinheiro('PETR4')
tratando_dados_com_dinheiro('IBOV')


df_dados = df_dados.set_index('data')

fgts_tr = df_dados['FGTS'] + 100

fgts_tr = fgts_tr.pct_change()

fgts_tr.loc["2016-12-30"] = fgts_tr.loc["2016-12-30"] + 0.0193
fgts_tr.loc["2017-12-29"] = fgts_tr.loc["2017-12-29"] + 0.0173
fgts_tr.loc["2018-12-28"] = fgts_tr.loc["2018-12-28"] + 0.0380
fgts_tr.loc["2019-12-30"] = fgts_tr.loc["2019-12-30"] + 0.0190
fgts_tr.loc["2020-12-30"] = fgts_tr.loc["2020-12-30"] + 0.0186


retornos_fgts_tr = (1 + fgts_tr).cumprod() - 1

retornos_fgts_tr[0] = 0

retornos_fgts_tr = retornos_fgts_tr * 100

df_dados['FGTS'] = retornos_fgts_tr

dados_x_petro = df_dados.drop("VALE3", axis = 1)

dados_x_vale = df_dados.drop('PETR4', axis = 1)

dados_x_vale = dados_x_vale[dados_x_vale.index > "2002-03-27"]


#-------------------------------------Estatisticas---------------------------------

df_heatmap_vale = pd.DataFrame(np.zeros((4, 5)), columns=['CDI', 'FGTS', 'IBGE_IPCA', 'VALE3', 'IBOV'], index=['1 ano', '3 anos', '5 anos', '10 anos'])

df_heatmap_vale.loc['1 ano'] = dados_x_vale.loc["2003-03-28"]
df_heatmap_vale.loc['3 anos'] = dados_x_vale.loc["2005-03-28"]
df_heatmap_vale.loc['5 anos'] = dados_x_vale.loc["2007-03-28"]
df_heatmap_vale.loc['10 anos'] = dados_x_vale.loc["2012-03-28"]

minima_historica = dados_x_vale[dados_x_vale['VALE3'] == min(dados_x_vale['VALE3'])]

minima_2015 = dados_x_vale[dados_x_vale['VALE3'] == min((dados_x_vale.loc['2015'])['VALE3'])]

df_heatmap_vale = df_heatmap_vale.transpose()

lista_anos = [1, 3, 5, 10]

for i, coluna in enumerate(df_heatmap_vale.columns):

    df_heatmap_vale[f'{coluna}'] = list(map(lambda x: ((1 + (x/100))**(1/lista_anos[i]) - 1) * 100, df_heatmap_vale[f'{coluna}']))
    df_heatmap_vale[f'{coluna}'] = df_heatmap_vale[f'{coluna}'].round(2)
    
# ax = sns.heatmap(df_heatmap_vale, annot=True, cmap="Greens", fmt = "g")

# for t in ax.texts: 
#     t.set_text(t.get_text() + "%")

# plt.show()

#long short vale x FGTS

long_short_vale = dados_x_vale['VALE3'] - dados_x_vale['FGTS']


# plt.plot(long_short_vale)
# plt.axhline(y=0.0, color='g', linestyle='-', linewidth = 0.5)
# plt.show()

#------------------------grafico geral------------------

# plt.plot(dados_x_vale, label = dados_x_vale.columns)
# plt.legend()
# plt.show()


#-----------------------------------petro

df_heatmap_petro = pd.DataFrame(np.zeros((4, 5)), columns=['CDI', 'FGTS', 'IBGE_IPCA', 'PETR4', 'IBOV'], index=['1 ano', '3 anos', '5 anos', '10 anos'])

df_heatmap_petro.loc['1 ano'] = dados_x_petro.loc["2001-08-20"]
df_heatmap_petro.loc['3 anos'] = dados_x_petro.loc["2003-08-18"]
df_heatmap_petro.loc['5 anos'] = dados_x_petro.loc["2005-08-18"]
df_heatmap_petro.loc['10 anos'] = dados_x_petro.loc["2010-08-18"]

minima_historica = dados_x_petro[dados_x_petro['PETR4'] == min(dados_x_petro['PETR4'])]

minima_2015 = dados_x_petro[dados_x_petro['PETR4'] == min((dados_x_petro.loc['2015'])['PETR4'])]


df_heatmap_petro = df_heatmap_petro.transpose()

lista_anos = [1, 3, 5, 10]

for i, coluna in enumerate(df_heatmap_petro.columns):

    df_heatmap_petro[f'{coluna}'] = list(map(lambda x: ((1 + (x/100))**(1/lista_anos[i]) - 1) * 100, df_heatmap_petro[f'{coluna}']))
    df_heatmap_petro[f'{coluna}'] = df_heatmap_petro[f'{coluna}'].round(2)
    
# ax = sns.heatmap(df_heatmap_petro, annot=True, cmap="Greens", fmt = "g")

# for t in ax.texts: 
#     t.set_text(t.get_text() + "%")

# plt.show()

#long short petro x FGTS

long_short_petro = dados_x_petro['PETR4'] - dados_x_petro['FGTS']


# plt.plot(long_short_petro)
# plt.axhline(y=0.0, color='g', linestyle='-', linewidth = 0.5)
# plt.show()

#------------------------grafico geral------------------

df_dados.to_csv('dados_grafico_linha.csv')

# fig, ax = plt.subplots()
# ax.plot(df_dados, label = df_dados.columns)
# ax.yaxis.set_major_formatter(mtick.PercentFormatter())
# plt.xticks(fontsize=13)
# plt.yticks(fontsize=13)
# plt.title("Rentabilidade ativos desde 2000")
# plt.legend()
# plt.show()

dados_x_petro = dados_x_petro + 100

def janelas_moveis_retorno(df, dias, ticker):

    df = df + 100

    janela_movel = df.pct_change(periods = dias)
    indice = janela_movel.index[0:-dias]
    janela_movel = janela_movel.dropna()
    janela_movel.index = indice
    serie_long_short = janela_movel[f'{ticker}'] - janela_movel['FGTS']
    amostra_percentual = sum(serie_long_short > 0)/len(serie_long_short)

    return amostra_percentual

janela_1_ano_petro = janelas_moveis_retorno(dados_x_petro, 250, ticker = "PETR4") 
janela_3_anos_petro = janelas_moveis_retorno(dados_x_petro, 250 * 3, ticker = "PETR4") 
janela_5_anos_petro = janelas_moveis_retorno(dados_x_petro, 250 * 5, ticker = "PETR4") 
janela_10_anos_petro = janelas_moveis_retorno(dados_x_petro, 250 * 10, ticker = "PETR4") 

janela_1_ano_vale = janelas_moveis_retorno(dados_x_vale, 250, ticker = "VALE3") 
janela_3_anos_vale = janelas_moveis_retorno(dados_x_vale, 250 * 3, ticker = "VALE3") 
janela_5_anos_vale = janelas_moveis_retorno(dados_x_vale, 250 * 5, ticker = "VALE3") 
janela_10_anos_vale = janelas_moveis_retorno(dados_x_vale, 250 * 10, ticker = "VALE3") 


tabela_janelas_moveis = pd.DataFrame(data = {'Vale': [janela_1_ano_vale, janela_3_anos_vale, janela_5_anos_vale, janela_10_anos_vale],
                                            'Petrobras': [janela_1_ano_petro, janela_3_anos_petro, janela_5_anos_petro, janela_10_anos_petro]}, 
                                                index=['1 ano', '3 anos', '5 anos', '10 anos'])


for coluna in tabela_janelas_moveis.columns:

    tabela_janelas_moveis[f'{coluna}'] = (tabela_janelas_moveis[f'{coluna}'].round(2)) * 100


tabela_janelas_moveis = tabela_janelas_moveis.transpose()

# ax = sns.heatmap(tabela_janelas_moveis, annot=True, cmap="Greens", fmt = "g")
# plt.title("Mapa de calor da % das vezes que o ativo superou o FGTS no período")
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)

# for t in ax.texts: 
#     t.set_text(t.get_text() + "%")

# plt.show()

# print(tabela_janelas_moveis)


# inverso = 100 - tabela_janelas_moveis.loc['Petrobras']

# fig, ax = plt.subplots()



# ax.bar(tabela_janelas_moveis.columns, tabela_janelas_moveis.loc['Petrobras'], color = "black")
# ax.bar(tabela_janelas_moveis.columns, inverso, bottom=tabela_janelas_moveis.loc['Petrobras'], color = "lime")

# ax.set_ylim([0, 120])

# ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# plt.show()

def janelas_moveis_retorno_acumulado(df, dias, anos):

    df = df + 100

    janela_movel = df.pct_change(periods = dias)
    indice = janela_movel.index[0:-dias]
    janela_movel = janela_movel.dropna()
    janela_movel.index = indice

    media_retorno_acumulado_vale = janela_movel['VALE3'].mean()
    valor_ao_ano_vale = (1 + media_retorno_acumulado_vale)**(1/anos) - 1 

    media_retorno_acumulado_petr = janela_movel['PETR4'].mean()
    valor_ao_ano_petr = (1 + (media_retorno_acumulado_petr))**(1/anos) - 1 

    media_retorno_acumulado_fgts = janela_movel['FGTS'].mean()
    valor_ao_ano_fgts = (1 + (media_retorno_acumulado_fgts))**(1/anos) - 1 

    media_retorno_acumulado_cdi = janela_movel['CDI'].mean()
    valor_ao_ano_cdi = (1 + (media_retorno_acumulado_cdi))**(1/anos) - 1 

    media_retorno_acumulado_ipca = janela_movel['IBGE_IPCA'].mean()
    valor_ao_ano_ipca = (1 + (media_retorno_acumulado_ipca))**(1/anos) - 1 

    media_retorno_acumulado_ibov = janela_movel['IBOV'].mean()
    valor_ao_ano_ibov = (1 + (media_retorno_acumulado_ibov))**(1/anos) - 1 

    return [valor_ao_ano_vale, valor_ao_ano_petr, valor_ao_ano_fgts, valor_ao_ano_cdi, valor_ao_ano_ipca, valor_ao_ano_ibov]


janela_1_ano_geral = janelas_moveis_retorno_acumulado(df_dados, 250, anos = 1) 
janela_3_anos_geral = janelas_moveis_retorno_acumulado(df_dados, 250 * 3, anos = 3) 
janela_5_anos_geral = janelas_moveis_retorno_acumulado(df_dados, 250 * 5, anos = 5) 
janela_10_anos_geral = janelas_moveis_retorno_acumulado(df_dados, 250 * 10, anos = 10) 


tabela_janelas_moveis = pd.DataFrame(data = {'1 ano': janela_1_ano_geral,
                                            '3 anos': janela_3_anos_geral,
                                            '5 anos': janela_5_anos_geral,
                                            '10 anos': janela_10_anos_geral}, 
                                                index=['VALE3', 'PETR4', 'FGTS', 'CDI', 'IPCA', 'IBOV'])


for coluna in tabela_janelas_moveis.columns:

    tabela_janelas_moveis[f'{coluna}'] = (tabela_janelas_moveis[f'{coluna}'].round(2)) * 100


# ax = sns.heatmap(tabela_janelas_moveis, annot=True, cmap="Greens", fmt = "g")

# plt.title("Mapa de calor do retorno médio (ao ano) de cada ativo")
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)

# for t in ax.texts: 
#     t.set_text(t.get_text() + "%")

# plt.show()

# print(tabela_janelas_moveis)