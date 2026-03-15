"""
Agentic RAG System menggunakan LangGraph
Agent ini bisa berpikir dan mengulang pencarian jika diperlukan
Dengan Few-Shot Learning untuk hasil lebih baik
"""
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
import operator
import os
from dotenv import load_dotenv

load_dotenv()

# Few-Shot Examples
FEW_SHOT_EXAMPLES = """
# Contoh Jawaban TripTrove yang Baik:

Contoh 1 - Pertanyaan Harga:
Q: Berapa harga paket tour Borobudur?
A: Harga paket tour Borobudur & Prambanan adalah Rp 2.000.000. Dengan diskon 20%, harga akhirnya Rp 1.600.000 untuk 2 hari. Sudah termasuk hotel, guide, kendaraan, dan tiket masuk.

Contoh 2 - Pertanyaan Terms:
Q: Apa kebijakan pembatalan?
A: Kebijakan pembatalan TripTrove:
• Pembatalan >7 hari: Refund 80%
• Pembatalan 3-7 hari: Refund 50%
• Pembatalan <3 hari: Tidak dapat refund

Contoh 3 - Rekomendasi:
Q: Tour untuk keluarga?
A: Rekomendasi untuk keluarga:
1. Borobudur & Prambanan (Rp 1.600.000) - Edukasi sejarah, 2 hari
2. Yogyakarta City (Rp 1.800.000) - Wisata kota nyaman
Semua sudah termasuk kendaraan dan guide profesional.
"""

# State untuk agent
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    query: str
    context: str
    search_count: int
    needs_web_search: bool
    final_answer: str

class TripTroveAgent:
    def __init__(self, vectorstore_path="./chroma_db"):
        # Initialize LLM dengan parameter yang lebih baik
        self.llm = ChatOllama(
            model=os.getenv('LLM_MODEL', 'llama3.1'),
            temperature=0.3,  # Lebih rendah untuk jawaban lebih konsisten
            num_predict=512,  # Panjang response maksimal
        )
        
        # Initialize embeddings
        self.embeddings = OllamaEmbeddings(
            model=os.getenv('EMBEDDING_MODEL', 'nomic-embed-text')
        )
        
        # Load vector store
        self.vectorstore = Chroma(
            persist_directory=vectorstore_path,
            embedding_function=self.embeddings
        )
        
        # Initialize web search tool
        self.web_search = DuckDuckGoSearchRun()
        
        # Build graph
        self.graph = self._build_graph()
    
    def _build_graph(self):
        """Bangun graph untuk agentic workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze_query", self.analyze_query)
        workflow.add_node("search_database", self.search_database)
        workflow.add_node("web_search", self.web_search_node)
        workflow.add_node("generate_answer", self.generate_answer)
        workflow.add_node("evaluate_answer", self.evaluate_answer)
        
        # Set entry point
        workflow.set_entry_point("analyze_query")
        
        # Add edges
        workflow.add_edge("analyze_query", "search_database")
        workflow.add_conditional_edges(
            "search_database",
            self.should_web_search,
            {
                "web_search": "web_search",
                "generate": "generate_answer"
            }
        )
        workflow.add_edge("web_search", "generate_answer")
        workflow.add_conditional_edges(
            "generate_answer",
            self.should_continue,
            {
                "evaluate": "evaluate_answer",
                "end": END
            }
        )
        workflow.add_conditional_edges(
            "evaluate_answer",
            self.needs_refinement,
            {
                "refine": "search_database",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def analyze_query(self, state: AgentState):
        """Analisis query user dengan lebih detail"""
        query = state['query']
        
        # Gunakan LLM untuk memahami intent dengan lebih baik
        prompt = f"""Analisis pertanyaan berikut dan identifikasi:
1. Jenis pertanyaan (policy/harga/rekomendasi/informasi umum)
2. Kata kunci penting untuk pencarian
3. Apakah perlu informasi dari dokumen PDF atau database

Pertanyaan: {query}

