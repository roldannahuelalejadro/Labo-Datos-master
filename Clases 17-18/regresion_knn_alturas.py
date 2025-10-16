#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 11:53:42 2025

@author: mcerdeiro
"""

import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
#%%
df = pd.read_csv('alturas.csv')
#%%
knn = KNeighborsRegressor(n_neighbors=5)
knn.fit(df[['altura mama']], df['altura'])
ypred = knn.predict(df[['altura mama']])
mean_squared_error(df['altura'], ypred)
np.sqrt(mean_squared_error(df['altura'], ypred))
#%%
