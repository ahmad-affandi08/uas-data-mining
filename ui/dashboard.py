import streamlit as st
import plotly.express as px

class DashboardUI:
    @staticmethod
    def render_calculation_steps(basket_sets, frequent_itemsets, rules, min_support, min_confidence):
        st.markdown("## Alur Kerja Algoritma Apriori")
        st.write("Seksi ini menjabarkan bagaimana sistem mengubah data mentah menjadi aturan bisnis melalui tahapan yang berurutan.")
        
        # LANGKAH 1
        st.markdown("### Langkah 1: Transformasi Data (One-Hot Encoding)")
        st.write("Data mentah diubah ke dalam bentuk matriks (*pivot*). Baris mewakili **ID Transaksi unik**, dan kolom mewakili **Nama Barang**. Nilai diisi `1` jika barang tersebut ada di dalam keranjang transaksi, dan `0` jika tidak.")
        st.write(f"Total Transaksi Unik setelah digabungkan (N): **{len(basket_sets)}**")
        st.dataframe(basket_sets.head(10))
        
        # LANGKAH 2
        st.markdown("### Langkah 2: Pembentukan Frequent Itemsets (Iterasi Apriori)")
        st.write(f"Sistem mengeliminasi barang/kombinasi yang jarang dibeli, dan hanya menyimpan yang memenuhi batas minimal kepopuleran (*Minimum Support* = {min_support}). Proses ini dilakukan bertahap mulai dari 1 barang, 2 barang, dst.")
        
        if not frequent_itemsets.empty:
            max_length = int(frequent_itemsets['length'].max())
            for i in range(1, max_length + 1):
                st.markdown(f"#### :material/autorenew: Iterasi ke-{i} (Kombinasi {i} Produk)")
                iter_data = frequent_itemsets[frequent_itemsets['length'] == i].copy()
                
                if not iter_data.empty:
                    iter_data['itemsets_str'] = iter_data['itemsets'].apply(lambda x: ', '.join(list(x)))
                    st.write(f"Ditemukan **{len(iter_data)}** kombinasi yang lolos seleksi:")
                    display_iter = iter_data[['itemsets_str', 'support']].rename(columns={'itemsets_str': 'Kombinasi Item', 'support': 'Nilai Support'})
                    st.dataframe(display_iter.sort_values(by='Nilai Support', ascending=False))
                else:
                    st.write("Tidak ada kombinasi yang lolos seleksi pada iterasi ini.")
        
        # LANGKAH 3
        st.markdown("### Langkah 3: Ekstraksi Aturan Asosiasi (Association Rules)")
        st.write(f"Dari kombinasi yang berhasil bertahan hingga akhir, sistem merakit aturan sebab-akibat dan menghitung metrik kepastian (*Confidence*) serta kekuatan korelasi (*Lift*). Hanya yang memenuhi *Minimum Confidence* >= {min_confidence} yang ditampilkan.")
        if rules is not None and not rules.empty:
            st.dataframe(rules[['Aturan', 'support', 'confidence', 'lift']])
        else:
            st.write("Belum ada aturan yang terbentuk.")
            
        # LANGKAH 4
        st.markdown("### Langkah 4: Bedah Rumus & Bukti Perhitungan Manual")
        st.info("Bagian ini membedah Aturan Peringkat #1 menggunakan rumus matematika untuk membuktikan bahwa metrik pada Langkah 3 valid dan dihitung secara tepat berdasarkan frekuensi kemunculan di Langkah 1.")
        
        if rules is not None and not rules.empty:
            best_rule_raw = rules.iloc[0]
            A_str = best_rule_raw['antecedents_str']
            B_str = best_rule_raw['consequents_str']
            
            N = len(basket_sets)
            supp_A = best_rule_raw['antecedent support']
            supp_B = best_rule_raw['consequent support']
            supp_AB = best_rule_raw['support']
            conf = best_rule_raw['confidence']
            lift = best_rule_raw['lift']
            
            freq_A = int(round(supp_A * N))
            freq_B = int(round(supp_B * N))
            freq_AB = int(round(supp_AB * N))
            
            st.write(f"**Studi Kasus:** Aturan **Jika membeli {A_str}, maka membeli {B_str}**")
            st.write(f"- Total Seluruh Transaksi (N) = **{N}**")
            st.write(f"- Frekuensi **{A_str}** dibeli = **{freq_A}**")
            st.write(f"- Frekuensi **{B_str}** dibeli = **{freq_B}**")
            st.write(f"- Frekuensi **{A_str} & {B_str}** dibeli BERSAMAAN = **{freq_AB}**")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.markdown("**A. Support**")
                st.latex(r"Supp(A \rightarrow B) = \frac{Freq(A \cap B)}{N}")
                st.latex(rf"= \frac{{{freq_AB}}}{{{N}}} = {supp_AB:.4f}")
            with col_m2:
                st.markdown("**B. Confidence**")
                st.latex(r"Conf = \frac{Supp(A \rightarrow B)}{Supp(A)}")
                st.latex(rf"= \frac{{{supp_AB:.4f}}}{{{supp_A:.4f}}} = {conf:.4f}")
            with col_m3:
                st.markdown("**C. Lift**")
                st.latex(r"Lift = \frac{Confidence}{Supp(B)}")
                st.latex(rf"= \frac{{{conf:.4f}}}{{{supp_B:.4f}}} = {lift:.4f}")

    @staticmethod
    def render_visual_dashboard(basket_sets, frequent_itemsets, rules):
        st.markdown("## Dasbor Ringkasan Bisnis")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Transaksi Unik", len(basket_sets))
        col2.metric("Kombinasi Item Ditemukan", len(frequent_itemsets) if frequent_itemsets is not None else 0)
        col3.metric("Aturan (Rules) Terbentuk", len(rules) if rules is not None else 0)
        col4.metric("Lift Tertinggi", f"{rules['lift'].max():.2f}" if rules is not None and not rules.empty else "0.00")
        
        st.markdown("---")
        
        st.markdown("### :material/emoji_events: Top 10 Produk & Kombinasi Terlaris Keseluruhan")
        if not frequent_itemsets.empty:
            top_10_items = frequent_itemsets.head(10).copy()
            top_10_items['itemsets_str'] = top_10_items['itemsets'].apply(lambda x: ', '.join(list(x)))
            top_10_items = top_10_items.sort_values(by='support', ascending=True)
            fig_freq = px.bar(top_10_items, x="support", y="itemsets_str", orientation='h', 
                              color="support", color_continuous_scale="Viridis",
                              labels={"support": "Nilai Support (Skala 0-1)", "itemsets_str": "Kombinasi Item"})
            st.plotly_chart(fig_freq, use_container_width=True)
            
        st.markdown("---")
        
        if rules is not None and not rules.empty:
            st.markdown("### :material/scatter_plot: Peta Kekuatan Aturan Asosiasi")
            st.info(":material/lightbulb: **Cara Membaca:** Semakin ke kanan posisinya (Support tinggi), item semakin sering dibeli. Semakin ke atas posisinya (Confidence tinggi), hubungan ketergantungannya semakin pasti. Ukuran dan warna gelembung yang membesar menandakan nilai *Lift* yang kuat.")
            fig_scatter = px.scatter(rules, x="support", y="confidence", color="lift", 
                                     hover_name="Aturan", size="lift", color_continuous_scale="Plasma",
                                     labels={"support": "Support", "confidence": "Confidence", "lift": "Lift"})
            st.plotly_chart(fig_scatter, use_container_width=True)
            
            st.markdown("---")
            
            st.markdown("### :material/insights: Kesimpulan & Rekomendasi Bisnis Teratas")
            st.write("Rekomendasi taktis untuk pengaturan tata letak (*layouting*) dan pembuatan paket promo (*bundling*):")
            
            num_rules_to_show = min(3, len(rules))
            for idx in range(num_rules_to_show):
                rule = rules.iloc[idx]
                if rule['lift'] > 1:
                    with st.container():
                        st.success(f"**:material/military_tech: Peringkat #{idx + 1}: {rule['Aturan']}**")
                        st.write(f"Jika pelanggan membeli **{rule['antecedents_str']}**, maka kepastian mereka untuk juga membeli **{rule['consequents_str']}** adalah sebesar **{rule['confidence']*100:.1f}%**.")
                        st.write(f"Kecenderungan (*Lift*) mereka membeli bersamaan ini lebih tinggi sebanyak **{rule['lift']:.2f}x lipat** dibandingkan jika pelanggan membeli barang secara kebetulan/acak.")
                else:
                    if idx == 0:
                        st.warning("Belum ditemukan relasi produk yang cukup kuat (Nilai Lift <= 1) untuk dijadikan paket promo unggulan.")
                    break