Jawab dalam format:
Jenis: [policy/price/recommendation/general/review]
Keywords: [kata kunci dipisah koma]
Source: [pdf/database/both]
Fokus: [penjelasan singkat fokus pertanyaan]"""
        
        response = self.llm.invoke(prompt)
        analysis = response.content
        
        return {
            "messages": [SystemMessage(content=f"Query analysis:\n{analysis}")],
            "search_count": 0,
            "needs_web_search": False
        }
    
    def search_database(self, state: AgentState):
        """Cari di vector database dengan retrieval yang lebih baik"""
        query = state['query']
        search_count = state.get('search_count', 0)
        
        # Retrieve relevant documents dengan k yang lebih besar
        docs = self.vectorstore.similarity_search(query, k=8)
        
        # Prioritaskan dokumen PDF untuk pertanyaan tentang terms, policy, dll
        query_lower = query.lower()
        policy_keywords = ['term', 'condition', 'syarat', 'ketentuan', 'policy', 'kebijakan', 
                          'aturan', 'peraturan', 'pembatalan', 'refund']
        
        is_policy_question = any(keyword in query_lower for keyword in policy_keywords)
        
        if is_policy_question:
            # Prioritaskan dokumen PDF
            pdf_docs = [doc for doc in docs if doc.metadata.get('source_type') == 'pdf']
            db_docs = [doc for doc in docs if doc.metadata.get('source_type') != 'pdf']
            docs = pdf_docs + db_docs  # PDF di depan
        
        # Format context dengan lebih baik
        context_parts = []
        for i, doc in enumerate(docs):
            source_type = doc.metadata.get('source_type', 'database')
            source_name = doc.metadata.get('source', 'Unknown')
            
            if source_type == 'pdf':
                context_parts.append(f"[Dokumen PDF: {source_name}]\n{doc.page_content}")
            else:
                context_parts.append(f"[Database: {doc.metadata.get('type', 'data')}]\n{doc.page_content}")
        
        context = "\n\n---\n\n".join(context_parts)
        
        return {
            "context": context,
            "search_count": search_count + 1,
            "messages": [SystemMessage(content=f"Found {len(docs)} relevant documents ({len([d for d in docs if d.metadata.get('source_type')=='pdf'])} from PDF)")]
        }
    
    def should_web_search(self, state: AgentState):
        """Tentukan apakah perlu web search"""
        context = state.get('context', '')
        query = state['query'].lower()
        
        # Cek apakah pertanyaan tentang info terkini atau di luar database
        needs_web = any(keyword in query for keyword in [
            'terbaru', 'sekarang', 'hari ini', 'cuaca', 'weather',
            'berita', 'news', 'update', 'tips', 'rekomendasi umum'
        ])
        
        # Atau jika context kosong/kurang
        if not context or len(context) < 100:
            needs_web = True
        
        return "web_search" if needs_web else "generate"
    
    def web_search_node(self, state: AgentState):
        """Lakukan web search jika diperlukan"""
        query = state['query']
        
        try:
            search_results = self.web_search.run(query)
            web_context = f"\n\n[Informasi dari Web]\n{search_results}"
            
            current_context = state.get('context', '')
            combined_context = current_context + web_context
            
            return {
                "context": combined_context,
                "needs_web_search": True,
                "messages": [SystemMessage(content="Web search completed")]
            }
        except Exception as e:
            return {
                "messages": [SystemMessage(content=f"Web search failed: {str(e)}")]
            }
    
    def generate_answer(self, state: AgentState):
        """Generate jawaban dengan prompt yang lebih baik"""
        query = state['query']
        context = state.get('context', '')
        
        # Deteksi jenis pertanyaan
        query_lower = query.lower()
        is_policy_question = any(keyword in query_lower for keyword in 
                                ['term', 'condition', 'syarat', 'ketentuan', 'policy', 'kebijakan'])
        is_price_question = any(keyword in query_lower for keyword in 
                               ['harga', 'price', 'biaya', 'cost', 'berapa'])
        is_recommendation = any(keyword in query_lower for keyword in 
                               ['rekomendasi', 'recommend', 'saran', 'suggest', 'bagus'])
        
        # Buat prompt yang lebih spesifik
        if is_policy_question:
            system_instruction = """Kamu adalah asisten TripTrove yang ahli dalam menjelaskan kebijakan dan syarat ketentuan.
Tugas kamu:
1. Berikan informasi yang AKURAT dari dokumen yang tersedia
2. Jelaskan dengan JELAS dan TERSTRUKTUR
3. Gunakan poin-poin atau numbering untuk kemudahan baca
4. Jika ada informasi dari PDF, prioritaskan itu
5. Jangan mengarang informasi yang tidak ada di dokumen"""
        
        elif is_price_question:
            system_instruction = """Kamu adalah asisten TripTrove yang ahli dalam informasi harga dan paket tour.
