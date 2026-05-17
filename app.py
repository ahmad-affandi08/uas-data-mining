import streamlit as st
import pandas as pd
import plotly.express as px
from mlxtend.frequent_patterns import apriori, association_rules

# NFR-3: Kualitas Kode (Clean Code Standard)
@st.cache_data
def load_data(uploaded_file):
    try:
        data = pd.read_csv(uploaded_file)
        return data
    except Exception as e:
        return None

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

def perform_apriori(basket_sets, min_support):
    frequent_itemsets = apriori(basket_sets, min_support=min_support, use_colnames=True)
    # Tambahkan kolom length untuk memvisualisasikan iterasi (langkah-langkah) Apriori
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    return frequent_itemsets

def generate_rules(frequent_itemsets, min_confidence):
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return rules

def main():
    st.set_page_config(page_title="Market Basket Analysis", layout="wide", page_icon="🛒")

    st.title("🛒 Sistem Analisis Pola Asosiasi Penjualan")
    st.markdown("### Market Basket Analysis menggunakan Algoritma Apriori")
    st.write("Aplikasi ini dibuat untuk menemukan pola pembelian konsumen (item yang sering dibeli secara bersamaan).")

    st.sidebar.header("1. Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Pilih file CSV", type=['csv'])

    st.sidebar.header("2. Konfigurasi Parameter")
    min_support = st.sidebar.slider("Minimum Support", min_value=0.01, max_value=0.50, value=0.05, step=0.01)
    min_confidence = st.sidebar.slider("Minimum Confidence", min_value=0.1, max_value=1.0, value=0.5, step=0.1)

    if uploaded_file is not None:
        data = load_data(uploaded_file)

        if data is None:
            st.error("Gagal memuat dataset. Pastikan format file CSV sudah benar.")
            return

        if 'Transaction' not in data.columns or 'Item' not in data.columns:
            st.error("Dataset tidak sesuai. Pastikan terdapat kolom 'Transaction' dan 'Item'.")
            return

        with st.expander("Klik untuk melihat Preview Data Mentah"):
            st.dataframe(data.head(5))
            st.write(f"Total baris data mentah: {len(data)}")

        if st.sidebar.button("Jalankan Analisis"):
            with st.spinner("Sedang memproses algoritma Apriori..."):
                try:
                    basket_sets = preprocess_data(data)
                    frequent_itemsets = perform_apriori(basket_sets, min_support)

                    if frequent_itemsets.empty:
                        st.warning("Tidak ditemukan Frequent Itemsets. Silakan turunkan nilai Minimum Support.")
                        return

                    frequent_itemsets = frequent_itemsets.sort_values(by='support', ascending=False).reset_index(drop=True)

                    rules = generate_rules(frequent_itemsets, min_confidence)

                    if rules.empty:
                        st.warning("Tidak ditemukan Aturan Asosiasi. Silakan turunkan nilai Minimum Confidence.")
                        return

                    rules_display = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].copy()
                    rules_display['antecedents'] = rules_display['antecedents'].apply(lambda x: ', '.join(list(x)))
                    rules_display['consequents'] = rules_display['consequents'].apply(lambda x: ', '.join(list(x)))
                    rules_display = rules_display.sort_values(by='lift', ascending=False).reset_index(drop=True)

                    st.markdown("---")
                    st.markdown("## 📊 Dasbor Hasil Analisis (Visual)")

                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Total Transaksi Unik", len(basket_sets))
                    col2.metric("Kombinasi Item Ditemukan", len(frequent_itemsets))
                    col3.metric("Aturan (Rules) Terbentuk", len(rules_display))
                    col4.metric("Lift Tertinggi", f"{rules_display['lift'].max():.2f}")

                    # ---------------------------------------------------------
                    # ALUR PERHITUNGAN VISUAL (STEP-BY-STEP ITERATION)
                    # ---------------------------------------------------------
                    st.markdown("---")
                    st.markdown("## 🔄 Simulasi Alur Perhitungan (Step-by-Step Apriori)")
                    st.info("Bagian ini memvisualisasikan bagaimana algoritma Apriori bekerja dengan menyaring itemset mulai dari kombinasi 1 item, kemudian 2 item, dan seterusnya berdasarkan parameter *Minimum Support* yang Anda tetapkan.")

                    max_length = int(frequent_itemsets['length'].max())

                    # Buat kolom sesuai dengan jumlah iterasi
                    cols = st.columns(max_length)

                    for i in range(1, max_length + 1):
                        with cols[i-1]:
                            st.markdown(f"<h4 style='text-align: center;'>Iterasi ke-{i}</h4>", unsafe_allow_html=True)
                            st.markdown(f"<p style='text-align: center; color: gray;'>Kombinasi {i} Produk</p>", unsafe_allow_html=True)

                            iter_data = frequent_itemsets[frequent_itemsets['length'] == i].copy()

                            if not iter_data.empty:
                                iter_data['itemsets_str'] = iter_data['itemsets'].apply(lambda x: ', '.join(list(x)))
                                st.write(f"✅ Ada **{len(iter_data)} kombinasi** yang lolos seleksi.")

                                # Tampilkan mini-chart untuk melihat 5 teratas tiap iterasi
                                top_iter_data = iter_data.head(5).sort_values(by='support', ascending=True)
                                fig_mini = px.bar(top_iter_data, x="support", y="itemsets_str", orientation='h', height=250, color="support", color_continuous_scale="Teal")
                                fig_mini.update_layout(margin=dict(l=0, r=0, t=10, b=0), yaxis_title=None, xaxis_title="Support")
                                st.plotly_chart(fig_mini, use_container_width=True)
                            else:
                                st.write("❌ Tidak ada kombinasi yang lolos.")

                    st.markdown("---")

                    # ---------------------------------------------------------
                    # PENJELASAN MATEMATIS / BUKTI PERHITUNGAN MANUAL
                    # ---------------------------------------------------------
                    st.markdown("## 🧮 Bedah Rumus & Bukti Perhitungan Manual")
                    st.info("Bagian ini menampilkan penjabaran rumus matematika dari aturan terbaik (Peringkat #1) untuk membuktikan kepada penguji bagaimana metrik *Support*, *Confidence*, dan *Lift* didapatkan dari dataset secara manual.")

                    if not rules.empty:
                        # Ambil aturan terbaik langsung dari dataframe 'rules' (karena masih memiliki kolom antecedent support utuh)
                        best_rule_raw = rules.sort_values(by='lift', ascending=False).iloc[0]

                        A_str = ', '.join(list(best_rule_raw['antecedents']))
                        B_str = ', '.join(list(best_rule_raw['consequents']))

                        N = len(basket_sets)
                        supp_A = best_rule_raw['antecedent support']
                        supp_B = best_rule_raw['consequent support']
                        supp_AB = best_rule_raw['support']
                        conf = best_rule_raw['confidence']
                        lift = best_rule_raw['lift']

                        # Frekuensi riil (kemunculan dalam transaksi)
                        freq_A = int(round(supp_A * N))
                        freq_B = int(round(supp_B * N))
                        freq_AB = int(round(supp_AB * N))

                        st.write(f"**Studi Kasus Pembuktian:** Aturan **{A_str}** ➔ **{B_str}**")
                        st.write(f"- Total Transaksi Keseluruhan (N) = **{N}**")
                        st.write(f"- Frekuensi **{A_str}** dibeli saja = **{freq_A}** transaksi")
                        st.write(f"- Frekuensi **{B_str}** dibeli saja = **{freq_B}** transaksi")
                        st.write(f"- Frekuensi **{A_str}** & **{B_str}** dibeli BERSAMAAN = **{freq_AB}** transaksi")

                        col_m1, col_m2, col_m3 = st.columns(3)

                        with col_m1:
                            st.markdown("#### 1. Menghitung Support")
                            st.write("Mengukur persentase kombinasi item dari seluruh transaksi yang ada.")
                            st.latex(r"Support(A \rightarrow B) = \frac{Freq(A \cap B)}{N}")
                            st.latex(rf"= \frac{{{freq_AB}}}{{{N}}}")
                            st.latex(rf"= {supp_AB:.4f} \;\text{{({supp_AB*100:.1f}\%)}}")

                        with col_m2:
                            st.markdown("#### 2. Menghitung Confidence")
                            st.write("Mengukur peluang terjualnya barang B, JIKA barang A sudah dibeli.")
                            st.latex(r"Confidence = \frac{Support(A \rightarrow B)}{Support(A)}")
                            st.latex(rf"= \frac{{{supp_AB:.4f}}}{{{supp_A:.4f}}}")
                            st.latex(rf"= {conf:.4f} \;\text{{({conf*100:.1f}\%)}}")

                        with col_m3:
                            st.markdown("#### 3. Menghitung Lift")
                            st.write("Mengukur kekuatan relasi. Jika Lift > 1, maka hubungan sangat valid.")
                            st.latex(r"Lift = \frac{Confidence}{Support(B)}")
                            st.latex(rf"= \frac{{{conf:.4f}}}{{{supp_B:.4f}}}")
                            st.latex(rf"= {lift:.4f}")

                    st.markdown("---")

                    # 2. Grafik Top Produk / Kombinasi Terlaris (Bisa lebih dari 10 jika ada)
                    st.markdown("### 🏆 Top 10 Produk & Kombinasi Terlaris Keseluruhan")
                    st.write("Grafik di bawah memetakan seberapa sering suatu produk / kombinasi dibeli dari total transaksi harian.")
                    top_10_items = frequent_itemsets.head(10).copy()
                    top_10_items['itemsets_str'] = top_10_items['itemsets'].apply(lambda x: ', '.join(list(x)))
                    top_10_items = top_10_items.sort_values(by='support', ascending=True)
                    fig_freq = px.bar(top_10_items, x="support", y="itemsets_str", orientation='h',
                                      color="support", color_continuous_scale="Viridis",
                                      labels={"support": "Nilai Support (Skala 0-1)", "itemsets_str": "Kombinasi Item"})
                    st.plotly_chart(fig_freq, use_container_width=True)

                    st.markdown("---")

                    # 3. Grafik Scatter Plot: Peta Kekuatan Aturan
                    st.markdown("### 📍 Peta Kekuatan Aturan Asosiasi")
                    st.info("💡 **Cara Membaca:** Semakin ke kanan posisinya (Support tinggi), item semakin sering dibeli. Semakin ke atas posisinya (Confidence tinggi), hubungan ketergantungannya semakin pasti. Ukuran dan warna gelembung yang membesar menandakan nilai *Lift* yang kuat.")
                    rules_display['Aturan'] = rules_display['antecedents'] + " ➔ " + rules_display['consequents']
                    fig_scatter = px.scatter(rules_display, x="support", y="confidence", color="lift",
                                             hover_name="Aturan", size="lift", color_continuous_scale="Plasma",
                                             labels={"support": "Support (Popularitas)", "confidence": "Confidence (Kepastian)", "lift": "Lift (Kekuatan Relasi)"})
                    st.plotly_chart(fig_scatter, use_container_width=True)

                    st.markdown("---")

                    # 6. Kesimpulan Bisnis Otomatis -> Diperbarui jadi menampilkan beberapa aturan (bukan 1 saja)
                    st.markdown("### 💡 Kesimpulan & Rekomendasi Bisnis Teratas")
                    st.write("Berdasarkan hasil analisis, berikut adalah beberapa rekomendasi strategi penjualan terbaik untuk Anda (Menampilkan **Top 3 Kombinasi Paling Kuat**):")

                    # Menampilkan 3 Aturan Terbaik
                    num_rules_to_show = min(3, len(rules_display))

                    for idx in range(num_rules_to_show):
                        rule = rules_display.iloc[idx]
                        if rule['lift'] > 1:
                            with st.container():
                                st.success(f"**🏅 Peringkat #{idx + 1}: {rule['antecedents']} ➔ {rule['consequents']}**")
                                st.write(f"Pelanggan yang membeli **{rule['antecedents']}** memiliki tingkat kepastian sebesar **{rule['confidence']*100:.1f}%** untuk juga membeli **{rule['consequents']}**.")
                                st.write(f"Kecenderungan (*Lift*) mereka membeli bersamaan ini lebih tinggi sebanyak **{rule['lift']:.2f}x lipat** dibandingkan jika pelanggan membeli barang secara kebetulan/acak.")
                                st.markdown(f"> **Rekomendasi Aksi Bisnis:** Anda dapat mengatur tata letak etalase agar **{rule['consequents']}** berada tepat di samping **{rule['antecedents']}**, atau gabungkan ke dalam paket diskon khusus (*bundling*).")
                        else:
                            if idx == 0:
                                st.warning("Belum ditemukan relasi produk yang cukup kuat (Nilai Lift <= 1) untuk dijadikan paket promo unggulan.")
                            break

                    # 5. Tabel Data Mentah
                    st.markdown("<br>", unsafe_allow_html=True)
                    with st.expander("🔍 Lihat Detail Tabel Data Analisis (Advanced / Mentah)"):
                        st.write("Tabel Association Rules Lengkap:")
                        st.dataframe(rules_display.drop(columns=['Aturan']))

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat memproses dataset: {e}")

    else:
        st.info("Silakan unggah dataset transaksi Anda melalui panel sidebar di sebelah kiri.")

if __name__ == '__main__':
    main()
