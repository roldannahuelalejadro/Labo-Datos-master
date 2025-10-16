#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 13 10:39:29 2025

@author: mcerdeiro
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
#%% función para graficar la forontera de decision
def plot_decision_boundary(X, y, clf):
    fig, ax = plt.subplots(figsize=(6, 6))    
    # Crear grilla
    h = 0.1
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h)) 
    # Predecir clases en cada punto de la grilla
    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    # Colores
    n_classes = len(np.unique(y))
    colors = plt.cm.Pastel1.colors[:n_classes]
    cmap_light = ListedColormap(colors)
    cmap_bold = ListedColormap(colors)
    # Graficar la frontera de decisión
    ax.contourf(xx, yy, Z, cmap=cmap_light, alpha=0.5)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold, s=40, edgecolor='k')
    ax.set_xlabel("Atributo 1")
    ax.set_ylabel("Atributo 2")
    ax.set_title("Frontera de decisión")
#%% generar los datos
X, y = make_moons(n_samples=200, noise=0.2)
#%% gráfico de dispersión
plt.figure(figsize=(6, 4))
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=ListedColormap(['#4CAF50', '#8e44ad']), edgecolor='k')
plt.title("Datos: Dos clases en forma de media luna")
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()
#%% clasificador
clf1 = KNeighborsClassifier(n_neighbors=1)  # <- completar valor de k
clf1.fit(X, y)
plot_decision_boundary( X, y,clf1)


