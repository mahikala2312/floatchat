# 🌊 FloatChat

> AI-powered conversational interface for ARGO Indian Ocean float data

🔗 **[Live Demo](https://floatchat-cnegona8bgfdnx5lvt....streamlit.app)**  
📁 **[GitHub](https://github.com/mahikala2312/floatchat)**
<img width="1897" height="896" alt="image" src="https://github.com/user-attachments/assets/d1706ba7-e793-4759-8109-e5362cb77542" />
<img width="1897" height="880" alt="image" src="https://github.com/user-attachments/assets/25d1b90c-4205-4d27-8e0d-aa4b431615e5" />


## What it does
FloatChat lets you ask natural language questions about real ARGO ocean float data from the Indian Ocean. Type a question, get an intelligent AI answer backed by actual oceanographic data from INCOIS.

## Demo
Ask questions like:
- "Which floats are in the Arabian Sea?"
- "What depths did float 2902120 reach?"
- "Show me data from 2014"

## Tech Stack
- **Data**: ARGO NetCDF files from INCOIS, PostgreSQL, FAISS vector store
- **AI**: RAG pipeline with sentence-transformers + Groq LLM (LLaMA 3.1)
- **Frontend**: Streamlit, Plotly maps
- **Dataset**: 78 real profiles from 3 Indian Ocean floats

## How to run locally
```bash
git clone https://github.com/mahikala2312/floatchat
cd floatchat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Add your GROQ_API_KEY to .env
streamlit run app.py
```

## Architecture
User Query → FAISS semantic search → retrieve relevant float profiles → LLM generates answer
