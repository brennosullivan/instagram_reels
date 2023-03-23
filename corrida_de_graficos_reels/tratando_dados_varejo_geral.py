import pandas as pd
import datetime
from conexao_banco import conexao_aws
import os

'''
IDEIAS

Numero de loja das varejistas ao longo do tempo
Maiores lucros líquidos por ano na bolsa
Maiores empresas na bolsa por ano

vAREJO gERAL
Varejo Outros
Varejo Alimentar
Saude/Medicina Diagnóstica
Mercados
Petróleo/Mineração
Financeiro
Educação
Bancos
Alimentos/Ambev
Aluguel de Veículos
Agronegócio

'''
usuario_sql = os.getenv('usuario_sql')
senha_sql = os.getenv('senha_sql')


aws = conexao_aws(senha = senha_sql, usuario=usuario_sql, nome_do_banco='edu_db')
aws.iniciar_conexao()

dados_preco = pd.read_sql('''SELECT * from price WHERE cod in ('LAME4', 'MGLU3', 'LJQQ3', 'VIIA3', 'AMER3')''', 
                            con= aws.conexao)

del dados_preco['id_cot']

dados_preco['date'] = pd.to_datetime(dados_preco['date']).dt.date
dados_preco = dados_preco[(dados_preco['date'] < datetime.date(2022, 1, 1)) & (dados_preco['date'] > datetime.date(2020, 12, 29))]

dados_preco = dados_preco.pivot(index = 'date', columns = 'cod')['value_price']



df_retornos_diarios = dados_preco.pct_change()
df_retornos_diarios = df_retornos_diarios.dropna()

df_final = df_retornos_diarios



tickers = df_final.columns

for coluna in  df_final.columns:


    df_final[f'{coluna}_acum'] = (1 + df_final[f'{coluna}']).cumprod() 
    df_final[f'{coluna}_acum'] = df_final[f'{coluna}_acum'] - 1



df_final = df_final.drop(tickers, axis = 1)

df_final.columns = tickers

df_final.to_csv("dados_varejo_geral.csv")



'''

Para fazer a animação, o dataframe deve estar no modo:

Datas        ATIVO1   ATIVO2  ATIVO3
2021-12-31   Dado       Dado
2021-12-30   Dado
2021-12-29

Assim o pacote consegue ser efetivo. 
'''
