# 🏗️ TripTrove RAG System Architecture

## Overview

TripTrove RAG System adalah sistem AI Assistant yang menggunakan pendekatan Agentic RAG (Retrieval-Augmented Generation) untuk memberikan informasi tentang paket tour secara intelligent dan interaktif.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Streamlit UI │  │ Advanced UI  │  │  Dashboard   │      │
│  │   (app.py)   │  │(advanced.py) │  │(dashboard.py)│      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                    Agent Layer                                │
│                  (agent_rag.py)                               │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LangGraph Orchestration                  │   │
│  │                                                        │   │
│  │  1. Analyze Query                                     │   │
│  │       ↓                                               │   │
│  │  2. Search Database (ChromaDB)                        │   │
│  │       ↓                                               │   │
│  │  3. Evaluate Context                                  │   │
│  │       ↓                                               │   │
│  │  4. Web Search (if needed)                            │   │
│  │       ↓                                               │   │
│  │  5. Generate Answer (LLM)                             │   │
│  │       ↓                                               │   │
│  │  6. Self-Evaluation                                   │   │
│  │       ↓                                               │   │
│  │  7. Refine (if needed) or Return                      │   │
│  └──────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────┘
          │                  │                  │
          ↓                  ↓                  ↓
┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
│   Ollama LLM    │  │  ChromaDB    │  │ DuckDuckGo   │
│  (Llama 3.1)    │  │ Vector Store │  │ Web Search   │
└─────────────────┘  └──────────────┘  └──────────────┘
                             ↑
                             │
┌────────────────────────────┼─────────────────────────────────┐
│                    Data Layer                                 │
│                  (data_loader.py)                             │
│                                                               │
│  ┌──────────────┐         ┌──────────────┐                  │
│  │    MySQL     │────────→│  Embeddings  │                  │
│  │  TripTrove   │         │  Generation  │                  │
│  │   Database   │         └──────┬───────┘                  │
│  └──────────────┘                │                           │
│                                   ↓                           │
│                          ┌──────────────┐                    │
│                          │  ChromaDB    │                    │
│                          │ Persistence  │                    │
│                          └──────────────┘                    │
└───────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. User Interface Layer

#### app.py (Basic UI)
- Simple chat interface
- Example queries
- Chat history
- Basic statistics

#### advanced_app.py (Advanced UI)
- Multi-language support
- Export functionality
- Advanced statistics
- Enhanced UX

#### dashboard.py (Analytics)
- Performance monitoring
- Query analytics
- Error tracking
- Trend visualization

### 2. Agent Layer (agent_rag.py)

#### LangGraph Workflow

```python
State = {
    messages: List[Message],
    query: str,
    context: str,
    search_count: int,
    needs_web_search: bool,
    final_answer: str
}

Nodes:
1. analyze_query    - Understand user intent
2. search_database  - Retrieve from vector store
3. web_search       - Search web if needed
4. generate_answer  - Create response
5. evaluate_answer  - Self-assess quality
```

#### Decision Points

```
should_web_search():
  - Check if context is sufficient
  - Detect need for current info
  - Return: "web_search" or "generate"

should_continue():
  - Check iteration count
  - Return: "evaluate" or "end"

needs_refinement():
  - Evaluate answer quality
  - Return: "refine" or "end"
```

### 3. Data Layer

#### data_loader.py

**Process:**
1. Connect to MySQL
2. Query tour packages + destinations + itineraries
3. Query reviews
4. Format as Documents
5. Generate embeddings (Nomic-Embed-Text)
6. Store in ChromaDB

**Data Structure:**
```python
Document {
    page_content: str,  # Rich text content
    metadata: {
        id: int,
        name: str,
        category: str,
        price: float,
        discount: int,
        type: str  # 'tour_package' or 'review'
    }
}
```

### 4. Supporting Components

#### config.py
- Environment configuration
- Database settings
- Model parameters
- RAG settings

