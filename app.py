import streamlit as st
import plotly.express as px
import pandas as pd
import sys
from datetime import datetime
sys.path.append("src")
from rag import ask

st.set_page_config(page_title="FloatChat | Marine Intelligence", page_icon="🌊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Inter:wght@300;400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
html, body, .stApp { background: radial-gradient(circle at 50% -20%, #002B4D 0%, #101415 60%) !important; color: #e0e3e5 !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stAppViewContainer"] { padding: 0 !important; }
.top-nav { background: rgba(16,20,21,0.9); backdrop-filter: blur(16px); border-bottom: 1px solid rgba(59,73,76,0.4); padding: 1rem 3rem; display: flex; justify-content: space-between; align-items: center; }
.nav-logo { font-size: 1.4rem; font-weight: 800; color: #00e5ff; letter-spacing: -0.5px; }
.glass-panel { background: rgba(255,255,255,0.03); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.08); border-radius: 16px; }
.widget-label { font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem; letter-spacing: 3px; color: #849396; text-transform: uppercase; margin-bottom: 0.8rem; }
.map-preview { border-radius: 10px; height: 130px; background: linear-gradient(135deg, #001a2e, #002d4a); display: flex; align-items: center; justify-content: center; font-size: 3rem; position: relative; margin-bottom: 0.8rem; }
.map-coords { position: absolute; bottom: 6px; left: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #849396; background: rgba(16,20,21,0.8); padding: 2px 6px; border-radius: 4px; }
.stat-row { display: flex; justify-content: space-between; align-items: center; padding: 0.45rem 0.6rem; background: rgba(25,28,30,0.8); border: 1px solid rgba(59,73,76,0.3); border-radius: 8px; margin-bottom: 0.4rem; }
.stat-row-label { font-size: 0.72rem; color: #849396; }
.stat-row-val { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #9cf0ff; }
.stream-item { padding: 0.6rem 0 0.6rem 0.8rem; margin-bottom: 0.6rem; }
.stream-item.active { border-left: 2px solid #00e5ff; }
.stream-item.inactive { border-left: 2px solid #3b494c; }
.stream-time { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #849396; margin-bottom: 0.2rem; }
.stream-text { font-size: 0.72rem; line-height: 1.4; }
.stream-text.highlight { color: #00e5ff; }
.user-msg { display: flex; flex-direction: column; align-items: flex-end; margin-bottom: 1.2rem; }
.user-bubble { background: rgba(50,53,55,0.8); border: 1px solid rgba(59,73,76,0.4); border-radius: 16px; border-top-right-radius: 4px; padding: 0.9rem 1.2rem; max-width: 85%; font-size: 0.88rem; line-height: 1.5; }
.ai-msg { display: flex; flex-direction: column; align-items: flex-start; margin-bottom: 1.2rem; }
.ai-bubble { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid #00e5ff; border-radius: 16px; border-top-left-radius: 4px; padding: 1.1rem 1.3rem; max-width: 92%; font-size: 0.88rem; line-height: 1.6; }
.ai-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.8rem; }
.ai-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 2px; color: #00e5ff; text-transform: uppercase; }
.msg-meta { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #849396; margin-top: 0.4rem; padding: 0 4px; }
.telemetry-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 1rem; }
.telemetry-card { background: rgba(0,0,0,0.25); border: 1px solid rgba(59,73,76,0.4); border-radius: 10px; padding: 0.7rem 0.9rem; }
.tele-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #849396; text-transform: uppercase; letter-spacing: 1px; }
.tele-val { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: #9cf0ff; font-weight: 600; margin-top: 0.2rem; }
.node-label { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; color: #00e5ff; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.3rem; }
.float-title { font-size: 1.3rem; font-weight: 800; color: #e0e3e5; margin-bottom: 1.2rem; }
.meta-label { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #849396; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 0.2rem; }
.meta-val { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #e0e3e5; margin-bottom: 0.9rem; }
.battery-bar { height: 5px; background: rgba(59,73,76,0.5); border-radius: 999px; overflow: hidden; margin-bottom: 0.3rem; }
.battery-fill { height: 100%; background: #00e5ff; border-radius: 999px; }
.cycle-dots { display: flex; gap: 4px; margin-bottom: 0.3rem; }
.cycle-dot { height: 4px; flex: 1; border-radius: 999px; }
.cycle-active { background: #00e5ff; }
.cycle-inactive { background: #3b494c; }
.cycle-note { font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #849396; text-align: right; }
.pulse-dot { width: 8px; height: 8px; background: #00e5ff; border-radius: 50%; animation: pulse 2s infinite; display: inline-block; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }
.bottom-bar { background: rgba(11,15,16,0.9); border-top: 1px solid rgba(59,73,76,0.25); padding: 0.8rem 3rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.68rem; color: #849396; font-family: 'JetBrains Mono', monospace; margin-top: 1rem; }
[data-testid="stChatInput"] textarea { background: rgba(25,28,30,0.9) !important; border: none !important; border-bottom: 2px solid #3b494c !important; border-radius: 12px 12px 0 0 !important; color: #e0e3e5 !important; font-size: 0.9rem !important; }
[data-testid="stChatInput"] textarea:focus { border-bottom-color: #00e5ff !important; }
[data-testid="stChatMessage"] { background: transparent !important; border: none !important; padding: 0 !important; }
.stButton > button { background: transparent !important; border: 1px solid rgba(59,73,76,0.5) !important; border-radius: 6px !important; color: #849396 !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 1px !important; padding: 0.35rem 0.6rem !important; transition: all 0.2s !important; }
.stButton > button:hover { background: rgba(0,229,255,0.08) !important; border-color: rgba(0,229,255,0.3) !important; color: #c3f5ff !important; }
.stSpinner > div { border-top-color: #00e5ff !important; }
</style>
""", unsafe_allow_html=True)

df = pd.read_csv("data/argo_profiles.csv")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "highlighted_floats" not in st.session_state:
    st.session_state.highlighted_floats = []
if "last_float" not in st.session_state:
    st.session_state.last_float = df["float_id"].iloc[0]

now = datetime.now().strftime("%H:%M")

# NAV
st.markdown(f"""
<div class="top-nav">
    <div class="nav-logo">≋ FloatChat</div>
    <div style="display:flex; align-items:center; gap:0.8rem;">
        <span class="pulse-dot"></span>
        <span style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; letter-spacing:2px; color:#849396;">ARGO TELEMETRY LIVE</span>
    </div>
    <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; color:#849396;">
        {len(df)} profiles · {df["float_id"].nunique()} floats · INCOIS
    </div>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 1.8, 1])

with left:
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; gap:0.8rem; padding:1rem 0.5rem;">
        <div class="glass-panel" style="padding:1rem;">
            <div class="widget-label">Geospatial Focus</div>
            <div class="map-preview">🌊<div class="map-coords">LAT: 15.42° N | LON: 65.12° E</div></div>
            <div class="stat-row"><span class="stat-row-label">Active Floats</span><span class="stat-row-val">{df["float_id"].nunique()}</span></div>
            <div class="stat-row"><span class="stat-row-label">Total Profiles</span><span class="stat-row-val">{len(df)}</span></div>
            <div class="stat-row"><span class="stat-row-label">Avg Temp</span><span class="stat-row-val">{df["temp_surface_c"].mean():.1f}°C</span></div>
            <div class="stat-row"><span class="stat-row-label">Avg Salinity</span><span class="stat-row-val">{df["salinity_surface"].mean():.1f} PSU</span></div>
            <div class="stat-row"><span class="stat-row-label">Anomaly Alert</span><span class="stat-row-val">None</span></div>
        </div>
        <div class="glass-panel" style="padding:1rem;">
            <div class="widget-label">Science Stream</div>
            <div class="stream-item active">
                <div class="stream-time">{now} UTC</div>
                <div class="stream-text highlight">Float #{st.session_state.last_float} depth: {df["max_depth_m"].max():.0f}m.</div>
            </div>
            <div class="stream-item inactive">
                <div class="stream-time">{now} UTC</div>
                <div class="stream-text">Salinity: {df["salinity_surface"].mean():.1f} PSU in Arabian Sea.</div>
            </div>
            <div class="stream-item inactive">
                <div class="stream-time">{now} UTC</div>
                <div class="stream-text">Sat handshake: {df["float_id"].nunique()} nodes active.</div>
            </div>
            <div class="stream-item inactive">
                <div class="stream-time">{now} UTC</div>
                <div class="stream-text">Temp anomaly: +{(df["temp_surface_c"].max() - df["temp_surface_c"].mean()):.1f}°C above baseline.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with center:
    if not st.session_state.messages:
        st.markdown("""
        <div class="glass-panel" style="margin:1rem 0; padding:3rem 2rem; text-align:center; box-shadow:0 25px 60px rgba(0,0,0,0.4);">
            <div style="font-size:3rem; margin-bottom:1rem;">🌊</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.65rem; letter-spacing:3px; color:#849396; text-transform:uppercase; margin-bottom:1rem;">ARGO TELEMETRY LIVE</div>
            <div style="font-size:1.8rem; font-weight:800; color:#e0e3e5; margin-bottom:0.8rem; line-height:1.2;">Democratizing<br><span style="color:#00e5ff;">Ocean Science.</span></div>
            <div style="font-size:0.85rem; color:#849396; line-height:1.6; max-width:400px; margin:0 auto;">Ask the Indian Ocean anything in plain English. Powered by real INCOIS ARGO float data.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-panel" style="margin:1rem 0; padding:1.5rem; box-shadow:0 25px 60px rgba(0,0,0,0.4);">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-msg">
                    <div class="user-bubble">{message["content"]}</div>
                    <div class="msg-meta">{now} • USER</div>
                </div>""", unsafe_allow_html=True)
            else:
                temp = df["temp_surface_c"].mean()
                sal = df["salinity_surface"].mean()
                st.markdown(f"""
                <div class="ai-msg">
                    <div class="ai-bubble">
                        <div class="ai-header"><span>🔬</span><span class="ai-label">FloatChat Engine v1.0</span></div>
                        <div>{message["content"]}</div>
                        <div class="telemetry-grid">
                            <div class="telemetry-card"><div class="tele-label">Avg Salinity</div><div class="tele-val">{sal:.1f} PSU</div></div>
                            <div class="telemetry-card"><div class="tele-label">Avg Temp</div><div class="tele-val">{temp:.1f}°C</div></div>
                        </div>
                    </div>
                    <div class="msg-meta">{now} • FLOATCHAT AI</div>
                </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns(4)
    samples = [
        ("Arabian Sea?", "Which floats are in the Arabian Sea?"),
        ("Surface Temp?", "What is the surface temperature?"),
        ("Deepest Float?", "Which float reached the deepest depth?"),
        ("Salinity Data?", "Compare salinity across floats")
    ]
    for col, (label, full) in zip([b1, b2, b3, b4], samples):
        with col:
            if st.button(label, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": full})
                with st.spinner("Searching..."):
                    response = ask(full)
                st.session_state.messages.append({"role": "assistant", "content": response})
                found = [fid for fid in df["float_id"].unique() if str(fid) in response]
                st.session_state.highlighted_floats = found
                if found:
                    st.session_state.last_float = found[0]
                st.rerun()

    if prompt := st.chat_input("Query the ocean nodes..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Searching..."):
            response = ask(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
        found = [fid for fid in df["float_id"].unique() if str(fid) in response]
        st.session_state.highlighted_floats = found
        if found:
            st.session_state.last_float = found[0]
        st.rerun()

with right:
    float_data = df[df["float_id"] == st.session_state.last_float]
    fd = float_data.iloc[0] if len(float_data) > 0 else df.iloc[0]
    st.markdown(f"""
    <div style="padding:1rem 0.5rem;">
    <div class="glass-panel" style="padding:1.3rem; position:relative; overflow:hidden;">
        <div style="position:absolute; right:-3rem; top:-3rem; width:12rem; height:12rem; background:rgba(0,229,255,0.04); border-radius:50%; filter:blur(30px);"></div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.3rem;">
            <div class="node-label">Node Identifier</div>
            <span class="pulse-dot"></span>
        </div>
        <div class="float-title">ARGO Float<br>#{st.session_state.last_float}</div>
        <div class="meta-label">Last Known Position</div>
        <div class="meta-val">{fd["latitude"]:.3f}°N, {fd["longitude"]:.3f}°E</div>
        <div class="meta-label">Last Profile Date</div>
        <div class="meta-val">{fd["date"]}</div>
        <div class="meta-label">Max Depth Reached</div>
        <div class="meta-val">{fd["max_depth_m"]}m</div>
        <div class="meta-label">Surface Temperature</div>
        <div class="meta-val" style="color:#00e5ff; font-size:1.1rem;">{fd["temp_surface_c"]}°C</div>
        <div class="meta-label">Surface Salinity</div>
        <div class="meta-val">{fd["salinity_surface"]} PSU</div>
        <div class="meta-label">Battery Health</div>
        <div class="battery-bar"><div class="battery-fill" style="width:82%;"></div></div>
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#849396; text-align:right; margin-bottom:0.8rem;">82%</div>
        <div class="meta-label">Cycle Progress</div>
        <div class="cycle-dots">
            <div class="cycle-dot cycle-active"></div>
            <div class="cycle-dot cycle-active"></div>
            <div class="cycle-dot cycle-active"></div>
            <div class="cycle-dot cycle-inactive"></div>
            <div class="cycle-dot cycle-inactive"></div>
        </div>
        <div class="cycle-note">Step 3 of 5: Descending</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# MAP SECTION
st.markdown('<div style="padding: 0 1.5rem;">', unsafe_allow_html=True)
st.markdown('<div style="font-family:JetBrains Mono,monospace; font-size:0.62rem; letter-spacing:3px; color:#849396; text-transform:uppercase; margin-bottom:0.8rem; padding-top:1rem;">🛰 ARGO MISSION STATUS — Live Float Positions</div>', unsafe_allow_html=True)

map_col1, map_col2 = st.columns([3, 1])
with map_col1:
    map_df = df.copy()
    view_mode = st.radio("", ["Float ID", "🌡 Temperature", "💧 Salinity"], horizontal=True, label_visibility="collapsed")
    if st.session_state.highlighted_floats:
        map_df["status"] = map_df["float_id"].apply(lambda x: "Mentioned" if x in st.session_state.highlighted_floats else "Other")
        fig = px.scatter_mapbox(map_df, lat="latitude", lon="longitude", hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True, "status": False},
            color="status", color_discrete_map={"Mentioned": "#00e5ff", "Other": "#294b6f"},
            zoom=3, height=380, mapbox_style="carto-darkmatter")
    elif "Temperature" in view_mode:
        fig = px.scatter_mapbox(map_df, lat="latitude", lon="longitude", hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="temp_surface_c", color_continuous_scale="thermal", labels={"temp_surface_c": "Temp (°C)"},
            zoom=3, height=380, mapbox_style="carto-darkmatter")
    elif "Salinity" in view_mode:
        fig = px.scatter_mapbox(map_df, lat="latitude", lon="longitude", hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="salinity_surface", color_continuous_scale="ice", labels={"salinity_surface": "Salinity (PSU)"},
            zoom=3, height=380, mapbox_style="carto-darkmatter")
    else:
        fig = px.scatter_mapbox(map_df, lat="latitude", lon="longitude", hover_name="float_id",
            hover_data={"date": True, "temp_surface_c": True, "salinity_surface": True, "max_depth_m": True},
            color="float_id", zoom=3, height=380, mapbox_style="carto-darkmatter")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(bgcolor="rgba(16,20,21,0.8)", bordercolor="rgba(59,73,76,0.4)", font=dict(color="#849396", size=10)))
    st.plotly_chart(fig, use_container_width=True)

with map_col2:
    insight = f'Floats {st.session_state.highlighted_floats} highlighted. Avg temp: {df[df["float_id"].isin(st.session_state.highlighted_floats)]["temp_surface_c"].mean():.1f}°C.' if st.session_state.highlighted_floats else "Ask a question to highlight specific floats and get AI-powered oceanographic insights."
    border_color = "#00e5ff" if st.session_state.highlighted_floats else "#3b494c"
    st.markdown(f"""
    <div class="glass-panel" style="padding:1.2rem; margin-top:2.5rem;">
        <div class="widget-label">AI Intelligence</div>
        <div style="border-left:3px solid {border_color}; padding-left:0.8rem; margin:0.8rem 0; font-size:0.78rem; color:#bac9cc; font-style:italic; line-height:1.6;">"{insight}"</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# FOOTER
st.markdown(f"""
<div class="bottom-bar">
    <span>© 2024 FloatChat Project. Indian Ocean Marine Data Initiative.</span>
    <span style="color:#00e5ff;">{len(df)} profiles · {df["float_id"].nunique()} floats · INCOIS Argo Program · RAG + LLaMA 3.1</span>
</div>
""", unsafe_allow_html=True)