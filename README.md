# 📊 Analisis Data E-Commerce Dashboard

## Gambaran Umum
Proyek ini bertujuan untuk menganalisis data transaksi e-commerce guna memahami performa penjualan produk serta perilaku pelanggan. Analisis dilakukan menggunakan pendekatan eksploratif dan divisualisasikan melalui dashboard interaktif berbasis Streamlit.

Fokus utama analisis mencakup:
- Identifikasi kategori produk dengan kontribusi revenue terbesar
- Segmentasi pelanggan menggunakan metode RFM (Recency, Frequency, Monetary)
- Analisis geografis pelanggan bernilai tinggi (Big Spenders)


## Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan revenue terbesar dalam 1 tahun terakhir?
2. Bagaimana segmentasi pelanggan berdasarkan nilai RFM untuk mendukung strategi pemasaran?
3. Di wilayah mana pelanggan dengan nilai transaksi tertinggi (Big Spenders) paling banyak ditemukan?


## Struktur Direktori

Submission Analisis Data - Aura Ghifarani/
│
├── Dashboard/
│ └── Dashboard.py
│
├── Data/
│ ├── orders_dataset.csv
│ ├── order_items_dataset.csv
│ ├── products_dataset.csv
│ └── customers_dataset.csv
│
└── Proyek_Analisis_Data_Aura_Ghifarani.ipynb


## Metodologi Analisis

### 1. Data Preparation
- Menggabungkan dataset orders, order_items, products, dan customers
- Mengonversi tipe data timestamp menjadi format datetime
- Menghapus missing values untuk menjaga kualitas analisis


### 2. Analisis Revenue
- Menghitung total revenue per kategori produk
- Mengurutkan kategori berdasarkan kontribusi revenue
- Visualisasi menggunakan bar chart dan pie chart


### 3. Segmentasi Pelanggan (RFM)
- **Recency**: selisih waktu sejak transaksi terakhir
- **Frequency**: jumlah transaksi
- **Monetary**: total nilai transaksi

Langkah:
- Menggunakan data 12 bulan terakhir
- Mengelompokkan pelanggan menggunakan quantile (qcut)
- Menghasilkan skor RFM dan segmentasi pelanggan:
  - Champions
  - Loyal Customers
  - Big Spenders
  - New Customers
  - Lost Customers

### 4. Analisis Geografis
- Mengidentifikasi pelanggan dengan segmen "Big Spenders"
- Mengelompokkan berdasarkan kota dan negara bagian
- Visualisasi distribusi pelanggan bernilai tinggi


## Hasil Analisis

### Revenue Produk
- Kategori seperti **Beauty & Health**, **Watches & Gifts**, dan **Bed, Bath & Table** memiliki kontribusi revenue tertinggi
- Sebagian besar revenue terkonsentrasi pada beberapa kategori utama


### Segmentasi Pelanggan
- Terdapat variasi segmentasi pelanggan berdasarkan RFM Score
- Segmen seperti **Champions** dan **Loyal Customers** memiliki nilai strategis tinggi
- Segmen **Lost Customers** menunjukkan peluang untuk reaktivasi


### Analisis Geografis
- Pelanggan dengan nilai tinggi (Big Spenders) terkonsentrasi pada kota-kota tertentu
- Informasi ini dapat digunakan untuk strategi pemasaran berbasis lokasi


## Cara Menjalankan Dashboard

### 1. Clone Repository
```bash
git clone https://github.com/AuraGhifarani15/Analisis-Data---Aura-Ghifarani.git
cd Analisis-Data---Aura-Ghifarani
### 2. Setup Environment
python -m venv .venv
.venv\Scripts\activate
pip install streamlit pandas matplotlib seaborn
### 3. Jalankan Dashboard
cd Dashboard
streamlit run Dashboard.py
