# ─────────────────────────────────────────
# styles.py — Global CSS untuk seluruh app
# ─────────────────────────────────────────

import streamlit as st


def inject_css():
    """Inject semua custom CSS ke halaman Streamlit."""
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* ── App Background ── */
.stApp {
    background: linear-gradient(160deg, #021B5E 0%, #042E7B 40%, #031E5A 100%);
    min-height: 100vh;
}
.block-container { padding: 1.2rem 2rem 2rem 2rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #004EE0 0%, #1883FF 60%, #0D3FA3 100%) !important;
    border-right: 2px solid rgba(153,202,255,0.3) !important;
}
[data-testid="stSidebar"] * { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    color: white !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] label {
    color: #E3F2FF !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── KPI Cards ── */
.kpi-card {
    background: linear-gradient(135deg, #0D3FA3 0%, #004EE0 100%);
    border: 1px solid rgba(153,202,255,0.35);
    border-radius: 14px;
    padding: 18px 20px 16px 20px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0,78,224,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(24,131,255,0.45);
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #1883FF, #99CAFF);
}
.kpi-top  { display: flex; justify-content: space-between; align-items: flex-start; }
.kpi-label {
    color: #99CAFF; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.2px; line-height: 1.3;
}
.kpi-icon  { font-size: 26px; opacity: 0.9; flex-shrink: 0; margin-left: 8px; }
.kpi-value {
    color: #FFFFFF; font-size: 26px; font-weight: 900;
    line-height: 1.1; white-space: nowrap;
    overflow: hidden; text-overflow: ellipsis;
}
.kpi-value-sm {
    color: #FFFFFF; font-size: 17px; font-weight: 800;
    line-height: 1.25; word-break: break-word;
}
.kpi-delta {
    font-size: 11px; font-weight: 600; color: #00E676;
    display: flex; align-items: center; gap: 3px;
}

/* ── Section Headers ── */
.section-hdr {
    color: #FFFFFF; font-size: 15px; font-weight: 800;
    letter-spacing: 0.3px; margin: 20px 0 12px 0;
    padding: 0 0 10px 12px;
    border-left: 4px solid #1883FF;
    border-bottom: 1px solid rgba(153,202,255,0.2);
    text-transform: uppercase;
    display: flex; align-items: center; gap: 8px;
}

/* ── Chart Wrapper ── */
.chart-wrap {
    background: linear-gradient(145deg, #0A2F85 0%, #0D3FA3 100%);
    border: 1px solid rgba(153,202,255,0.25);
    border-radius: 14px; padding: 16px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.25);
    margin-bottom: 12px;
}
.chart-title {
    color: #E3F2FF; font-size: 13px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.8px;
    margin-bottom: 10px; padding-bottom: 8px;
    border-bottom: 1px solid rgba(153,202,255,0.15);
    display: flex; align-items: center; gap: 6px;
}

/* ── Insight Cards ── */
.ins-card {
    background: linear-gradient(135deg, #0A2F85, #0D3FA3);
    border-left: 4px solid #1883FF; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 10px;
    border: 1px solid rgba(24,131,255,0.4);
    border-left: 4px solid #1883FF;
}
.ins-title {
    color: #99CAFF; font-size: 13px; font-weight: 800;
    margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;
}
.ins-text { color: #E3F2FF; font-size: 13px; line-height: 1.55; }

/* ── Recommendation Cards ── */
.rec-card {
    background: linear-gradient(135deg, #0A2F85, #042E7B);
    border-left: 4px solid #00E676; border-radius: 10px;
    padding: 14px 16px; margin-bottom: 10px;
    border: 1px solid rgba(0,230,118,0.3);
    border-left: 4px solid #00E676;
}
.rec-title {
    color: #00E676; font-size: 13px; font-weight: 800;
    margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.5px;
}
.rec-text { color: #E3F2FF; font-size: 13px; line-height: 1.55; }

/* ── Map Cards ── */
.map-card {
    background: linear-gradient(135deg, #0D3FA3, #004EE0);
    border: 1px solid rgba(153,202,255,0.35); border-radius: 14px;
    padding: 18px 20px; box-shadow: 0 4px 20px rgba(0,78,224,0.3);
    position: relative; overflow: hidden; height: 130px;
}
.map-card::after {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 3px; background: linear-gradient(90deg, #1883FF, #99CAFF);
}
.map-branch {
    color: #99CAFF; font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 4px;
}
.map-rev   { color: #FFFFFF; font-size: 28px; font-weight: 900; line-height: 1.1; }
.map-meta  { color: #C8DEFF; font-size: 11px; margin-top: 6px; line-height: 1.6; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(13,63,163,0.6); border-radius: 10px;
    padding: 4px; gap: 4px;
    border: 1px solid rgba(153,202,255,0.2);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 8px !important;
    color: #99CAFF !important; font-weight: 600 !important;
    font-size: 13px !important; padding: 6px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: #1883FF !important; color: #FFFFFF !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #004EE0, #1883FF) !important;
    color: white !important; border: none !important;
    border-radius: 8px !important; font-weight: 700 !important;
    padding: 8px 20px !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1883FF, #99CAFF) !important;
    transform: translateY(-1px) !important;
}

/* ── Form Inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background: rgba(13,63,163,0.6) !important;
    border: 1px solid rgba(153,202,255,0.4) !important;
    color: white !important; border-radius: 8px !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label, .stMultiSelect label {
    color: #99CAFF !important; font-weight: 700 !important;
    font-size: 12px !important; text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── Multiselect Tags ── */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #004EE0 !important;
    border: 1px solid rgba(153,202,255,0.5) !important;
    border-radius: 6px !important;
    color: #FFFFFF !important; font-weight: 600 !important; font-size: 12px !important;
}
[data-testid="stMultiSelect"] span[data-baseweb="tag"] span { color: #FFFFFF !important; }
[data-testid="stMultiSelect"] > div > div {
    background: rgba(13,63,163,0.6) !important;
    border: 1px solid rgba(153,202,255,0.4) !important;
    border-radius: 8px !important;
}

/* ── Plotly Legend Fix ── */
.js-plotly-plot .plotly .legend text { fill: #E3F2FF !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid rgba(153,202,255,0.2);
}

/* ── Hide Streamlit Defaults ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Logo Header ── */
.logo-wrap { display: flex; align-items: center; gap: 10px; padding: 4px 0 16px 0; }
.logo-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, #1883FF, #004EE0);
    border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 22px;
}
.logo-title { font-size: 26px; font-weight: 900; color: #FFFFFF; line-height: 1; }
.logo-sub   { font-size: 11px; color: #99CAFF; font-weight: 500; margin-top: 2px; }
</style>
    """, unsafe_allow_html=True)
