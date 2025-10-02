import pandas as pd
import duckdb as dd
import sys
import os

carpeta = "TablasOriginales"

padron_poblacion =  pd.read_excel(carpeta + "/padron_poblacion.xlsX")

padron_poblacion.columns = ['nada', 'edad', 'casos', 'porcentaje', 'porcentaje_acumulado']
padron_poblacion.columns


edad_index = []
total_index = []
areas = []
counter = 0
counter_total = 0
for i in range(len(padron_poblacion['edad'].tolist())):
    if padron_poblacion['edad'].tolist()[i] == 'Edad':
        counter += 1
        edad_index.append(i+1)
        areas.append(padron_poblacion['casos'].tolist()[i-2])
    

for i in range(len(padron_poblacion['edad'].tolist())):
    if padron_poblacion['edad'].tolist()[i] == 'Total':
        total_index.append(i)
        counter_total += 1

if  counter != counter_total:
    print("Error: Tamaños de indexacion diferentes")
    sys.exit()


df_list = []
for index in range(counter-1):
    edad = padron_poblacion['edad'][edad_index[index]: total_index[index]].tolist()
    casos = padron_poblacion['casos'][edad_index[index]: total_index[index]].tolist()
    porcentaje = padron_poblacion['porcentaje'][edad_index[index]: total_index[index]].tolist()
    porcentaje_acumulado = padron_poblacion['porcentaje_acumulado'][edad_index[index]: total_index[index]].tolist()
    
    data = {
        'edad': edad,
        'casos': casos,
        'porcentaje': porcentaje,
        'porcentaje_acumulado': porcentaje_acumulado
    }

    df_ = pd.DataFrame(data)

    ruta_subcarpeta = os.path.join('TablasModificadas', 'Padrones')

    os.makedirs(ruta_subcarpeta, exist_ok=True)

    ruta_archivo = os.path.join(ruta_subcarpeta, f'padron_poblacion_{areas[index]}.csv')
    df_.to_csv(ruta_archivo, index=False)
    
    df_list.append(df_)