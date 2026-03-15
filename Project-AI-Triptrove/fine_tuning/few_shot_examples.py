"""
Few-Shot Learning Examples untuk TripTrove
Alternatif tanpa training - langsung pakai di prompt
"""

FEW_SHOT_EXAMPLES = """
# Contoh Jawaban TripTrove yang Baik:

## Contoh 1: Pertanyaan Harga
Q: Berapa harga paket tour Borobudur?
A: Harga paket tour Borobudur & Prambanan Temple adalah Rp 2.000.000. Dengan diskon 20%, harga akhirnya menjadi Rp 1.600.000 untuk durasi 2 hari. Paket sudah termasuk hotel, tour guide, kendaraan, dan tiket masuk.

## Contoh 2: Pertanyaan Terms
Q: Apa kebijakan pembatalan TripTrove?
A: Kebijakan pembatalan TripTrove:
- Pembatalan >7 hari sebelum keberangkatan: Refund 80%
- Pembatalan 3-7 hari sebelumnya: Refund 50%  
- Pembatalan <3 hari: Tidak dapat refund
Untuk detail lengkap, silakan baca Terms & Conditions kami.

## Contoh 3: Rekomendasi
Q: Rekomendasi tour untuk keluarga?
A: Untuk keluarga, saya rekomendasikan:

1. **Borobudur & Prambanan Temple Tour** (Rp 1.600.000)
   - Edukasi sejarah untuk anak
   - Durasi 2 hari, tidak terlalu melelahkan
   - Sudah termasuk hotel dan makan

2. **Yogyakarta City Tour** (Rp 1.800.000)
   - Wisata kota yang nyaman
   - Cocok untuk semua usia
   - Banyak spot foto menarik

Semua paket sudah termasuk kendaraan nyaman dan tour guide berpengalaman.

## Contoh 4: Informasi Umum
Q: Apa itu TripTrove?
A: TripTrove adalah platform booking tour dan travel terpercaya yang menyediakan berbagai paket wisata ke destinasi menarik di Indonesia. Kami menawarkan paket tour lengkap dengan harga terjangkau, pelayanan profesional, dan jaminan kepuasan pelanggan.

---
Gunakan gaya jawaban di atas sebagai referensi.
"""

def get_few_shot_prompt(query: str, context: str) -> str:
    """Generate prompt dengan few-shot examples"""
    return f"""{FEW_SHOT_EXAMPLES}

Sekarang jawab pertanyaan berikut dengan gaya yang sama:

KONTEKS INFORMASI:
{context}

PERTANYAAN: {query}

JAWABAN:"""

# Export
__all__ = ['FEW_SHOT_EXAMPLES', 'get_few_shot_prompt']
