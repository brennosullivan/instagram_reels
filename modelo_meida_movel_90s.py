import pandas as pd
import numpy as np
from matplotlib.pyplot import show
import vectorbt as vbt


start = '2010-01-01 UTC-3'  
end = '2022-03-10 UTC-3'
dados_ibovespa = vbt.YFData.download('BOVA11.SA', start=start, end=end).get('Close')


media_movel_rapida = vbt.MA.run(dados_ibovespa, 10, short_name='fast')
media_movel_devagar = vbt.MA.run(dados_ibovespa, 50, short_name='slow')


entradas = media_movel_rapida.ma_crossed_above(media_movel_devagar) 
saidas = media_movel_rapida.ma_crossed_below(media_movel_devagar)


resultado = vbt.Portfolio.from_signals(dados_ibovespa, entries=entradas, exits=saidas, 
                                       short_entries = saidas, short_exits = entradas, 
                                       fees=0.005, freq = 'd') 


resultado.plot().show()

fig = dados_ibovespa.vbt.plot(trace_kwargs=dict(name='Close'))
media_movel_rapida.ma.vbt.plot(trace_kwargs=dict(name='Fast MA'), fig=fig)
media_movel_devagar.ma.vbt.plot(trace_kwargs=dict(name='Slow MA'), fig=fig)
resultado.positions.plot(close_trace_kwargs=dict(visible=False), fig=fig)

fig.show()
