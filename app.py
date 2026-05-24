import streamlit as st
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from core.data_handler import DataHandler
from core.mining_engine import MiningEngine
from ui.dashboard import DashboardUI

@st.cache_data
def compute_support_bounds(_basket_sets):
    """Hitung batas support dari dataset (hanya bergantung pada data, bukan parameter user)."""
    total_transactions = len(_basket_sets)
    item_supports = _basket_sets.sum() / total_transactions
    max_support = item_supports.max()
    top_items_support = item_supports.sort_values(ascending=False).head(10)
    return {
        'total_transactions': total_transactions,
        'max_support': max_support,
        'top_items_support': top_items_support,
    }

@st.cache_data
def compute_confidence_at_support(_basket_sets, min_support_val):
    """
    Hitung confidence max yang BENAR-BENAR bisa dicapai pada level support tertentu.
    Ini memastikan user tidak diberi info yang menyesatkan.
    """
    max_confidence = 0.0
    best_rule_info = None
    total_rules = 0
    try:
        freq_items = apriori(_basket_sets, min_support=min_support_val, use_colnames=True)
        if not freq_items.empty:
            freq_items['length'] = freq_items['itemsets'].apply(lambda x: len(x))
            try:
                rules_explore = association_rules(freq_items, metric="confidence", min_threshold=0.01)
                if not rules_explore.empty:
                    total_rules = len(rules_explore)
                    max_confidence = rules_explore['confidence'].max()
                    best_row = rules_explore.loc[rules_explore['confidence'].idxmax()]
                    best_rule_info = {
                        'antecedents': ', '.join(list(best_row['antecedents'])),
                        'consequents': ', '.join(list(best_row['consequents'])),
                        'confidence': best_row['confidence'],
                        'support': best_row['support'],
                        'lift': best_row['lift'],
                    }
            except Exception:
                pass
    except Exception:
        pass
    
    return {
        'max_confidence': max_confidence,
        'best_rule_info': best_rule_info,
        'total_rules': total_rules,
    }

