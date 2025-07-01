# 🚀 ETL Pipeline: Fashion Data

![ETL Pipeline](https://img.shields.io/badge/ETL-Pipeline-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)
![Data Processing](https://img.shields.io/badge/Data-Processing-yellowgreen)

Proyek ini merupakan implementasi **ETL Pipeline** (Extract, Transform, Load) untuk mengumpulkan data fashion dari website Dicoding.

## 📌 Fitur Utama
- Ekstraksi data fashion dari website Dicoding
- Menyimpan data dalam 3 format berbeda:
  - **Database** (SQL)
  - **File CSV**
  - **Google Sheet**
- Data yang dikumpulkan meliputi:
  - Judul Produk
  - Harga
  - Rating
  - Warna yang tersedia
  - Ukuran
  - Kategori Gender

## 🛠 Teknologi yang Digunakan
- Python 3.8+
- BeautifulSoup/Scrapy untuk web scraping
- Pandas untuk transformasi data
- SQLAlchemy untuk koneksi database
- Google Sheets API untuk integrasi dengan Google Sheet
