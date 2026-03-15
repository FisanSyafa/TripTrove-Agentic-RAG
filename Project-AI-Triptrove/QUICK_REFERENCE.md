# ⚡ Quick Reference - TripTrove RAG

Referensi cepat untuk command dan path yang sering digunakan.

---

## 🚀 Quick Commands

### Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Setup database & data
cd scripts
setup.bat
```

### Run Applications
```bash
# Main UI (Port 8501)
cd scripts
run.bat

# Advanced UI (Port 8503)
run_advanced.bat

# Analytics Dashboard (Port 8502)
run_dashboard.bat
```

### Jupyter Notebooks
```bash
# Start Jupyter
jupyter notebook notebooks/

# Or specific notebook
jupyter notebook notebooks/02_rag_testing.ipynb
```

### Testing
```bash
# Test agent in terminal
python scripts/test_agent.py

# Check system requirements
python scripts/check_system.py
```

### Data Management
```bash
# Reload data to ChromaDB
python src/data_loader.py

# Prepare training data
python fine_tuning/prepare_training_data.py
```

---

## 📁 Important Paths

### Source Code
```
src/agent_rag.py          # Main RAG agent
src/data_loader.py        # Data loader
src/config.py             # Configuration
src/ui/app.py             # Main UI
src/ui/dashboard.py       # Analytics
src/ui/advanced_app.py    # Advanced UI
```

### Notebooks
```
notebooks/00_quick_test.ipynb              # Quick test
notebooks/01_data_exploration.ipynb        # Data analysis
notebooks/02_rag_testing.ipynb             # RAG testing
notebooks/03_prompt_engineering.ipynb      # Prompt optimization
notebooks/04_fine_tuning_experiments.ipynb # Fine-tuning
```

### Documentation
```
START_HERE.md                              # Quick start
README.md                                  # Main README
CHECKLIST.md                               # Setup checklist
docs/QUICK_START.md                        # Quick start guide
docs/PANDUAN_PENGGUNAAN.md                 # Usage guide
docs/INSTALASI_LENGKAP.md                  # Installation guide
docs/ARCHITECTURE.md                       # Architecture
docs/FINE_TUNING_COMPLETE_GUIDE.md        # Fine-tuning guide
```

### Configuration
```
.env                      # Environment variables
.env.example             # Template
src/config.py            # App configuration
requirements.txt         # Dependencies
```

---

## 🔧 Configuration Quick Edit

### Database (.env)
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=triptrove_db
```

### LLM Settings (src/config.py)
```python
LLM_MODEL = "llama3.1"
LLM_TEMPERATURE = 0.3
TOP_K_RESULTS = 8
```

### Few-Shot Examples (src/agent_rag.py)
```python
# Search for: FEW_SHOT_EXAMPLES
# Add your examples there
```

---

## 🎯 Common Tasks

### Add New PDF Document
```bash
# 1. Copy PDF to documents/
copy your-file.pdf documents/

# 2. Reload data
python src/data_loader.py
```

### Update Few-Shot Examples
```python
# Edit src/agent_rag.py
# Find FEW_SHOT_EXAMPLES list
# Add new example:
{
    'question': 'Your question',
    'answer': 'Ideal answer'
}
```

### Change LLM Temperature
```python
# Edit src/config.py
LLM_TEMPERATURE = 0.3  # Lower = more consistent
```

### Increase Retrieval Results
```python
# Edit src/config.py
TOP_K_RESULTS = 10  # More documents retrieved
```

---

## 🐛 Quick Troubleshooting

### Ollama Not Running
```bash
ollama serve
```

### Model Not Found
```bash
ollama pull llama3.1
```

### Database Connection Error
```bash
# Check MySQL service
# Verify .env credentials
```

### Port Already in Use
```bash
# Kill process on port
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Import Error
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### ChromaDB Error
```bash
# Delete and recreate
rmdir /s /q chroma_db
python src/data_loader.py
```

---

## 📊 URLs

```
Main UI:          http://localhost:8501
Dashboard:        http://localhost:8502
Advanced UI:      http://localhost:8503
```

---

## 🎓 Learning Path

1. **Start**: Read `START_HERE.md`
2. **Setup**: Follow `CHECKLIST.md`
3. **Learn**: Read `docs/QUICK_START.md`
4. **Experiment**: Try notebooks
5. **Optimize**: Read fine-tuning guide
6. **Deploy**: Production ready!

---

## 💡 Pro Tips

### Performance
- Lower temperature for consistency
- Increase k for better retrieval
- Add more few-shot examples
- Use specific queries

### Development
- Use notebooks for experiments
- Test in terminal first
- Check analytics dashboard
- Monitor performance

### Production
- Use advanced UI features
- Enable analytics tracking
- Export chat history
- Monitor errors

---

## 🔑 Key Files to Remember

```
START_HERE.md              # Your starting point
CHECKLIST.md               # Setup verification
QUICK_REFERENCE.md         # This file
src/agent_rag.py          # Main agent logic
src/config.py             # Configuration
.env                      # Credentials
```

---

## 📞 Quick Help

```bash
# System check
python scripts/check_system.py

# Test agent
python scripts/test_agent.py

# View logs
# Check terminal output
```

---

## 🎯 Most Used Commands

```bash
# 1. Run app
cd scripts && run.bat

# 2. Test in notebook
jupyter notebook notebooks/02_rag_testing.ipynb

# 3. Reload data
python src/data_loader.py

# 4. Check system
python scripts/check_system.py

# 5. View dashboard
cd scripts && run_dashboard.bat
```

---

**Bookmark this page for quick reference! 📌**
