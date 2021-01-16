# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 16:06:53 2021

@author: Anurodh Mohapatra
"""

import pandas as pd

# Function to check and create dataframe for missing value


def check_miss(df):
    '''
    This function will check number and % of missing value in each column 
    if it is more than 0 then it will return a dataframe
    '''

    # Column which have missing value
    miss_col = [col for col in df.columns if df[col].isnull().sum() > 0]

    # DataFrame that contains no. and % of missing value
    miss_df = pd.DataFrame([df[miss_col].isnull().sum(), df[miss_col].isnull().mean()*100],
                           index=['Missing Value', 'Missing Value %'])

    return miss_df


df1 = pd.read_csv('House_Data_Bangalore.csv')

# Droping missing value
df2 = df1.copy()
df2.dropna(inplace=True)

# Remove text data from Rent column
df3 = df2[df2['Rent(Rs)'].str.isalnum()]

# Change dtypes of some columns
df3['Rent(Rs)'] = df3['Rent(Rs)'].astype('int')

# Exporting Data
df3.to_csv('House_Data_Bangalore_for_EDA.csv', index=False)
