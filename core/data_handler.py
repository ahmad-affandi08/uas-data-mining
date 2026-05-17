import pandas as pd
import streamlit as st

class DataHandler:
    @staticmethod
    @st.cache_data
    def load_data(uploaded_file):
        try:
            data = pd.read_csv(uploaded_file)
            return data
        except Exception:
            return None

    @staticmethod
    def preprocess_data(data):
        if data['Item'].dtype == 'object':
            data['Item'] = data['Item'].str.strip()
            
        basket = data.groupby(['Transaction', 'Item'])['Item'].count().unstack().fillna(0)
        
        def encode_units(x):
            if x <= 0:
                return 0
            if x >= 1:
                return 1
                
        basket_sets = basket.map(encode_units)
        return basket_sets
