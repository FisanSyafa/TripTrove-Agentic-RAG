# 🚀 START HERE - TripTrove RAG

## ⚡ Quick Start (5 Menit)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Database
```bash
# Import database
mysql -u root -p < "triptrove_db (2).sql"

# Edit .env file
copy .env.example .env
# Isi dengan database credentials Anda
```

### 3️⃣ Setup Data
```bash
cd scripts
setup.bat
```

### 4️⃣ Run Application
```bash
# Main UI
run.bat

# Advanced UI (port 8503)
run_advanced.bat

# Analytics Dashboard (port 8502)
run_dashboard.bat
```

---

## 📁 Struktur Project

```
Project-AI-Triptrove/
├── src/              # Source code
├── notebooks/        # Jupyter notebooks untuk eksperimen
├── scripts/          # Utility scripts
├── docs/             # Dokumentasi lengkap
├── fine_tuning/      # Fine-tuning scripts
└── documents/        # PDF files untuk RAG
```

---

## 🎯 Apa yang Bisa Dilakukan?

### 1. Main Application (Streamlit UI)
```bash
cd scripts
run.bat
```
- Chat dengan AI assistant
- Tanya tentang tour packages
- Cari rekomendasi
- Lihat harga dan detail

### 2. Eksperimen dengan Notebooks
```bash
jupyter notebook notebooks/
```
- `01_data_exploration.ipynb` - Analisis data
- `02_rag_testing.ipynb` - Test RAG system
- `03_prompt_engineering.ipynb` - Optimasi prompt
- `04_fine_tuning_experiments.ipynb` - Fine-tuning

### 3. Analytics Dashboard
```bash
cd scripts
run_dashboard.bat
```
- Monitor performance
- Lihat statistik query
- Track errors
- Analyze trends

### 4. Advanced UI
```bash
cd scripts
run_advanced.bat
```
- Export chat history
- Multi-language support
- Statistics tracking
- Advanced features

---

## 📚 Dokumentasi Lengkap

Baca dokumentasi di folder `docs/`:

1. **Mulai**: `docs/00_BACA_INI_DULU.txt`
2. **Quick Start**: `docs/QUICK_START.md`
3. **Panduan**: `docs/PANDUAN_PENGGUNAAN.md`
4. **Instalasi**: `docs/INSTALASI_LENGKAP.md`
5. **Arsitektur**: `docs/ARCHITECTURE.md`

---

## 🎓 Fine-Tuning

System sudah menggunakan **Few-Shot Learning** (aktif secara default).

Untuk fine-tuning lebih lanjut:
```bash
cd fine_tuning
python fine_tune_lora.py
```

Lihat: `docs/FINE_TUNING_COMPLETE_GUIDE.md`

---

## 🛠️ Tech Stack

- 🤖 **LLM**: Llama 3.1 (Ollama)
- 🔍 **Vector DB**: ChromaDB
- 📊 **Database**: MySQL
- 🎨 **UI**: Streamlit
- 🧠 **Framework**: LangChain + LangGraph
- 💯 **100% Gratis & Lokal!**

---

## ⚠️ Prerequisites

- ✅ Python 3.8+
- ✅ Ollama dengan model llama3.1
- ✅ MySQL Server
- ✅ 8GB RAM minimum

---

## 🆘 Troubleshooting

### Ollama Error
```bash
# Check Ollama
ollama list

# Pull model jika belum ada
ollama pull llama3.1
```

### Database Error
```bash
# Cek .env file
# Pastikan credentials benar
```

### Import Error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Main app uses port 8501
# Advanced app uses port 8503
# Dashboard uses port 8502
```

---

## 🎯 Next Steps

1. ✅ Setup selesai? → Jalankan `run.bat`
2. 🧪 Mau eksperimen? → Buka notebooks
3. 📊 Lihat analytics? → Jalankan `run_dashboard.bat`
4. 🎓 Improve AI? → Lihat fine-tuning guide

---

## 📞 Need Help?

- Cek `docs/` folder untuk dokumentasi lengkap
- Jalankan `python scripts/check_system.py` untuk cek system
- Lihat `docs/INSTALASI_LENGKAP.md` untuk troubleshooting

---

**Happy Coding! 🏝️**
