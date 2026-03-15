"""
Configuration management untuk TripTrove RAG System
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Configuration class"""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
    DB_PORT = int(os.getenv('DB_PORT', 3306))
    DB_NAME = os.getenv('DB_NAME', 'triptrove_db')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
    LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.1')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
    
    # RAG Configuration
    VECTOR_STORE_PATH = os.getenv('VECTOR_STORE_PATH', './chroma_db')
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', 1000))
    CHUNK_OVERLAP = int(os.getenv('CHUNK_OVERLAP', 200))
    TOP_K_RESULTS = int(os.getenv('TOP_K_RESULTS', 5))
    
    # Agent Configuration
    MAX_SEARCH_ITERATIONS = int(os.getenv('MAX_SEARCH_ITERATIONS', 2))
    ENABLE_WEB_SEARCH = os.getenv('ENABLE_WEB_SEARCH', 'true').lower() == 'true'
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', 0.7))
    
    # UI Configuration
    APP_TITLE = os.getenv('APP_TITLE', 'TripTrove AI Assistant')
    APP_ICON = os.getenv('APP_ICON', '🏝️')
    THEME_COLOR = os.getenv('THEME_COLOR', '#1E88E5')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    ENABLE_DEBUG = os.getenv('ENABLE_DEBUG', 'false').lower() == 'true'
    
    @classmethod
    def get_db_config(cls) -> dict:
        """Get database configuration as dict"""
        return {
            'host': cls.DB_HOST,
            'port': cls.DB_PORT,
            'database': cls.DB_NAME,
            'user': cls.DB_USER,
            'password': cls.DB_PASSWORD
        }
    
    @classmethod
    def validate(cls) -> tuple[bool, list]:
        """Validate configuration"""
        errors = []
        
        # Check required fields
        if not cls.DB_NAME:
            errors.append("DB_NAME is required")
        if not cls.DB_USER:
            errors.append("DB_USER is required")
        if not cls.LLM_MODEL:
            errors.append("LLM_MODEL is required")
        if not cls.EMBEDDING_MODEL:
            errors.append("EMBEDDING_MODEL is required")
        
        # Check vector store path
        vector_path = Path(cls.VECTOR_STORE_PATH)
        if not vector_path.exists():
            errors.append(f"Vector store path does not exist: {cls.VECTOR_STORE_PATH}")
        
        return len(errors) == 0, errors
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("="*60)
        print("Current Configuration")
        print("="*60)
        print(f"Database: {cls.DB_USER}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}")
        print(f"Ollama URL: {cls.OLLAMA_BASE_URL}")
        print(f"LLM Model: {cls.LLM_MODEL}")
        print(f"Embedding Model: {cls.EMBEDDING_MODEL}")
        print(f"Vector Store: {cls.VECTOR_STORE_PATH}")
        print(f"Top K Results: {cls.TOP_K_RESULTS}")
        print(f"Max Iterations: {cls.MAX_SEARCH_ITERATIONS}")
        print(f"Web Search: {'Enabled' if cls.ENABLE_WEB_SEARCH else 'Disabled'}")
        print(f"Temperature: {cls.LLM_TEMPERATURE}")
        print("="*60)

# Create config instance
config = Config()

if __name__ == "__main__":
    # Test configuration
    config.print_config()
    
    is_valid, errors = config.validate()
    if is_valid:
        print("\n✅ Configuration is valid")
    else:
        print("\n❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
