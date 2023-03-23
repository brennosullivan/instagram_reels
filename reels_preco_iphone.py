from datetime import tzinfo
from timeit import repeat
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import seaborn as sns
import numpy as np
from datetime import date

os.chdir('/home/brenno//Documentos/Instagram/dados')

dados_iphone = pd.read_csv("dados_iphone.csv", index_col="lancamento")

serie_preco_iphone = dados_iphone['quantidade_salario_minimo']

serie_preco_iphone = serie_preco_iphone.str.replace(",", ".")

serie_preco_iphone = serie_preco_iphone.astype(float)

serie_preco_iphone.index = pd.to_datetime(serie_preco_iphone.index)

x_values = []
y_values = []

fig, ax = plt.subplots()
ax.set_xlim(date(2008, 1, 6), date(2022, 1, 10))
ax.set_ylim(3, 15)


#isso aqui aumenta o numero de frames. Basta passa o eixo x, y e o numero de steps que você deseja a mais. Por exemplo, num dataset de 10 itens,
#caso numsteps = 10, o dataset final terá 100 itens
def augment(xold,yold,numsteps):
    xnew = []
    ynew = []
    for i in range(len(xold)-1):
        difX = xold[i+1]-xold[i]
        stepsX = difX/numsteps
        difY = yold[i+1]-yold[i]
        stepsY = difY/numsteps
        for s in range(numsteps):
            xnew = np.append(xnew,xold[i]+s*stepsX)
            ynew = np.append(ynew,yold[i]+s*stepsY)
    return xnew,ynew

novos_dadosx, novos_dadosy =augment(serie_preco_iphone.index, serie_preco_iphone, numsteps=40)

#essa função suaviza o gráfico, deixando as transições mais arredondadas. 

def smoothListGaussian(listin, degree=5):  
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

novo_indice = pd.date_range(start=serie_preco_iphone.index[0], end=serie_preco_iphone.index[-1], periods=len(smoothListGaussian(novos_dadosy)))

serie_preco_iphone = pd.Series(data=smoothListGaussian(novos_dadosy), index=novo_indice)

def animate(i):
    data = serie_preco_iphone.iloc[:int(i+1)]
    data.index = pd.to_datetime(data.index)
    p = sns.lineplot(x=data.index, y=data.values, color="b")
    p.tick_params(labelsize=14)
    plt.setp(p.lines,linewidth=4)

animacao = FuncAnimation(fig=fig, func= animate, frames= range(0, len(serie_preco_iphone)), interval = 50, repeat = False)

plt.show()

#animacao.save("preco_iphone.mp4", codec='mpeg4', fps = 30, bitrate= -1)

