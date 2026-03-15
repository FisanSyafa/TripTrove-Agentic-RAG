"""
Advanced Streamlit UI dengan fitur tambahan
- Export chat history
- Statistics dashboard
- Advanced filters
- Multi-language support (ID/EN)
"""
import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent_rag import TripTroveAgent
from utils import *
from config import config
import pandas as pd
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="TripTrove AI Assistant Pro",
    page_icon="🏝️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(120deg, #1E88E5, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        animation: fadeIn 0.3s;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .user-message {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-left: 4px solid #1E88E5;
    }
    .assistant-message {
        background: linear-gradient(135deg, #F5F5F5 0%, #EEEEEE 100%);
        border-left: 4px solid #4CAF50;
    }
    .feature-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-size: 0.8rem;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'language' not in st.session_state:
    st.session_state.language = 'id'
if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_queries': 0,
        'successful_queries': 0,
        'failed_queries': 0,
        'avg_response_time': 0
    }

# Language translations
TRANSLATIONS = {
    'id': {
        'title': '🏝️ TripTrove AI Assistant Pro',
        'subtitle': 'Asisten Cerdas untuk Menemukan Paket Tour Impian Anda',
        'init_agent': '🔄 Inisialisasi Agent',
        'clear_history': '🗑️ Hapus Riwayat',
        'export_chat': '📥 Export Chat',
        'agent_active': '✅ AI Agent Aktif',
        'agent_inactive': '⚠️ AI Agent Belum Diinisialisasi',
        'quick_actions': '🚀 Aksi Cepat',
        'statistics': '📊 Statistik',
        'examples': '💡 Contoh Pertanyaan',
        'chat_input': '💬 Tanyakan tentang paket tour, harga, destinasi, atau apapun...',
        'thinking': '🤔 AI sedang berpikir...'
    },
    'en': {
        'title': '🏝️ TripTrove AI Assistant Pro',
        'subtitle': 'Smart Assistant to Find Your Dream Tour Package',
        'init_agent': '🔄 Initialize Agent',
        'clear_history': '🗑️ Clear History',
        'export_chat': '📥 Export Chat',
        'agent_active': '✅ AI Agent Active',
        'agent_inactive': '⚠️ AI Agent Not Initialized',
        'quick_actions': '🚀 Quick Actions',
        'statistics': '📊 Statistics',
        'examples': '💡 Example Questions',
        'chat_input': '💬 Ask about tour packages, prices, destinations, or anything...',
        'thinking': '🤔 AI is thinking...'
    }
}

def t(key):
    """Get translation"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

def initialize_agent():
    """Initialize the RAG agent"""
    try:
        with st.spinner(t('thinking')):
            agent = TripTroveAgent()
            st.session_state.agent = agent
            st.session_state.initialized = True
            return True
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return False

def export_chat_history():
    """Export chat history to JSON"""
    if st.session_state.chat_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"chat_history_{timestamp}.json"
        
        data = {
            'exported_at': get_timestamp(),
            'total_messages': len(st.session_state.chat_history),
            'messages': st.session_state.chat_history,
            'statistics': st.session_state.stats
        }
        
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        
        st.download_button(
            label="📥 Download Chat History",
            data=json_str,
            file_name=filename,
            mime="application/json"
        )

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1E88E5/FFFFFF?text=TripTrove+Pro", use_container_width=True)
    
    # Language selector
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇮🇩 ID", use_container_width=True):
            st.session_state.language = 'id'
            st.rerun()
    with col2:
        if st.button("🇬🇧 EN", use_container_width=True):
            st.session_state.language = 'en'
            st.rerun()
    
    st.markdown(f"### {t('title')}")
    st.markdown("---")
    
    # Status
    if st.session_state.initialized:
        st.success(t('agent_active'))
    else:
        st.warning(t('agent_inactive'))
    
    st.markdown("---")
    
    # Quick actions
    st.markdown(f"### {t('quick_actions')}")
    
    if st.button(t('init_agent'), use_container_width=True):
        if initialize_agent():
            st.success("✅ Success!")
            st.rerun()
    
    if st.button(t('clear_history'), use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    export_chat_history()
    
    st.markdown("---")
    
    # Statistics
    st.markdown(f"### {t('statistics')}")
    stats = st.session_state.stats
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Queries", stats['total_queries'])
    with col2:
        st.metric("Success Rate", 
                 f"{(stats['successful_queries']/max(stats['total_queries'],1)*100):.0f}%")
    
    st.markdown("---")
    
    # Example queries
    st.markdown(f"### {t('examples')}")
    example_queries = [
        "Paket tour apa saja yang tersedia?",
        "Berapa harga paket tour ke Bali?",
        "Paket tour untuk keluarga dengan budget 5 juta?",
        "Review paket tour yang paling bagus?",
        "Paket tour adventure apa yang ada?",
        "Rekomendasi paket tour 3 hari 2 malam?"
    ]
    
    for query in example_queries:
        if st.button(f"📝 {truncate_text(query, 35)}", key=query, use_container_width=True):
            st.session_state.current_query = query
    
    st.markdown("---")
    
    # System info
    with st.expander("ℹ️ System Info"):
        st.code(f"""
