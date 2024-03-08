import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as mtick
import mplcyberpunk

plt.style.use('cyberpunk')

gta = {
    'GTA (1997)': {'Custo': '1.5 M', 'Lucro': '100 M'},
    'GTA 2 (1999)': {'Custo': '3.5 M', 'Lucro': '150 M'},
    'GTA 3 (2001)': {'Custo': '5 M', 'Lucro': '300 M'},
    'GTA: Vice City (2022)': {'Custo': '5 M', 'Lucro': '300 M'},
    'GTA: San Andreas (2004)': {'Custo': '10 M', 'Lucro': '750 M'},
    'GTA 4 (2008)': {'Custo': '100 M', 'Lucro': '1500 MM'},
    'GTA 5 (2013)': {'Custo': '250 M', 'Lucro': '7500 MM'},
}

for jogo, valores in gta.items():
    valores['Custo'] = float(valores['Custo'].replace('M', '')) if 'M' in valores['Custo'] else float(valores['Custo'].replace('MM', '')) * 1000
    valores['Lucro'] = float(valores['Lucro'].replace('M', '')) if 'M' in valores['Lucro'] else float(valores['Lucro'].replace('MM', '')) * 1000

df = pd.DataFrame(gta)

jogos = list(gta.keys())
custos = [valores['Custo'] for valores in gta.values()]
lucros = [valores['Lucro'] for valores in gta.values()]

fig, ax = plt.subplots(figsize=(12, 6))
ax.set_xlim(-0.5, len(df.columns) - 0.5)  # Ajustando os limites do eixo X
ax.set_ylim(-50, df.max().max() + 100)

colors = ['red', 'green']

lines = [plt.plot([], [], marker='o')[0] for i in range(len(df))]

def init():
    for line in lines:
        line.set_data([], [])
    return lines

def animate(i):
    for idx, line in enumerate(lines):
        line.set_data(list(range(i + 1)), df.iloc[idx, :i + 1])
    return lines

ani = FuncAnimation(fig, animate, init_func=init, frames=len(df.columns), interval=500, blit=True, repeat=False)
plt.ylabel('Valor (em milhões)')
plt.title('Evolução de Custo e Lucro ao longo dos Jogos GTA')

plt.xticks(range(len(jogos)), jogos, rotation=45, ha='right')

mplcyberpunk.add_glow_effects()
plt.tight_layout()
plt.show()