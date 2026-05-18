import pandas as pd
import streamlit as st

class DataHandler:
    @staticmethod
    @st.cache_data
    def load_data(uploaded_file):
        try:
            import io
            content = uploaded_file.read().decode('utf-8', errors='ignore')
            uploaded_file.seek(0)
            
            lines = content.split('\n')
            
            header_idx = -1
            for i, line in enumerate(lines[:50]):
                if "No Transaksi" in line and "Produk" in line and ";" in line:
                    header_idx = i
                    break
                    
            if header_idx != -1:
                df = pd.read_csv(io.StringIO(content), sep=';', skiprows=header_idx)
                if 'No Transaksi' in df.columns and 'Produk' in df.columns:
                    df = df.dropna(subset=['No Transaksi', 'Produk'])
                    
                    transactions = []
                    items = []
                    
                    for _, row in df.iterrows():
                        trans = str(row['No Transaksi']).strip()
                        raw_produk = row['Produk']
                        if pd.isna(raw_produk):
                            continue
                            
                        prods = str(raw_produk).split(',')
                        for prod in prods:
                            prod = prod.strip()
                            if prod and prod.lower() != 'nan':
                                transactions.append(trans)
                                items.append(prod)
                                
                    processed_df = pd.DataFrame({'Transaction': transactions, 'Item': items})
                    return processed_df
                
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
