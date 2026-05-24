# Sistem Analisis Pola Asosiasi Penjualan (Market Basket Analysis)

Sistem ini dirancang untuk mengotomatisasi penemuan pola pembelian konsumen menggunakan teknik **Association Rule Mining**. Dengan memanfaatkan algoritma **Apriori**, sistem dapat menganalisis item-item yang sering dibeli secara bersamaan oleh pelanggan dalam satu transaksi (Market Basket Analysis).

Proyek ini dibuat untuk memenuhi **Tugas Ujian Akhir Semester (UAS) Mata Kuliah Data Mining**, Universitas Duta Bangsa Surakarta.

## Kelompok 3 (Topik: Asosiasi)
1. FEBRI SETIYANTO
2. AHMAD AFFANDI SIKUMBANG
3. ROYAN FIRDAUS UBAIDAH
4. AGASTA DUAN RAHMA

---

## Fitur Utama

1. **Arsitektur Berbasis OOP (Clean Code)**: Kode sistem telah dipisah secara modular antara logika penanganan data (`DataHandler`), mesin algoritma *mining* (`MiningEngine`), dan rendering antarmuka (`DashboardUI`).
2. **Deteksi Otomatis Batas Parameter**: Setelah dataset diunggah, sistem secara otomatis menghitung dan menampilkan **Support tertinggi** item dan **Confidence tertinggi** rule yang tersedia, sehingga pengguna tidak perlu menebak-nebak nilai parameter.
3. **Konfigurasi Parameter Dinamis**: Slider *Minimum Support* dan *Minimum Confidence* menyesuaikan rentang secara otomatis berdasarkan data. Ketika nilai Support diubah, informasi Confidence tertinggi dihitung ulang secara real-time sesuai level Support yang dipilih.
4. **Transparansi Proses Iterasi Apriori**: Setiap iterasi (1-itemset, 2-itemset, dst.) menampilkan **seluruh kandidat** beserta statusnya -- item yang **Lolos** ditandai hijau dan yang **Tidak Lolos** ditandai merah, dilengkapi kolom Frekuensi dan Nilai Support.
5. **Pembuktian Rumus Otomatis**: Secara dinamis membedah Aturan Asosiasi Peringkat #1 menjadi rumus matematis LaTeX menggunakan frekuensi angka riil dari dataset (Support, Confidence, Lift).
6. **Dasbor Multi-Tab Interaktif**:
   - **Tab 1 -- Langkah Perhitungan**: Menampilkan alur kerja algoritma secara kronologis mulai dari transformasi data, iterasi Apriori (lengkap dengan kandidat lolos/tidak lolos), ekstraksi rule, hingga pembuktian rumus.
   - **Tab 2 -- Insight & Analisis Mendalam**: Menyajikan statistik deskriptif, produk terlaris vs kurang diminati, distribusi item per transaksi, analisis pola temporal, heatmap co-occurrence, network graph, serta interpretasi dan rekomendasi bisnis otomatis.
7. **Visualisasi Tingkat Lanjut**: Heatmap korelasi antar produk, Network Graph hubungan asosiasi, grafik temporal (per jam & per hari), serta bar chart produk terlaris -- semua menggunakan Plotly interaktif.
8. **Interpretasi & Rekomendasi Otomatis**: Sistem secara otomatis menghasilkan rekomendasi strategis (bundling produk, tata letak toko, pemasaran digital) berdasarkan aturan asosiasi yang ditemukan.

---

## Stack Teknologi
* **Bahasa Pemrograman:** Python 3.10+
* **Antarmuka Web:** Streamlit
* **Visualisasi Grafik:** Plotly Express & Plotly Graph Objects
* **Manipulasi Data:** Pandas, NumPy
* **Algoritma Data Mining:** Mlxtend (Apriori & Association Rules)
* **Manajemen Lingkungan:** Docker & Docker Compose

---

## Cara Menjalankan Aplikasi

Aplikasi ini dapat dijalankan menggunakan **Docker** (Direkomendasikan) atau menggunakan **Python Virtual Environment** (Konvensional).

### Opsi 1: Menggunakan Docker (Rekomendasi)
Sistem sudah dikonfigurasi ke dalam *container* agar kode dapat dieksekusi di OS mana pun tanpa takut dependensi bentrok.

1. Buka *terminal* di direktori proyek ini.
2. Jalankan perintah untuk *build* dan *run* container:
   ```bash
   docker compose up -d --build
   ```