Tugas kamu:
1. Sebutkan harga ASLI dan harga setelah DISKON (jika ada)
2. Format harga dengan jelas: Rp X.XXX.XXX
3. Sebutkan durasi dan fasilitas yang termasuk
4. Bandingkan beberapa paket jika relevan"""
        
        elif is_recommendation:
            system_instruction = """Kamu adalah asisten TripTrove yang ahli memberikan rekomendasi tour.
Tugas kamu:
1. Berikan 2-3 rekomendasi terbaik
2. Jelaskan KENAPA paket tersebut cocok
3. Sebutkan keunggulan masing-masing
4. Pertimbangkan budget, durasi, dan preferensi user"""
        
        else:
            system_instruction = """Kamu adalah asisten TripTrove yang ramah dan profesional.
Tugas kamu:
1. Jawab pertanyaan dengan AKURAT berdasarkan data yang ada
2. Gunakan format yang mudah dibaca
3. Berikan informasi lengkap tapi tidak bertele-tele
4. Jika tidak tahu, katakan dengan jujur"""
        
        prompt = f"""{system_instruction}

{FEW_SHOT_EXAMPLES}

---
Sekarang jawab dengan gaya yang sama seperti contoh di atas.

KONTEKS INFORMASI:
{context}

PERTANYAAN USER: {query}

INSTRUKSI JAWABAN:
- Jawab dalam Bahasa Indonesia yang natural dan profesional
- Gunakan format yang rapi (bullet points, numbering, atau paragraf)
- Jika menyebutkan harga, format: Rp X.XXX.XXX
- Jika ada diskon, hitung dan sebutkan harga akhir
- Jika informasi dari PDF, sebutkan sumbernya
- Jika tidak ada informasi yang cukup, katakan dengan jelas
- JANGAN mengarang informasi yang tidak ada di konteks
- Ikuti gaya jawaban dari contoh di atas

JAWABAN:"""
        
        response = self.llm.invoke(prompt)
        answer = response.content
        
        return {
            "final_answer": answer,
            "messages": [AIMessage(content=answer)]
        }
    
    def should_continue(self, state: AgentState):
        """Tentukan apakah perlu evaluasi atau langsung selesai"""
        search_count = state.get('search_count', 0)
        
        # Jika sudah search lebih dari 2 kali, langsung selesai
        if search_count >= 2:
            return "end"
        
        return "evaluate"
    
    def evaluate_answer(self, state: AgentState):
        """Evaluasi kualitas jawaban"""
        answer = state.get('final_answer', '')
        query = state['query']
        
        # Gunakan LLM untuk self-evaluation
        eval_prompt = f"""Evaluasi apakah jawaban berikut sudah cukup menjawab pertanyaan:

PERTANYAAN: {query}
JAWABAN: {answer}

Apakah jawaban ini:
1. Lengkap dan informatif?
2. Menjawab pertanyaan dengan tepat?
3. Memberikan detail yang cukup?

Jawab hanya: GOOD atau NEEDS_REFINEMENT"""
        
        evaluation = self.llm.invoke(eval_prompt)
        
        return {
            "messages": [SystemMessage(content=f"Evaluation: {evaluation.content}")]
        }
    
    def needs_refinement(self, state: AgentState):
        """Cek apakah perlu refinement"""
        messages = state.get('messages', [])
        search_count = state.get('search_count', 0)
        
        # Jika sudah 2x search, stop
        if search_count >= 2:
            return "end"
        
        # Cek evaluation result
        if messages:
            last_msg = messages[-1].content
            if "NEEDS_REFINEMENT" in last_msg:
                return "refine"
        
        return "end"
    
    def query(self, question: str):
        """Main method untuk query"""
        initial_state = {
            "messages": [HumanMessage(content=question)],
            "query": question,
            "context": "",
            "search_count": 0,
            "needs_web_search": False,
            "final_answer": ""
        }
        
        # Run the graph
        result = self.graph.invoke(initial_state)
        
        return result.get('final_answer', 'Maaf, saya tidak dapat menjawab pertanyaan Anda.')

if __name__ == "__main__":
    # Test agent
    agent = TripTroveAgent()
    
    test_queries = [
        "Paket tour apa saja yang tersedia?",
        "Berapa harga paket tour ke Bali?",
        "Ada rekomendasi paket tour untuk keluarga?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Q: {query}")
        print(f"{'='*60}")
        answer = agent.query(query)
        print(f"A: {answer}")
