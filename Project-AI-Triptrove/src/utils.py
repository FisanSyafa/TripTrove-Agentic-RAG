"""
Utility functions untuk TripTrove RAG System
"""
import os
from datetime import datetime
from typing import List, Dict
import json

def format_price(price: float) -> str:
    """Format harga ke format Rupiah"""
    return f"Rp {price:,.0f}".replace(",", ".")

def calculate_discount_price(price: float, discount: int) -> float:
    """Hitung harga setelah diskon"""
    return price * (1 - discount / 100)

def format_duration(days: int) -> str:
    """Format durasi tour"""
    if days == 1:
        return "1 hari"
    else:
        nights = days - 1
        return f"{days} hari {nights} malam"

def get_difficulty_emoji(difficulty: str) -> str:
    """Get emoji untuk tingkat kesulitan"""
    difficulty_map = {
        'easy': '🟢 Mudah',
        'moderate': '🟡 Sedang',
        'hard': '🔴 Sulit',
        'extreme': '⚫ Ekstrem'
    }
    return difficulty_map.get(difficulty.lower(), difficulty)

def get_category_emoji(category: str) -> str:
    """Get emoji untuk kategori tour"""
    category_map = {
        'adventure': '🏔️ Adventure',
        'beach': '🏖️ Beach',
        'cultural': '🏛️ Cultural',
        'nature': '🌿 Nature',
        'city': '🏙️ City Tour',
        'mountain': '⛰️ Mountain',
        'island': '🏝️ Island',
        'religious': '🕌 Religious',
        'culinary': '🍜 Culinary',
        'family': '👨‍👩‍👧‍👦 Family'
    }
    return category_map.get(category.lower(), f"📍 {category}")

def format_rating(rating: float) -> str:
    """Format rating dengan bintang"""
    full_stars = int(rating)
    half_star = 1 if (rating - full_stars) >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    
    stars = "⭐" * full_stars
    if half_star:
        stars += "✨"
    stars += "☆" * empty_stars
    
    return f"{stars} ({rating}/5)"

def save_chat_history(history: List[Dict], filename: str = "chat_history.json"):
    """Simpan riwayat chat ke file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving chat history: {e}")
        return False

def load_chat_history(filename: str = "chat_history.json") -> List[Dict]:
    """Load riwayat chat dari file"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading chat history: {e}")
    return []

def get_timestamp() -> str:
    """Get timestamp sekarang"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Potong teks jika terlalu panjang"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def extract_keywords(query: str) -> List[str]:
    """Extract kata kunci dari query"""
    # Kata-kata umum yang diabaikan
    stop_words = {
        'apa', 'yang', 'ada', 'untuk', 'dengan', 'dari', 'ke', 'di',
        'dan', 'atau', 'adalah', 'ini', 'itu', 'saya', 'kamu', 'kami'
    }
    
    words = query.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    return keywords

def format_package_summary(package_data: Dict) -> str:
    """Format ringkasan paket tour"""
    name = package_data.get('name', 'Unknown')
    price = package_data.get('price', 0)
    discount = package_data.get('discount', 0)
    duration = package_data.get('duration', 0)
    category = package_data.get('category', 'General')
    
    final_price = calculate_discount_price(price, discount)
    
    summary = f"""
📦 {name}
{get_category_emoji(category)}
⏱️ {format_duration(duration)}
💰 {format_price(final_price)}"""
    
    if discount > 0:
        summary += f" (Diskon {discount}% dari {format_price(price)})"
    
    return summary

def validate_env_config() -> Dict[str, bool]:
    """Validasi konfigurasi environment"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = {
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'LLM_MODEL': os.getenv('LLM_MODEL'),
        'EMBEDDING_MODEL': os.getenv('EMBEDDING_MODEL')
    }
    
    validation = {}
    for var, value in required_vars.items():
        validation[var] = value is not None and value != ''
    
    return validation

def get_system_info() -> Dict[str, str]:
    """Get informasi sistem"""
    import platform
    import sys
    
    return {
        'os': platform.system(),
        'os_version': platform.version(),
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'architecture': platform.machine()
    }

if __name__ == "__main__":
    # Test utilities
    print("Testing utilities...")
    print(format_price(2000000))
    print(format_duration(3))
    print(get_difficulty_emoji('moderate'))
    print(get_category_emoji('adventure'))
    print(format_rating(4.5))
    print(extract_keywords("Apa paket tour yang ada untuk keluarga?"))
