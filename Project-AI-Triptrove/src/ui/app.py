"""
Streamlit UI untuk TripTrove Agentic RAG
User-friendly interface untuk berinteraksi dengan AI Agent
"""
import streamlit as st
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from agent_rag import TripTroveAgent
import os
from datetime import datetime

# Page config
st.set_page_config(
    page_title="TripTrove AI Assistant",
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1.2rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-left: 5px solid #5a67d8;
        color: white;
    }
    .user-message strong {
        color: #fff;
        font-weight: 600;
    }
    .user-message p {
        color: #fff;
        margin: 0.5rem 0 0 0;
    }
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-left: 5px solid #e91e63;
        color: white;
    }
    .assistant-message strong {
        color: #fff;
        font-weight: 600;
    }
    .assistant-message p {
        color: #fff;
        margin: 0.5rem 0 0 0;
        line-height: 1.6;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6a3f8f 100%);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    .info-box {
        background-color: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 1rem;
    }
    .info-box strong {
        color: #856404;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Success/Warning/Error boxes */
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-left: 5px solid #28a745;
    }
    .stWarning {
        background-color: #fff3cd;
        color: #856404;
        border-left: 5px solid #ffc107;
    }
    .stError {
        background-color: #f8d7da;
        color: #721c24;
        border-left: 5px solid #dc3545;
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

def initialize_agent():
    """Initialize the RAG agent"""
    try:
        with st.spinner("🔄 Memuat AI Agent..."):
            agent = TripTroveAgent()
            st.session_state.agent = agent
            st.session_state.initialized = True
            return True
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return False

def display_chat_message(role, content, timestamp=None):
    """Display a chat message"""
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>🧑 Anda</strong> {f'<span style="color: rgba(255,255,255,0.8); font-size: 0.85rem;">({timestamp})</span>' if timestamp else ''}
            <p style="margin-top: 0.5rem; font-size: 1rem; line-height: 1.6;">{content}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>🤖 TripTrove AI</strong> {f'<span style="color: rgba(255,255,255,0.8); font-size: 0.85rem;">({timestamp})</span>' if timestamp else ''}
            <p style="margin-top: 0.5rem; font-size: 1rem; line-height: 1.6;">{content}</p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/1E88E5/FFFFFF?text=TripTrove", use_container_width=True)
    
    st.markdown("### 🏝️ TripTrove AI Assistant")
    st.markdown("---")
    
    # Status
    if st.session_state.initialized:
        st.success("✅ AI Agent Aktif")
    else:
        st.warning("⚠️ AI Agent Belum Diinisialisasi")
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### 🚀 Aksi Cepat")
    
    if st.button("🔄 Inisialisasi Agent"):
        if initialize_agent():
            st.success("✅ Agent berhasil diinisialisasi!")
            st.rerun()
    
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    # Example queries
    st.markdown("### 💡 Contoh Pertanyaan")
    example_queries = [
        "Paket tour apa saja yang tersedia?",
        "Berapa harga paket tour ke Bali?",
        "Paket tour untuk keluarga dengan budget 5 juta?",
        "Review paket tour yang paling bagus?",
        "Paket tour adventure apa yang ada?",
        "Rekomendasi paket tour 3 hari 2 malam?"
    ]
    
    for query in example_queries:
        if st.button(f"📝 {query[:30]}...", key=query):
            st.session_state.current_query = query
    
    st.markdown("---")
    
    # Info
    st.markdown("### ℹ️ Informasi")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1rem; border-radius: 10px; color: white;">
        <p style="margin: 0; color: white;"><strong style="color: white;">🧠 TripTrove AI</strong> menggunakan:</p>
        <ul style="margin: 0.5rem 0; padding-left: 1.2rem; color: white;">
            <li style="color: white;">🤖 Llama 3.1 (Local)</li>
            <li style="color: white;">🔍 ChromaDB Vector Store</li>
            <li style="color: white;">🌐 DuckDuckGo Search</li>
            <li style="color: white;">🎯 LangGraph Agent</li>
        </ul>
        <p style="margin: 0.5rem 0 0 0; color: white; font-weight: 600;">💯 100% Gratis & Lokal!</p>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-header">🏝️ TripTrove AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Asisten Cerdas untuk Menemukan Paket Tour Impian Anda</div>', unsafe_allow_html=True)

# Check if agent is initialized
if not st.session_state.initialized:
    st.markdown("""
    <div class="info-box">
        <strong>⚠️ Perhatian:</strong> AI Agent belum diinisialisasi. 
        Klik tombol "Inisialisasi Agent" di sidebar untuk memulai.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Inisialisasi Agent Sekarang", use_container_width=True):
            if initialize_agent():
                st.success("✅ Agent berhasil diinisialisasi!")
                st.rerun()
else:
    # Display chat history
    for message in st.session_state.chat_history:
        display_chat_message(
            message['role'],
            message['content'],
            message.get('timestamp')
        )
    
    # Chat input
    st.markdown("---")
    
    # Check if there's a query from sidebar
    if 'current_query' in st.session_state:
        user_input = st.session_state.current_query
        del st.session_state.current_query
    else:
        user_input = st.chat_input("💬 Tanyakan tentang paket tour, harga, destinasi, atau apapun...")
    
    if user_input:
        # Add user message to history
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': timestamp
        })
        
        # Display user message
        display_chat_message('user', user_input, timestamp)
        
        # Get AI response
        with st.spinner("🤔 AI sedang berpikir..."):
            try:
                response = st.session_state.agent.query(user_input)
                
                # Add assistant message to history
                timestamp = datetime.now().strftime("%H:%M")
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': timestamp
                })
                
                # Display assistant message
                display_chat_message('assistant', response, timestamp)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #999; font-size: 0.9rem;">
    <p>🏝️ TripTrove AI Assistant | Powered by Llama 3.1 & LangGraph | 100% Local & Free</p>
</div>
""", unsafe_allow_html=True)
