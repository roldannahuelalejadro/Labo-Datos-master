#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 15:07:27 2025

@author: mcerdeiro
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import r2_score

#%% roundup

df_ru = pd.read_csv("datos_roundup.txt", sep=' ')

plt.scatter(df_ru['RU'], df_ru['ID'])

# Y = a + b*X
X = np.linspace(min(df_ru['RU']), max(df_ru['RU']))
a = 100 ### probar con otros valores
b = 0.06 ### probar con otros valores
Y = a + b*X

plt.plot(X, Y,  'r')
plt.show()
#%% coeficientes a partir de la fórmula vista en clase

xbar = np.mean(X)
ybar = np.mean(Y)
b1 = sum((X-xbar)*(Y-ybar))/sum((X-xbar)*(X-xbar))
b0 = ybar - b1*xbar

#%%
plt.scatter(df_ru['RU'], df_ru['ID'])
X = np.linspace(min(df_ru['RU']), max(df_ru['RU']))
Y = b0 + b1*X

plt.plot(X, Y,  'r')
plt.show()
#%% coeficientes utilizando sklearn

modelo_lineal = LinearRegression()
modelo_lineal.fit(df_ru[['RU']],df_ru['ID'])
modelo_lineal.intercept_
modelo_lineal.coef_
modelo_lineal.score(df_ru[['RU']],df_ru['ID']) ## es el r2
#%%

Y = modelo_lineal.intercept_ + modelo_lineal.coef_*X

plt.scatter(df_ru['RU'], df_ru['ID'])
plt.plot(X, Y, 'black')

plt.show()

#%%
# Y_pred son los valores que toma la recta sobre los valores RU de la muestra
Y_pred =modelo_lineal.intercept_ + modelo_lineal.coef_*df_ru['RU']

r2 = r2_score(df_ru['ID'], Y_pred)
print("R²: " + str(r2))


#%% Anascombe

df = sns.load_dataset("anscombe")

sns.lmplot(
    data=df, x="x", y="y", col="dataset", hue="dataset",
    col_wrap=2, palette="muted", ci=None,
    height=4, scatter_kws={"s": 50, "alpha": 1}
)
#%% primer dataset de anscombe

df1 = df[df['dataset'] == "I"]
df1
X1 = df1['x']
Y1 = df1['y']

xbar = np.mean(X1)
ybar = np.mean(Y1)
b1 = sum((X1-xbar)*(Y1-ybar))/sum((X1-xbar)*(X1-xbar))
b0 = ybar - b1*xbar

#%%
X = np.linspace(min(df1['x']), max(df1['x']))
Y = b0 + b1*X

plt.scatter(df1['x'], df1['y'])
plt.plot(X, Y, 'black')
plt.show()
#%%
Ypred = b0+b1*X1
r2_score(Y1, Ypred)

#%% repetir con los demás datasets de Anscombe

