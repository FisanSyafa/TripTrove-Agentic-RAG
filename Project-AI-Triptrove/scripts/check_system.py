"""
Script untuk mengecek apakah sistem siap digunakan
"""
import sys
import subprocess
import os
from pathlib import Path

def check_python():
    """Cek versi Python"""
    print("🐍 Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)")
        return False

def check_ollama():
    """Cek apakah Ollama terinstall"""
    print("\n🦙 Checking Ollama...")
    try:
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("   ✅ Ollama installed")
            
            # Cek model
            output = result.stdout
            has_llama = 'llama3.1' in output
            has_nomic = 'nomic-embed-text' in output
            
            if has_llama:
                print("   ✅ llama3.1 model found")
            else:
                print("   ⚠️  llama3.1 model not found. Run: ollama pull llama3.1")
            
            if has_nomic:
                print("   ✅ nomic-embed-text model found")
            else:
                print("   ⚠️  nomic-embed-text not found. Run: ollama pull nomic-embed-text")
            
            return has_llama and has_nomic
        else:
            print("   ❌ Ollama not responding")
            return False
    except FileNotFoundError:
        print("   ❌ Ollama not installed")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def check_dependencies():
    """Cek dependencies Python"""
    print("\n📦 Checking Python dependencies...")
    required = [
        'langchain',
        'langchain_ollama',
        'langchain_community',
        'langgraph',
        'chromadb',
        'streamlit',
        'mysql.connector'
    ]
    
    all_installed = True
    for package in required:
        try:
            if package == 'mysql.connector':
                __import__('mysql.connector')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} not installed")
            all_installed = False
    
    if not all_installed:
        print("\n   Run: pip install -r requirements.txt")
    
    return all_installed

def check_env_file():
    """Cek file .env"""
    print("\n⚙️  Checking configuration...")
    env_path = Path('.env')
    
    if env_path.exists():
        print("   ✅ .env file exists")
        
        # Baca dan cek isi
        with open(env_path, 'r') as f:
            content = f.read()
            
        if 'DB_NAME' in content:
            print("   ✅ Database config found")
        else:
            print("   ⚠️  Database config incomplete")
            
        return True
    else:
        print("   ⚠️  .env file not found")
        print("   Copy .env.example to .env and configure it")
        return False

def check_database():
    """Cek koneksi database"""
    print("\n🗄️  Checking database connection...")
    try:
        import mysql.connector
        from dotenv import load_dotenv
        
        load_dotenv()
        
        config = {
            'host': os.getenv('DB_HOST', '127.0.0.1'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'triptrove_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tour_packages")
        count = cursor.fetchone()[0]
        
        print(f"   ✅ Database connected ({count} tour packages)")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"   ❌ Database error: {e}")
        return False

def check_vector_store():
    """Cek apakah vector store sudah dibuat"""
    print("\n🔍 Checking vector store...")
    chroma_path = Path('chroma_db')
    
    if chroma_path.exists() and chroma_path.is_dir():
        files = list(chroma_path.glob('*'))
        if files:
            print(f"   ✅ Vector store exists ({len(files)} files)")
            return True
        else:
            print("   ⚠️  Vector store folder empty")
            print("   Run: python data_loader.py")
            return False
    else:
        print("   ⚠️  Vector store not found")
        print("   Run: python data_loader.py")
        return False

def main():
    print("="*60)
    print("🏝️  TripTrove RAG System Check")
    print("="*60)
    
    checks = {
        'Python': check_python(),
        'Ollama': check_ollama(),
        'Dependencies': check_dependencies(),
        'Configuration': check_env_file(),
        'Database': check_database(),
        'Vector Store': check_vector_store()
    }
    
    print("\n" + "="*60)
    print("📊 Summary")
    print("="*60)
    
    for name, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
    
    all_passed = all(checks.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All checks passed! System ready to use.")
        print("\nRun the application:")
        print("  streamlit run app.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nQuick fixes:")
        if not checks['Ollama']:
            print("  1. Install Ollama: https://ollama.ai/")
            print("  2. Pull models: ollama pull llama3.1 && ollama pull nomic-embed-text")
        if not checks['Dependencies']:
            print("  3. Install dependencies: pip install -r requirements.txt")
        if not checks['Configuration']:
            print("  4. Configure .env file")
        if not checks['Database']:
            print("  5. Check database connection and credentials")
        if not checks['Vector Store']:
            print("  6. Load data: python data_loader.py")
    print("="*60)

if __name__ == "__main__":
    main()
