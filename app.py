import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import re
sys.path.append("src")
from rag import ask

st.set_page_config(page_title="FloatChat", page_icon="🌊", layout="wide")

st.title("🌊 FloatChat")
st.caption("AI-powered conversational interface for ARGO Indian Ocean float data")

df = pd.read_csv("data/argo_profiles.csv")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "highlighted_floats" not in st.session_state:
    st.session_state.highlighted_floats = []

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Ask about the ocean data")
    
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
        
        found_ids = []
        for float_id in df["float_id"].unique():
            if str(float_id) in response:
                found_ids.append(float_id)
        st.session_state.highlighted_floats = found_ids
        st.rerun()

with col2:
    st.subheader("Float Locations — Indian Ocean")
    
    map_df = df.copy()
    if st.session_state.highlighted_floats:
        map_df["highlighted"] = map_df["float_id"].apply(
            lambda x: "Mentioned" if x in st.session_state.highlighted_floats else "Other"
        )
        color_col = "highlighted"
        color_map = {"Mentioned": "red", "Other": "blue"}
    else:
        map_df["highlighted"] = "All floats"
        color_col = "highlighted"
        color_map = {"All floats": "blue"}
    
    fig = px.scatter_mapbox(
        map_df,
        lat="latitude",
        lon="longitude",
        hover_name="float_id",
        hover_data=["date", "max_depth_m"],
        color=color_col,
        color_discrete_map=color_map,
        zoom=3,
        height=550,
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    if st.session_state.highlighted_floats:
        st.info(f"🔴 Highlighted floats mentioned in answer: {st.session_state.highlighted_floats}")

st.markdown("---")
st.caption(f"Dataset: {len(df)} profiles from INCOIS ARGO floats | Indian Ocean")