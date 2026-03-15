# ⚡ Quick Start Guide

## 🚀 Setup dalam 3 Langkah

### 1️⃣ Install Dependencies

```bash
cd Project-AI-Triptrove
pip install -r requirements.txt
```

### 2️⃣ Konfigurasi Database

Edit file `.env`:
```env
DB_PASSWORD=password_anda
```

### 3️⃣ Load Data & Run

```bash
# Load data
python data_loader.py

# Jalankan aplikasi
streamlit run app.py
```

## ✅ Checklist Sebelum Mulai

- [ ] Python 3.8+ terinstall
- [ ] Ollama terinstall dan berjalan
- [ ] Model sudah di-pull: `ollama pull llama3.1` dan `ollama pull nomic-embed-text`
- [ ] MySQL/MariaDB berjalan dengan database `triptrove_db`
- [ ] File `.env` sudah dikonfigurasi

## 🎯 Cara Pakai (Super Simple)

1. Buka browser ke `http://localhost:8501`
2. Klik "Inisialisasi Agent" di sidebar
3. Ketik pertanyaan, contoh: "Paket tour apa saja yang tersedia?"
4. Selesai! 🎉

## 🆘 Troubleshooting Cepat

**Error saat load data?**
→ Cek password database di `.env`

**Agent tidak bisa diinisialisasi?**
→ Pastikan Ollama berjalan: `ollama serve`

**UI tidak muncul?**
→ Coba: `streamlit run app.py --server.port 8502`

## 📚 Dokumentasi Lengkap

- `README.md` - Dokumentasi teknis lengkap
- `PANDUAN_PENGGUNAAN.md` - Panduan detail dalam Bahasa Indonesia

---

**Need help?** Baca dokumentasi lengkap atau buat issue di repository.
