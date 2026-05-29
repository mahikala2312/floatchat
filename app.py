import streamlit as st
import plotly.express as px
import pandas as pd
import sys
sys.path.append("src")
from rag import ask, load_vector_store
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="FloatChat", page_icon="🌊", layout="wide")

st.title("🌊 FloatChat")
st.caption("AI-powered conversational interface for ARGO Indian Ocean float data")

df = pd.read_csv("data/argo_profiles.csv")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Ask about the ocean data")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("e.g. Which floats are in the Arabian Sea?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Searching ocean data..."):
                response = ask(prompt)
            st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.subheader("Float Locations — Indian Ocean")
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="float_id",
        hover_data=["date", "max_depth_m"],
        color="float_id",
        zoom=3,
        height=500,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption(f"Dataset: {len(df)} profiles from INCOIS ARGO floats | Indian Ocean")