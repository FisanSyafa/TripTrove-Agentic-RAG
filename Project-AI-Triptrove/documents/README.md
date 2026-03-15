# 📄 PDF Documents Folder

Folder ini digunakan untuk menyimpan dokumen PDF yang akan di-index ke dalam RAG system.

## 📋 Cara Menggunakan

1. **Letakkan file PDF** di folder ini
2. **Jalankan data loader** untuk mengindex PDF:
   ```bash
   python data_loader.py
   ```
3. PDF akan otomatis di-load dan di-index bersama data database

## 📚 Contoh Dokumen yang Cocok

### Untuk TripTrove:
- ✅ **Terms & Conditions** - Syarat dan ketentuan booking
- ✅ **Travel Guide** - Panduan perjalanan destinasi
- ✅ **Company Policies** - Kebijakan perusahaan
- ✅ **Destination Brochures** - Brosur destinasi wisata
- ✅ **FAQ Document** - Frequently Asked Questions
- ✅ **Safety Guidelines** - Panduan keamanan perjalanan
- ✅ **Packing Lists** - Daftar barang bawaan
- ✅ **Cultural Guides** - Panduan budaya lokal

## 🎯 Format yang Didukung

- ✅ PDF (.pdf)
- Dokumen akan dipecah menjadi chunks untuk indexing yang optimal
- Setiap chunk akan memiliki metadata source file

## 📊 Metadata yang Ditambahkan

Setiap dokumen PDF akan memiliki metadata:
- `source`: Nama file PDF
- `type`: 'pdf_document'
- `source_type`: 'pdf'
- `page`: Nomor halaman (jika ada)

## 💡 Tips

1. **Nama file yang jelas**: Gunakan nama file yang deskriptif
   - ✅ `terms-and-conditions-2024.pdf`
   - ✅ `bali-travel-guide.pdf`
   - ❌ `document1.pdf`

2. **Ukuran file**: Usahakan file tidak terlalu besar (< 10MB per file)

3. **Kualitas teks**: Pastikan PDF bisa di-extract textnya (bukan scan image)

4. **Update berkala**: Re-run data loader jika ada PDF baru atau update

## 🔄 Re-indexing

Jika ada perubahan PDF:
1. Hapus folder `chroma_db`
2. Jalankan `python data_loader.py` lagi

## 📝 Contoh Struktur

```
documents/
├── README.md (file ini)
├── terms-and-conditions.pdf
├── bali-travel-guide.pdf
├── yogyakarta-guide.pdf
├── safety-guidelines.pdf
└── faq.pdf
```

## ⚠️ Catatan

- Folder ini **optional** - sistem tetap berjalan tanpa PDF
- Jika tidak ada PDF, hanya data database yang akan di-index
- PDF akan menambah waktu loading, tapi memberikan konteks lebih kaya

---

**Status**: Folder siap digunakan. Tambahkan PDF Anda di sini!
