# 🔄 Hybrid RAG System Guide

## Apa itu Hybrid RAG?

Sistem ini menggabungkan 2 sumber data:
1. **Database MySQL** - Data dinamis (tour packages, reviews)
2. **PDF Documents** - Dokumentasi statis (guides, policies)

## 🎯 Keuntungan Hybrid Approach

### Database
- ✅ Real-time data
- ✅ Terstruktur
- ✅ Mudah di-update

### PDF
- ✅ Dokumentasi lengkap
- ✅ Konten rich text
- ✅ Tidak perlu database

## 📁 Struktur Folder

```
Project-AI-Triptrove/
├── documents/          # Letakkan PDF di sini
│   ├── README.md
│   └── *.pdf          # File PDF Anda
├── chroma_db/         # Vector store (auto-generated)
└── data_loader.py     # Script untuk load data
```

## 🚀 Cara Menggunakan

### 1. Tambahkan PDF (Optional)

Letakkan file PDF di folder `documents/`:
- terms-and-conditions.pdf
- travel-guide.pdf
- faq.pdf
- dll.

### 2. Load Data

```bash
python data_loader.py
```

Output:
```
📦 HYBRID DATA LOADING: Database + PDF
🗄️  Loading data dari MySQL database...
✅ Loaded X paket tour dari database
✅ Loaded X reviews dari database
📄 Loading data dari PDF documents...
✅ Loaded X chunks dari PDF
📊 TOTAL: X dokumen
```

### 3. Jalankan Aplikasi

```bash
streamlit run app.py
```

## 💡 Tips Penggunaan

### Untuk Database
- Data selalu up-to-date
- Tidak perlu re-index
- Otomatis sync

### Untuk PDF
- Tambahkan PDF baru kapan saja
- Re-run `data_loader.py` untuk update
- Hapus `chroma_db/` jika perlu fresh start

## 📝 Contoh Use Case

### TripTrove dengan PDF:
1. **Database**: Tour packages, prices, availability
2. **PDF**: Terms & conditions, travel guides, safety info

### Pertanyaan yang Bisa Dijawab:
- "Apa syarat dan ketentuan booking?" → Dari PDF
- "Berapa harga tour Bali?" → Dari Database
- "Panduan perjalanan ke Yogyakarta?" → Dari PDF
- "Review tour Borobudur?" → Dari Database

## 🔧 Troubleshooting

### PDF tidak ter-load?
- Cek folder `documents/` ada file PDF
- Pastikan PDF bisa di-extract (bukan scan image)
- Lihat error message saat run data_loader.py

### Data database tidak muncul?
- Cek koneksi database di `.env`
- Test: `mysql -u root -p triptrove_db`

### Vector store error?
- Hapus folder `chroma_db/`
- Run ulang `python data_loader.py`

## 📊 Monitoring

Cek berapa dokumen yang ter-index:
```python
from data_loader import TripTroveDataLoader
loader = TripTroveDataLoader()
# Lihat output saat create_vector_store()
```

---

**Status**: Hybrid RAG System Ready! 🎉
