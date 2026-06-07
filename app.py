# ─────────────────────────────────────────
# app.py — Entry point utama
# Jalankan: streamlit run app.py
# ─────────────────────────────────────────

import streamlit as st

# ── Setup page (WAJIB paling pertama) ──
st.set_page_config(
    page_title="Ocean Supercenter Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Import modul lokal ──
from styles   import inject_css
from database import load_data, invalidate_cache
from components.sidebar     import render_sidebar, apply_filters
from components.header_kpi  import render_header, render_kpi
from components.tab_overview  import render as render_overview
from components.tab_analytics import render as render_analytics
from components.tab_map       import render as render_map
from components.tab_data      import render as render_data
from components.tab_insights  import render as render_insights


def main():
    # 1. Inject CSS global
    inject_css()

    # 2. Load data mentah dari DB
    df_raw = load_data()

    # 3. Render sidebar & ambil nilai filter
    filters = render_sidebar(df_raw)

    # 4. Apply filter ke data
    df = apply_filters(df_raw.copy(), filters)

    # 5. Header + KPI (refresh button juga di sini)
    render_header(on_refresh=lambda: (invalidate_cache(), st.rerun()))
    metrics = render_kpi(df)

    # 6. Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview",
        "📈 Analytics",
        "🗺️ Branch Map",
        "📋 Data Table",
        "💡 Insights",
    ])

    with tab1: render_overview(df, metrics)
    with tab2: render_analytics(df)
    with tab3: render_map(df)
    with tab4:
        all_products = sorted(df_raw['product_line'].dropna().unique()) if not df_raw.empty else []
        all_pays     = sorted(df_raw['payment_method'].dropna().unique()) if not df_raw.empty else []
        all_cities   = sorted(df_raw['city'].dropna().unique()) if not df_raw.empty else []
        render_data(df, all_products, all_pays, all_cities)
    with tab5: render_insights(df)

    # 7. Footer
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px 0;
                border-top:1px solid rgba(153,202,255,0.15);
                margin-top:28px; color:#4A6FA5; font-size:12px;'>
        🌊 <b style='color:#1883FF;'>Ocean Supercenter</b> Analytics Dashboard
        &nbsp;|&nbsp; Myanmar Branches: Yangon · Mandalay · Naypyitaw
        &nbsp;|&nbsp; Data: Jan–Mar 2019 &nbsp;|&nbsp; Built with Streamlit & Plotly
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
