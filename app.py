import streamlit as st
import plotly.express as px
import pandas as pd
import sys
sys.path.append("src")
from rag import ask

st.set_page_config(page_title="FloatChat", page_icon="🌊", layout="wide")

st.title("🌊 FloatChat")
st.caption("AI-powered conversational interface for ARGO Indian Ocean float data")

df = pd.read_csv("data/argo_profiles.csv")

# Stats bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Profiles", len(df))
col2.metric("Unique Floats", df["float_id"].nunique())
col3.metric("Avg Temperature", f"{df['temp_surface_c'].mean():.1f}°C")
col4.metric("Avg Salinity", f"{df['salinity_surface'].mean():.1f} PSU")

st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "highlighted_floats" not in st.session_state:
    st.session_state.highlighted_floats = []

left, right = st.columns([1, 1])

with left:
    st.subheader("💬 Ask about the ocean data")
    
    # Sample questions
    st.caption("Try asking:")
    sample_cols = st.columns(2)
    samples = [
        "Which floats are in the Arabian Sea?",
        "What is the surface temperature?",
        "Which float reached the deepest depth?",
        "Show me salinity data"
    ]
    for i, sample in enumerate(samples):
        with sample_cols[i % 2]:
            if st.button(sample, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": sample})
                with st.spinner("Searching ocean data..."):
                    response = ask(sample)
                st.session_state.messages.append({"role": "assistant", "content": response})
                found_ids = [fid for fid in df["float_id"].unique() if str(fid) in response]
                st.session_state.highlighted_floats = found_ids
                st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything about the Indian Ocean float data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Searching ocean data..."):
                response = ask(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        found_ids = [fid for fid in df["float_id"].unique() if str(fid) in response]
        st.session_state.highlighted_floats = found_ids
        st.rerun()

with right:
    st.subheader("🗺️ Float Locations — Indian Ocean")

    view_mode = st.radio("Color by:", ["Float ID", "Temperature", "Salinity"], horizontal=True)

    map_df = df.copy()
    if st.session_state.highlighted_floats:
        map_df["highlighted"] = map_df["float_id"].apply(
            lambda x: "Mentioned" if x in st.session_state.highlighted_floats else "Other"
        )
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True, "highlighted": False},
            color="highlighted",
            color_discrete_map={"Mentioned": "red", "Other": "blue"},
            zoom=3, height=520, mapbox_style="open-street-map"
        )
    elif view_mode == "Temperature":
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="temp_surface_c",
            color_continuous_scale="RdYlBu_r",
            labels={"temp_surface_c": "Temp (°C)"},
            zoom=3, height=520, mapbox_style="open-street-map"
        )
    elif view_mode == "Salinity":
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="salinity_surface",
            color_continuous_scale="Blues",
            labels={"salinity_surface": "Salinity (PSU)"},
            zoom=3, height=520, mapbox_style="open-street-map"
        )
    else:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="float_id",
            zoom=3, height=520, mapbox_style="open-street-map"
        )

    st.plotly_chart(fig, use_container_width=True)

    if st.session_state.highlighted_floats:
        st.info(f"🔴 Floats highlighted: {st.session_state.highlighted_floats}")

st.divider()
st.caption(f"Data: {len(df)} profiles from {df['float_id'].nunique()} INCOIS ARGO floats | Indian Ocean | Source: data-argo.ifremer.fr")