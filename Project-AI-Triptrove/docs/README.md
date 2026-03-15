# 🏝️ TripTrove Agentic RAG System

Sistem AI Assistant untuk TripTrove yang 100% gratis dan berjalan secara lokal menggunakan teknologi open-source.

## 🎯 Fitur Utama

- **Agentic RAG**: AI yang bisa berpikir dan mengulang pencarian jika diperlukan
- **100% Lokal**: Tidak ada biaya API, semua berjalan di komputer Anda
- **Multi-Source**: Mengambil data dari database dan web search
- **User-Friendly UI**: Interface yang mudah digunakan dengan Streamlit
- **Bahasa Indonesia**: Mendukung percakapan dalam Bahasa Indonesia

## 🛠️ Teknologi yang Digunakan

- **LLM**: Llama 3.1 (via Ollama)
- **Embedding**: Nomic-Embed-Text (via Ollama)
- **Vector DB**: ChromaDB
- **Framework**: LangChain + LangGraph
- **Web Search**: DuckDuckGo Search
- **UI**: Streamlit
- **Database**: MySQL

## 📋 Prasyarat

1. **Ollama** sudah terinstall
2. **Python 3.8+** terinstall
3. **MySQL/MariaDB** dengan database `triptrove_db`
4. Model Ollama sudah di-pull:
   ```bash
   ollama pull llama3.1
   ollama pull nomic-embed-text
   ```

## 🚀 Instalasi

### 1. Install Dependencies

```bash
cd Project-AI-Triptrove
pip install -r requirements.txt
```

### 2. Konfigurasi Environment

Edit file `.env` sesuai dengan konfigurasi database Anda:

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=triptrove_db
DB_USER=root
DB_PASSWORD=your_password
```

### 3. Load Data ke Vector Store

Jalankan script untuk memuat data dari MySQL ke ChromaDB:

```bash
python data_loader.py
```

Output yang diharapkan:
```
📦 Loading data dari database...
✅ Loaded X paket tour
✅ Loaded X reviews
📊 Total X dokumen
🔄 Membuat embeddings dan menyimpan ke ChromaDB...
✅ Vector store berhasil dibuat di ./chroma_db
🎉 Selesai! Data siap digunakan untuk RAG.
```

### 4. Jalankan Aplikasi

```bash
streamlit run app.py
```

Aplikasi akan terbuka di browser pada `http://localhost:8501`

## 📖 Cara Menggunakan

### Melalui UI (Streamlit)

1. Buka aplikasi di browser
2. Klik tombol **"Inisialisasi Agent"** di sidebar
3. Tunggu hingga agent siap (status akan berubah menjadi hijau)
4. Ketik pertanyaan Anda di chat input
5. AI akan menjawab berdasarkan data yang tersedia

### Contoh Pertanyaan

- "Paket tour apa saja yang tersedia?"
- "Berapa harga paket tour ke Bali?"
- "Paket tour untuk keluarga dengan budget 5 juta?"
- "Review paket tour yang paling bagus?"
- "Paket tour adventure apa yang ada?"
- "Rekomendasi paket tour 3 hari 2 malam?"

### Melalui Python Script

```python
from agent_rag import TripTroveAgent

# Initialize agent
agent = TripTroveAgent()

# Query
answer = agent.query("Paket tour apa saja yang tersedia?")
print(answer)
```

## 🔄 Update Data

Jika ada perubahan data di database, jalankan kembali:

```bash
python data_loader.py
```

Ini akan memperbarui vector store dengan data terbaru.

## 🏗️ Arsitektur Sistem

```
┌─────────────────┐
│   User Input    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│         TripTrove Agent             │
│  (LangGraph Orchestration)          │
│                                     │
│  1. Analyze Query                   │
│  2. Search Database (ChromaDB)      │
│  3. Web Search (if needed)          │
│  4. Generate Answer (Llama 3.1)     │
│  5. Evaluate & Refine               │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Final Answer   │
└─────────────────┘
```

## 🎨 Fitur Agent

### 1. Query Analysis
Agent menganalisis pertanyaan untuk memahami intent dan kata kunci penting.

### 2. Database Search
Mencari dokumen relevan dari ChromaDB menggunakan similarity search.

### 3. Web Search (Conditional)
Jika diperlukan informasi terkini atau data tidak cukup, agent akan melakukan web search.

### 4. Answer Generation
Menghasilkan jawaban yang natural dan informatif dalam Bahasa Indonesia.

### 5. Self-Evaluation
Agent mengevaluasi kualitas jawabannya sendiri dan bisa mengulang pencarian jika perlu.

## 🐛 Troubleshooting

### Error: "Connection refused" saat load data

**Solusi**: Pastikan MySQL/MariaDB sudah berjalan dan kredensial di `.env` benar.

```bash
# Cek status MySQL
mysql -u root -p

# Test koneksi
mysql -h 127.0.0.1 -u root -p triptrove_db
```

### Error: "Ollama not found"

**Solusi**: Pastikan Ollama sudah terinstall dan berjalan.

```bash
# Cek Ollama
ollama list

# Jalankan Ollama (jika belum)
ollama serve
```

### Error: Model tidak ditemukan

**Solusi**: Pull model yang diperlukan.

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### UI tidak muncul

**Solusi**: Pastikan Streamlit terinstall dengan benar.

```bash
pip install --upgrade streamlit
streamlit run app.py
```

## 📊 Struktur File

```
Project-AI-Triptrove/
├── .env                    # Konfigurasi environment
├── .env.example           # Template konfigurasi
├── requirements.txt       # Dependencies Python
├── README.md             # Dokumentasi ini
├── data_loader.py        # Script load data ke ChromaDB
├── agent_rag.py          # Agentic RAG system
├── app.py                # Streamlit UI
├── chroma_db/            # Vector store (auto-generated)
└── agent_rag.ipynb       # Notebook testing
```

## 🔐 Keamanan

- Semua data disimpan lokal di komputer Anda
- Tidak ada data yang dikirim ke cloud
- Tidak ada biaya API atau tracking
- 100% privasi terjaga

## 🚀 Pengembangan Lebih Lanjut

### Menambah Sumber Data

Edit `data_loader.py` untuk menambah tabel lain:

```python
def load_custom_data(self):
    # Query data Anda
    # Buat documents
    # Return documents
    pass
```

### Menambah Tools untuk Agent

Edit `agent_rag.py` untuk menambah tools:

```python
from langchain_community.tools import YourCustomTool

self.custom_tool = YourCustomTool()
```

### Customize UI

Edit `app.py` untuk mengubah tampilan, warna, atau layout.

## 📝 Lisensi

Open Source - Bebas digunakan dan dimodifikasi.

## 🤝 Kontribusi

Silakan buat pull request atau laporkan issue jika menemukan bug.

## 📞 Support

Jika ada pertanyaan, silakan buat issue di repository ini.

---

**Dibuat dengan ❤️ menggunakan teknologi 100% gratis dan open-source**
