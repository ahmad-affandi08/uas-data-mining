# 🛒 Sistem Analisis Pola Asosiasi Penjualan (Market Basket Analysis)

Sistem ini dirancang untuk mengotomatisasi penemuan pola pembelian konsumen menggunakan teknik **Association Rule Mining**. Dengan memanfaatkan algoritma **Apriori**, sistem dapat menganalisis item-item yang sering dibeli secara bersamaan oleh pelanggan dalam satu transaksi (Market Basket Analysis).

Proyek ini dibuat untuk memenuhi **Tugas Besar Ujian Akhir Semester (UAS) Mata Kuliah Data Mining**, Universitas Duta Bangsa Surakarta.

## 👥 Kelompok 3 (Topik: Asosiasi)
1. FEBRI SETIYANTO
2. AHMAD AFFANDI SIKUMBANG
3. ROYAN FIRDAUS UBAIDAH
4. AGASTA DUAN RAHMA

---

## ✨ Fitur Utama
1. **Upload Dataset Otomatis**: Pengguna dapat mengunggah dataset transaksi berformat CSV.
2. **Kustomisasi Parameter**: Terdapat penggeser (*slider*) untuk mengatur parameter minimum *Support* dan minimum *Confidence*.
3. **Data Preprocessing & One-Hot Encoding**: Otomatis mengubah data baris tunggal menjadi matriks biner untuk proses Apriori (menggunakan `.map()`).
4. **Eksekusi Penambangan Pola Real-time**: Menghasilkan *Frequent Itemsets* dan *Association Rules* yang memenuhi parameter input.
5. **Interpretasi Bisnis Otomatis**: Menampilkan *insight* dan rekomendasi penempatan produk berdasarkan nilai *Lift* terbesar.
6. **Performa dengan Caching**: Menggunakan fitur *cache* untuk menghindari *reload* memori setiap kali interaksi terjadi di dalam antarmuka.

---

## 🛠️ Stack Teknologi
* **Bahasa Pemrograman:** Python 3.10+
* **Antarmuka Web:** Streamlit
* **Manipulasi Data:** Pandas
* **Algoritma Data Mining:** Mlxtend
* **Manajemen Kontainer:** Docker & Docker Compose

---

## 🚀 Cara Menjalankan Aplikasi

Aplikasi ini dapat dijalankan menggunakan **Docker** (Direkomendasikan) atau menggunakan **Python Virtual Environment** (Konvensional).

### Opsi 1: Menggunakan Docker (Rekomendasi)
Sistem sudah dikonfigurasi sepenuhnya ke dalam *container* menggunakan Docker untuk menghindari konflik *environment* lokal.
Pastikan Docker dan Docker Compose telah terinstal di sistem Anda.

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
Jika Anda tidak memiliki Docker, ikuti langkah berikut:

1. Buka *terminal* dan buat Virtual Environment:
   ```bash
   python -m venv .venv
   ```
2. Aktivasi Virtual Environment:
   - **Linux / Pop!_OS:** `source .venv/bin/activate`
   - **Windows:** `.venv\Scripts\activate`
3. Instal semua dependensi yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi Streamlit:
   ```bash
   streamlit run app.py
   ```
5. Akses aplikasi melalui tautan *Local URL* (biasanya http://localhost:8501) yang muncul di layar terminal.

---

## 💡 Cara Penggunaan Aplikasi
1. Setelah aplikasi berjalan, perhatikan panel *sidebar* di sebelah kiri layar.
2. Unggah dataset referensi (contoh: `dataset/BreadBasket.csv`) menggunakan tombol pengunggah file CSV.
3. Sesuaikan metrik pembatasan:
   - **Minimum Support**: Toleransi kepopuleran kombinasi item yang ingin ditampilkan.
   - **Minimum Confidence**: Tingkat kepercayaan atau jaminan kedekatan relasi item.
4. Klik tombol **"Jalankan Analisis"**.
5. Sistem akan memuat Pratinjau Matriks Data, *Frequent Itemsets*, serta Daftar Aturan Asosiasi (*Association Rules*) beserta nilai metrik (termasuk *Lift*).
6. Gulir (*scroll*) hingga bagian terbawah untuk melihat kotak rekomendasi yang di-generasi berdasarkan nilai *Lift* terbesar. Rekomendasi ini dapat dimanfaatkan untuk kebutuhan presentasi bisnis.

---

## 📂 Struktur Direktori Proyek
```text
project-uas-datamining/
├── dataset/
│   └── BreadBasket.csv    # Berkas sampel data mentah (dummy dataset)
├── app.py                 # File kode program utama (Streamlit Application)
├── requirements.txt       # Daftar pustaka dependensi Python
├── Dockerfile             # Konfigurasi pembuatan image untuk Docker
├── docker-compose.yml     # Konfigurasi container service
├── PRD.md                 # Berkas dokumentasi kebutuhan produk (Requirement)
└── README.md              # Dokumentasi umum proyek ini
```

---

Dibuat dengan ❤️ untuk UAS Data Mining 2026.
