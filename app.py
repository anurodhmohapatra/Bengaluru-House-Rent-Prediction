# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 22:17:19 2021

@author: Anurodh Mohapatra
"""

import pickle
import json
import streamlit as st
import pandas as pd

st.set_page_config(page_title='AM', page_icon=None, layout='centered', initial_sidebar_state='auto')

# To hide hamburger (top right corner) and “Made with Streamlit” footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# load the model from disk
model = pickle.load(open('model.pkl', 'rb'))
map_add = json.load(open('map.json', 'r'))

def predict(Address,Size):
    X = pd.DataFrame([[Address,Size]],columns=['Address','Size(Acres)'])
    X['Address'] = X['Address'].map(map_add)
    prediction = model.predict(X)
    return int(prediction)

def main():
    st.title("Bengaluru House Rent Prediction")
    address = st.selectbox("Select Address(Select others if not in the list)",list(map_add.keys()))
    st.markdown('''#### Enter Size Below(min = 500)
                 Avg. Size for 1 BHK = 500 Sqft
                 Avg. Size for 2 BHK = 1000 Sqft
                 Avg. Size for 3 BHK = 1500 Sqft
                 Avg. Size for 4 BHK = 2600 Sqft
                ''')
    Size = st.number_input("Size",min_value=500)
    if st.button("Predict"):
        rent = predict(address,Size)
        st.write("### Rent(Rs): ")
        st.success(rent)

if __name__ == '__main__':
    main()
