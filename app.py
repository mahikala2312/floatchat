import streamlit as st
import plotly.express as px
import pandas as pd
import sys
sys.path.append("src")
from rag import ask

st.set_page_config(page_title="FloatChat", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

.stApp {
    background: linear-gradient(180deg, 
        #001a2e 0%, 
        #002d4a 15%, 
        #003d5c 30%, 
        #00526e 45%, 
        #006480 55%, 
        #004060 70%, 
        #002040 85%, 
        #001020 100%);
    min-height: 100vh;
}

#MainMenu, footer, header {visibility: hidden;}

/* Floating particles */
.ocean-bg {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}

.bubble {
    position: absolute;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(0,212,255,0.15), rgba(0,150,200,0.05));
    border: 1px solid rgba(0,212,255,0.1);
    animation: float 8s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0px) scale(1); opacity: 0.3; }
    50% { transform: translateY(-20px) scale(1.05); opacity: 0.6; }
}

/* Hero */
.hero-section {
    padding: 3rem 2rem 2rem 2rem;
    text-align: center;
    position: relative;
}

.ocean-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 4px;
    color: #38bdf8;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-main {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 7rem;
    line-height: 0.9;
    letter-spacing: 2px;
    color: white;
    text-shadow: 0 0 60px rgba(0,212,255,0.3), 0 0 120px rgba(0,150,200,0.2);
}

.hero-main span {
    color: #38bdf8;
    text-shadow: 0 0 40px rgba(56,189,248,0.6);
}

.hero-sub {
    font-family: 'Inter', sans-serif;
    color: rgba(255,255,255,0.55);
    font-size: 1rem;
    font-weight: 300;
    margin-top: 1.2rem;
    letter-spacing: 0.5px;
}

.divider-line {
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    margin: 1.5rem auto;
}

/* Badges */
.badge-row {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}

.tech-badge {
    background: rgba(56,189,248,0.08);
    border: 1px solid rgba(56,189,248,0.2);
    border-radius: 6px;
    padding: 0.4rem 1rem;
    font-size: 0.73rem;
    color: #7dd3fc;
    font-weight: 500;
    letter-spacing: 0.5px;
    font-family: 'Inter', sans-serif;
}

/* Stat cards */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}

.stat-card {
    background: rgba(0,45,74,0.6);
    border: 1px solid rgba(56,189,248,0.15);
    border-top: 2px solid;
    border-radius: 16px;
    padding: 1.5rem 1rem;
    text-align: center;
    backdrop-filter: blur(20px);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    font-family: 'Inter', sans-serif;
}

.stat-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
}

.stat-icon { font-size: 1.8rem; margin-bottom: 0.6rem; }

.stat-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: white;
    line-height: 1;
    letter-spacing: 1px;
}

.stat-lbl {
    font-size: 0.68rem;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 0.3rem;
    font-weight: 600;
}

/* Content panels */
.content-panel {
    background: rgba(0,30,55,0.7);
    border: 1px solid rgba(56,189,248,0.12);
    border-radius: 20px;
    padding: 1.8rem;
    backdrop-filter: blur(30px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3), inset 0 1px 0 rgba(56,189,248,0.1);
}

.panel-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    color: white;
    letter-spacing: 2px;
    margin-bottom: 0.3rem;
}

.panel-sub {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.35);
    font-family: 'Inter', sans-serif;
    margin-bottom: 1.2rem;
    letter-spacing: 0.3px;
}

/* Buttons */
.stButton > button {
    background: rgba(56,189,248,0.06) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    color: #7dd3fc !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
    text-align: left !important;
}

.stButton > button:hover {
    background: rgba(56,189,248,0.15) !important;
    border-color: #38bdf8 !important;
    color: white !important;
    transform: translateX(5px) !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.2) !important;
}

/* Chat */
[data-testid="stChatMessage"] {
    background: rgba(0,40,70,0.5) !important;
    border: 1px solid rgba(56,189,248,0.1) !important;
    border-radius: 14px !important;
    margin-bottom: 0.6rem !important;
}

[data-testid="stChatMessage"] p {
    color: rgba(255,255,255,0.85) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}

[data-testid="stChatInput"] textarea {
    background: rgba(0,30,55,0.8) !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    border-radius: 12px !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
}

/* Radio */
.stRadio [data-testid="stMarkdownContainer"] p {
    color: rgba(255,255,255,0.6) !important;
    font-size: 0.82rem !important;
    font-family: 'Inter', sans-serif !important;
}

/* Info */
[data-testid="stAlert"] {
    background: rgba(56,189,248,0.06) !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 10px !important;
    color: #7dd3fc !important;
}

hr { border-color: rgba(56,189,248,0.08) !important; }

