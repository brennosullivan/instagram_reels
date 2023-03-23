import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import numpy as np
from datetime import date
import matplotlib.dates as mdate
import mplcyberpunk

os.chdir('/home/brenno/Documentos/Instagram/dados')

dados_di = pd.read_csv("dados_di.csv", index_col='indice')

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

# novo_indice = pd.date_range(start=dados_di.index[0], end=dados_di.index[-1], periods=len(smoothListGaussian(dados_di)))
# dados_di = pd.Series(data=smoothListGaussian(dados_di['value_price']), index=novo_indice)



x_values = []
y_values = []

fig, ax = plt.subplots()
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'Nimbus Sans'
plt.rcParams['font.weight'] = 'bold'
ax.set_xlim(date(2022, 12, 31), date(2034, 12, 31))
ax.set_ylim(6, 15)
plt.style.use("cyberpunk")

ax.xaxis.set_major_locator(mdate.YearLocator(3))
print(dados_di)

def animate(i):
    data = dados_di.iloc[ : , (i - 1)] #select data range
    p = ax.plot(data.index, data.values, color = "#00FFFF")



animacao = FuncAnimation(fig=fig, func = animate, frames= range(0, 28), interval = 50, repeat = False)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, bitrate=-1)

plt.show()
