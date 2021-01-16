# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 23:51:16 2021

@author: Anurodh Mohapatra
"""

import pandas as pd
# import numpy as np

df = pd.read_csv('House_Data_Bangalore_for_Model.csv')
df = df[['Address','Size(Acres)','Rent(Rs)']]

# Changing address to ordinal column
ord_address = df.groupby('Address').mean()['Rent(Rs)'].sort_values().index
map_add = {}
for index, value in enumerate(ord_address):
    map_add[value] = index

df.loc[:,'Address'] = df.loc[:,'Address'].map(map_add)

# Log transformation of Size and Rent column
# df['Size(Acres)'] = np.log(df['Size(Acres)'])
# df['Rent(Rs)'] = np.log(df['Rent(Rs)'])

from sklearn.model_selection import train_test_split
X = df[['Address','Size(Acres)']]
y = df['Rent(Rs)']
X_train,X_test,y_train,y_test = train_test_split(X,y)

from sklearn.linear_model import LinearRegression
lg = LinearRegression()
lg.fit(X_train,y_train)