# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 23:51:16 2021

@author: Anurodh Mohapatra
"""

import pandas as pd

df = pd.read_csv('House_Data_Bangalore_for_Model.csv')
df = df[['Address','Size(Acres)','Rent(Rs)']]

X = df[['Address','Size(Acres)']]
y = df['Rent(Rs)']

# Changing address to ordinal column
ord_address = df.groupby('Address').mean()['Rent(Rs)'].sort_values().index
map_add = {}
for index, value in enumerate(ord_address):
    map_add[value] = index

X.loc[:,'Address'] = X.loc[:,'Address'].map(map_add)

# Splitting model as train and test
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test = train_test_split(X,y)

'''
I tried linear regression with minmaxscallar, standardscallar and log transformation
but was getting 0.66 as train score and 0.63 as test score. 
'''
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

# Hyper Parameter tuning
# Step 1: Tune max_depth and min_child_weight
param_test1 = {
 'max_depth':range(3,10,2),
 'min_child_weight':range(1,6,2)
}
gsearch1 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=140, max_depth=5,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 nthread=4, scale_pos_weight=1, seed=27), 
 param_grid = param_test1, scoring='neg_root_mean_squared_error',n_jobs=4, cv=5)
gsearch1.fit(X_train,y_train)

param_test2 = {
 'max_depth':[2,3,4],
 'min_child_weight':[4,5,6]
}
gsearch2 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=140, max_depth=5,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 nthread=4, scale_pos_weight=1, seed=27), 
 param_grid = param_test2, scoring='neg_root_mean_squared_error',n_jobs=4, cv=5)
gsearch2.fit(X_train,y_train)

param_test2b = {
 'min_child_weight':[5,7,9,11,13,15,17,19,21]
}
gsearch2b = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=140, max_depth=4,
 min_child_weight=1, gamma=0, subsample=0.8, colsample_bytree=0.8,
 nthread=4, scale_pos_weight=1, seed=27), 
 param_grid = param_test2b, scoring='neg_root_mean_squared_error',n_jobs=4, cv=5)
gsearch2b.fit(X_train,y_train)

# Step 2: Tune gamma
param_test3 = {
 'gamma':[i/10.0 for i in range(0,5)]
}
gsearch3 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=140, max_depth=4,
 min_child_weight=15, gamma=0, subsample=0.8, colsample_bytree=0.8,
 nthread=4, scale_pos_weight=1, seed=27), 
 param_grid = param_test3, scoring='neg_root_mean_squared_error',n_jobs=4, cv=5)
gsearch3.fit(X_train,y_train)

# Step 3: Tune subsample and colsample_bytree
param_test4 = {
 'subsample':[i/10.0 for i in range(6,10)],
 'colsample_bytree':[i/10.0 for i in range(6,10)]
}
gsearch4 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=140, max_depth=4,
 min_child_weight=12, gamma=0, subsample=0.8, colsample_bytree=0.8,
 nthread=4, scale_pos_weight=1, seed=27), 
 param_grid = param_test4, scoring='neg_root_mean_squared_error',n_jobs=4, cv=5)
gsearch4.fit(X_train,y_train)

# Step 5: Tuning Regularization Parameters
param_test5 = {
 'reg_alpha':[1e-5, 1e-2, 0.1, 1, 100,1000,10000,1e5,1e6]
}
gsearch5 = GridSearchCV(estimator = XGBRegressor( learning_rate =0.1, n_estimators=140, max_depth=4,
 min_child_weight=12, gamma=0, subsample=0.6, colsample_bytree=0.9,
 nthread=4, scale_pos_weight=1, seed=27), 
 param_grid = param_test5, scoring='neg_root_mean_squared_error',n_jobs=4, cv=5)
gsearch5.fit(X_train,y_train)

model1 = XGBRegressor(  learning_rate =0.1,
                        n_estimators=1000,
                        max_depth=4,
                        min_child_weight=12,
                        gamma=0, 
                        subsample=0.6,
                        colsample_bytree=0.9,
                        reg_alpha=10000,
                        nthread=4, 
                        scale_pos_weight=1, 
                        seed=27).fit(X_train,y_train)

# Step 6: Reducing Learning Rate
model2 = XGBRegressor(  learning_rate =0.01,
                        n_estimators=5000,
                        max_depth=4,
                        min_child_weight=12,
                        gamma=0, 
                        subsample=0.6,
                        colsample_bytree=0.9,
                        reg_alpha=10000,
                        nthread=4, 
                        scale_pos_weight=1, 
                        seed=27).fit(X_train,y_train)

'''
After using XGBoost with hyperparameter tuning I was able to increase train score to 0.71
and test score to 0.70 and rmse of 4693
'''

# Pickleing model
import pickle
with open('model.pkl', 'wb') as file1:
    pickle.dump(model2, file1)

# Saving map dictionary to json
import json
with open('map.json','w') as file2:
    json.dump(map_add,file2)