3. Buka peramban (*browser*) dan akses: **http://localhost:8501**
4. Jika ingin mematikan aplikasi, jalankan:
   ```bash
   docker compose down
   ```

### Opsi 2: Menggunakan Virtual Environment (Konvensional)
Jika Anda tidak menggunakan Docker, Anda bisa menjalankannya di mesin lokal:

1. Buat Virtual Environment:
   ```bash
   python -m venv .venv
   ```
2. Aktivasi Virtual Environment:
   - **Linux / Pop!_OS:** `source .venv/bin/activate`
   - **Windows:** `.venv\Scripts\activate`
3. Instal semua dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```

---

## Panduan Penggunaan

1. **Unggah Data**: Di panel sebelah kiri, unggah file transaksi berekstensi CSV. Anda bisa mengunduh dataset studi kasus ini melalui [Kaggle: The Bread Basket](https://www.kaggle.com/datasets/mittalvasu95/the-bread-basket).
2. **Lihat Info Parameter**: Setelah data diunggah, sidebar otomatis menampilkan informasi Support tertinggi item, Top 10 item, serta jumlah transaksi. Gunakan informasi ini sebagai acuan.
3. **Atur Minimum Support**: Geser slider Support. Sistem akan langsung menampilkan informasi Confidence tertinggi dan jumlah rule yang tersedia pada level Support tersebut.
4. **Atur Minimum Confidence**: Geser slider Confidence berdasarkan informasi yang ditampilkan. Sistem akan memberi peringatan jika nilai melebihi batas.
5. **Jalankan Algoritma**: Tekan tombol "Jalankan Analisis".
6. **Tab 1 -- Langkah Perhitungan**: Gunakan tab ini untuk menjelaskan langkah matematis algoritma secara kronologis. Setiap iterasi Apriori menampilkan semua kandidat beserta status lolos/tidak lolos (hijau/merah).
7. **Tab 2 -- Insight & Analisis**: Gunakan tab ini untuk presentasi gaya eksekutif dengan statistik deskriptif, visualisasi grafik, dan rekomendasi bisnis otomatis.

---

## Struktur Modular Direktori (OOP)
Dengan mematuhi kaidah _Object-Oriented Programming_, logika utama proyek dipisahkan menjadi komponen berikut:
```text
project-uas-datamining/
├── core/
│   ├── data_handler.py    # Kelas DataHandler: Pra-pemrosesan CSV, analisis temporal, statistik deskriptif
│   └── mining_engine.py   # Kelas MiningEngine: Proses iterasi Apriori & ekstraksi Association Rules
├── ui/
│   └── dashboard.py       # Kelas DashboardUI: Komponen antarmuka (Grafik, Tabel, Insight)
├── dataset/
│   └── (file CSV)         # Berkas sampel data mentah transaksional
├── app.py                 # Titik masuk utama (Main Controller) + Deteksi parameter otomatis
├── requirements.txt       # Daftar dependensi pustaka Python
├── Dockerfile             # Skrip pembuat citra container
├── docker-compose.yml     # Konfigurasi orkestrasi container
└── README.md              # Dokumentasi teknis proyek (Berkas ini)
```

---

## Alur Kerja Sistem

```text
Upload CSV ──> Parsing & Preprocessing ──> Deteksi Batas Parameter (Support & Confidence)
                                                      │
                                                      ▼
                                          User Atur Slider Support
                                                      │
                                                      ▼
                                      Hitung Ulang Confidence Max (Real-Time)
                                                      │
                                                      ▼
                                          User Atur Slider Confidence
                                                      │
                                                      ▼
                                         Klik "Jalankan Analisis"
                                                      │
                                    ┌─────────────────┴─────────────────┐
                                    ▼                                   ▼
                         Tab 1: Langkah Perhitungan          Tab 2: Insight & Analisis
                         - One-Hot Encoding                  - Statistik Deskriptif
                         - Iterasi Apriori (Lolos/Gagal)     - Top/Bottom Produk
                         - Ekstraksi Rules                   - Distribusi Item
                         - Pembuktian Rumus LaTeX            - Analisis Temporal
                                                             - Heatmap Co-occurrence
                                                             - Network Graph
                                                             - Rekomendasi Bisnis
```

---

Dibuat untuk UAS Data Mining 2026.
