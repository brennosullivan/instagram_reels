import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import seaborn as sns
from datetime import date
import matplotlib.dates as mdate


os.chdir('/home/brenno/Documentos/Instagram/dados')


dados_gasosa_ate_2012 = pd.read_excel("gasolina_ate_2012.xlsx")
dados_gasosa_pos_2012 = pd.read_excel("gasolina_pos_2012.xlsx", skiprows= 16)

dados_gasosa_ate_2012 = dados_gasosa_ate_2012[["DATA FINAL", 'PRODUTO', 'PREÇO MÉDIO REVENDA']]
dados_gasosa_ate_2012 = dados_gasosa_ate_2012[dados_gasosa_ate_2012['PRODUTO'] == "GASOLINA COMUM"]
dados_gasosa_ate_2012 = dados_gasosa_ate_2012.set_index("DATA FINAL")
dados_gasosa_ate_2012 = dados_gasosa_ate_2012.resample("M").last()


dados_gasosa_pos_2012 = dados_gasosa_pos_2012[["MÊS", 'PRODUTO', 'PREÇO MÉDIO REVENDA']]
dados_gasosa_pos_2012 = dados_gasosa_pos_2012[dados_gasosa_pos_2012['PRODUTO'] == "GASOLINA COMUM"]
dados_gasosa_pos_2012 = dados_gasosa_pos_2012.set_index("MÊS")

dados_gasolina = pd.concat([dados_gasosa_ate_2012, dados_gasosa_pos_2012])

dados_gasolina = dados_gasolina['PREÇO MÉDIO REVENDA']


x_values = []
y_values = []

fig, ax = plt.subplots()
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'Nimbus Sans'
plt.rcParams['font.weight'] = 'bold'
ax.set_xlim(date(2004, 1, 1), date(2023, 12, 31))
ax.set_ylim(1, 8)
ax.yaxis.set_major_formatter('R${x:1.2f}')



ax.xaxis.set_major_locator(mdate.YearLocator(3))


def animate(i):
    data = dados_gasolina.iloc[:int(i+1)] #select data range
    p = sns.lineplot(data.index, data.values, color = "b", ls='-', ms=4)
   


animacao = FuncAnimation(fig=fig, func = animate, frames= range(0, len(dados_gasolina)), interval = 50, repeat = False)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=60, bitrate=-1)

plt.show()
















