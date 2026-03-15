# 📓 Notebooks - Experimentation & Testing

Folder ini berisi Jupyter notebooks untuk eksperimen, testing, dan prototyping.

## 📋 Daftar Notebooks

### 00_quick_test.ipynb
**Tujuan**: Quick test koneksi Ollama dan basic LLM
**Kapan digunakan**: Untuk memastikan setup dasar berjalan

### 01_data_exploration.ipynb
**Tujuan**: Eksplorasi data dari database dan PDF
**Kapan digunakan**: 
- Melihat data yang tersedia
- Analisis tour packages
- Cek kualitas data

### 02_rag_testing.ipynb
**Tujuan**: Test RAG system secara interaktif
**Kapan digunakan**:
- Test berbagai query
- Lihat dokumen yang di-retrieve
- Debug retrieval issues

### 03_prompt_engineering.ipynb
**Tujuan**: Eksperimen dengan berbagai prompt
**Kapan digunakan**:
- Improve prompt quality
- Test different prompt strategies
- A/B testing prompts

### 04_fine_tuning_experiments.ipynb
**Tujuan**: Eksperimen fine-tuning
**Kapan digunakan**:
- Test training data quality
- Evaluate fine-tuned models
- Compare before/after

## 🚀 Cara Menggunakan

### 1. Install Jupyter
```bash
pip install jupyter notebook
```

### 2. Jalankan Jupyter
```bash
jupyter notebook
```

### 3. Buka notebook yang diinginkan
Browser akan terbuka otomatis, pilih notebook dari list

## 💡 Tips

1. **Run cells sequentially** - Jangan skip cells
2. **Restart kernel** jika ada error aneh
3. **Save often** - Ctrl+S atau Command+S
4. **Clear output** sebelum commit ke git

## 📝 Best Practices

- ✅ Gunakan markdown cells untuk dokumentasi
- ✅ Clear output sebelum commit
- ✅ Jangan commit data sensitif
- ✅ Test di notebook, production di .py

## 🔄 Workflow

```
Eksperimen di notebook → Berhasil → Convert ke .py → Production
```

---

**Happy Experimenting! 🧪**
