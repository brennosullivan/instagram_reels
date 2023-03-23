import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas_datareader import data as pdr

data_final = dt.datetime.now()
data_inicial = data_final - dt.timedelta(days=300)

#pegando dados
ibovespa_precos = pdr.get_data_yahoo("^BVSP", data_inicial, data_final)['Adj Close']

#extraindo vetor de retornos dos últimos 300 dias
retornos_ibov = ibovespa_precos.pct_change().dropna().to_numpy()

#vamos simular 3 anos para frente, considerando o ano com 252 dias úteis. 

num_dias = 3 * 252
numero_simulacoes = 10000
dinheiro_inicial = 1000
lista_montante_final = np.array([])

for n in range(numero_simulacoes):

    retorno_simulado = np.random.choice(retornos_ibov, 
                                        size = num_dias, replace = True)

    resultado_acumulado = dinheiro_inicial * (retorno_simulado + 1).cumprod()

    montante_final = resultado_acumulado[-1]
    lista_montante_final = np.append(lista_montante_final, montante_final)

montante_99 = "R$ " + str(np.percentile(lista_montante_final, 1))
montante_95 = "R$ " + str(np.percentile(lista_montante_final, 5))
montante_mediano = "R$ " + str(np.percentile(lista_montante_final, 50))
cenarios_com_lucro = str((len(lista_montante_final[lista_montante_final > 1000])/
                                len(lista_montante_final)) * 100) + "%"


 
print(montante_99)
print(montante_95)
print(montante_mediano)
print(cenarios_com_lucro)


config = dict(histtype = "stepfilled", alpha = 0.8, density = False, bins = 150)
fig, ax = plt.subplots()
ax.hist(lista_montante_final, **config)
ax.xaxis.set_major_formatter('R${x:.0f}')
plt.title('Distribuição montantes finais com simulação MC')
plt.xlabel('Montante final (R$)')
plt.ylabel("Frequência")
plt.show()