Model: {config.LLM_MODEL}
Embedding: {config.EMBEDDING_MODEL}
Vector Store: {config.VECTOR_STORE_PATH}
Top K: {config.TOP_K_RESULTS}
Temperature: {config.LLM_TEMPERATURE}
        """)

# Main content
st.markdown(f'<div class="main-header">{t("title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="sub-header">{t("subtitle")}</div>', unsafe_allow_html=True)

# Features badges
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <span class="feature-badge">🧠 Agentic RAG</span>
    <span class="feature-badge">🔍 Smart Search</span>
    <span class="feature-badge">🌐 Web Search</span>
    <span class="feature-badge">💯 100% Local</span>
    <span class="feature-badge">🆓 Free Forever</span>
</div>
""", unsafe_allow_html=True)

# Check if agent is initialized
if not st.session_state.initialized:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.warning("⚠️ AI Agent belum diinisialisasi. Klik tombol di sidebar untuk memulai.")
        if st.button("🚀 Inisialisasi Agent Sekarang", use_container_width=True):
            if initialize_agent():
                st.success("✅ Success!")
                st.rerun()
else:
    # Display chat history
    for message in st.session_state.chat_history:
        role_icon = "🧑" if message['role'] == 'user' else "🤖"
        role_name = "Anda" if message['role'] == 'user' else "TripTrove AI"
        css_class = "user-message" if message['role'] == 'user' else "assistant-message"
        
        st.markdown(f"""
        <div class="chat-message {css_class}">
            <strong>{role_icon} {role_name}</strong> 
            <span style="color: #999; font-size: 0.8rem;">({message.get('timestamp', '')})</span>
            <p>{message['content']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Chat input
    st.markdown("---")
    
    # Check if there's a query from sidebar
    if 'current_query' in st.session_state:
        user_input = st.session_state.current_query
        del st.session_state.current_query
    else:
        user_input = st.chat_input(t('chat_input'))
    
    if user_input:
        # Add user message
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Get AI response
        start_time = datetime.now()
        with st.spinner(t('thinking')):
            try:
                response = st.session_state.agent.query(user_input)
                
                # Update stats
                st.session_state.stats['total_queries'] += 1
                st.session_state.stats['successful_queries'] += 1
                
                # Add assistant message
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': timestamp
                })
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.stats['total_queries'] += 1
                st.session_state.stats['failed_queries'] += 1
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9rem;">
    <p>🏝️ TripTrove AI Assistant Pro | Powered by Llama 3.1 & LangGraph | 100% Local & Free</p>
    <p>Made with ❤️ using Open Source Technology</p>
</div>
""", unsafe_allow_html=True)
