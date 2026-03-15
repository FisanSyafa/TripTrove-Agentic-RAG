# 🚀 MULAI DARI SINI

Selamat datang di **TripTrove Agentic RAG System**!

Ini adalah panduan super cepat untuk memulai dalam 5 menit.

## ✅ Checklist Persiapan

Sebelum mulai, pastikan Anda sudah punya:

- [ ] **Python 3.8+** terinstall
- [ ] **Ollama** terinstall dan berjalan
- [ ] **MySQL/MariaDB** dengan database `triptrove_db`
- [ ] Model Ollama sudah di-pull:
  ```bash
  ollama pull llama3.1
  ollama pull nomic-embed-text
  ```

## 🎯 Langkah Setup (5 Menit)

### Opsi 1: Setup Otomatis (Windows) ⚡

```bash
# Jalankan script setup
setup.bat
```

Script ini akan:
1. ✅ Cek Python
2. ✅ Install dependencies
3. ✅ Cek Ollama
4. ✅ Load data ke ChromaDB

### Opsi 2: Setup Manual 🔧

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Edit konfigurasi database
# Buka file .env dan sesuaikan password database Anda

# 3. Load data
python data_loader.py

# 4. Jalankan aplikasi
streamlit run app.py
```

## 🎮 Cara Menggunakan

### 1. Jalankan Aplikasi

**Windows:**
```bash
run.bat
```

**Manual:**
```bash
streamlit run app.py
```

### 2. Buka Browser

Aplikasi akan otomatis terbuka di: `http://localhost:8501`

### 3. Inisialisasi Agent

- Klik tombol **"🔄 Inisialisasi Agent"** di sidebar
- Tunggu hingga status berubah menjadi hijau ✅

### 4. Mulai Bertanya!

Contoh pertanyaan:
- "Paket tour apa saja yang tersedia?"
- "Berapa harga paket tour ke Bali?"
- "Rekomendasi paket tour untuk keluarga?"

## 📚 Dokumentasi Lengkap

Jika butuh informasi lebih detail:

- **README.md** - Dokumentasi teknis lengkap
- **PANDUAN_PENGGUNAAN.md** - Panduan lengkap dalam Bahasa Indonesia
- **QUICK_START.md** - Quick start guide
- **ARCHITECTURE.md** - Arsitektur sistem

## 🛠️ Tools Tambahan

### Cek Sistem

Pastikan semua komponen siap:
```bash
python check_system.py
```

### Test Agent (Terminal)

Test agent tanpa UI:
```bash
python test_agent.py
```

### Dashboard Analytics

Lihat statistik dan monitoring:
```bash
streamlit run dashboard.py
```

### Advanced UI

UI dengan fitur lebih lengkap:
```bash
streamlit run advanced_app.py
```

## ❓ Troubleshooting Cepat

### Problem: Agent tidak bisa diinisialisasi

**Solusi:**
```bash
# Pastikan Ollama berjalan
ollama serve

# Cek model sudah ada
ollama list
```

### Problem: Database connection error

**Solusi:**
1. Buka file `.env`
2. Cek username dan password database
3. Test koneksi: `mysql -u root -p triptrove_db`

### Problem: Data tidak ditemukan

**Solusi:**
```bash
# Load ulang data
python data_loader.py
```

## 🎉 Selesai!

Jika semua berjalan lancar, Anda sekarang punya:

✅ AI Assistant yang berjalan 100% lokal  
✅ Tidak ada biaya API  
✅ Privacy terjaga  
✅ Bisa dikustomisasi sesuai kebutuhan  

## 📞 Butuh Bantuan?

- Baca dokumentasi lengkap di folder ini
- Cek file PANDUAN_PENGGUNAAN.md untuk tutorial detail
- Jalankan `python check_system.py` untuk diagnosa

---

**Selamat mencoba! 🏝️**

Jika ada pertanyaan atau masalah, jangan ragu untuk bertanya!
