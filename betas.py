import pandas as pd
from datetime import date
import yfinance as yf
from datetime import timedelta
from sklearn.linear_model import LinearRegression
import numpy as np



mes = "02"
ano = "23"
dia = "22"

ibovespa_comp = pd.read_csv(f"/home/brenno/Downloads/IBOVDia_{dia}-{mes}-{ano}.csv", sep = ";", 
                            skipfooter = 2, encoding = 'ISO-8859-1', engine = 'python', decimal = ',',
                           thousands = ".", header = 1, index_col = False)

lista_acoes = ibovespa_comp['Código'].to_list()

lista_acoes_yahoo_finance = [x + ".SA" for x in lista_acoes]

dez_anos_atras = date.today() - timedelta(days = 3650)
cinco_anos_atras = date.today() - timedelta(days = 1825)
tres_anos_atras = date.today() - timedelta(days = 1095)
um_ano_atras = date.today() - timedelta(days = 365)

lista_acoes_yahoo_finance.append('^BVSP')

cotacoes_ajustadas = yf.download(lista_acoes_yahoo_finance, start = dez_anos_atras)['Adj Close']

cotacoes_ajustadas.index = pd.to_datetime(cotacoes_ajustadas.index)

betas = ['1 ano', '3 anos', '5 anos', '10 anos']
datas = [um_ano_atras, tres_anos_atras, cinco_anos_atras, dez_anos_atras]

lista_dfs = []

for i, periodo_beta in enumerate(betas):

    cotacoes_no_periodo = cotacoes_ajustadas[cotacoes_ajustadas.index > pd.to_datetime(datas[i])]

    for acao in cotacoes_ajustadas.columns:

        if acao != "^BVSP":

            if pd.isna(cotacoes_no_periodo[acao].iloc[0]) == False:

                cotacoes_acao_e_ibov = cotacoes_no_periodo[[acao, '^BVSP']].dropna()
                retornos_acao_e_ibov = cotacoes_acao_e_ibov.pct_change().dropna()

                retornos_ibovespa_no_periodo = np.array(retornos_acao_e_ibov['^BVSP']).reshape(-1, 1)
                retornos_ativo_no_periodo = np.array(retornos_acao_e_ibov[acao]).reshape(-1, 1)

                linear_regressor = LinearRegression()
                reg = linear_regressor.fit(retornos_ibovespa_no_periodo, retornos_ativo_no_periodo)
                beta_ativo = reg.coef_[0][0]
                r_quadrado = linear_regressor.score(retornos_ibovespa_no_periodo, retornos_ativo_no_periodo)
                df_beta = pd.DataFrame({

                    'empresa':  acao,
                    'value_rquadrado': r_quadrado,
                    "value_beta": beta_ativo,
                    'periodo_beta': periodo_beta,
                    }, index=[0])

                lista_dfs.append(df_beta)


betas_empresas_ibov = pd.concat(lista_dfs)

betas_empresas_ibov.to_excel("betas_empresa_ibov.xlsx")

print(betas_empresas_ibov)
