#### utils.py
- Price formatting
- Duration formatting
- Text processing
- Data validation

#### analytics.py
- Query logging
- Performance tracking
- Error logging
- Statistics generation

## Data Flow

### Query Processing Flow

```
User Input
    ↓
[Analyze Query]
    ↓
Extract intent & keywords
    ↓
[Search Database]
    ↓
Similarity search in ChromaDB
    ↓
Retrieve top-k documents
    ↓
[Evaluate Context]
    ↓
Is context sufficient? ──No──→ [Web Search]
    ↓ Yes                            ↓
[Generate Answer] ←──────────────────┘
    ↓
Use LLM to create response
    ↓
[Self-Evaluation]
    ↓
Is answer good? ──No──→ [Refine Search]
    ↓ Yes                      ↓
Return to User ←───────────────┘
```

### Data Loading Flow

```
MySQL Database
    ↓
[Extract Data]
    ↓
Tour Packages + Reviews
    ↓
[Format Documents]
    ↓
Rich text with metadata
    ↓
[Generate Embeddings]
    ↓
Nomic-Embed-Text model
    ↓
[Store in ChromaDB]
    ↓
Vector Database Ready
```

## Technology Stack

### Core Technologies
- **Python 3.8+**: Programming language
- **LangChain**: LLM framework
- **LangGraph**: Agent orchestration
- **Ollama**: Local LLM runtime

### Models
- **Llama 3.1**: Main LLM (8B parameters)
- **Nomic-Embed-Text**: Embedding model

### Storage
- **ChromaDB**: Vector database
- **MySQL**: Source database

### UI & Visualization
- **Streamlit**: Web interface
- **Plotly**: Charts and graphs

### Tools
- **DuckDuckGo Search**: Web search
- **python-dotenv**: Configuration

## Key Features

### 1. Agentic Behavior
- Self-directed search
- Iterative refinement
- Quality evaluation
- Adaptive responses

### 2. Multi-Source RAG
- Database retrieval
- Web search integration
- Context combination
- Source prioritization

### 3. Local-First
- No API costs
- Privacy preserved
- Offline capable
- Full control

### 4. Scalable Design
- Modular components
- Easy to extend
- Configurable
- Well-documented

## Performance Considerations

### Optimization Strategies

1. **Embedding Caching**
   - Pre-compute embeddings
   - Store in ChromaDB
   - Fast retrieval

2. **Query Optimization**
   - Limit top-k results
   - Filter by metadata
   - Efficient similarity search

3. **LLM Efficiency**
   - Appropriate temperature
   - Context window management
   - Prompt optimization

4. **Resource Management**
   - Lazy loading
   - Connection pooling
   - Memory management

## Security & Privacy

### Data Protection
- Local processing only
- No external API calls (except web search)
- Database credentials in .env
- No data logging to cloud

### Best Practices
- Environment variables for secrets
- Input validation
- Error handling
- Secure connections

## Extensibility

### Adding New Data Sources

```python
# In data_loader.py
def load_custom_data(self):
    # Query your data
    # Format as Documents
    # Return documents
    pass
```

### Adding New Tools

```python
# In agent_rag.py
from langchain_community.tools import YourTool

self.custom_tool = YourTool()
# Add to workflow
```

### Customizing UI

```python
# In app.py or advanced_app.py
# Modify CSS
# Add new components
# Change layout
```

## Deployment

### Local Development
```bash
python data_loader.py
streamlit run app.py
```

### Production Considerations
- Use production database
- Configure proper logging
- Set up monitoring
- Optimize performance
- Handle errors gracefully

## Future Enhancements

### Planned Improvements
1. Multi-agent collaboration
2. Persistent sessions
3. User authentication
4. API endpoints
5. Mobile app
6. Real-time updates
7. Advanced analytics
8. A/B testing

---

**Architecture Version**: 1.0.0  
**Last Updated**: 2026-03-10
