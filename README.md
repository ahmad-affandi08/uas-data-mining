# Sistem Analisis Pola Asosiasi Penjualan (Market Basket Analysis)

Sistem ini dirancang untuk mengotomatisasi penemuan pola pembelian konsumen menggunakan teknik **Association Rule Mining**. Dengan memanfaatkan algoritma **Apriori**, sistem dapat menganalisis item-item yang sering dibeli secara bersamaan oleh pelanggan dalam satu transaksi (Market Basket Analysis).

Proyek ini dibuat untuk memenuhi **Tugas Besar Ujian Akhir Semester (UAS) Mata Kuliah Data Mining**, Universitas Duta Bangsa Surakarta.

## Kelompok 3 (Topik: Asosiasi)
1. FEBRI SETIYANTO
2. AHMAD AFFANDI SIKUMBANG
3. ROYAN FIRDAUS UBAIDAH
4. AGASTA DUAN RAHMA

---

## Fitur Utama
1. **Arsitektur Berbasis OOP (Clean Code)**: Kode sistem telah dipisah secara modular antara logika penanganan data, mesin algoritma *mining*, dan rendering antarmuka (*UI*).
2. **Dasbor Multi-Tab Interaktif**: Memisahkan panggung presentasi ke dalam dua Tab: "Tabel Langkah Perhitungan" (untuk penguji algoritma) dan "Dasbor Eksekutif Visual" (untuk wawasan bisnis).
3. **Peta Kekuatan Aturan (Plotly Scatter Plot)**: Visualisasi tingkat lanjut yang memetakan probabilitas antara metrik *Support*, *Confidence*, dan *Lift* menggunakan titik spasial.
4. **Pembuktian Rumus Otomatis**: Secara dinamis membedah Aturan Asosiasi Peringkat #1 menjadi rumus matematis LaTeX menggunakan frekuensi angka riil dari dataset.
5. **Kustomisasi Parameter Real-Time**: Terdapat penggeser (*slider*) di sisi layar untuk mendikte nilai pembatas *Minimum Support* dan *Minimum Confidence*.

---

## Stack Teknologi
* **Bahasa Pemrograman:** Python 3.10+
* **Antarmuka Web:** Streamlit
* **Visualisasi Grafik:** Plotly Express
* **Manipulasi Data:** Pandas
* **Algoritma Data Mining:** Mlxtend
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
1. **Unggah Data**: Di panel sebelah kiri, unggah file transaksi berekstensi CSV.
2. **Atur Batas Toleransi**: Sesuaikan angka pembatas *Minimum Support* (syarat kepopuleran) dan *Minimum Confidence* (syarat kepastian).
3. **Jalankan Algoritma**: Tekan tombol "Jalankan Analisis".
4. **Tab 1 - Langkah Perhitungan**: Gunakan tab ini jika Anda ingin menjelaskan langkah matematis algoritma secara kronologis mulai dari *Data Preprocessing*, Iterasi Apriori, hingga pembuktian rumus secara numerik.
5. **Tab 2 - Visualisasi & Dasbor**: Gunakan tab ini untuk menampilkan presentasi gaya eksekutif yang hanya menampilkan kesimpulan *Top 3 Aturan Terbaik* dan rekomendasi pengaturan tata letak (*layouting*).

---

## Struktur Modular Direktori (OOP)
Dengan mematuhi kaidah _Object-Oriented Programming_, logika utama proyek dipisahkan menjadi komponen berikut:
```text
project-uas-datamining/
├── core/
│   ├── data_handler.py    # Kelas DataHandler: Pra-pemrosesan CSV mentah
│   └── mining_engine.py   # Kelas MiningEngine: Proses iterasi Apriori
├── ui/
│   └── dashboard.py       # Kelas DashboardUI: Komponen antarmuka (Grafik, Tabel)
├── dataset/
│   └── BreadBasket.csv    # Berkas sampel data mentah transaksional
├── app.py                 # Titik masuk utama (Main Controller)
├── requirements.txt       # Daftar dependensi pustaka Python
├── Dockerfile             # Skrip pembuat citra container
├── docker-compose.yml     # Konfigurasi orkestrasi container
└── README.md              # Dokumentasi teknis proyek (Berkas ini)
```

---

Dibuat untuk UAS Data Mining 2026.
