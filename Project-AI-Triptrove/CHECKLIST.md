# ✅ TripTrove RAG - Setup Checklist

Gunakan checklist ini untuk memastikan semua sudah siap.

---

## 📋 Pre-Installation Checklist

- [ ] Python 3.8+ terinstall
- [ ] Ollama terinstall
- [ ] MySQL Server terinstall dan running
- [ ] Git terinstall (optional)
- [ ] 8GB RAM minimum
- [ ] 10GB disk space tersedia

---

## 🔧 Installation Checklist

### 1. Dependencies
- [ ] `pip install -r requirements.txt` berhasil
- [ ] Tidak ada error saat install
- [ ] Semua package terinstall

### 2. Ollama Setup
- [ ] `ollama list` menampilkan list models
- [ ] `ollama pull llama3.1` berhasil
- [ ] Model llama3.1 tersedia

### 3. Database Setup
- [ ] MySQL Server running
- [ ] Database `triptrove_db` dibuat
- [ ] Import `triptrove_db (2).sql` berhasil
- [ ] Ada data di table `tour_packages`

### 4. Environment Variables
- [ ] File `.env` sudah dibuat (copy dari `.env.example`)
- [ ] `DB_HOST` diisi dengan benar
- [ ] `DB_USER` diisi dengan benar
- [ ] `DB_PASSWORD` diisi dengan benar
- [ ] `DB_NAME` diisi dengan benar

### 5. Data Loading
- [ ] `python src/data_loader.py` berhasil
- [ ] ChromaDB folder `chroma_db/` terbuat
- [ ] Tidak ada error saat loading

---

## 🚀 Testing Checklist

### 1. Basic Test
- [ ] `cd scripts` berhasil
- [ ] `run.bat` berhasil dijalankan
- [ ] Streamlit UI terbuka di browser
- [ ] Port 8501 tidak error

### 2. Agent Test
- [ ] Klik "Inisialisasi Agent" di sidebar
- [ ] Agent berhasil diinisialisasi
- [ ] Tidak ada error di console
- [ ] Status "AI Agent Aktif" muncul

### 3. Query Test
- [ ] Input query: "Paket tour apa saja yang tersedia?"
- [ ] Agent memberikan response
- [ ] Response relevan dengan data
- [ ] Tidak ada error

### 4. PDF Test (Optional)
- [ ] Ada file PDF di folder `documents/`
- [ ] Query tentang terms & conditions
- [ ] Agent menggunakan data dari PDF
- [ ] Response mencakup info dari PDF

---

## 📓 Notebooks Checklist

- [ ] `jupyter notebook` terinstall
- [ ] Bisa membuka `notebooks/` folder
- [ ] `00_quick_test.ipynb` bisa dijalankan
- [ ] `01_data_exploration.ipynb` bisa dijalankan
- [ ] Tidak ada import error

---

## 🎨 UI Variants Checklist

### Main UI (Port 8501)
- [ ] `scripts/run.bat` berhasil
- [ ] UI terbuka di http://localhost:8501
- [ ] Chat interface berfungsi
- [ ] Sidebar berfungsi

### Advanced UI (Port 8503)
- [ ] `scripts/run_advanced.bat` berhasil
- [ ] UI terbuka di http://localhost:8503
- [ ] Export chat berfungsi
- [ ] Multi-language berfungsi

### Analytics Dashboard (Port 8502)
- [ ] `scripts/run_dashboard.bat` berhasil
- [ ] Dashboard terbuka di http://localhost:8502
- [ ] Charts tampil
- [ ] Data analytics berfungsi

---

## 🎓 Fine-Tuning Checklist

### Few-Shot Learning (Default)
- [ ] Few-shot examples aktif di `agent_rag.py`
- [ ] Response quality sudah bagus
- [ ] Tidak perlu training tambahan

### LoRA Fine-Tuning (Optional)
- [ ] `python fine_tuning/prepare_training_data.py` berhasil
- [ ] File `training_data.jsonl` terbuat
- [ ] `python fine_tuning/fine_tune_lora.py` berhasil (jika dijalankan)
- [ ] Model fine-tuned tersimpan

---

## 📊 Performance Checklist

- [ ] Response time < 5 detik
- [ ] Retrieval menemukan dokumen relevan
- [ ] Response quality bagus
- [ ] Tidak ada memory leak
- [ ] CPU usage normal

---

## 🐛 Troubleshooting Checklist

Jika ada masalah, cek:

### Ollama Issues
- [ ] `ollama serve` running
- [ ] `ollama list` menampilkan llama3.1
- [ ] Port 11434 tidak digunakan app lain

### Database Issues
- [ ] MySQL service running
- [ ] Credentials di `.env` benar
- [ ] Database `triptrove_db` ada
- [ ] Table `tour_packages` ada dan berisi data

### Import Issues
- [ ] Semua dependencies terinstall
- [ ] Python version 3.8+
- [ ] Virtual environment aktif (jika pakai)

### Port Issues
- [ ] Port 8501 tidak digunakan app lain
- [ ] Port 8502 tidak digunakan app lain
- [ ] Port 8503 tidak digunakan app lain

---

## ✨ Optional Features Checklist

- [ ] PDF documents ditambahkan ke `documents/`
- [ ] Custom few-shot examples ditambahkan
- [ ] Analytics tracking aktif
- [ ] Export chat history berfungsi
- [ ] Multi-language support tested

---

## 📝 Documentation Checklist

- [ ] Baca `START_HERE.md`
- [ ] Baca `README.md`
- [ ] Baca `docs/00_BACA_INI_DULU.txt`
- [ ] Baca `docs/QUICK_START.md`
- [ ] Pahami struktur project

---

## 🎯 Production Ready Checklist

- [ ] Semua tests passed
- [ ] Performance acceptable
- [ ] Error handling works
- [ ] Documentation complete
- [ ] Code clean and organized
- [ ] Ready for deployment

---

## 🎉 Final Check

Jika semua checklist di atas ✅, maka:

**🎊 CONGRATULATIONS! 🎊**

Project TripTrove RAG Anda sudah siap digunakan!

---

## 📞 Need Help?

Jika ada yang tidak ✅:
1. Cek `docs/INSTALASI_LENGKAP.md`
2. Jalankan `python scripts/check_system.py`
3. Lihat error message dengan teliti
4. Cek troubleshooting section di dokumentasi

---

**Good luck! 🚀**
