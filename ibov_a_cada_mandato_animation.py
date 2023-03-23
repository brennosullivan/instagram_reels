import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np
from datetime import date
import matplotlib.dates as mdate
import mplcyberpunk
import yfinance as yf


plt.style.use("cyberpunk")

sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white','axes.grid':False})

os.chdir('/home/brenno/Documentos/Instagram/dados')

dados_ibov = pd.read_csv("dados_ibovespa.csv")

dados_ibov = dados_ibov.drop("cod", axis = 1)

dados_ibov['date'] = pd.to_datetime(dados_ibov['date'])

dados_ibov = dados_ibov.set_index("date")

dados_ibov = dados_ibov['value_price']

dados_ibov_att = yf.download("^BVSP", "2022-08-24", "2023-03-20")['Adj Close']

dados_ibov = dados_ibov.append(dados_ibov_att)

dados_ibov = dados_ibov.to_frame()

dados_ibov.columns = ['value_price']

dados_ibov = dados_ibov.resample("M").last()

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

novo_indice = pd.date_range(start=dados_ibov.index[0], end=dados_ibov.index[-1], periods=len(smoothListGaussian(dados_ibov)))
dados_ibov = pd.Series(data=smoothListGaussian(dados_ibov['value_price']), index=novo_indice)



x_values = []
y_values = []

fig, ax = plt.subplots()
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'Nimbus Sans'
plt.rcParams['font.weight'] = 'bold'
ax.set_xlim(date(1994, 1, 1), date(2023, 12, 31))
ax.set_ylim(3000, 130000)

plt.show()

ax.xaxis.set_major_locator(mdate.YearLocator(3))
#marker = [46, 93, 140, 186, 233, 268]


def animate(i):
    data = dados_ibov.iloc[:int(i+1)] #select data range
    p = ax.plot(data.index, data.values, color = "b", ls='-')
   


animacao = FuncAnimation(fig=fig, func = animate, frames= range(0, len(dados_ibov)), interval = 50, repeat = False)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, bitrate=-1)

plt.show()

# # animacao.save("juro_real_americano.mp4", codec='mpeg4', fps = 30, bitrate= -1)
