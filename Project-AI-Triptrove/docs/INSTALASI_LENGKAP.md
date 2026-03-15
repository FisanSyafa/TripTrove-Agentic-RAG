# 🔧 Panduan Instalasi Lengkap TripTrove RAG

Panduan step-by-step untuk instalasi dari nol hingga siap digunakan.

---

## 📋 Daftar Isi

1. [Persiapan Sistem](#1-persiapan-sistem)
2. [Install Python](#2-install-python)
3. [Install Ollama](#3-install-ollama)
4. [Install MySQL/MariaDB](#4-install-mysqlmariadb)
5. [Setup Project](#5-setup-project)
6. [Konfigurasi](#6-konfigurasi)
7. [Load Data](#7-load-data)
8. [Jalankan Aplikasi](#8-jalankan-aplikasi)
9. [Verifikasi](#9-verifikasi)

---

## 1. Persiapan Sistem

### Spesifikasi Minimum
- **OS**: Windows 10/11, Linux, atau macOS
- **RAM**: 8 GB (16 GB recommended)
- **Storage**: 10 GB free space
- **CPU**: Intel i5 atau setara (i7 recommended)

### Spesifikasi Recommended
- **RAM**: 16 GB atau lebih
- **Storage**: SSD dengan 20 GB free space
- **CPU**: Intel i7 atau AMD Ryzen 7
- **GPU**: Optional (untuk future enhancement)

---

## 2. Install Python

### Windows

**Opsi 1: Download dari python.org**

1. Buka https://www.python.org/downloads/
2. Download Python 3.11 atau 3.12 (recommended)
3. Jalankan installer
4. ✅ **PENTING**: Centang "Add Python to PATH"
5. Klik "Install Now"

**Opsi 2: Menggunakan Microsoft Store**

1. Buka Microsoft Store
2. Cari "Python 3.11" atau "Python 3.12"
3. Klik "Get" atau "Install"

**Verifikasi:**
```bash
python --version
# Output: Python 3.11.x atau 3.12.x
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.11 python3-pip python3-venv
```

### macOS

```bash
# Menggunakan Homebrew
brew install python@3.11
```

---

## 3. Install Ollama

### Windows

1. Buka https://ollama.ai/download
2. Download "Ollama for Windows"
3. Jalankan installer
4. Ikuti wizard instalasi
5. Ollama akan berjalan otomatis di background

**Verifikasi:**
```bash
ollama --version
# Output: ollama version x.x.x
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### macOS

```bash
# Download dari website atau gunakan Homebrew
brew install ollama
```

### Pull Model yang Diperlukan

```bash
# Pull Llama 3.1 (ini akan download ~4.7 GB)
ollama pull llama3.1

# Pull Nomic Embed Text (ini akan download ~274 MB)
ollama pull nomic-embed-text
```

**Catatan**: Download mungkin memakan waktu tergantung kecepatan internet Anda.

**Verifikasi:**
```bash
ollama list
# Output harus menampilkan:
# llama3.1:latest
# nomic-embed-text:latest
```

---

## 4. Install MySQL/MariaDB

### Windows

**Opsi 1: MySQL**

1. Download MySQL Installer dari https://dev.mysql.com/downloads/installer/
2. Pilih "MySQL Installer for Windows"
3. Jalankan installer
4. Pilih "Developer Default" atau "Server only"
5. Set root password (INGAT PASSWORD INI!)
6. Selesaikan instalasi

**Opsi 2: XAMPP (Lebih Mudah)**

1. Download XAMPP dari https://www.apachefriends.org/
2. Install XAMPP
3. Buka XAMPP Control Panel
4. Start "MySQL"

### Linux (Ubuntu/Debian)

```bash
# Install MySQL
sudo apt update
sudo apt install mysql-server

# Atau install MariaDB
sudo apt install mariadb-server

# Secure installation
sudo mysql_secure_installation
```

### macOS

```bash
# Menggunakan Homebrew
brew install mysql

# Start MySQL
brew services start mysql
```

### Import Database TripTrove

1. Buka MySQL/phpMyAdmin
2. Buat database baru: `triptrove_db`
3. Import file `triptrove_db (2).sql`

**Via Command Line:**
```bash
mysql -u root -p
# Masukkan password

CREATE DATABASE triptrove_db;
exit;

# Import SQL file
mysql -u root -p triptrove_db < "path/to/triptrove_db (2).sql"
```

**Via phpMyAdmin (XAMPP):**
1. Buka http://localhost/phpmyadmin
2. Klik "New" untuk buat database
3. Nama: `triptrove_db`
4. Klik "Import"
5. Pilih file `triptrove_db (2).sql`
6. Klik "Go"

---

## 5. Setup Project

### Clone atau Download Project

**Jika menggunakan Git:**
```bash
git clone <repository-url>
cd Project-AI-Triptrove
```

**Jika download ZIP:**
1. Extract ZIP file
2. Buka Command Prompt/Terminal
3. Navigate ke folder Project-AI-Triptrove

### Install Dependencies Python

```bash
# Pastikan Anda di folder Project-AI-Triptrove
cd Project-AI-Triptrove

# Install semua dependencies
pip install -r requirements.txt
```

**Jika ada error:**
```bash
# Upgrade pip terlebih dahulu
python -m pip install --upgrade pip

# Coba install lagi
pip install -r requirements.txt
```

**Verifikasi:**
```bash
pip list
# Harus menampilkan semua package yang terinstall
```

---

## 6. Konfigurasi

### Edit File .env

1. Buka file `.env` dengan text editor
2. Edit bagian database:

```env
# Database Configuration
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=triptrove_db
DB_USER=root
DB_PASSWORD=password_anda_disini    # ⬅️ EDIT INI!

# Ollama Configuration (biasanya tidak perlu diubah)
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3.1
EMBEDDING_MODEL=nomic-embed-text
```

**Contoh:**
```env
DB_PASSWORD=mypassword123
```

### Test Koneksi Database

```bash
# Test koneksi
mysql -h 127.0.0.1 -u root -p triptrove_db
# Masukkan password
# Jika berhasil, Anda akan masuk ke MySQL prompt

# Keluar
exit;
```

---

## 7. Load Data

### Jalankan Data Loader

```bash
python data_loader.py
```

**Output yang diharapkan:**
```
📦 Loading data dari database...
✅ Loaded 6 paket tour
✅ Loaded 15 reviews
📊 Total 21 dokumen
🔄 Membuat embeddings dan menyimpan ke ChromaDB...
✅ Vector store berhasil dibuat di ./chroma_db
🎉 Selesai! Data siap digunakan untuk RAG.
```

**Jika ada error:**

1. **Error: Access denied**
   - Cek password di file `.env`
   - Pastikan MySQL berjalan

2. **Error: Database not found**
   - Pastikan database `triptrove_db` sudah dibuat
   - Import file SQL terlebih dahulu

3. **Error: Ollama connection**
   - Pastikan Ollama berjalan: `ollama serve`
   - Cek model sudah di-pull: `ollama list`

---

## 8. Jalankan Aplikasi

### Opsi 1: Menggunakan Script (Windows)

```bash
run.bat
```

### Opsi 2: Manual

```bash
streamlit run app.py
```

**Output yang diharapkan:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Buka Browser

Aplikasi akan otomatis terbuka di browser, atau buka manual:
```
http://localhost:8501
```

---

## 9. Verifikasi

### Checklist Verifikasi

Jalankan system checker:
```bash
python check_system.py
```

**Output yang diharapkan:**
```
🐍 Checking Python...
   ✅ Python 3.11.x

🦙 Checking Ollama...
   ✅ Ollama installed
   ✅ llama3.1 model found
   ✅ nomic-embed-text model found

📦 Checking Python dependencies...
   ✅ langchain
   ✅ langchain_ollama
   ✅ chromadb
   ✅ streamlit
   ... (dan lainnya)

⚙️  Checking configuration...
   ✅ .env file exists
   ✅ Database config found

🗄️  Checking database connection...
   ✅ Database connected (6 tour packages)

🔍 Checking vector store...
   ✅ Vector store exists (X files)

📊 Summary
✅ Python
✅ Ollama
✅ Dependencies
✅ Configuration
✅ Database
✅ Vector Store

🎉 All checks passed! System ready to use.
```

### Test Agent

```bash
python test_agent.py
```

Coba tanyakan:
```
Paket tour apa saja yang tersedia?
```

Jika agent menjawab dengan baik, instalasi berhasil! 🎉

---

## 🎯 Langkah Selanjutnya

Setelah instalasi berhasil:

1. **Baca Panduan Penggunaan**
   ```
   PANDUAN_PENGGUNAAN.md
   ```

2. **Explore UI**
   - Basic UI: `streamlit run app.py`
   - Advanced UI: `streamlit run advanced_app.py`
   - Dashboard: `streamlit run dashboard.py`

3. **Customize**
   - Edit `config.py` untuk settings
   - Edit `app.py` untuk UI
   - Edit `agent_rag.py` untuk agent logic

---

## 🆘 Troubleshooting

### Problem: Python tidak ditemukan

**Solusi:**
```bash
# Windows: Tambahkan Python ke PATH
# 1. Cari "Environment Variables" di Windows Search
# 2. Edit "Path" di System Variables
# 3. Tambahkan path Python (contoh: C:\Python311)
```

### Problem: pip tidak ditemukan

**Solusi:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Problem: Ollama tidak berjalan

**Solusi:**
```bash
# Windows: Buka Task Manager, cari "Ollama"
# Jika tidak ada, jalankan Ollama dari Start Menu

# Linux/Mac:
ollama serve
```

### Problem: MySQL tidak bisa connect

**Solusi:**
```bash
# Cek MySQL berjalan
# Windows (XAMPP): Buka XAMPP Control Panel, start MySQL
# Linux: sudo systemctl start mysql
# Mac: brew services start mysql

# Reset password jika lupa
# Ikuti panduan: https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html
```

### Problem: ChromaDB error

**Solusi:**
```bash
# Hapus folder chroma_db
rm -rf chroma_db  # Linux/Mac
rmdir /s chroma_db  # Windows

# Load ulang data
python data_loader.py
```

### Problem: Streamlit tidak bisa diakses

**Solusi:**
```bash
# Coba port lain
streamlit run app.py --server.port 8502

# Atau buka manual di browser
http://localhost:8501
```

---

## 📞 Butuh Bantuan?

Jika masih ada masalah:

1. Baca dokumentasi lengkap di `README.md`
2. Cek `PANDUAN_PENGGUNAAN.md`
3. Jalankan `python check_system.py` untuk diagnosa
4. Buat issue di repository dengan detail error

---

## ✅ Checklist Instalasi

Gunakan checklist ini untuk memastikan semua langkah sudah dilakukan:

- [ ] Python 3.8+ terinstall
- [ ] Ollama terinstall
- [ ] Model llama3.1 sudah di-pull
- [ ] Model nomic-embed-text sudah di-pull
- [ ] MySQL/MariaDB terinstall dan berjalan
- [ ] Database triptrove_db sudah dibuat
- [ ] File SQL sudah di-import
- [ ] Dependencies Python sudah terinstall
- [ ] File .env sudah dikonfigurasi
- [ ] Data sudah di-load ke ChromaDB
- [ ] Aplikasi bisa dijalankan
- [ ] Agent bisa menjawab pertanyaan

---

**Selamat! Anda berhasil menginstall TripTrove RAG System! 🎉**

Sekarang Anda siap menggunakan AI Assistant yang 100% gratis dan lokal!
