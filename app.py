import streamlit as st
import plotly.express as px
import pandas as pd
import sys
sys.path.append("src")
from rag import ask

st.set_page_config(page_title="FloatChat", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

.stApp {
    background: #f8faff;
}

#MainMenu, footer, header {visibility: hidden;}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 40%, #f093fb 100%);
    border-radius: 28px;
    padding: 3rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '🌊';
    position: absolute;
    font-size: 12rem;
    opacity: 0.06;
    top: -2rem;
    left: -2rem;
    transform: rotate(-15deg);
}

.hero::after {
    content: '🛰';
    position: absolute;
    font-size: 8rem;
    opacity: 0.06;
    bottom: -1rem;
    right: 2rem;
    transform: rotate(15deg);
}

.hero-title {
    font-size: 3.8rem;
    font-weight: 800;
    color: white;
    letter-spacing: -2px;
    line-height: 1;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
}

.hero-sub {
    color: rgba(255,255,255,0.85);
    font-size: 1.1rem;
    margin-top: 0.8rem;
    font-weight: 400;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    font-size: 0.78rem;
    color: white;
    margin: 0.6rem 0.2rem 0 0.2rem;
    font-weight: 500;
    letter-spacing: 0.3px;
}

.stat-card {
    background: white;
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 24px rgba(102,126,234,0.08);
    border: 1px solid rgba(102,126,234,0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    height: 100%;
}

.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(102,126,234,0.15);
}

.stat-icon { font-size: 2rem; margin-bottom: 0.5rem; }

.stat-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #1e1b4b;
    line-height: 1;
}

.stat-label {
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.4rem;
    font-weight: 600;
}

.stat-accent { 
    width: 40px; 
    height: 3px; 
    border-radius: 4px; 
    margin: 0.6rem auto 0 auto; 
}

.panel {
    background: white;
    border-radius: 24px;
    padding: 1.8rem;
    box-shadow: 0 4px 24px rgba(102,126,234,0.06);
    border: 1px solid rgba(102,126,234,0.06);
    height: 100%;
}

.panel-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e1b4b;
    margin-bottom: 0.3rem;
}

.panel-sub {
    font-size: 0.82rem;
    color: #94a3b8;
    margin-bottom: 1.2rem;
}

.stButton > button {
    background: #f8faff !important;
    border: 1.5px solid #e0e7ff !important;
    border-radius: 12px !important;
    color: #4338ca !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: #eef2ff !important;
    border-color: #818cf8 !important;
    color: #3730a3 !important;
    transform: translateX(3px) !important;
    box-shadow: 0 4px 12px rgba(102,126,234,0.15) !important;
}

[data-testid="stChatMessage"] {
    background: #f8faff !important;
    border: 1px solid #e0e7ff !important;
    border-radius: 16px !important;
    margin-bottom: 0.6rem !important;
}

[data-testid="stChatInput"] textarea {
    background: #f8faff !important;
    border: 1.5px solid #e0e7ff !important;
    border-radius: 14px !important;
    color: #1e1b4b !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #818cf8 !important;
    box-shadow: 0 0 0 3px rgba(129,140,248,0.15) !important;
}

.stRadio > label { color: #64748b !important; font-size: 0.82rem !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #475569 !important; font-size: 0.85rem !important; }

hr { border-color: #e0e7ff !important; margin: 2rem 0 !important; }

[data-testid="stAlert"] {
    background: #eef2ff !important;
    border: 1px solid #c7d2fe !important;
    border-radius: 12px !important;
    color: #4338ca !important;
}

[data-testid="stCaptionContainer"] p { color: #94a3b8 !important; font-size: 0.78rem !important; }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/argo_profiles.csv")

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-title">🌊 FloatChat</div>
    <div class="hero-sub">Ask questions about real Indian Ocean data in plain English — get instant AI answers</div>
    <div>
        <span class="badge">🤖 RAG + LLaMA 3.1</span>
        <span class="badge">🗄 PostgreSQL</span>
        <span class="badge">🔍 FAISS Vector Search</span>
        <span class="badge">🛰 INCOIS Argo Data</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats
s1, s2, s3, s4 = st.columns(4)
cards = [
    (s1, "🗂", len(df), "Total Profiles", "#667eea"),
    (s2, "🛰", df["float_id"].nunique(), "Unique Floats", "#f093fb"),
    (s3, "🌡", f"{df['temp_surface_c'].mean():.1f}°C", "Avg Temperature", "#f5576c"),
    (s4, "💧", f"{df['salinity_surface'].mean():.1f} PSU", "Avg Salinity", "#4facfe"),
]
for col, icon, val, label, color in cards:
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-value">{val}</div>
            <div class="stat-label">{label}</div>
            <div class="stat-accent" style="background:{color}"></div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "highlighted_floats" not in st.session_state:
    st.session_state.highlighted_floats = []

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("""
    <div class="panel-title">💬 Ask about the ocean</div>
    <div class="panel-sub">Click a sample question or type your own</div>
    """, unsafe_allow_html=True)

    sc1, sc2 = st.columns(2)
    samples = [
        "Which floats are in the Arabian Sea?",
        "What is the surface temperature?",
        "Which float reached deepest depth?",
        "Compare salinity across floats"
    ]
    for i, sample in enumerate(samples):
        with (sc1 if i % 2 == 0 else sc2):
            if st.button(sample, use_container_width=True, key=f"btn_{i}"):
                st.session_state.messages.append({"role": "user", "content": sample})
                with st.spinner("Searching ocean data..."):
                    response = ask(sample)
                st.session_state.messages.append({"role": "assistant", "content": response})
                found_ids = [fid for fid in df["float_id"].unique() if str(fid) in response]
                st.session_state.highlighted_floats = found_ids
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything about Indian Ocean float data..."):
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
    st.markdown("""
    <div class="panel-title">🗺️ Float Locations — Indian Ocean</div>
    <div class="panel-sub">362 real profiles from INCOIS Argo floats</div>
    """, unsafe_allow_html=True)

    view_mode = st.radio("Color by:", ["Float ID", "🌡 Temperature", "💧 Salinity"], horizontal=True)

    map_df = df.copy()

    if st.session_state.highlighted_floats:
        map_df["status"] = map_df["float_id"].apply(
            lambda x: "Mentioned" if x in st.session_state.highlighted_floats else "Other"
        )
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True, "status": False},
            color="status",
            color_discrete_map={"Mentioned": "#f5576c", "Other": "#667eea"},
            zoom=3, height=480, mapbox_style="carto-positron"
        )
    elif "Temperature" in view_mode:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="temp_surface_c", color_continuous_scale="RdYlBu_r",
            labels={"temp_surface_c": "Temp (°C)"},
            zoom=3, height=480, mapbox_style="carto-positron"
        )
    elif "Salinity" in view_mode:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="salinity_surface", color_continuous_scale="Blues",
            labels={"salinity_surface": "Salinity (PSU)"},
            zoom=3, height=480, mapbox_style="carto-positron"
        )
    else:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="float_id",
            zoom=3, height=480, mapbox_style="carto-positron"
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    st.plotly_chart(fig, use_container_width=True)

    if st.session_state.highlighted_floats:
        st.info(f"🔴 Floats highlighted on map: {st.session_state.highlighted_floats}")

st.divider()
st.caption(f"📡 {len(df)} profiles · {df['float_id'].nunique()} floats · INCOIS / Argo Program · Built with RAG + LLaMA 3.1 + FAISS Vector Search")