def main():
    st.set_page_config(page_title="Market Basket Analysis", layout="wide")
    
    st.title(":material/shopping_cart: Sistem Analisis Pola Asosiasi Penjualan")
    st.markdown("### Market Basket Analysis menggunakan Algoritma Apriori")
    st.write("Aplikasi ini dibuat untuk menemukan pola pembelian konsumen (item yang sering dibeli secara bersamaan).")
    
    st.sidebar.header("1. Upload Dataset")
    st.sidebar.markdown(":material/link: [Unduh Dataset Kaggle di sini](https://www.kaggle.com/datasets/mittalvasu95/the-bread-basket)")
    uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=['csv'])
    
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
        
        # --- Preprocessing & Hitung Batas Support ---
        basket_sets = DataHandler.preprocess_data(data)
        sup_bounds = compute_support_bounds(basket_sets)
        
        max_sup_pct = sup_bounds['max_support'] * 100
        
        # --- Tampilkan Info Dataset di Sidebar ---
        st.sidebar.header(":material/bar_chart: Info Parameter Dataset")
        st.sidebar.markdown(f"**Total Transaksi:** `{sup_bounds['total_transactions']:,}`")
        st.sidebar.markdown(f"**Support Tertinggi Item:** `{max_sup_pct:.1f}%`")
        
        with st.sidebar.expander(":material/trending_up: Top 10 Item (Support Tertinggi)"):
            for item_name, sup_val in sup_bounds['top_items_support'].items():
                st.markdown(f"- **{item_name}**: `{sup_val*100:.2f}%`")
        
        st.sidebar.markdown("---")
        
        # ========================================
        # STEP 1: User pilih Support dulu
        # ========================================
        st.sidebar.header("2. Konfigurasi Parameter")
        
        slider_max_support = min(int(max_sup_pct) + 5, 100)
        slider_default_support = max(1, int(max_sup_pct * 0.1))
        
        st.sidebar.caption(f":material/lightbulb: Support item tertinggi: **{max_sup_pct:.1f}%** -- atur di bawah nilai ini.")
        min_support_pct = st.sidebar.slider(
            "Minimum Support (%)", 
            min_value=1, 
            max_value=slider_max_support, 
            value=slider_default_support, 
            step=1
        )
        min_support = min_support_pct / 100.0
        
        if min_support_pct > max_sup_pct:
            st.sidebar.error(f":material/warning: Support ({min_support_pct}%) melebihi support tertinggi ({max_sup_pct:.1f}%). Tidak akan ditemukan hasil.")
        
        # ========================================
        # STEP 2: Hitung confidence max BERDASARKAN support yang dipilih
        # ========================================
        conf_bounds = compute_confidence_at_support(basket_sets, min_support)
        max_conf_pct = conf_bounds['max_confidence'] * 100
        
        # Tampilkan info confidence yang akurat untuk support ini
        if max_conf_pct > 0:
            st.sidebar.success(
                f":material/check_circle: Pada Support {min_support_pct}%:\n"
                f"- Confidence tertinggi: **{max_conf_pct:.1f}%**\n"
                f"- Total rule tersedia: **{conf_bounds['total_rules']}**"
            )
            
            if conf_bounds['best_rule_info']:
                with st.sidebar.expander(":material/emoji_events: Rule Terkuat pada Support ini"):
                    info = conf_bounds['best_rule_info']
                    st.markdown(f"**Jika beli** {info['antecedents']}")
                    st.markdown(f"**Maka beli** {info['consequents']}")
                    st.markdown(f"- Confidence: `{info['confidence']*100:.1f}%`")
                    st.markdown(f"- Support: `{info['support']*100:.2f}%`")
                    st.markdown(f"- Lift: `{info['lift']:.2f}x`")
            
            slider_max_confidence = min(int(max_conf_pct) + 5, 100)
            slider_default_confidence = max(10, int(max_conf_pct * 0.5))
            
            st.sidebar.caption(f":material/lightbulb: Confidence tertinggi pada support ini: **{max_conf_pct:.1f}%** -- atur di bawah nilai ini.")
        else:
            st.sidebar.warning(
                f":material/warning: Pada Support {min_support_pct}%, tidak ditemukan rule apapun. "
                f"Turunkan nilai Minimum Support."
            )
            slider_max_confidence = 100
            slider_default_confidence = 50
        
        min_confidence_pct = st.sidebar.slider(
            "Minimum Confidence (%)", 
            min_value=10, 
            max_value=slider_max_confidence, 
            value=min(slider_default_confidence, slider_max_confidence),
            step=5
        )
        min_confidence = min_confidence_pct / 100.0
        
        # Peringatan jika confidence terlalu tinggi
        if max_conf_pct > 0 and min_confidence_pct > max_conf_pct:
            st.sidebar.error(
                f":material/warning: Confidence ({min_confidence_pct}%) melebihi confidence tertinggi "
                f"({max_conf_pct:.1f}%) pada support {min_support_pct}%. Tidak akan ditemukan rule."
            )
        
        # ========================================
        # STEP 3: Jalankan Analisis
        # ========================================
        if st.sidebar.button(":material/rocket_launch: Jalankan Analisis", use_container_width=True):
            with st.spinner("Sedang memproses algoritma Apriori..."):
                try:
                    # Hitung data temporal dan statistik deskriptif
                    temporal_data = DataHandler.get_temporal_data(data)
                    desc_stats = DataHandler.compute_descriptive_stats(data)
                    
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
                    tab1, tab2 = st.tabs(["Langkah Perhitungan (Tabel)", "Insight & Analisis Mendalam"])
                    
                    # Render UI berdasarkan komponen (OOP)
                    with tab1:
                        DashboardUI.render_calculation_steps(basket_sets, frequent_itemsets, rules, min_support, min_confidence)
                    
                    with tab2:
                        DashboardUI.render_insights(data, temporal_data, desc_stats, basket_sets, frequent_itemsets, rules)
                        
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses dataset: {e}")
                    
    else:
        st.sidebar.header("2. Konfigurasi Parameter")
        st.sidebar.caption(":material/folder_open: Upload dataset terlebih dahulu untuk melihat info parameter.")
        st.sidebar.slider("Minimum Support (%)", min_value=1, max_value=50, value=5, step=1, disabled=True)
        st.sidebar.slider("Minimum Confidence (%)", min_value=10, max_value=100, value=50, step=5, disabled=True)
        st.info("Silakan unggah dataset transaksi Anda melalui panel sidebar di sebelah kiri.")

if __name__ == '__main__':
    main()
