# ─────────────────────────────────────────
# components/tab_analytics.py — Tab 2: Deep Analytics
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import PRODUCT_COLOR_MAP


def apply_theme(fig, h=340, legend=True):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E3F2FF', family='Inter', size=12),
        height=h, margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(
            bgcolor='rgba(13,63,163,0.7)', bordercolor='rgba(153,202,255,0.3)',
            borderwidth=1, font=dict(color='#FFFFFF', size=11),
        ) if legend else dict(visible=False),
        hoverlabel=dict(bgcolor='#0A2F85', bordercolor='#1883FF',
                        font=dict(color='white', size=12))
    )
    fig.update_xaxes(gridcolor='rgba(153,202,255,0.08)', color='#E3F2FF',
                     linecolor='rgba(153,202,255,0.2)', tickfont=dict(color='#FFFFFF', size=11))
    fig.update_yaxes(gridcolor='rgba(153,202,255,0.08)', color='#E3F2FF',
                     linecolor='rgba(153,202,255,0.2)', tickfont=dict(color='#FFFFFF', size=11))
    return fig


def render(df: pd.DataFrame):
    if df.empty:
        st.warning("Tidak ada data.")
        return

    # ── Row 1: Payment Revenue + Top Qty ──
    a1, a2 = st.columns(2, gap="medium")

    with a1:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>💳 Revenue by Payment Method</div>",
                    unsafe_allow_html=True)
        pm = (df.groupby('payment_method')['total'].sum()
                .reset_index().sort_values('total', ascending=False))
        fig = go.Figure(go.Bar(
            x=pm['payment_method'], y=pm['total'],
            marker=dict(color=['#1883FF', '#004EE0', '#99CAFF'], cornerradius=6),
            text=[f'${v:,.0f}' for v in pm['total']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=12),
            hovertemplate='<b>%{x}</b><br>$%{y:,.0f}<extra></extra>'
        ))
        fig = apply_theme(fig, 300, legend=False)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        fig.update_xaxes(tickangle=0, tickfont=dict(color='#FFFFFF', size=12))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with a2:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>🏆 Top Product Line by Quantity</div>",
                    unsafe_allow_html=True)
        pq = (df.groupby('product_line')['quantity'].sum()
                .sort_values(ascending=True).reset_index())
        colors = [PRODUCT_COLOR_MAP.get(p, '#1883FF') for p in pq['product_line']]
        fig = go.Figure(go.Bar(
            x=pq['quantity'], y=pq['product_line'], orientation='h',
            marker=dict(color=colors, cornerradius=5),
            text=[f'{v:,} pcs' for v in pq['quantity']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=11),
            hovertemplate='<b>%{y}</b><br>Qty: %{x:,}<extra></extra>'
        ))
        fig = apply_theme(fig, 300, legend=False)
        fig.update_yaxes(tickfont=dict(color='#FFFFFF', size=11))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 2: Gender x Product + Heatmap ──
    a3, a4 = st.columns(2, gap="medium")

    with a3:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>⚧ Revenue by Gender & Product</div>",
                    unsafe_allow_html=True)
        gp = df.groupby(['product_line', 'gender'])['total'].sum().reset_index()
        fig = px.bar(
            gp, x='product_line', y='total', color='gender', barmode='group',
            color_discrete_map={'Male': '#1883FF', 'Female': '#F50057'},
            labels={'total': 'Revenue ($)', 'product_line': '', 'gender': 'Gender'},
        )
        fig = apply_theme(fig, 340)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        fig.update_xaxes(
            tickangle=0, tickfont=dict(color='#FFFFFF', size=10),
            tickmode='array',
            tickvals=gp['product_line'].unique(),
            ticktext=[p.replace(' and ', '<br>') for p in gp['product_line'].unique()]
        )
        fig.update_layout(
            margin=dict(l=12, r=12, t=36, b=80),
            legend=dict(title=dict(text='Gender', font=dict(color='#FFFFFF')),
                        font=dict(color='#FFFFFF', size=12),
                        bgcolor='rgba(13,63,163,0.7)',
                        bordercolor='rgba(153,202,255,0.3)', borderwidth=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with a4:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>🔥 Heatmap: Branch × Product Revenue</div>",
                    unsafe_allow_html=True)
        from config import BRANCH_LABEL
        ht = df.pivot_table(index='branch', columns='product_line',
                            values='total', aggfunc='sum').fillna(0)
        ht.index = [BRANCH_LABEL.get(i, i) for i in ht.index]
        fig = go.Figure(go.Heatmap(
            z=ht.values, x=[c[:12] for c in ht.columns], y=list(ht.index),
            colorscale=[[0.0,'#042E7B'],[0.3,'#004EE0'],[0.6,'#1883FF'],[1.0,'#E3F2FF']],
            text=[[f'${v:,.0f}' for v in row] for row in ht.values],
            texttemplate='%{text}', textfont=dict(size=10, color='white'),
            hovertemplate='%{y} × %{x}<br><b>$%{z:,.0f}</b><extra></extra>',
            showscale=True,
            colorbar=dict(tickfont=dict(color='#FFFFFF'),
                          title=dict(text='Revenue', font=dict(color='#FFFFFF')))
        ))
        fig = apply_theme(fig, 320, legend=False)
        fig.update_xaxes(tickfont=dict(color='#FFFFFF', size=10), tickangle=0)
        fig.update_yaxes(tickfont=dict(color='#FFFFFF', size=11))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Scatter Plot: Avg Revenue per Price Bin ──
    st.markdown(
        "<div class='chart-wrap'><div class='chart-title'>"
        "🔵 Unit Price vs Avg Total Revenue (per Product)</div>",
        unsafe_allow_html=True
    )
    df_sc = df.copy()
    df_sc['price_bin'] = (df_sc['unit_price'] // 5 * 5).astype(int)
    sc_agg = (df_sc.groupby(['price_bin', 'product_line'])
                   .agg(avg_total=('total', 'mean'), count=('total', 'count'))
                   .reset_index()
                   .rename(columns={'price_bin': 'unit_price', 'avg_total': 'total'}))
    fig = px.scatter(
        sc_agg, x='unit_price', y='total',
        color='product_line', size='count', size_max=30,
        color_discrete_map=PRODUCT_COLOR_MAP,
        hover_data={'count': True, 'unit_price': ':.0f', 'total': ':,.0f'},
        labels={'unit_price': 'Unit Price ($)', 'total': 'Avg Total Revenue ($)',
                'product_line': 'Product', 'count': 'Jumlah Transaksi'},
        opacity=0.85
    )
    fig = apply_theme(fig, 400)
    fig.update_xaxes(tickprefix='$')
    fig.update_yaxes(tickprefix='$', tickformat=',.0f')
    fig.update_layout(
        legend=dict(title=dict(text='Product Line', font=dict(color='#FFFFFF')),
                    font=dict(color='#FFFFFF', size=11))
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
