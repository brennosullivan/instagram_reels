import pandas as pd
import os
import requests
import json


os.chdir('/home/brenno/Documentos/Instagram/dados')

senha_comdinheiro = os.getenv('senha_comdinheiro')

url = "https://www.comdinheiro.com.br/Clientes/API/EndPoint001.php"

querystring = {"code":"import_data"}

payload = f"username=edufinance_&password={senha_comdinheiro}&URL=HistoricoCotacao002.php%3F%26x%3DIBOV%2BPTAXV%26data_ini%3D20121994%26data_fim%3D31129999%26pagina%3D1%26d%3DMOEDA_ORIGINAL%26g%3D0%26m%3D0%26info_desejada%3Dpreco%26retorno%3Ddiscreto%26tipo_data%3Ddu_br%26tipo_ajuste%3Dtodosajustes%26num_casas%3D2%26enviar_email%3D0%26ordem_legenda%3D1%26cabecalho_excel%3Dmodo1%26classes_ativos%3D9ur54ut49vj%26ordem_data%3D0%26rent_acum%3Drent_acum%26minY%3D%26maxY%3D%26deltaY%3D%26preco_nd_ant%3D0%26base_num_indice%3D100%26flag_num_indice%3D0%26eixo_x%3DData%26startX%3D0%26max_list_size%3D20%26line_width%3D2%26titulo_grafico%3D%26legenda_eixoy%3D%26tipo_grafico%3Dline%26script%3D&format=json2"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

json_resposta = json.loads(response.text)


lista_info_historica = []

for cotacao in json_resposta['resposta']['tab-p1']['linha']:

    lista_info_historica.append(pd.DataFrame(data = cotacao, index=[0]))


df_indices_historicos = pd.concat(lista_info_historica, ignore_index=True)
df_indices_historicos = pd.melt(df_indices_historicos, id_vars='data', var_name='cod', value_name='value_price')
df_indices_historicos =  df_indices_historicos[df_indices_historicos['value_price'] != "nd"]
df_indices_historicos = df_indices_historicos.dropna()

df_indices_historicos['value_price'] = list(map(lambda x: x.replace(",", "."), df_indices_historicos['value_price']))

df_indices_historicos['value_price'] = df_indices_historicos['value_price'].astype(float).round(2)


df_indices_historicos['data'] = pd.to_datetime(df_indices_historicos['data'], format= '%d/%m/%Y')
df_indices_historicos = df_indices_historicos.rename(columns={'data': 'date'})

df_ibov = df_indices_historicos[df_indices_historicos['cod'] == "ibov"]
df_dolar = df_indices_historicos[df_indices_historicos['cod'] == "ptaxv"]

print(df_dolar)

df_ibov = df_ibov.set_index("date")
df_dolar = df_dolar.set_index("date")

df_ibov.to_csv("dados_ibovespa.csv")
df_dolar.to_csv("dados_dolar.csv")
