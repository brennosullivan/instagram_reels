import pandas as pd
import yfinance as yf

dados = yf.download('PETR4.SA', start = "2020-12-31")

dados['retornos'] = dados['Adj Close'].pct_change()
dados = dados.dropna()

quantidade_de_dias = len(dados)

retornos_ordenados = dados['retornos'].sort_values(ascending=True).to_list()

var_95 = retornos_ordenados[(int(quantidade_de_dias*0.05))]

print(f"Em 95% dos dias a PETR4 caiu menos do que {round(var_95 * 100, 2)}%")