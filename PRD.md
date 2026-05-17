# Product Requirement Document (PRD)
## Sistem Analisis Pola Asosiasi (Market Basket Analysis) - Project UAS Data Mining

---

### 1. Informasi Umum Project
* **Nama Project:** Sistem Analisis Pola Asosiasi Penjualan (Market Basket Analysis)
* **Tujuan:** Memenuhi tugas besar Ujian Akhir Semester (UAS) Mata Kuliah Data Mining
* **Institusi:** Universitas Duta Bangsa Surakarta
* **Kelompok:** Kelompok 3 (Topik: Asosiasi)
* **Anggota Kelompok:**
  1. FEBRI SETIYANTO
  2. AHMAD AFFANDI SIKUMBANG
  3. ROYAN FIRDAUS UBAIDAH
  4. AGASTA DUAN RAHMA

---

### 2. Latar Belakang & Deskripsi Produk
Sistem ini dirancang untuk mengotomatisasi penemuan pola pembelian konsumen menggunakan teknik **Association Rule Mining**. Dengan memanfaatkan algoritma **Apriori**, sistem dapat menganalisis item-item yang sering dibeli secara bersamaan oleh pelanggan dalam satu transaksi (Market Basket Analysis). 

Produk akhir berupa aplikasi web interaktif berbasis **Python (Streamlit)** yang memungkinkan pengguna (pemilik toko/dosen penguji) untuk mengunggah dataset transaksi, mengatur parameter batasan metrik penambangan data (*Support* dan *Confidence*), serta melihat pola asosiasi yang terbentuk secara *real-time*.

---

### 3. Lingkup Kerja & Target Dataset
Sistem dirancang secara modular dan fokus pada satu studi kasus utama yang intuitif dan mudah dipresentasikan:
* **Kasus Utama:** Pola transaksi pada Toko Roti & Kopi (Bakery Shop).
* **Dataset Target:** *"The Bread Basket" Dataset* (Kaggle).
* **Atribut Dataset Minimal:**
  * `Transaction`: ID unik untuk setiap keranjang belanja/transaksi.
  * `Item`: Nama produk atau barang yang dibeli dalam transaksi tersebut.

---

### 4. Kebutuhan Fungsional (Functional Requirements)

#### FR-1: Manajemen Environment dan Dependensi
* Sistem harus diisolasi dalam *Virtual Environment* (`venv`) untuk menjaga dependensi global sistem operasi tetap bersih.
* Menyediakan konfigurasi multi-OS (Pop!_OS/Linux dan Windows 11).

#### FR-2: Manajemen Input Data (File Uploader)
* Sistem harus menyediakan antarmuka untuk mengunggah berkas dataset berformat `.csv` melalui komponen *sidebar*.
* Sistem harus menampilkan pratinjau data mentah (*Preview Data*) sebanyak 5 baris pertama segera setelah berkas berhasil diunggah.

#### FR-3: Konfigurasi Parameter Algoritma (Dynamic Hyperparameters)
* Menyediakan kontrol interaktif (*slider*) pada *sidebar* untuk menentukan:
  * **Minimum Support:** Rentang nilai $0.01$ hingga $0.50$ (Default: $0.05$, kenaikan langkah: $0.01$).
  * **Minimum Confidence:** Rentang nilai $0.1$ hingga $1.0$ (Default: $0.5$, kenaikan langkah: $0.1$).

#### FR-4: Transformasi & Preprocessing Data Otomatis
* Sistem harus mentransformasikan data bertipe transaksional baris tunggal menjadi bentuk matriks biner beraliran *One-Hot Encoded*.
* Melakukan agregasi data berdasarkan `Transaction` dan `Item`.
* Mengubah representasi jumlah item menjadi nilai biner ($1$ jika item dibeli dalam transaksi, $0$ jika tidak).
* *Constraint Teknis:* Wajib menggunakan metode `.map()` pada pandas (bukan `.applymap()`) untuk menghindari *DeprecationWarning* di versi pustaka terbaru.

#### FR-5: Pemrosesan Algoritma & Penambangan Pola (Data Mining Process)
* Eksekusi pemrosesan algoritma Apriori dilakukan setelah pengguna menekan tombol *"Jalankan Analisis"*.
* Menyediakan *visual indicator* (seperti *loading spinner*) saat proses komputasi berlangsung.
* Menghasilkan tabel *Frequent Itemsets* yang memenuhi ambang batas *Minimum Support*.
* Menghasilkan aturan asosiasi (*Association Rules*) yang memenuhi ambang batas *Minimum Confidence*.

