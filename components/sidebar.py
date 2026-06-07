# ─────────────────────────────────────────
# components/sidebar.py — Sidebar & Filter
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd


def render_sidebar(df_raw: pd.DataFrame) -> dict:
    """
    Render sidebar dengan logo, filter, dan info.
    Return dict berisi nilai filter yang dipilih user.
    """
    with st.sidebar:
        # ── Logo ──
        st.markdown("""
        <div style='text-align:center; padding:18px 0 20px 0;'>
            <div style='font-size:46px; margin-bottom:6px;'>🌊</div>
            <div style='font-size:18px; font-weight:900; letter-spacing:2px; color:#FFFFFF;'>OCEAN</div>
            <div style='font-size:11px; letter-spacing:4px; color:#C8DEFF; font-weight:600;'>SUPERCENTER</div>
            <div style='margin-top:6px; font-size:10px; color:rgba(255,255,255,0.5);'>Analytics Dashboard</div>
        </div>
        <hr style='border-color:rgba(255,255,255,0.2); margin:0 0 18px 0;'>
        """, unsafe_allow_html=True)

        def label(text):
            st.markdown(
                f"<div style='font-size:11px; color:#C8DEFF; font-weight:700; "
                f"text-transform:uppercase; letter-spacing:1px; margin:10px 0 6px 0;'>"
                f"{text}</div>",
                unsafe_allow_html=True
            )

        # ── Opsi filter (dinamis dari data) ──
        cities   = sorted(df_raw['city'].dropna().unique()) if not df_raw.empty else []
        pays     = sorted(df_raw['payment_method'].dropna().unique()) if not df_raw.empty else []
        custs    = sorted(df_raw['customer_type'].dropna().unique()) if not df_raw.empty else []
        genders  = sorted(df_raw['gender'].dropna().unique()) if not df_raw.empty else []

        label("🏙️ Filter City")
        sel_city = st.selectbox("", ['All Cities'] + cities,
                                label_visibility="collapsed", key='sb_city')

        label("💳 Filter Payment")
        sel_pay = st.selectbox("", ['All Payments'] + pays,
                               label_visibility="collapsed", key='sb_pay')

        label("👤 Filter Customer Type")
        sel_cust = st.selectbox("", ['All Types'] + custs,
                                label_visibility="collapsed", key='sb_cust')

        label("⚧ Filter Gender")
        sel_gender = st.selectbox("", ['All Gender'] + genders,
                                  label_visibility="collapsed", key='sb_gender')

        # ── Info ──
        st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin:18px 0;'>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:11px; color:rgba(255,255,255,0.65);
                    text-align:center; line-height:1.9;'>
            📅 Data Period<br>
            <strong style='color:white;'>Jan – Mar 2019</strong><br><br>
            🏪 3 Branches &nbsp;|&nbsp; 🇲🇲 Myanmar
        </div>
        """, unsafe_allow_html=True)

    return {
        'city':    sel_city,
        'payment': sel_pay,
        'cust':    sel_cust,
        'gender':  sel_gender,
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """
    Apply filter dari sidebar ke dataframe.
    Return dataframe yang sudah difilter.
    """
    if df.empty:
        return df
    if filters['city']    != 'All Cities':   df = df[df['city'] == filters['city']]
    if filters['payment'] != 'All Payments': df = df[df['payment_method'] == filters['payment']]
    if filters['cust']    != 'All Types':    df = df[df['customer_type'] == filters['cust']]
    if filters['gender']  != 'All Gender':   df = df[df['gender'] == filters['gender']]
    return df
