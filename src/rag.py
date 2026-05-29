from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

def load_vector_store():
    index = faiss.read_index("data/faiss_index.bin")
    with open("data/texts.pkl", "rb") as f:
        texts = pickle.load(f)
    df = pd.read_pickle("data/profiles_df.pkl")
    return index, texts, df

def search(query, index, texts, model, k=5):
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), k)
    results = [texts[i] for i in indices[0]]
    return results

def ask(question):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index, texts, df = load_vector_store()
    
    relevant = search(question, index, texts, model)
    context = "\n".join(relevant)
    
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are FloatChat, an AI assistant for ARGO ocean float data from the Indian Ocean. Answer questions based on the data provided."},
                {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I encountered an error retrieving data. Please try again. ({str(e)})"
    
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Testing RAG pipeline...")
    answer = ask("Which floats are in the Arabian Sea?")
    print("\nAnswer:", answer)