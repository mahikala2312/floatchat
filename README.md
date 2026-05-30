# 🌊 FloatChat — AI Ocean Intelligence

> Ask the Indian Ocean anything. Get instant, AI-powered answers backed by real oceanographic data.

**[🔗 Live Demo](https://floatchat-cnegona8bgfdnx5lvt....streamlit.app)** · **[📁 GitHub](https://github.com/mahikala2312/floatchat)**

<img width="1897" height="896" alt="image" src="https://github.com/user-attachments/assets/d1706ba7-e793-4759-8109-e5362cb77542" />
<img width="1897" height="880" alt="image" src="https://github.com/user-attachments/assets/25d1b90c-4205-4d27-8e0d-aa4b431615e5" />

---

## What is FloatChat?

The Indian Ocean has hundreds of robotic ARGO floats diving up to 2000 meters deep, collecting real temperature, salinity, and depth data. This data is publicly available — but locked inside complex scientific formats that only researchers with technical skills can access.

**FloatChat changes that.**

Type a question in plain English — *"What's the surface temperature in the Arabian Sea?"* — and get an intelligent answer instantly, backed by real data from INCOIS (Indian National Centre for Ocean Information Services).

---

## Features

- **Conversational AI** — Ask questions in plain English, get structured answers with real data
- **RAG Pipeline** — Retrieval Augmented Generation using FAISS vector search + LLaMA 3.1
- **Interactive Map** — Float locations visualized by temperature, salinity, or float ID
- **Live Float Panel** — Real-time metadata for each float (depth, temp, salinity, position)
- **Science Stream** — Live feed of oceanographic events and anomalies
- **Map Highlighting** — Floats mentioned in AI answers highlighted in cyan on the map

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Data | ARGO NetCDF files from INCOIS |
| Database | PostgreSQL |
| Vector Search | FAISS + sentence-transformers |
| LLM | LLaMA 3.1 via Groq API |
| AI Pipeline | RAG (Retrieval Augmented Generation) |
| Frontend | Streamlit + Plotly |
| Deployment | Streamlit Cloud |

---

## Architecture
User Query
↓
FAISS Vector Search (finds relevant float profiles)
↓
Context passed to LLaMA 3.1 via Groq
↓
Natural language answer + map highlighting

---

## Dataset

- **362 profiles** from 14 INCOIS ARGO floats
- **Indian Ocean** coverage — Arabian Sea, Bay of Bengal
- Real measurements: surface temperature (~28.8°C avg), salinity (~35.6 PSU avg), max depth up to 2033m
- Source: [data-argo.ifremer.fr](https://data-argo.ifremer.fr/dac/incois/)

---

## Run Locally

```bash
git clone https://github.com/mahikala2312/floatchat
cd floatchat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

Get a free Groq API key at [console.groq.com](https://console.groq.com)

Build the vector index:
```bash
python src/embeddings.py
```

Run the app:
```bash
streamlit run app.py
```

---

## Project Structure
floatchat/
├── src/
│   ├── ingest.py        # Downloads and parses NetCDF files
│   ├── embeddings.py    # Builds FAISS vector index
│   ├── rag.py           # RAG pipeline — search + LLM
│   └── utils.py
├── data/
│   ├── argo_profiles.csv
│   ├── faiss_index.bin
│   └── texts.pkl
├── app.py               # Streamlit frontend
├── requirements.txt
└── README.md

---

*Built with real oceanographic data from INCOIS and the global Argo float program.*
