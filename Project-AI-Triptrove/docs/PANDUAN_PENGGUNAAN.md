# 📚 Panduan Penggunaan TripTrove AI Assistant

## 🎯 Langkah-Langkah Setup (Pertama Kali)

### 1. Persiapan

Pastikan Anda sudah memiliki:
- ✅ Python 3.8 atau lebih baru
- ✅ Ollama sudah terinstall
- ✅ MySQL/MariaDB dengan database `triptrove_db`
- ✅ Model Ollama: `llama3.1` dan `nomic-embed-text`

### 2. Instalasi Otomatis (Windows)

Jalankan file `setup.bat`:

```bash
setup.bat
```

Script ini akan:
1. Mengecek Python
2. Install semua dependencies
3. Mengecek Ollama
4. Memuat data ke ChromaDB

### 3. Konfigurasi Database

Edit file `.env` dan sesuaikan dengan database Anda:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=triptrove_db
DB_USER=root
DB_PASSWORD=password_anda_disini
```

### 4. Load Data

Jika belum otomatis, jalankan manual:

```bash
python data_loader.py
```

## 🚀 Menjalankan Aplikasi

### Cara 1: Menggunakan UI (Streamlit) - RECOMMENDED

**Windows:**
```bash
run.bat
```

**Manual:**
```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser: `http://localhost:8501`

### Cara 2: Mode Terminal (Testing)

```bash
python test_agent.py
```

Mode ini untuk testing cepat tanpa UI.

## 💬 Cara Menggunakan UI

### Langkah 1: Inisialisasi Agent

1. Buka aplikasi di browser
2. Lihat sidebar di sebelah kiri
3. Klik tombol **"🔄 Inisialisasi Agent"**
4. Tunggu hingga status berubah menjadi **"✅ AI Agent Aktif"**

### Langkah 2: Mulai Bertanya

Ada 2 cara bertanya:

**Cara A: Ketik Manual**
- Ketik pertanyaan di kolom chat di bagian bawah
- Tekan Enter atau klik ikon kirim

**Cara B: Gunakan Contoh Pertanyaan**
- Lihat sidebar bagian "💡 Contoh Pertanyaan"
- Klik salah satu pertanyaan
- AI akan langsung menjawab

### Langkah 3: Lihat Jawaban

- AI akan berpikir sebentar (ada animasi loading)
- Jawaban akan muncul di chat
- Anda bisa lanjut bertanya lagi

### Langkah 4: Kelola Chat

**Hapus Riwayat:**
- Klik tombol **"🗑️ Hapus Riwayat Chat"** di sidebar
- Semua percakapan akan dihapus

## 🎯 Tips Bertanya yang Efektif

### ✅ Pertanyaan yang Baik

```
✓ "Paket tour ke Bali yang harganya di bawah 3 juta"
✓ "Rekomendasi paket tour untuk keluarga 4 orang"
✓ "Paket tour adventure dengan durasi 3 hari"
✓ "Review paket tour Bromo yang paling bagus"
✓ "Bandingkan paket tour Bali dan Lombok"
```

### ❌ Pertanyaan yang Kurang Efektif

```
✗ "Halo" (terlalu umum)
✗ "Ada apa aja?" (tidak spesifik)
✗ "Murah" (tidak lengkap)
```

## 🔍 Jenis Pertanyaan yang Bisa Dijawab

### 1. Informasi Paket Tour

```
- "Paket tour apa saja yang tersedia?"
- "Paket tour ke Bali"
- "Paket tour kategori adventure"
- "Paket tour dengan durasi 5 hari"
```

### 2. Harga dan Budget

```
- "Berapa harga paket tour ke Bali?"
- "Paket tour dengan budget 5 juta"
- "Paket tour termurah"
- "Ada diskon tidak?"
```

### 3. Rekomendasi

```
- "Rekomendasi paket tour untuk honeymoon"
- "Paket tour untuk keluarga dengan anak kecil"
- "Paket tour yang cocok untuk pemula"
- "Paket tour terbaik untuk liburan akhir tahun"
```

