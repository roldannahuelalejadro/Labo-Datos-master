#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 12:15:53 2025

@author: mcerdeiro
"""

import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
#%%
df_mpg = pd.read_csv("auto-mpg.xls")

X = df_mpg[['weight', 'displacement', 'acceleration']]
y = df_mpg['mpg']

# división en train y test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=12)
#%%

valores_k = [1, 3, 5, 10, 20, 30]

resultados = []

for k in valores_k:
    modelo = KNeighborsRegressor(n_neighbors=k)
    modelo.fit(X_train, y_train)

    y_pred_train = modelo.predict(X_train)
    y_pred_test = modelo.predict(X_test)

    resultados.append({
        'k': k,
        'Train_RMSE': np.sqrt(mean_squared_error(y_train, y_pred_train)),
        'Test_RMSE': np.sqrt(mean_squared_error(y_test, y_pred_test)),
        'Train_MAE': mean_absolute_error(y_train, y_pred_train),
        'Test_MAE': mean_absolute_error(y_test, y_pred_test),
    })

# Mostrar resultados
df_resultados = pd.DataFrame(resultados)
print(df_resultados)
#%%

plt.figure(figsize=(8, 5))
plt.plot(valores_k, df_resultados['Train_RMSE'], marker='o', label='Train')
plt.plot(valores_k, df_resultados['Test_RMSE'], marker='o', label='Test')

plt.xlabel('Número de vecinos (k)')
plt.ylabel('RMSE')
plt.title('Error cuadrático medio (RMSE) según k en KNN')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
