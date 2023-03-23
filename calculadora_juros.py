import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

lista_dfs = []

df = pd.DataFrame()

def calculadora_de_montante_juros_compostos(valor_inicial, taxa, tempo_total_do_investimento, aporte = 0, escala = "M"):

    if escala in ["M", "A", "D"]:
        
        tempo_investido = 0

        lista_dfs.append(pd.DataFrame(data={'Acumulado': 100}, index= [0]))

        vetor_montante_ao_longo_do_tempo = []

        while tempo_investido < tempo_total_do_investimento:

            if tempo_investido == 0:

                valor_final = valor_inicial + ((valor_inicial + aporte) * (taxa/100)) 

                tempo_investido = tempo_investido + 1

                vetor_montante_ao_longo_do_tempo.append(valor_final)

                lista_dfs.append(pd.DataFrame(data={'Acumulado': valor_final}, index= [0]))

            else:

                valor_final = valor_final + (valor_final * (taxa/100)) + aporte

                valor_ganho = (valor_final * (taxa/100)) + aporte

                tempo_investido = tempo_investido + 1

                vetor_montante_ao_longo_do_tempo.append(valor_final)

                lista_dfs.append(pd.DataFrame(data={'Acumulado': valor_final}, index=[0]))

        
        return pd.concat(lista_dfs)

    else:

        return('Escolha uma escala válida')


modelo_ia = calculadora_de_montante_juros_compostos(valor_inicial = 100000, taxa = 0.03, tempo_total_do_investimento = 756, escala = "D")

print(modelo_ia)