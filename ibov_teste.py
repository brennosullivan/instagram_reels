import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mplcyberpunk

# Obtendo os dados do Ibovespa do Yahoo Finance
ibov = yf.download('^BVSP', start='1996-01-01', period="1m")['Adj Close']

ibov = ibov.resample("M").last()

# Extraindo as datas e valores da série histórica da Taxa Selic Mensal
dates = ibov.index
values = ibov.values

# Suavizando a série histórica da Taxa Selic Mensal utilizando uma média móvel
def smooth(data, window_size):
    smoothed_data = []
    for i in range(len(data)):
        if i < window_size:
            smoothed_data.append(sum(data[:i+1]) / (i+1))
        else:
            smoothed_data.append(sum(data[i-window_size+1:i+1]) / window_size)
    return smoothed_data

#smoothed_values = smooth(values, 12)

# Função para atualizar o gráfico a cada quadro
def update(frame):
    ax.clear()
    ax.plot(dates[:frame], values[:frame], linewidth=2)
    ax.set_xlabel('Data')
    ax.set_ylabel('Índice Ibovespa')
    ax.set_title('Índice Ibovespa ao longo do tempo')
    ax.set_xlim(dates[0], dates[-1])  # Define os limites do eixo x
    ax.set_ylim(0, max(values) + 10000)  # Define os limites do eixo y

# Configurando o gráfico inicial
fig, ax = plt.subplots()
ax.set_xticks(dates)
ax.tick_params(axis='both', which='both', length=0)

line, = ax.plot([], [], linewidth=2)



# Criando a animação
ani = animation.FuncAnimation(fig=fig, func=update, frames=len(dates), interval=12, repeat=False)

#plt.show()

# Salvando a animação em um arquivo MP4
Writer = animation.writers['ffmpeg']
writer = Writer(fps=9, metadata=dict(artist='Me'), bitrate=1800, codec='mpeg4')
ani.save('ibov.mp4', writer=writer)