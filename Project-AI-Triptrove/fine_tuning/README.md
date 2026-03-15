# 🎓 Fine-Tuning Guide untuk TripTrove

## Apa itu Fine-Tuning?

Fine-tuning adalah proses melatih model LLM dengan data spesifik agar lebih baik dalam domain tertentu (TripTrove).

## 🎯 Tujuan Fine-Tuning

1. Model lebih paham konteks TripTrove
2. Jawaban lebih akurat dan konsisten
3. Style jawaban sesuai brand TripTrove
4. Mengurangi hallucination

## 📊 Pendekatan yang Tersedia

### 1. LoRA Fine-Tuning (RECOMMENDED) ⭐
- **Kelebihan**: Efisien, cepat, tidak butuh GPU besar
- **Kekurangan**: Perlu setup tambahan
- **Hardware**: CPU/GPU biasa (8GB RAM cukup)
- **Waktu**: 1-2 jam

### 2. Full Fine-Tuning
- **Kelebihan**: Hasil terbaik
- **Kekurangan**: Butuh GPU powerful (24GB+ VRAM)
- **Hardware**: GPU high-end
- **Waktu**: 4-8 jam

### 3. Few-Shot Learning (Tanpa Training)
- **Kelebihan**: Instant, tidak perlu training
- **Kekurangan**: Terbatas pada prompt size
- **Hardware**: Apapun
- **Waktu**: Instant

## 🚀 Quick Start

Saya sudah siapkan 3 file:
1. `prepare_training_data.py` - Buat dataset training
2. `fine_tune_lora.py` - Fine-tune dengan LoRA
3. `use_finetuned_model.py` - Gunakan model hasil fine-tune

## 📝 Langkah-Langkah

### Step 1: Prepare Data
```bash
python fine_tuning/prepare_training_data.py
```

### Step 2: Fine-Tune (Pilih salah satu)

**Opsi A: LoRA (Recommended)**
```bash
python fine_tuning/fine_tune_lora.py
```

**Opsi B: Few-Shot (No Training)**
```bash
# Langsung pakai, sudah terintegrasi di agent_rag.py
```

### Step 3: Use Fine-Tuned Model
```bash
# Update .env
FINETUNED_MODEL_PATH=./fine_tuning/models/triptrove-llama

# Restart aplikasi
streamlit run app.py
```

## 📚 Training Data Format

File: `training_data.jsonl`

```json
{"instruction": "Apa term and condition TripTrove?", "input": "", "output": "Term and condition TripTrove meliputi..."}
{"instruction": "Berapa harga tour Borobudur?", "input": "", "output": "Harga tour Borobudur adalah..."}
```

## ⚠️ Catatan Penting

1. **Data Quality > Quantity**: 50-100 contoh berkualitas lebih baik dari 1000 contoh buruk
2. **Diverse Examples**: Variasi pertanyaan dan jawaban
3. **Consistent Style**: Gaya jawaban harus konsisten
4. **Accurate Information**: Pastikan jawaban akurat

## 🔧 Hardware Requirements

### Minimum (LoRA):
- RAM: 8GB
- Storage: 10GB free
- CPU: Intel i5 atau setara

### Recommended (LoRA):
- RAM: 16GB
- Storage: 20GB free
- GPU: Optional (mempercepat 5-10x)

### For Full Fine-Tuning:
- RAM: 32GB+
- GPU: 24GB VRAM (RTX 3090/4090)
- Storage: 50GB free

## 📈 Expected Results

Setelah fine-tuning:
- ✅ Jawaban lebih spesifik ke TripTrove
- ✅ Konsistensi format jawaban
- ✅ Mengurangi hallucination
- ✅ Better understanding of domain terms

## 🆘 Troubleshooting

**Out of Memory?**
- Kurangi batch_size
- Gunakan LoRA rank lebih kecil
- Tutup aplikasi lain

**Training terlalu lama?**
- Kurangi epochs
- Kurangi jumlah data
- Gunakan GPU jika ada

**Model tidak improve?**
- Cek kualitas training data
- Tambah lebih banyak contoh
- Adjust learning rate

---

**Status**: Ready untuk fine-tuning! 🚀
