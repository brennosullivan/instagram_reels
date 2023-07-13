import pandas as pd
import yfinance as yf
import mplcyberpunk
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None 
import matplotlib.ticker as tick
import numpy as np


dados_ibov = yf.download("^BVSP", start="1994-06-15")

dinheiro_inicial = 1000000
aporte = dinheiro_inicial/23

retorno_2_y_ibov = dados_ibov['Adj Close'].pct_change(periods = 503).dropna()

retorno_2_y_ibov = (1 + retorno_2_y_ibov) * dinheiro_inicial

retorno_2_y_ibov = retorno_2_y_ibov.to_frame()

retorno_2_y_ibov.columns = ['de_uma_vez']

retorno_2_y_ibov['aos_poucos'] = pd.NA

tamanho = range(504, len(dados_ibov))

for i in tamanho:

    dados_pontuais = dados_ibov.iloc[(i - 504): i, ]
    dados_pontuais['numero_dias'] = list(range(1, 505))
    dados_pontuais['retorno_21'] = dados_pontuais['Adj Close'].pct_change(periods = 20)
    dados_pontuais = dados_pontuais[dados_pontuais['numero_dias'].isin(list(range(21, 505, 21)))]
    
    dados_pontuais['dinheiro'] = pd.NA
    dinheiro_inicial = 0
    z = 0

    for dia in dados_pontuais.index:

        if dia != dados_pontuais.index[-1]:

            dinheiro = dinheiro_inicial * (1 + dados_pontuais.loc[dia, 'retorno_21']) + aporte
            z = z + 1
            #print(f'aportou {z} vezes')

        else:

            dinheiro = dinheiro_inicial * (1 + dados_pontuais.loc[dia, 'retorno_21'])

        dados_pontuais.loc[dia, 'dinheiro'] = dinheiro
        dinheiro_inicial = dinheiro

    retorno_2_y_ibov.loc[dados_pontuais.index[-1], 'aos_poucos'] = dados_pontuais['dinheiro'].iloc[-1]


retorno_2_y_ibov = retorno_2_y_ibov.dropna()

retorno_2_y_ibov['overperform'] = retorno_2_y_ibov['de_uma_vez'] - retorno_2_y_ibov['aos_poucos']





def smoothListGaussian(listin, degree=200):  
    window=degree*2-1  
    weight=np.array([1.0]*window)  
    weightGauss=[] 
    for i in range(window):  
        i=i-degree+1  
        frac=i/float(window)  
        gauss=1/(np.exp((4*(frac))**2))  
        weightGauss.append(gauss)
    weight=np.array(weightGauss)*weight  
    smoothed=[0.0]*(len(listin)-window)  
    for i in range(len(smoothed)):        
        smoothed[i]=sum(np.array(listin[i:i+window])*weight)/sum(weight)  
    return smoothed

novo_indice = pd.date_range(start=retorno_2_y_ibov.index[0], end=retorno_2_y_ibov.index[-1], periods=len(smoothListGaussian(retorno_2_y_ibov['overperform'].values)))

retorno_2_y_ibov = pd.DataFrame(data={"overperform": smoothListGaussian(retorno_2_y_ibov['overperform'].values)},
                                       index=novo_indice)


print(sum(retorno_2_y_ibov['overperform'] > 0)/len(retorno_2_y_ibov['overperform']))
print(max(retorno_2_y_ibov['overperform']))

retorno_2_y_ibov = retorno_2_y_ibov.astype(int)

print(retorno_2_y_ibov)

plt.style.use('cyberpunk')

fig, ax = plt.subplots()

ax.grid(False)

ax.ticklabel_format(style='plain')

ax.plot(retorno_2_y_ibov.index, retorno_2_y_ibov['overperform'].values)
# ax.plot(retorno_2_y_ibov.index, retorno_2_y_ibov['aos_poucos'], label = "Aos poucos")

#ax.yaxis.set_major_formatter(tick.FuncFormatter('R${x:1.0f}'))
# ax.get_yaxis().set_major_formatter(
#    tick.FuncFormatter(lambda x, p: "R$" + format(int(x), '{x:,.0f}')))
ax.yaxis.set_major_formatter(tick.StrMethodFormatter('R${x:,.0f}'))

plt.axhline(y=0, color = 'w')

plt.title("Investir de uma vez MENOS Investir aos poucos em perídos de 2 anos no ibovespa")

plt.show()