#### FR-6: Visualisasi & Output Hasil Analisis
* Menampilkan matriks hasil aturan asosiasi secara terstruktur dengan kolom wajib:
  * `antecedents` (Item yang dibeli terlebih dahulu)
  * `consequents` (Item yang menyertai)
  * `support` (Nilai popularitas kombinasi item)
  * `confidence` (Nilai kepastian hubungan antar item)
  * `lift` (Kekuatan/validitas aturan asosiasi)
* Menyediakan mekanisme penanganan *error* (*error handling* berbasis `try-except`) jika format berkas CSV tidak sesuai, sehingga aplikasi tidak mengalami *crash*.

---

### 5. Kebutuhan Non-Fungsional (Non-Functional Requirements)

#### NFR-1: Performa dan Efisiensi Komputasi
* Pemuatan dataset harus memanfaatkan mekanisme *caching* (`@st.cache_data`) agar proses *re-rendering* halaman Streamlit tidak memicu pembacaan ulang berkas dari media penyimpanan.

#### NFR-2: Portabilitas dan Skalabilitas Lingkungan Kerja
* Aplikasi harus dapat dijalankan secara konsisten pada ekosistem lokal pengembang:
  * **OS:** Dual-boot Pop!_OS 24.04 LTS atau Windows 11.
  * **Perangkat Keras:** Laptop Gaming Victus by HP 15.

#### NFR-3: Kualitas Kode (Clean Code Standard)
* Gaya penulisan kode harus modular dengan memisahkan fungsi pemrosesan data murni dari fungsi manipulasi antarmuka pengguna grafis (Streamlit).

---

### 6. Arsitektur Teknis & Stack Teknologi
* **Bahasa Pemrograman:** Python 3.10+
* **Antarmuka Sistem:** Streamlit (Pustaka Web App berbasis Python)
* **Manipulasi Data:** Pandas (Dataframe Engine)
* **Algoritma Data Mining:** Mlxtend (*Machine Learning Extensions* untuk fungsi Apriori dan Association Rules)
* **Manajer Dependensi:** Python Virtual Environment (`venv`) & `requirements.txt`

---

### 7. Alur Logika Pemrosesan Data (Data Flow)
```
[ Dataset Mentah (CSV) ] 
          │
          ▼
[ Load Data via Streamlit File Uploader ] -> Mengaktifkan Cache
          │
          ▼
[ Preprocessing & Pivot Matriks ] 
   - Groupby ('Transaction', 'Item')
   - Unstack & Fillna(0)
   - Binarization via .map() (0 atau 1)
          │
          ▼
[ Eksekusi Algoritma Apriori (mlxtend) ] -> Menghasilkan Frequent Itemsets
          │
          ▼
[ Generasi Association Rules (mlxtend) ] -> Menguji metrik Confidence & Lift
          │
          ▼
[ Render Tabel Interaktif pada UI Utama Streamlit ]
```

---

### 8. Rencana Struktur Repositori Project
```
project-uas-datamining/
├── .venv/                 # Folder isolasi virtual environment (diabaikan dari git jika perlu)
├── dataset/
│   └── BreadBasket.csv   # Berkas data mentah dari Kaggle
├── app.py                 # File kode program utama (Streamlit Application)
├── requirements.txt       # Daftar pustaka yang wajib diinstal
└── PRD.md                 # Berkas dokumentasi kebutuhan produk ini
```

---

### 9. Kerangka Kerja Pengujian Presentasi (UAS Testing Framework)
Saat melakukan demonstrasi di hadapan dosen penguji, skenario penarikan kesimpulan aturan harus difokuskan pada interpretasi tiga metrik utama:
1. **Aturan Logis:** Membuktikan nilai **Lift Metric $> 1$**, yang menandakan aturan asosiasi antara barang $X$ (antecedents) dan barang $Y$ (consequents) memiliki relasi positif yang kuat, bukan sebuah kebetulan acak.
2. **Skenario Bisnis:** Menunjukkan bagaimana pemilik toko roti dapat menyusun tata letak barang (misal: mendekatkan penempatan roti di dekat mesin kopi) atau membuat paket promo *bundling* berdasarkan nilai *Confidence* tertinggi yang dihasilkan sistem.
