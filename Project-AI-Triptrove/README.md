# 🏝️ TripTrove Agentic RAG System

Sistem AI Assistant untuk platform booking tour travel menggunakan **100% teknologi lokal dan gratis**.

## 🎯 Fitur Utama

- 🤖 **Agentic RAG** dengan LangGraph
- 🧠 **Llama 3.1** via Ollama (100% lokal)
- 🔍 **ChromaDB** vector store
- 📊 **Hybrid Data Source**: MySQL Database + PDF Documents
- 🌐 **Web Search** integration (DuckDuckGo)
- 🎓 **Few-Shot Learning** terintegrasi
- 💯 **100% Gratis & Lokal** - No API costs!

## 📁 Struktur Project

```
Project-AI-Triptrove/
├── src/                      # Source code utama
│   ├── agent_rag.py         # Main RAG agent
│   ├── data_loader.py       # Hybrid data loader (DB + PDF)
│   ├── config.py            # Konfigurasi
│   ├── utils.py             # Utility functions
│   ├── analytics.py         # Analytics & monitoring
│   └── ui/                  # User interfaces
│       ├── app.py           # Main Streamlit UI
│       ├── dashboard.py     # Analytics dashboard
│       └── advanced_app.py  # Advanced UI with features
│
├── notebooks/               # Jupyter notebooks untuk eksperimen
│   ├── 00_quick_test.ipynb           # Quick testing
│   ├── 01_data_exploration.ipynb     # Data analysis
│   ├── 02_rag_testing.ipynb          # RAG system testing
│   ├── 03_prompt_engineering.ipynb   # Prompt optimization
│   ├── 04_fine_tuning_experiments.ipynb  # Fine-tuning
│   └── README.md
│
├── fine_tuning/             # Fine-tuning scripts
│   ├── few_shot_examples.py      # Few-shot learning examples
│   ├── prepare_training_data.py  # Training data generator
│   ├── fine_tune_lora.py         # LoRA fine-tuning
│   └── README.md
│
├── scripts/                 # Utility scripts
│   ├── setup.bat           # Setup script
│   ├── run.bat             # Run application
│   ├── test_agent.py       # Test agent in terminal
│   └── check_system.py     # System requirements check
│
├── docs/                    # Dokumentasi lengkap
│   ├── 00_BACA_INI_DULU.txt
│   ├── MULAI_DISINI.md
│   ├── QUICK_START.md
│   ├── PANDUAN_PENGGUNAAN.md
│   ├── INSTALASI_LENGKAP.md
│   ├── ARCHITECTURE.md
│   ├── HYBRID_RAG_GUIDE.md
│   ├── FINE_TUNING_COMPLETE_GUIDE.md
│   ├── STRUKTUR_PROJECT.txt
│   ├── PROJECT_SUMMARY.md
│   └── CHANGELOG.md
│
├── documents/               # PDF documents untuk RAG
│   ├── general-terms-conditions-en-id.pdf
│   └── README.md
│
├── .env                     # Environment variables
├── .env.example            # Template environment variables
├── requirements.txt        # Python dependencies
└── triptrove_db (2).sql   # Database schema

```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Ollama dengan model llama3.1
- MySQL Server
- Git

### 2. Installation

```bash
# Clone repository
git clone <repository-url>
cd Project-AI-Triptrove

# Install dependencies
pip install -r requirements.txt

# Setup database
mysql -u root -p < "triptrove_db (2).sql"

# Configure environment
copy .env.example .env
# Edit .env dengan database credentials Anda
```

### 3. Setup Data

```bash
# Load data ke ChromaDB
cd scripts
setup.bat
```

### 4. Run Application

```bash
# Run Streamlit UI
cd scripts
run.bat

# Atau manual
streamlit run src/ui/app.py
```

## 📚 Dokumentasi

Baca dokumentasi lengkap di folder `docs/`:

1. **Mulai dari sini**: `docs/00_BACA_INI_DULU.txt`
2. **Quick Start**: `docs/QUICK_START.md`
3. **Panduan Lengkap**: `docs/PANDUAN_PENGGUNAAN.md`
4. **Instalasi Detail**: `docs/INSTALASI_LENGKAP.md`
5. **Arsitektur**: `docs/ARCHITECTURE.md`

## 🧪 Eksperimen dengan Notebooks

Gunakan Jupyter notebooks untuk eksperimen:

```bash
# Install Jupyter
pip install jupyter

# Run Jupyter
jupyter notebook notebooks/
```

Notebooks yang tersedia:
- `00_quick_test.ipynb` - Quick testing
- `01_data_exploration.ipynb` - Analisis data
- `02_rag_testing.ipynb` - Test RAG system
- `03_prompt_engineering.ipynb` - Optimasi prompt
- `04_fine_tuning_experiments.ipynb` - Fine-tuning

## 🎓 Fine-Tuning

Sistem sudah menggunakan **Few-Shot Learning** secara default. Untuk fine-tuning lebih lanjut:

```bash
cd fine_tuning
python fine_tune_lora.py
```

Lihat `fine_tuning/README.md` untuk detail lengkap.

## 🔧 Konfigurasi

Edit `src/config.py` untuk mengubah:
- Model LLM
- Temperature
- Top K results
- Vector store path
- Dan lainnya

## 📊 Monitoring

Jalankan analytics dashboard:

```bash
streamlit run src/ui/dashboard.py
```

## 🛠️ Tech Stack

- **LLM**: Llama 3.1 via Ollama
- **Framework**: LangChain + LangGraph
- **Vector DB**: ChromaDB
- **Database**: MySQL
- **UI**: Streamlit
- **PDF Processing**: PyPDF2
- **Web Search**: DuckDuckGo

## 📝 Environment Variables

```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=triptrove_db

# LLM
LLM_MODEL=llama3.1
LLM_TEMPERATURE=0.3

# Vector Store
VECTOR_STORE_PATH=./chroma_db
TOP_K_RESULTS=8
```

## 🤝 Contributing

Contributions are welcome! Please read the documentation first.

## 📄 License

This project is for educational purposes.

## 🆘 Troubleshooting

Jika mengalami masalah:

1. Cek `docs/INSTALASI_LENGKAP.md`
2. Jalankan `python scripts/check_system.py`
3. Pastikan Ollama running: `ollama list`
4. Cek database connection di `.env`

## 📞 Support

Untuk bantuan lebih lanjut, lihat dokumentasi di folder `docs/`.

---

**Made with ❤️ using 100% Free & Open Source Technology**
