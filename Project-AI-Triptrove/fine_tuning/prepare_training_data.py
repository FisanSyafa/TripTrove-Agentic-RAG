"""
Script untuk membuat training data dari database dan PDF
"""
import sys
sys.path.append('..')

import json
import mysql.connector
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class TrainingDataPreparer:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'triptrove_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        self.training_data = []
    
    def create_tour_package_examples(self):
        """Buat contoh Q&A dari tour packages"""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT id, name, destination_summary, description, 
               duration_days, price, discount_percent
        FROM tour_packages
        WHERE status = 'published'
        LIMIT 10
        """
        
        cursor.execute(query)
        packages = cursor.fetchall()
        
        for pkg in packages:
            price = float(pkg['price'])
            discount = pkg.get('discount_percent', 0)
            final_price = price * (1 - discount/100)
            
            # Contoh 1: Pertanyaan harga
            self.training_data.append({
                "instruction": f"Berapa harga paket tour {pkg['name']}?",
                "input": "",
                "output": f"Harga paket tour {pkg['name']} adalah Rp {price:,.0f}. " + 
                         (f"Dengan diskon {discount}%, harga akhirnya menjadi Rp {final_price:,.0f}." if discount > 0 else "")
            })
            
            # Contoh 2: Pertanyaan deskripsi
            self.training_data.append({
                "instruction": f"Ceritakan tentang paket tour {pkg['name']}",
                "input": "",
                "output": f"Paket tour {pkg['name']} adalah tour ke {pkg['destination_summary']} " +
                         f"dengan durasi {pkg['duration_days']} hari. {pkg['description'][:200]}..."
            })
            
            # Contoh 3: Pertanyaan durasi
            self.training_data.append({
                "instruction": f"Berapa lama durasi tour {pkg['name']}?",
                "input": "",
                "output": f"Durasi paket tour {pkg['name']} adalah {pkg['duration_days']} hari."
            })
        
        cursor.close()
        conn.close()
        
        print(f"✅ Created {len(self.training_data)} examples from tour packages")
    
    def create_general_examples(self):
        """Buat contoh Q&A umum tentang TripTrove"""
        general_qa = [
            {
                "instruction": "Apa itu TripTrove?",
                "input": "",
                "output": "TripTrove adalah platform booking tour dan travel yang menyediakan berbagai paket wisata ke destinasi menarik di Indonesia. Kami menawarkan paket tour yang lengkap dengan harga terjangkau dan pelayanan terbaik."
            },
            {
                "instruction": "Bagaimana cara booking di TripTrove?",
                "input": "",
                "output": "Untuk booking di TripTrove, Anda bisa: 1) Pilih paket tour yang diinginkan, 2) Isi data peserta, 3) Pilih tanggal keberangkatan, 4) Lakukan pembayaran, 5) Konfirmasi booking akan dikirim via email."
            },
            {
                "instruction": "Metode pembayaran apa saja yang tersedia?",
                "input": "",
                "output": "TripTrove menerima pembayaran melalui transfer bank, kartu kredit, dan e-wallet. Semua transaksi dijamin aman dan terenkripsi."
            },
            {
                "instruction": "Apakah bisa refund jika membatalkan booking?",
                "input": "",
                "output": "Ya, TripTrove memiliki kebijakan refund. Pembatalan lebih dari 7 hari sebelum keberangkatan akan mendapat refund 80%. Pembatalan 3-7 hari sebelumnya mendapat refund 50%. Pembatalan kurang dari 3 hari tidak dapat refund. Silakan baca Terms & Conditions untuk detail lengkap."
            },
            {
                "instruction": "Apa saja yang termasuk dalam paket tour?",
                "input": "",
                "output": "Paket tour TripTrove umumnya sudah termasuk: transportasi (kendaraan dan driver), akomodasi hotel, tour guide profesional, tiket masuk objek wisata, dan makan sesuai itinerary. Detail lengkap ada di deskripsi masing-masing paket."
            }
        ]
        
        self.training_data.extend(general_qa)
        print(f"✅ Added {len(general_qa)} general examples")
    
    def create_style_examples(self):
        """Contoh style jawaban yang diinginkan"""
        style_examples = [
            {
                "instruction": "Rekomendasi tour untuk keluarga?",
                "input": "",
                "output": "Untuk keluarga, saya rekomendasikan:\n\n1. **Paket Tour Borobudur & Prambanan** - Cocok untuk edukasi anak tentang sejarah dan budaya\n2. **Paket Tour Bali Family** - Pantai dan aktivitas ramah anak\n3. **Paket Tour Yogyakarta City** - Wisata kota yang nyaman untuk semua usia\n\nSemua paket sudah termasuk kendaraan nyaman dan tour guide berpengalaman."
            },
            {
                "instruction": "Tour mana yang paling populer?",
                "input": "",
                "output": "Paket tour paling populer di TripTrove adalah:\n\n🏆 **Borobudur & Prambanan Temple Tour**\n- Sudah terjual 21 kali\n- Rating tinggi dari customer\n- Harga: Rp 2.000.000 (diskon 20% = Rp 1.600.000)\n- Durasi: 2 hari\n\nPaket ini populer karena mengunjungi 2 candi UNESCO World Heritage dalam satu trip!"
            }
        ]
        
        self.training_data.extend(style_examples)
        print(f"✅ Added {len(style_examples)} style examples")
    
    def save_training_data(self, filename="training_data.jsonl"):
        """Save training data ke file JSONL"""
        output_path = Path(__file__).parent / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in self.training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        print(f"\n✅ Training data saved to {output_path}")
        print(f"📊 Total examples: {len(self.training_data)}")
        
        return output_path

if __name__ == "__main__":
    print("="*60)
    print("📝 Preparing Training Data for TripTrove Fine-Tuning")
    print("="*60)
    
    preparer = TrainingDataPreparer()
    
    print("\n1️⃣ Creating examples from tour packages...")
    preparer.create_tour_package_examples()
    
    print("\n2️⃣ Creating general Q&A examples...")
    preparer.create_general_examples()
    
    print("\n3️⃣ Creating style examples...")
    preparer.create_style_examples()
    
    print("\n4️⃣ Saving training data...")
    output_file = preparer.save_training_data()
    
    print("\n" + "="*60)
    print("🎉 Training data preparation complete!")
    print("="*60)
    print(f"\nNext steps:")
    print(f"1. Review the data: {output_file}")
    print(f"2. Add more examples if needed")
    print(f"3. Run fine-tuning: python fine_tune_lora.py")
    print("="*60)
