"""Trabajo practico 1 - Manejo de Datos y visualizacion"""

import pandas as pd
import duckdb as dd

## Cargamos todos los Datasets para Limpiarlos

establecimientos_educativos = pd.read_excel('2022_padron_oficial_establecimientos_educativos.xlsx',skiprows=6)
actividades_establecimientos= pd.read_csv('actividades_establecimientos.csv')
datos_por_departamento = pd.read_csv('Datos_por_departamento_actividad_y_sexo.csv')
padron = pd.read_excel('padron_poblacion.xlsX',skiprows= 12)

padron.head()

padron = padron.iloc[:, [1, 2]]
columna2 = padron.iloc[:, 1]
columna1 = padron.iloc[:, 0]

departamentos = []
id_departamentos = []
departamento = None
id_departamento = None

for valor in columna2:  # segunda columna
   if isinstance(valor, str) and valor!= 'Casos':
       departamentos.append(None)
       departamento = valor
   else:
       departamentos.append(departamento)
        
       
                  
padron['Departamento'] = departamentos


for valor in columna1:  # segunda columna
   if isinstance(valor, str) and valor!= 'Edad':
       id_departamentos.append(None)
       if valor[8:9]== '0':
           id_departamento = valor[7:]
       else:
           id_departamento = valor[8:]
       
   else:
       id_departamentos.append(id_departamento)


padron['id_departamento']= id_departamentos

padron = padron.dropna().drop(2).reset_index(drop=True)

padron.columns = ['Edad','Casos','Departamento','Id_departamento']



# Mostramos las primeras filas
print(padron.head())




 
