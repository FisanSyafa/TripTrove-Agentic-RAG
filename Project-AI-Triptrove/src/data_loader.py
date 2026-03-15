"""
Data Loader untuk memuat data dari MySQL dan PDF ke ChromaDB
Hybrid approach: Database + PDF Documents
"""
import warnings
warnings.filterwarnings('ignore')

import mysql.connector
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class TripTroveDataLoader:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'triptrove_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        self.embeddings = OllamaEmbeddings(
            model=os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
    def load_tour_packages(self):
        """Load data paket tour dari database"""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        
        # Query sesuai struktur database yang sebenarnya
        query = """
        SELECT 
            id, name, slug, destination_summary, location_details,
            description, duration_days, price, discount_percent,
            sold_count, includes_hotel, includes_guide, 
            includes_entrance_fee, includes_driver_vehicle,
            cover_image_url, status, category,
            created_at, updated_at
        FROM tour_packages
        WHERE status = 'published'
        """
        
        cursor.execute(query)
        packages = cursor.fetchall()
        
        documents = []
        for pkg in packages:
            # Format harga
            price = float(pkg['price'])
            discount = pkg.get('discount_percent') or 0
            final_price = price * (1 - discount/100)
            
            # Format fasilitas
            facilities = []
            if pkg.get('includes_hotel'): facilities.append("Hotel")
            if pkg.get('includes_guide'): facilities.append("Tour Guide")
            if pkg.get('includes_entrance_fee'): facilities.append("Entrance Fee")
            if pkg.get('includes_driver_vehicle'): facilities.append("Driver & Vehicle")
            facilities_str = ", ".join(facilities) if facilities else "Tidak ada fasilitas"
            
            # Buat konten yang kaya informasi
            content = f"""
Nama Paket: {pkg['name']}
Kategori: {pkg.get('category', 'General')}
Destinasi: {pkg.get('destination_summary', 'Tidak ada destinasi')}
Lokasi Detail: {pkg.get('location_details', 'Tidak ada detail lokasi')}
Durasi: {pkg['duration_days']} hari
Harga: Rp {price:,.0f} (Diskon {discount}% = Rp {final_price:,.0f})
Terjual: {pkg.get('sold_count', 0)} kali
Fasilitas: {facilities_str}

Deskripsi:
{pkg.get('description', 'Tidak ada deskripsi')}
"""
            
            metadata = {
                'id': pkg['id'],
                'name': pkg['name'],
                'slug': pkg.get('slug', ''),
                'category': pkg.get('category', 'General'),
                'destination': pkg.get('destination_summary', ''),
                'price': float(price),
                'discount': discount,
                'final_price': float(final_price),
                'duration': pkg['duration_days'],
                'sold_count': pkg.get('sold_count', 0),
                'type': 'tour_package'
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        cursor.close()
        conn.close()
        
        return documents
    
    def load_reviews(self):
        """Load data review dari database"""
        conn = mysql.connector.connect(**self.db_config)
        cursor = conn.cursor(dictionary=True)
        
        query = """
        SELECT 
            r.id, r.rating, r.comment, r.created_at,
            u.name as user_name,
            tp.name as package_name
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        JOIN tour_packages tp ON r.tour_package_id = tp.id
        ORDER BY r.created_at DESC
        """
        
        cursor.execute(query)
        reviews = cursor.fetchall()
        
        documents = []
        for rev in reviews:
            content = f"""
Review untuk: {rev['package_name']}
Rating: {rev['rating']}/5
Reviewer: {rev['user_name']}
Tanggal: {rev['created_at']}

Komentar:
{rev['comment']}
"""
            
            metadata = {
                'id': rev['id'],
                'package_name': rev['package_name'],
                'rating': rev['rating'],
                'type': 'review'
            }
            
            documents.append(Document(page_content=content, metadata=metadata))
        
        cursor.close()
        conn.close()
        
        return documents
    
    def load_pdf_documents(self, pdf_directory="./documents"):
        """Load dokumen PDF dari folder"""
        pdf_path = Path(pdf_directory)
        
        if not pdf_path.exists():
            print(f"⚠️  Folder {pdf_directory} tidak ditemukan, skip PDF loading")
            return []
        
        pdf_files = list(pdf_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"ℹ️  Tidak ada file PDF di {pdf_directory}")
            return []
        
        print(f"📄 Loading {len(pdf_files)} PDF file(s)...")
        
        all_documents = []
        
        for pdf_file in pdf_files:
            try:
                print(f"   📖 Loading: {pdf_file.name}")
                loader = PyPDFLoader(str(pdf_file))
                documents = loader.load()
                
                print(f"      Raw pages loaded: {len(documents)}")
                
                # Split dokumen menjadi chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200,
                    length_function=len,
                )
                chunks = text_splitter.split_documents(documents)
                
                # Add metadata
                for i, chunk in enumerate(chunks):
                    chunk.metadata['source'] = pdf_file.name
                    chunk.metadata['type'] = 'pdf_document'
                    chunk.metadata['source_type'] = 'pdf'
                    chunk.metadata['chunk_id'] = i
                
                all_documents.extend(chunks)
                print(f"   ✅ Loaded {len(chunks)} chunks from {pdf_file.name}")
                
            except Exception as e:
                print(f"   ❌ Error loading {pdf_file.name}: {e}")
                import traceback
                traceback.print_exc()
        
        return all_documents
    
    def create_vector_store(self, persist_directory="./chroma_db", pdf_directory="./documents"):
        """Buat vector store dari database DAN PDF"""
        print("="*60)
        print("📦 HYBRID DATA LOADING: Database + PDF")
        print("="*60)
        
        # Load data dari database
        print("\n🗄️  Loading data dari MySQL database...")
        tour_docs = self.load_tour_packages()
        review_docs = self.load_reviews()
        
        print(f"✅ Loaded {len(tour_docs)} paket tour dari database")
        print(f"✅ Loaded {len(review_docs)} reviews dari database")
        
        # Load data dari PDF
        print(f"\n📄 Loading data dari PDF documents...")
        pdf_docs = self.load_pdf_documents(pdf_directory)
        
        if pdf_docs:
            print(f"✅ Loaded {len(pdf_docs)} chunks dari PDF")
        else:
            print("ℹ️  Tidak ada PDF yang di-load (optional)")
        
        # Gabungkan semua dokumen
        all_documents = tour_docs + review_docs + pdf_docs
        
        print(f"\n📊 TOTAL: {len(all_documents)} dokumen")
        print(f"   - Database: {len(tour_docs) + len(review_docs)} dokumen")
        print(f"   - PDF: {len(pdf_docs)} chunks")
        
        # Buat vector store
        print("\n🔄 Membuat embeddings dan menyimpan ke ChromaDB...")
        print("   (Ini mungkin memakan waktu beberapa menit...)")
        
        vectorstore = Chroma.from_documents(
            documents=all_documents,
            embedding=self.embeddings,
            persist_directory=persist_directory
        )
        
        print(f"\n✅ Vector store berhasil dibuat di {persist_directory}")
        print("="*60)
        return vectorstore

if __name__ == "__main__":
    loader = TripTroveDataLoader()
    vectorstore = loader.create_vector_store()
    print("\n🎉 Selesai! Data siap digunakan untuk RAG.")
