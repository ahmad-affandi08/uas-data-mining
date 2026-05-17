import streamlit as st
from core.data_handler import DataHandler
from core.mining_engine import MiningEngine
from ui.dashboard import DashboardUI

def main():
    st.set_page_config(page_title="Market Basket Analysis", layout="wide")
    
    st.title(":material/shopping_cart: Sistem Analisis Pola Asosiasi Penjualan")
    st.markdown("### Market Basket Analysis menggunakan Algoritma Apriori")
    st.write("Aplikasi ini dibuat untuk menemukan pola pembelian konsumen (item yang sering dibeli secara bersamaan).")
    
    st.sidebar.header("1. Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=['csv'])
    
    st.sidebar.header("2. Konfigurasi Parameter")
    min_support_pct = st.sidebar.slider("Minimum Support (%)", min_value=1, max_value=50, value=5, step=1)
    min_confidence_pct = st.sidebar.slider("Minimum Confidence (%)", min_value=10, max_value=100, value=50, step=5)
    
    # Konversi ke desimal untuk algoritma
    min_support = min_support_pct / 100.0
    min_confidence = min_confidence_pct / 100.0
    
    if uploaded_file is not None:
        data = DataHandler.load_data(uploaded_file)
        
        if data is None:
            st.error("Gagal memuat dataset. Pastikan format file CSV sudah benar.")
            return
            
        if 'Transaction' not in data.columns or 'Item' not in data.columns:
            st.error("Dataset tidak sesuai. Pastikan terdapat kolom 'Transaction' dan 'Item'.")
            return
            
        with st.expander("Klik untuk melihat Preview Data Mentah (CSV)"):
            st.dataframe(data.head())
            st.write(f"Total baris data mentah: {len(data)}")
        
        if st.sidebar.button("Jalankan Analisis"):
            with st.spinner("Sedang memproses algoritma Apriori..."):
                try:
                    # Proses Transformasi Data
                    basket_sets = DataHandler.preprocess_data(data)
                    
                    # Inisialisasi Engine Data Mining (OOP)
                    engine = MiningEngine(min_support, min_confidence)
                    
                    # Proses Apriori
                    frequent_itemsets = engine.perform_apriori(basket_sets)
                    
                    if frequent_itemsets.empty:
                        st.warning("Tidak ditemukan Frequent Itemsets. Silakan turunkan nilai Minimum Support.")
                        return
                        
                    # Ekstraksi Rule
                    rules = engine.generate_rules(frequent_itemsets)
                    if rules is None or rules.empty:
                        st.warning("Tidak ditemukan Aturan Asosiasi. Silakan turunkan nilai Minimum Confidence.")
                        return
                    
                    st.markdown("---")
                    tab1, tab2 = st.tabs(["Langkah Perhitungan (Tabel)", "Visualisasi Grafik & Dasbor"])
                    
                    # Render UI berdasarkan komponen (OOP)
                    with tab1:
                        DashboardUI.render_calculation_steps(basket_sets, frequent_itemsets, rules, min_support, min_confidence)
                        
                    with tab2:
                        DashboardUI.render_visual_dashboard(basket_sets, frequent_itemsets, rules)
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses dataset: {e}")
                    
    else:
        st.info("Silakan unggah dataset transaksi Anda melalui panel sidebar di sebelah kiri.")

if __name__ == '__main__':
    main()
