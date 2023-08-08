
from datetime import datetime, date
from matplotlib import pyplot as plt
import numpy as np
from  bcb import sgs


def checking_dates_and_frequency():
    
    capital = input(f"Digite o capital investido R$: ")
    frequency = input("Digite a frequência do periodo: ").lower()
    start = input("Digite a data inicial maior do que 1995/01/01 no seguinte formato YYYY/mm/dd: ")
    end = input(f"Digite a data final menor do que {date.today()} no seguinte formato YYYY/mm/dd: ")
    start = datetime.strptime(start, '%Y/%m/%d').date()
    end = datetime.strptime(end, '%Y/%m/%d').date()

    return capital, start, end, frequency

def challenge(selic, capital, start_date, end_date, frequency):
    
    selic_challenge = selic[(selic.index.date >= start_date ) & (selic.index.date < end_date)]
    
    selic_acum_return = (selic_challenge + 1).cumprod() - 1
    selic_acum_return = selic_acum_return.resample(f"{frequency.upper()}").last() 

    selic_acum_return["capital"] = (selic_acum_return["juros"] * float(capital)) + float(capital)
    selic_acum_return["earned"] = selic_acum_return["capital"] - selic_acum_return["capital"].iloc[0]
    selic_acum_return.fillna(0,inplace=True)
    
    print(selic_acum_return)

def question(selic):
    
    initial_date = date(2000,1,1)
    final_date = date(2022,3,31)
    selic_question = selic[(selic.index.date >= initial_date ) & (selic.index.date < final_date)]

    windows = ((1 + selic_question).rolling(window=500).apply(np.prod) - 1)
    windows.plot()
    windows = windows.reset_index()
    windows.columns = ["end_date","returns"]
    windows.insert(0,"init_date",0)
    windows["init_date"] = windows["end_date"].shift(499)
    windows.dropna(inplace=True)
    plt.show()

    id_row = windows["returns"].idxmax()
    row = windows.loc[id_row]
    initial_return_date = row[0]
    final_return_date  = row[1]
    max_return = row[2]
    print(f'''O intervalo de datas de maior retorno foi: 
          {initial_return_date} até {final_return_date} com retorno de {round(max_return,3)*100} %''')
    selic_range = selic_question[(selic_question.index >= initial_return_date) & (selic_question.index <= final_return_date)]
    acum_return_range = (selic_range + 1).cumprod() - 1
    acum_return_range.plot()
    plt.show()
        


capital, start_date, end_date, frequency = checking_dates_and_frequency()

date_min = date(1995,1,1)
selic = sgs.get({"juros":11}, start=date_min)/100

challenge(selic, capital, start_date, end_date, frequency)
question(selic)