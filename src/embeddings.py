from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pandas as pd
import pickle
import os

def build_vector_store():
    print("Loading data...")
    df = pd.read_csv("data/argo_profiles.csv")
    
    texts = []
    for _, row in df.iterrows():
        text = f"Argo float {row['float_id']} at latitude {row['latitude']} longitude {row['longitude']} on {row['date']}. Max depth {row['max_depth_m']} meters. Source file {row['source_file']}."
        texts.append(text)
    
    print("Creating embeddings...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True)
    
    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))
    
    os.makedirs("data", exist_ok=True)
    faiss.write_index(index, "data/faiss_index.bin")
    
    with open("data/texts.pkl", "wb") as f:
        pickle.dump(texts, f)
    
    df.to_pickle("data/profiles_df.pkl")
    
    print(f"Done! Indexed {len(texts)} profiles.")

if __name__ == "__main__":
    build_vector_store()