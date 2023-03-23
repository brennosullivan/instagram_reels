from dataclasses import replace
from timeit import repeat
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import matplotlib.ticker as mtick
import seaborn as sns
import numpy as np

sns.set(rc={'axes.facecolor':'white', 'figure.facecolor':'white','axes.grid':False})

os.chdir('/home/brenno/Documentos/Instagram/dados')

inflacao_americana = pd.read_csv("CPIAUCSL.csv", index_col="DATE")

taxa_de_juros_americana = pd.read_csv("DFF.csv", index_col="DATE")

taxa_de_juros_americana = taxa_de_juros_americana.squeeze()

taxa_de_juros_americana = taxa_de_juros_americana.str.replace(",", ".")

taxa_de_juros_americana = taxa_de_juros_americana.astype(float)

inflacao_americana = inflacao_americana.squeeze()

inflacao_americana = inflacao_americana.str.replace(",", ".")

inflacao_americana = inflacao_americana.astype(float)

inflacao_americana.index = pd.to_datetime(inflacao_americana.index)

taxa_de_juros_americana.index = pd.to_datetime(taxa_de_juros_americana.index)

inflacao_americana = inflacao_americana.resample("1Q").last()
taxa_de_juros_americana = taxa_de_juros_americana.resample("1Q").last()

inflacao_americana = inflacao_americana[inflacao_americana.index > "1960-12-31"]
taxa_de_juros_americana = taxa_de_juros_americana[taxa_de_juros_americana.index > "1960-12-31"]

var_inflacao_americana = (inflacao_americana.pct_change(periods=4)) * 100
var_inflacao_americana = var_inflacao_americana.dropna()

juro_real = taxa_de_juros_americana - var_inflacao_americana
juro_real = juro_real.dropna()
juro_real = juro_real.astype(float)

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

novo_indice = pd.date_range(start=juro_real.index[0], end=juro_real.index[-1], periods=len(smoothListGaussian(juro_real)))



juro_real = pd.Series(data=smoothListGaussian(juro_real), index=novo_indice)


x_values = []
y_values = []

fig, ax = plt.subplots()
ax.set_xlim(juro_real.index[0], juro_real.index[-1])
ax.set_ylim(-10, 15)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
line, = ax.plot(0, 0)
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'Nimbus Sans'
plt.rcParams['font.weight'] = 'bold'





def animate(i):
    data = juro_real.iloc[:int(i+1)] #select data range
    p = sns.lineplot(x=data.index, y=data.values, data=data, color="b")
    p.tick_params(labelsize=14)
    plt.setp(p.lines,linewidth=2)



animacao = FuncAnimation(fig=fig, func= animate, frames= range(0, len(juro_real)), interval = 50, repeat = False)

# Writer = animation.writers['ffmpeg']
# writer = Writer(fps=60, bitrate=-1)

animacao.save("juro_real_americano.mp4", codec='mpeg4', fps = 30, bitrate= -1)

