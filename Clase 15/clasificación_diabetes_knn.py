#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 11:00:22 2025

@author: mcerdeiro
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
#%% cargar datos de diabetes
df_diabetes = pd.read_csv('diabetes.csv')
df_diabetes.columns
#%% X atributos, y etiqueta
X = df_diabetes[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
y = df_diabetes['Outcome']
#%% para usar solo 2 atributos
X2 = df_diabetes[['Glucose', 'BMI']].values
y = df_diabetes['Outcome'].values
#%% gráfico de dispersión
plt.figure(figsize=(6, 4))
plt.scatter(X2[:, 0], X2[:, 1], c=y)
plt.xlabel('Glucose')
plt.ylabel('BMI')
plt.title('Distribución de los datos: Glucose vs BMI')
plt.show()
#%% construyo y ajusto el clasificador
clasificador = KNeighborsClassifier(n_neighbors=10)
clasificador.fit(X2, y)
#%% predicción para un nuevo paciente
nuevo_paciente = [[130, 32.0]] 
prediccion = clasificador.predict(nuevo_paciente)
print("Predicción para el nuevo paciente:", "Diabetes" if prediccion[0] == 1 else "No diabetes")
#%%








