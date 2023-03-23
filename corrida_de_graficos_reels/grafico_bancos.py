import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt
import os




plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'Nimbus Sans'
plt.rcParams['font.weight'] = 'bold'

os.chdir('/home/brenno/Documentos/corrida_de_graficos')

df = pd.read_csv('dados_bancos.csv')

df['date'] = pd.to_datetime(df['date'])

df = df.set_index('date')

fig, ax = plt.subplots(figsize=(10.5, 10), dpi=200)

ax.set_xlim([-0.5, 1.85])
ax.set_frame_on(False)

plt.xticks(fontsize = 20)
ax.tick_params(axis='x', which='major', pad=15)


bcr.bar_chart_race(
    df=df,
    filename='bancos_fonte.mp4',
    orientation='h',
    sort='desc',
    n_bars=5,
    fixed_order=True,
    fixed_max=False,
    steps_per_period=10,
    bar_size=.65,
    period_label= {
            'x': .99,
            'y': .1,
            'ha': 'right',
            'va': 'center',
            'size': 22
        },

    period_length=202.7, #acelera o gráfico
    bar_textposition='inside',
    scale='linear',
    writer=None,
    fig=fig,
    period_template='%b/%y',
    bar_kwargs={'alpha': .6, 'capstyle': 'round'},
    #colors = [(0.68, 0.0, 0.74, 0.0), '#00c556', '#b6ffd3', '#dbe2df'],
    bar_label_font={
            'size': 22,
            'color': '#000000',
            
        },
    bar_texttemplate='{x:.0%}',
    tick_template='{x:.0%}',
    tick_label_font={'size': 22},
    
    ) 