### 4. Review dan Rating

```
- "Review paket tour Bromo"
- "Paket tour dengan rating tertinggi"
- "Testimoni pelanggan"
- "Pengalaman orang yang sudah ikut tour"
```

### 5. Detail dan Spesifikasi

```
- "Apa saja yang termasuk dalam paket tour Bali?"
- "Itinerary paket tour 3 hari 2 malam"
- "Tingkat kesulitan paket tour Rinjani"
- "Kapasitas maksimal peserta"
```

### 6. Perbandingan

```
- "Bandingkan paket tour Bali dan Lombok"
- "Perbedaan paket tour A dan B"
- "Mana yang lebih worth it?"
```

## 🛠️ Troubleshooting

### Problem 1: Agent Tidak Bisa Diinisialisasi

**Gejala:**
```
❌ Error: Connection refused
```

**Solusi:**
1. Cek apakah Ollama berjalan:
   ```bash
   ollama list
   ```
2. Jika tidak, jalankan:
   ```bash
   ollama serve
   ```
3. Coba inisialisasi lagi

### Problem 2: Data Tidak Ditemukan

**Gejala:**
```
AI menjawab: "Maaf, saya tidak menemukan informasi..."
```

**Solusi:**
1. Pastikan data sudah di-load:
   ```bash
   python data_loader.py
   ```
2. Cek apakah folder `chroma_db` ada
3. Restart aplikasi

### Problem 3: Jawaban Lambat

**Penyebab:**
- Model Llama 3.1 memproses di CPU
- Komputer sedang sibuk

**Solusi:**
- Tunggu sebentar (normal 5-30 detik)
- Tutup aplikasi lain yang berat
- Gunakan model yang lebih kecil (edit `.env`)

### Problem 4: Database Connection Error

**Gejala:**
```
❌ Error: Access denied for user
```

**Solusi:**
1. Cek kredensial di file `.env`
2. Test koneksi manual:
   ```bash
   mysql -u root -p triptrove_db
   ```
3. Pastikan MySQL/MariaDB berjalan

### Problem 5: UI Tidak Muncul

**Solusi:**
1. Cek apakah Streamlit terinstall:
   ```bash
   pip install streamlit
   ```
2. Coba port lain:
   ```bash
   streamlit run app.py --server.port 8502
   ```
3. Buka manual di browser: `http://localhost:8501`

## 🔄 Update Data

Jika ada perubahan data di database (paket tour baru, review baru, dll):

```bash
python data_loader.py
```

Kemudian restart aplikasi.

## 📊 Monitoring

### Cek Status Ollama

```bash
ollama list
```

Output:
```
NAME              ID              SIZE      MODIFIED
llama3.1:latest   xxx             4.7 GB    2 days ago
nomic-embed-text  xxx             274 MB    2 days ago
```

### Cek Vector Store

Folder `chroma_db` harus ada dan berisi file-file database.

### Cek Logs

Streamlit akan menampilkan logs di terminal. Perhatikan jika ada error.

## 🎨 Kustomisasi

### Mengubah Model LLM

Edit file `.env`:

```env
LLM_MODEL=llama3.1:8b
# atau
LLM_MODEL=qwen2.5:7b
```

### Mengubah Jumlah Dokumen yang Dicari

Edit `agent_rag.py`, line ~120:

```python
docs = self.vectorstore.similarity_search(query, k=5)  # ubah k=5 ke k=10
```

### Mengubah Tampilan UI

Edit `app.py` bagian CSS atau layout sesuai keinginan.

## 📞 Bantuan Lebih Lanjut

Jika masih ada masalah:

1. Baca file `README.md` untuk detail teknis
2. Cek dokumentasi Ollama: https://ollama.ai/
3. Cek dokumentasi LangChain: https://python.langchain.com/

---

**Selamat menggunakan TripTrove AI Assistant! 🏝️**
