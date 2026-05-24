import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from itertools import combinations

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
        st.write(f"Sistem mengevaluasi **semua** kandidat barang/kombinasi dan menandai mana yang memenuhi batas minimal kepopuleran (*Minimum Support* = {min_support}). Proses ini dilakukan bertahap mulai dari 1 barang, 2 barang, dst.")
        
        N = len(basket_sets)
        
        if not frequent_itemsets.empty:
            max_length = int(frequent_itemsets['length'].max())
            
            # Kumpulkan frequent items dari iterasi sebelumnya untuk generate kandidat
            prev_frequent_items = None
            
            for i in range(1, max_length + 1):
                st.markdown(f"#### :material/autorenew: Iterasi ke-{i} (Kombinasi {i} Produk)")
                
                # Ambil itemsets yang lolos di iterasi ini
                iter_passed = frequent_itemsets[frequent_itemsets['length'] == i].copy()
                passed_sets = set()
                if not iter_passed.empty:
                    passed_sets = set(iter_passed['itemsets'].apply(lambda x: frozenset(x)))
                
                all_candidates = []
                
                if i == 1:
                    # Iterasi 1: semua item individual adalah kandidat
                    for col in basket_sets.columns:
                        sup = basket_sets[col].sum() / N
                        item_fs = frozenset([col])
                        status = "Lolos" if item_fs in passed_sets else "Tidak Lolos"
                        all_candidates.append({
                            'Kombinasi Item': col,
                            'Frekuensi': int(basket_sets[col].sum()),
                            'Nilai Support': round(sup, 6),
                            'Keterangan': status,
                        })
                    prev_frequent_items = [fs for fs in passed_sets]
                else:
                    # Iterasi 2+: generate kandidat dari frequent items iterasi sebelumnya
                    if prev_frequent_items and len(prev_frequent_items) >= 2:
                        # Kumpulkan semua item unik dari frequent itemsets sebelumnya
                        unique_items = set()
                        for fs in prev_frequent_items:
                            unique_items.update(fs)
                        unique_items = sorted(unique_items)
                        
                        # Generate kombinasi i-item dari item-item yang frequent
                        seen_candidates = set()
                        for combo in combinations(unique_items, i):
                            candidate = frozenset(combo)
                            if candidate in seen_candidates:
                                continue
                            seen_candidates.add(candidate)
                            
                            # Hitung support untuk kandidat ini
                            cols = list(candidate)
                            if all(c in basket_sets.columns for c in cols):
                                freq = int((basket_sets[cols].sum(axis=1) == i).sum())
                                sup = freq / N
                                status = "Lolos" if candidate in passed_sets else "Tidak Lolos"
                                all_candidates.append({
                                    'Kombinasi Item': ', '.join(sorted(candidate)),
                                    'Frekuensi': freq,
                                    'Nilai Support': round(sup, 6),
                                    'Keterangan': status,
                                })
                    
                    # Update prev_frequent_items untuk iterasi berikutnya
                    prev_frequent_items = [fs for fs in passed_sets]
                
                if all_candidates:
                    df_candidates = pd.DataFrame(all_candidates)
                    df_candidates = df_candidates.sort_values(by='Nilai Support', ascending=False).reset_index(drop=True)
                    
                    lolos_count = len(df_candidates[df_candidates['Keterangan'] == 'Lolos'])
                    gagal_count = len(df_candidates[df_candidates['Keterangan'] == 'Tidak Lolos'])
                    
                    st.write(
                        f"Total kandidat: **{len(df_candidates)}** — "
                        f":material/check_circle: Lolos: **{lolos_count}** — "
                        f":material/cancel: Tidak Lolos: **{gagal_count}**"
                    )
                    
                    # Styling: warna hijau untuk Lolos, merah untuk Tidak Lolos
                    def color_status(val):
                        if val == 'Lolos':
                            return 'background-color: #1B5E20; color: #A5D6A7; font-weight: bold'
                        else:
                            return 'background-color: #B71C1C; color: #EF9A9A; font-weight: bold'
                    
                    styled_df = df_candidates.style.applymap(
                        color_status, subset=['Keterangan']
                    )
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)
                else:
                    st.write("Tidak ada kandidat yang dapat dihasilkan pada iterasi ini.")
        
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
    def render_insights(data, temporal_data, stats, basket_sets, frequent_itemsets, rules):
        st.markdown("## :material/psychology: Insight & Analisis Mendalam")
        st.write("Seksi ini menyajikan temuan-temuan penting dari data transaksi yang telah dianalisis, mencakup statistik deskriptif, pola temporal, dan interpretasi hasil algoritma Apriori.")

        # ── SECTION 1: Statistik Deskriptif ──
        st.markdown("### :material/bar_chart: 1. Ringkasan Statistik Deskriptif")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Baris Data", f"{stats['total_rows']:,}")
        c2.metric("Transaksi Unik", f"{stats['total_transactions']:,}")
        c3.metric("Jenis Produk Unik", f"{stats['total_unique_items']:,}")
        c4.metric("Rata-rata Item/Transaksi", f"{stats['avg_items_per_transaction']:.2f}")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Min Item/Transaksi", int(stats['min_items_per_transaction']))
        c6.metric("Max Item/Transaksi", int(stats['max_items_per_transaction']))
        c7.metric("Median Item/Transaksi", f"{stats['median_items_per_transaction']:.1f}")
        total_rules = len(rules) if rules is not None and not rules.empty else 0
        c8.metric("Aturan Asosiasi Ditemukan", total_rules)

        st.info(f"**Insight:** Rata-rata pelanggan membeli **{stats['avg_items_per_transaction']:.2f}** item per kunjungan. "
                f"Dari **{stats['total_unique_items']}** jenis produk, hanya sebagian kecil yang mendominasi penjualan. "
                f"Ini menunjukkan distribusi penjualan yang **tidak merata** (skewed), di mana beberapa produk inti menjadi penggerak utama revenue.")

        st.markdown("---")

        # ── SECTION 2: Top & Bottom Produk ──
        st.markdown("### :material/emoji_events: 2. Produk Terlaris vs Produk Kurang Diminati")
        col_top, col_bot = st.columns(2)
        with col_top:
            st.markdown("**Top 10 Produk Terlaris**")
            top_df = stats['top_items'].reset_index()
            top_df.columns = ['Produk', 'Jumlah Terjual']
            fig_top = px.bar(top_df, x='Jumlah Terjual', y='Produk', orientation='h',
                             color='Jumlah Terjual', color_continuous_scale='Greens')
            fig_top.update_layout(yaxis=dict(autorange="reversed"), height=350, margin=dict(t=10))
            st.plotly_chart(fig_top, use_container_width=True)
        with col_bot:
            st.markdown("**10 Produk Paling Jarang Dibeli**")
            bot_df = stats['bottom_items'].reset_index()
            bot_df.columns = ['Produk', 'Jumlah Terjual']
            fig_bot = px.bar(bot_df, x='Jumlah Terjual', y='Produk', orientation='h',
                             color='Jumlah Terjual', color_continuous_scale='Reds_r')
            fig_bot.update_layout(yaxis=dict(autorange="reversed"), height=350, margin=dict(t=10))
            st.plotly_chart(fig_bot, use_container_width=True)

        top_product = stats['top_items'].index[0]
        top_count = stats['top_items'].iloc[0]
        pct = (top_count / stats['total_rows']) * 100
        st.success(f"**Insight:** Produk **{top_product}** adalah yang paling laris dengan **{top_count:,}** kemunculan "
                   f"(**{pct:.1f}%** dari seluruh baris transaksi). Produk-produk di kolom kanan sangat jarang dibeli dan bisa dipertimbangkan untuk "
                   f"di-*bundle* bersama produk populer atau dievaluasi ulang keberadaannya di inventaris.")

        st.markdown("---")

        # ── SECTION 3: Distribusi Item per Transaksi ──
        st.markdown("### :material/inventory_2: 3. Distribusi Jumlah Item per Transaksi")
        dist = stats['items_per_transaction_distribution'].reset_index()
        dist.columns = ['Jumlah Item', 'Frekuensi Transaksi']
        fig_dist = px.bar(dist, x='Jumlah Item', y='Frekuensi Transaksi',
                          color='Frekuensi Transaksi', color_continuous_scale='Blues',
                          labels={'Jumlah Item': 'Jumlah Item dalam 1 Transaksi', 'Frekuensi Transaksi': 'Jumlah Transaksi'})
        fig_dist.update_layout(height=350, margin=dict(t=10))
        st.plotly_chart(fig_dist, use_container_width=True)

        mode_items = dist.loc[dist['Frekuensi Transaksi'].idxmax(), 'Jumlah Item']
        mode_freq = dist['Frekuensi Transaksi'].max()
        st.info(f"**Insight:** Mayoritas transaksi (**{mode_freq:,}** transaksi) hanya berisi **{mode_items} item**. "
                f"Ini menunjukkan bahwa pelanggan cenderung melakukan pembelian dalam jumlah kecil. "
                f"Strategi *cross-selling* dan *bundling* bisa digunakan untuk meningkatkan jumlah item per keranjang.")

        st.markdown("---")

        # ── SECTION 4: Analisis Temporal ──
        has_temporal = 'hour' in temporal_data.columns
        if has_temporal:
            st.markdown("### :material/schedule: 4. Analisis Pola Temporal (Waktu)")

            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown("**Transaksi per Jam**")
                hourly = temporal_data.groupby('hour')['Transaction'].nunique().reset_index()
                hourly.columns = ['Jam', 'Jumlah Transaksi']
                fig_hour = px.area(hourly, x='Jam', y='Jumlah Transaksi',
                                   color_discrete_sequence=['#636EFA'])
                fig_hour.update_layout(height=300, margin=dict(t=10))
                st.plotly_chart(fig_hour, use_container_width=True)

            with col_t2:
                st.markdown("**Transaksi per Hari**")
                day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                daily = temporal_data.groupby('day_name')['Transaction'].nunique().reindex(day_order).reset_index()
                daily.columns = ['Hari', 'Jumlah Transaksi']
                daily = daily.dropna()
                fig_day = px.bar(daily, x='Hari', y='Jumlah Transaksi',
                                 color='Jumlah Transaksi', color_continuous_scale='Sunset')
                fig_day.update_layout(height=300, margin=dict(t=10))
                st.plotly_chart(fig_day, use_container_width=True)

            # Period analysis
            if 'period_day' in temporal_data.columns:
                st.markdown("**Transaksi Berdasarkan Periode Hari**")
                period = temporal_data.groupby('period_day')['Transaction'].nunique().reset_index()
                period.columns = ['Periode', 'Jumlah Transaksi']
                fig_period = px.pie(period, values='Jumlah Transaksi', names='Periode',
                                    color_discrete_sequence=px.colors.qualitative.Set2, hole=0.4)
                fig_period.update_layout(height=350, margin=dict(t=10))
                st.plotly_chart(fig_period, use_container_width=True)

            peak_hour = hourly.loc[hourly['Jumlah Transaksi'].idxmax()]
            busiest_day = daily.loc[daily['Jumlah Transaksi'].idxmax()] if not daily.empty else None
            insight_text = f"**Insight:** Jam tersibuk adalah pukul **{int(peak_hour['Jam']):02d}:00** dengan **{int(peak_hour['Jumlah Transaksi']):,}** transaksi."
            if busiest_day is not None:
                insight_text += f" Hari tersibuk adalah **{busiest_day['Hari']}**. Pengetahuan ini dapat digunakan untuk mengoptimalkan jadwal stok, shift karyawan, dan waktu promosi."
            st.success(insight_text)
            st.markdown("---")

        # ── SECTION 5: Heatmap Co-occurrence ──
        section_num = 5 if has_temporal else 4
        st.markdown(f"### :material/local_fire_department: {section_num}. Heatmap Korelasi Antar Produk Populer")
        st.write("Matriks ini menunjukkan seberapa sering dua produk dibeli bersamaan dalam satu transaksi (co-occurrence).")

        top_n = min(15, len(basket_sets.columns))
        top_items_list = data['Item'].value_counts().head(top_n).index.tolist()
        filtered_cols = [c for c in top_items_list if c in basket_sets.columns]

        if len(filtered_cols) >= 2:
            subset = basket_sets[filtered_cols]
            cooccurrence = subset.T.dot(subset)
            np.fill_diagonal(cooccurrence.values, 0)

            fig_heat = px.imshow(cooccurrence, color_continuous_scale='YlOrRd', aspect='auto',
                                 labels=dict(color="Frekuensi Co-occurrence"))
            fig_heat.update_layout(height=500, margin=dict(t=10))
            st.plotly_chart(fig_heat, use_container_width=True)

            max_val = cooccurrence.max().max()
            max_pair = cooccurrence.stack().idxmax()
            st.info(f"**Insight:** Pasangan produk dengan co-occurrence tertinggi adalah **{max_pair[0]}** & **{max_pair[1]}** "
                    f"(muncul bersamaan di **{int(max_val)}** transaksi). Pasangan ini sangat potensial untuk dijadikan paket promo bundling.")
        else:
            st.write("Data tidak cukup untuk membuat heatmap.")

        st.markdown("---")

        # ── SECTION 6: Network Graph ──
        section_num += 1
        if rules is not None and not rules.empty:
            st.markdown(f"### :material/hub: {section_num}. Network Graph Hubungan Produk")
            st.write("Visualisasi jaringan yang menunjukkan hubungan asosiasi antar produk berdasarkan aturan yang ditemukan.")

            import plotly.graph_objects as go
            import math

            edges = rules.head(min(20, len(rules)))
            nodes = list(set(edges['antecedents_str'].tolist() + edges['consequents_str'].tolist()))
            node_idx = {n: i for i, n in enumerate(nodes)}

            angle_step = 2 * math.pi / len(nodes) if len(nodes) > 0 else 0
            node_x = [math.cos(i * angle_step) for i in range(len(nodes))]
            node_y = [math.sin(i * angle_step) for i in range(len(nodes))]

            edge_x, edge_y = [], []
            for _, row in edges.iterrows():
                x0, y0 = node_x[node_idx[row['antecedents_str']]], node_y[node_idx[row['antecedents_str']]]
                x1, y1 = node_x[node_idx[row['consequents_str']]], node_y[node_idx[row['consequents_str']]]
                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

            fig_net = go.Figure()
            fig_net.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines',
                                         line=dict(width=1, color='#888'), hoverinfo='none'))
            fig_net.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers+text',
                                         text=nodes, textposition='top center',
                                         marker=dict(size=20, color=list(range(len(nodes))),
                                                     colorscale='Viridis', line=dict(width=2, color='white')),
                                         hoverinfo='text'))
            fig_net.update_layout(showlegend=False, height=500, margin=dict(t=10, b=10, l=10, r=10),
                                  xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                  yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
            st.plotly_chart(fig_net, use_container_width=True)
            st.markdown("---")

        # ── SECTION 7: Interpretasi Otomatis Rules ──
        section_num += 1
        st.markdown(f"### :material/lightbulb: {section_num}. Interpretasi & Kesimpulan Akhir")

        if rules is not None and not rules.empty:
            avg_conf = rules['confidence'].mean() * 100
            avg_lift = rules['lift'].mean()
            strong_rules = rules[rules['lift'] > 1]
            weak_rules = rules[rules['lift'] <= 1]

            st.write(f"Dari total **{len(rules)}** aturan asosiasi yang berhasil diekstrak:")
            st.write(f"- **{len(strong_rules)}** aturan memiliki *Lift* > 1 (**hubungan positif** -- produk saling memperkuat pembelian)")
            st.write(f"- **{len(weak_rules)}** aturan memiliki *Lift* <= 1 (hubungan lemah/independen)")
            st.write(f"- Rata-rata *Confidence*: **{avg_conf:.1f}%**")
            st.write(f"- Rata-rata *Lift*: **{avg_lift:.2f}x**")

            st.markdown("#### Rekomendasi Strategis Berdasarkan Data:")
            if len(strong_rules) > 0:
                best = strong_rules.iloc[0]
                st.success(f":material/target: **Bundling Utama:** Gabungkan **{best['antecedents_str']}** dengan **{best['consequents_str']}** "
                           f"dalam satu paket promo. Confidence {best['confidence']*100:.1f}% berarti {best['confidence']*100:.0f} dari 100 "
                           f"pembeli {best['antecedents_str']} juga akan membeli {best['consequents_str']}.")

            st.markdown("**Strategi Paket Combo & Menu Bundling:**")
            if len(strong_rules) >= 2:
                for i in range(min(3, len(strong_rules))):
                    r = strong_rules.iloc[i]
                    st.write(f"  {i+1}. Buat **Paket Combo** yang menggabungkan **{r['antecedents_str']}** + **{r['consequents_str']}** "
                             f"dengan harga spesial (Lift: {r['lift']:.2f}x, Confidence: {r['confidence']*100:.1f}%)")

            st.markdown("**Strategi Suggestive Selling (Penawaran di Kasir/Counter):**")
            if len(strong_rules) > 0:
                best_sg = strong_rules.iloc[0]
                st.write(f"- Latih kasir/barista untuk menawarkan **{best_sg['consequents_str']}** setiap kali pelanggan memesan **{best_sg['antecedents_str']}**. "
                         f"Data menunjukkan **{best_sg['confidence']*100:.0f}%** pembeli {best_sg['antecedents_str']} juga membeli {best_sg['consequents_str']}.")
            st.write("- Pasang *tent card* atau *table standee* di meja/counter yang mempromosikan kombinasi produk terkuat.")
            st.write("- Tampilkan menu combo di posisi paling terlihat pada *menu board* (papan menu) atau etalase.")

            st.markdown("**Strategi Etalase & Display Produk:**")
            if len(strong_rules) >= 2:
                for i in range(min(3, len(strong_rules))):
                    r = strong_rules.iloc[i]
                    st.write(f"  {i+1}. Posisikan **{r['antecedents_str']}** dan **{r['consequents_str']}** berdekatan di etalase/display "
                             f"agar pelanggan mudah mengambil keduanya saat memilih (Lift: {r['lift']:.2f}x)")

            st.markdown("**Strategi Pemasaran Digital & Promosi:**")
            st.write("- Gunakan aturan asosiasi terkuat untuk sistem *recommendation engine* di platform pemesanan online (GoFood, GrabFood, dll).")
            st.write("- Tampilkan \"*Pelanggan yang memesan X juga sering memesan Y*\" pada aplikasi atau media sosial.")
            if has_temporal:
                st.write(f"- Jalankan promosi flash sale / happy hour pada pukul **{int(peak_hour['Jam']):02d}:00** saat kunjungan pelanggan paling tinggi.")
            st.write("- Buat promo *bundle* khusus di platform delivery untuk meningkatkan nilai rata-rata pesanan.")
        else:
            st.warning("Belum ada aturan asosiasi untuk diinterpretasikan. Coba turunkan parameter Minimum Support atau Minimum Confidence.")
