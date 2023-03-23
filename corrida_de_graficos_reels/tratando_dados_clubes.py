import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import bar_chart_race as bcr
import pandas as pd
import matplotlib.pyplot as plt


dados_clubes = pd.read_csv('dados_clubes_br.csv', sep=",")

datas_receitas = [date(2007, 12, 31)]

for i in range(1, 157):

    datas_receitas.append(datas_receitas[0] + relativedelta(months=i))

dados_clubes = dados_clubes.pivot(index = 'data', columns = 'time')['receita']

dados_clubes = dados_clubes.reset_index(drop=False)

dados_clubes = dados_clubes.fillna(0)

dados_clubes_trimestrais = pd.DataFrame(data={'datas': datas_receitas}, index=list(range(0, len(datas_receitas))))

for i, clube in enumerate(dados_clubes.columns):

    if i == 0:
        pass
    else:

        dados_do_time_em_questao = dados_clubes.iloc[:, i]
        
        vetor_receita_mensal = []

        for z in range(1, len(dados_clubes['data'].to_list())):
            
            valor_inicial = dados_do_time_em_questao[z - 1]
            valor_final = dados_do_time_em_questao[z]
            

            diferenca = valor_final - valor_inicial
            valor_a_ser_acrescentado_mensalmente = diferenca/12

            valor_a_ser_anexado = valor_inicial
            
            if z == 1:

                vetor_receita_mensal.append(valor_a_ser_anexado)

            for j in range(1,13):
                
                valor_a_ser_anexado = valor_a_ser_anexado + valor_a_ser_acrescentado_mensalmente
                vetor_receita_mensal.append(valor_a_ser_anexado)

        dados_clubes_trimestrais[f"{clube}"] = vetor_receita_mensal


dados_clubes_trimestrais.columns = dados_clubes_trimestrais.columns.str.strip()

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams['font.sans-serif'] = 'SF Pro Display'
plt.rcParams['font.weight'] = 'light'

df = dados_clubes_trimestrais

df = df.set_index('datas')

fig, ax = plt.subplots(figsize=(15, 10), dpi=200)

#ax.set_xlim([-1, 1.2])

plt.xticks(fontsize = 20)
ax.tick_params(axis='x', which='major', pad=15)


bcr.bar_chart_race(
    df=df,
    filename='video3.mp4',
    img_label_folder="/home/brenno/Documentos/corrida_de_graficos/escudos_clubes",
    fig_kwargs={
        'figsize': (5,5),
        'dpi': 120
    },
    orientation='h',
    sort='desc',
    n_bars=10,
    fixed_order=False,
    fixed_max=False,
    steps_per_period=12, #12
    bar_size=.95,
    period_label= {
            'x': .99,
            'y': .1,
            'ha': 'right',
            'va': 'center',
            'size': 22
        },

    period_length=350, #acelera o gráfico #370
    bar_textposition='inside',
    scale='linear',
    writer=None,
    fig=fig,
    #period_template= '{x:x.format(%b/%y)}',
    bar_kwargs={'alpha': .6, 'capstyle': 'round'},
    #colors = [(0.68, 0.0, 0.74, 0.0), '#00c556', '#b6ffd3', '#dbe2df'],
    bar_label_font={
            'size': 15,
            'color': '#000000',
            
        },
    bar_texttemplate='R${x:.0f} milhões',
    #tick_template='R${x:.2f} milhões',
    tick_label_font={'size': 22},
    
    ) 