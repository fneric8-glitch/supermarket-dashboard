# ─────────────────────────────────────────
# components/header_kpi.py — Header & KPI Cards
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd


def render_header(on_refresh):
    """Render logo header + tombol refresh."""
    hc1, hc2 = st.columns([9, 1])
    with hc1:
        st.markdown("""
        <div class='logo-wrap'>
            <div class='logo-icon'>🌊</div>
            <div>
                <div class='logo-title'>Ocean Supercenter</div>
                <div class='logo-sub'>
                    📊 Sales Analytics Dashboard &nbsp;|&nbsp;
                    Myanmar Branches 2019 &nbsp;|&nbsp;
                    Real-time Data Intelligence
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with hc2:
        if st.button("🔄", help="Refresh Data"):
            on_refresh()


def _kpi_card(col, icon: str, label: str, value: str,
               delta: str, is_sm: bool = False):
    """Render 1 KPI card ke dalam column yang diberikan."""
    val_class = "kpi-value-sm" if is_sm else "kpi-value"
    with col:
        st.markdown(f"""
        <div class='kpi-card'>
            <div class='kpi-top'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-icon'>{icon}</div>
            </div>
            <div class='{val_class}'>{value}</div>
            <div class='kpi-delta'>▲ {delta}</div>
        </div>
        """, unsafe_allow_html=True)


def render_kpi(df: pd.DataFrame):
    """
    Hitung metrik lalu render 6 KPI cards.
    Return dict metrics untuk dipakai komponen lain.
    """
    if not df.empty:
        tot_rev  = df['total'].sum()
        tot_trx  = len(df)
        tot_qty  = int(df['quantity'].sum())
        avg_ord  = df['total'].mean()
        top_prod = df.groupby('product_line')['total'].sum().idxmax()
        top_city = df.groupby('city')['total'].sum().idxmax()
        mem_pct  = df[df['customer_type'] == 'Member'].shape[0] / tot_trx * 100
    else:
        tot_rev = tot_trx = tot_qty = avg_ord = mem_pct = 0
        top_prod = top_city = '-'

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    _kpi_card(k1, "💰", "Total Revenue",   f"${tot_rev/1000:.2f}",  "+12.3% vs prev")
    _kpi_card(k2, "🧾", "Total Transaksi", f"{tot_trx:,}",      "+8.1% vs prev")
    _kpi_card(k3, "📦", "QTY Terjual",     f"{tot_qty:,}",      "+5.7% vs prev")
    _kpi_card(k4, "💵", "Avg Order Value", f"${avg_ord:,.0f}",  "+3.2% vs prev")
    _kpi_card(k5, "👑", "Top Product",     top_prod,            "Best Seller",   is_sm=True)
    _kpi_card(k6, "🏙️", "Top City",        top_city,            f"{mem_pct:.0f}% Member", is_sm=True)

    st.markdown("<div style='margin-top:6px;'></div>", unsafe_allow_html=True)

    return {
        'tot_rev': tot_rev, 'tot_trx': tot_trx,
        'tot_qty': tot_qty, 'avg_ord': avg_ord,
        'top_prod': top_prod, 'top_city': top_city,
        'mem_pct': mem_pct,
    }
