import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt




plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'SF Pro Display'
plt.rcParams['font.weight'] = 'light'

df = pd.read_csv('dados_clubes_br_tratados.csv')


df = df.set_index('datas')

print(df)

fig, ax = plt.subplots(figsize=(12, 10), dpi=200)

#ax.set_xlim([-1, 1.2])

plt.xticks(fontsize = 15)
#ax.tick_params(axis='x', which='major', pad=15)


bcr.bar_chart_race(
    df=df,
    filename='video3.mp4',
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=12,
    bar_size=.95,
    period_label= {
            'x': .99,
            'y': .1,
            'ha': 'right',
            'va': 'center',
            'size': 22
        },

    period_length=380, #acelera o gráfico
    bar_textposition='inside',
    scale='linear',
    writer=None,
    fig=fig,
    #period_template= "%b/%Y",
    bar_kwargs={'alpha': .6, 'capstyle': 'round'},
    #colors = [(0.68, 0.0, 0.74, 0.0), '#00c556', '#b6ffd3', '#dbe2df'],
    bar_label_font={
            'size': 22,
            'color': '#000000',
            
        },
    #bar_texttemplate='{x:.0%}',
    #tick_template='{x:.0%}',
    tick_label_font={'size': 22},
    
    ) 