[data-testid="stCaptionContainer"] p {
    color: rgba(255,255,255,0.2) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.75rem !important;
}

/* Decorative ocean elements */
.ocean-deco {
    position: fixed;
    font-size: 8rem;
    opacity: 0.03;
    pointer-events: none;
    z-index: 0;
}
</style>

<!-- Decorative elements -->
<div class="ocean-deco" style="bottom: 10%; right: 3%; transform: rotate(20deg);">🐋</div>
<div class="ocean-deco" style="top: 20%; left: 2%; transform: rotate(-15deg); font-size: 5rem;">🪸</div>
<div class="ocean-deco" style="bottom: 30%; left: 5%; font-size: 4rem;">🐠</div>
""", unsafe_allow_html=True)

df = pd.read_csv("data/argo_profiles.csv")

# Hero
st.markdown("""
<div class="hero-section">
    <div class="ocean-label">🛰 Indian Ocean · ARGO Float Intelligence</div>
    <div class="hero-main">FLOAT<br><span>CHAT</span></div>
    <div class="divider-line"></div>
    <div class="hero-sub">Ask questions about real ocean data in plain English — get instant AI-powered answers</div>
    <div class="badge-row">
        <span class="tech-badge">🤖 RAG + LLaMA 3.1</span>
        <span class="tech-badge">🗄 PostgreSQL</span>
        <span class="tech-badge">🔍 FAISS Vector Search</span>
        <span class="tech-badge">📡 INCOIS Argo Data</span>
        <span class="tech-badge">🗺 Interactive Map</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats
s1, s2, s3, s4 = st.columns(4)
stats = [
    (s1, "🗂", len(df), "TOTAL PROFILES", "#38bdf8"),
    (s2, "🛰", df["float_id"].nunique(), "UNIQUE FLOATS", "#a78bfa"),
    (s3, "🌡", f"{df['temp_surface_c'].mean():.1f}°C", "AVG TEMPERATURE", "#fb7185"),
    (s4, "💧", f"{df['salinity_surface'].mean():.1f}", "AVG SALINITY PSU", "#34d399"),
]
for col, icon, val, label, color in stats:
    with col:
        st.markdown(f"""
        <div class="stat-card" style="border-top-color: {color};">
            <div class="stat-icon">{icon}</div>
            <div class="stat-num" style="color: {color};">{val}</div>
            <div class="stat-lbl">{label}</div>
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
    <div class="content-panel">
        <div class="panel-header">ASK THE OCEAN</div>
        <div class="panel-sub">Click a sample question or type your own below</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

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
                with st.spinner("🌊 Searching ocean data..."):
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
            with st.spinner("🌊 Searching ocean data..."):
                response = ask(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        found_ids = [fid for fid in df["float_id"].unique() if str(fid) in response]
        st.session_state.highlighted_floats = found_ids
        st.rerun()

with right:
    st.markdown("""
    <div class="content-panel">
        <div class="panel-header">OCEAN MAP</div>
        <div class="panel-sub">362 real profiles · INCOIS Argo floats · Indian Ocean</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    view_mode = st.radio("Visualize by:", ["Float ID", "🌡 Temperature", "💧 Salinity"], horizontal=True)

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
            color_discrete_map={"Mentioned": "#fb7185", "Other": "#38bdf8"},
            zoom=3, height=460, mapbox_style="carto-darkmatter"
        )
    elif "Temperature" in view_mode:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="temp_surface_c", color_continuous_scale="thermal",
            labels={"temp_surface_c": "Temp (°C)"},
            zoom=3, height=460, mapbox_style="carto-darkmatter"
        )
    elif "Salinity" in view_mode:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="salinity_surface", color_continuous_scale="ice",
            labels={"salinity_surface": "Salinity (PSU)"},
            zoom=3, height=460, mapbox_style="carto-darkmatter"
        )
    else:
        fig = px.scatter_mapbox(
            map_df, lat="latitude", lon="longitude",
            hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="float_id",
            zoom=3, height=460, mapbox_style="carto-darkmatter"
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(
            bgcolor="rgba(0,20,40,0.8)",
            bordercolor="rgba(56,189,248,0.2)",
            font=dict(color="rgba(255,255,255,0.7)", size=11)
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color="rgba(255,255,255,0.6)"),
            title=dict(font=dict(color="rgba(255,255,255,0.6)"))
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    if st.session_state.highlighted_floats:
        st.info(f"🔴 Highlighted: Float IDs {st.session_state.highlighted_floats}")

st.divider()
st.caption(f"📡 {len(df)} profiles · {df['float_id'].nunique()} floats · INCOIS / Argo Program · RAG + LLaMA 3.1 + FAISS")