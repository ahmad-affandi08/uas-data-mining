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

    @staticmethod
    def get_temporal_data(data):
        """Extract temporal information from the raw data for insight analysis."""
        temporal = data.copy()
        
        # Parse date_time if available
        if 'date_time' in temporal.columns:
            temporal['date_time'] = pd.to_datetime(temporal['date_time'], format='mixed', dayfirst=True, errors='coerce')
            temporal['hour'] = temporal['date_time'].dt.hour
            temporal['day_name'] = temporal['date_time'].dt.day_name()
            temporal['month'] = temporal['date_time'].dt.month
            temporal['month_name'] = temporal['date_time'].dt.month_name()
            temporal['date'] = temporal['date_time'].dt.date
        
        return temporal

    @staticmethod
    def compute_descriptive_stats(data):
        """Compute descriptive statistics from the transaction data."""
        stats = {}
        stats['total_rows'] = len(data)
        stats['total_transactions'] = data['Transaction'].nunique()
        stats['total_unique_items'] = data['Item'].nunique()
        
        items_per_trans = data.groupby('Transaction')['Item'].count()
        stats['avg_items_per_transaction'] = items_per_trans.mean()
        stats['max_items_per_transaction'] = items_per_trans.max()
        stats['min_items_per_transaction'] = items_per_trans.min()
        stats['median_items_per_transaction'] = items_per_trans.median()
        
        stats['top_items'] = data['Item'].value_counts().head(10)
        stats['bottom_items'] = data['Item'].value_counts().tail(10)
        stats['items_per_transaction_distribution'] = items_per_trans.value_counts().sort_index()
        
        return stats
