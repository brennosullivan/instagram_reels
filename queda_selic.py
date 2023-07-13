from bcb import sgs
from datetime import timedelta
import yfinance as yf
import mplcyberpunk
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.ticker as mtick

selic = sgs.get({'selic':432})

selic['cortes'] = (selic['selic'] < selic['selic'].shift(1))

dias = selic[selic['cortes']].index
dias_finais = dias + timedelta(days=365)

ibov = yf.download('^BVSP')['Adj Close']

retornos= pd.DataFrame(columns=['dia', 'retorno'])


for i, data in enumerate(dias):

    ibov_365 = ibov[(ibov.index > data) & (ibov.index < dias_finais[i])]
    retorno = ibov_365.iloc[-1]/ibov_365.iloc[0] - 1
    retornos = pd.concat([retornos, pd.DataFrame({'dia': data, 'retorno': retorno}, index = [0])], ignore_index=True)


retornos['dia']=retornos['dia'].dt.strftime('%b-%y')
retornos = retornos.sort_values('retorno')
retornos['dia'] = retornos['dia'].astype(str)

print(sum(retornos['retorno'] > 0))
print((retornos[retornos['retorno'] > 0]['retorno']).mean())
    
plt.style.use('cyberpunk')

fig, ax = plt.subplots(figsize = (12, 8))

colormat= np.where(retornos['retorno'] > 0, '#08F7FE','#FE53BB')
ax.grid(False)
ax.bar(retornos.dia.values, retornos.retorno.values, color = colormat)
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1))
ax.set_xticks([])
plt.yticks(fontsize=20)
plt.title("Rentabilidade IBOV 12 meses após corte de juros", fontsize = 20)

plt.savefig("corte_selic")

plt.show()





