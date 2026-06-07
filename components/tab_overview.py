# ─────────────────────────────────────────
# components/tab_overview.py — Tab 1: Overview
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import PRODUCT_COLOR_MAP, BRANCH_LABEL


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


def render(df: pd.DataFrame, metrics: dict):
    if df.empty:
        st.warning("Tidak ada data.")
        return

    tot_trx = metrics['tot_trx']

    # ── Row 1: Revenue Trend + Branch ──
    r1, r2 = st.columns([6, 4], gap="medium")

    with r1:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>📈 Revenue Trend Bulanan</div>",
                    unsafe_allow_html=True)
        trend = (df.groupby('month_sort')
                   .agg(Revenue=('total', 'sum'), month_name=('month_name', 'first'))
                   .reset_index().sort_values('month_sort'))
        fig = go.Figure(go.Scatter(
            x=trend['month_name'], y=trend['Revenue'],
            mode='lines+markers',
            line=dict(color='#1883FF', width=3.5),
            marker=dict(size=10, color='#99CAFF', line=dict(width=2.5, color='#1883FF')),
            fill='tozeroy', fillcolor='rgba(24,131,255,0.12)',
            hovertemplate='<b>%{x}</b><br>Revenue: <b>$%{y:,.0f}</b><extra></extra>',
        ))
        fig = apply_theme(fig, 280, legend=False)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r2:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>🏢 Revenue per Branch</div>",
                    unsafe_allow_html=True)
        br = (df.groupby('branch')['total'].sum()
                .reset_index().sort_values('total', ascending=False))
        br['label'] = br['branch'].map(BRANCH_LABEL).fillna(br['branch'])
        fig = go.Figure(go.Bar(
            x=br['label'], y=br['total'],
            marker=dict(color=['#1883FF', '#004EE0', '#99CAFF'][:len(br)],
                        cornerradius=6, line=dict(color='rgba(255,255,255,0.1)', width=1)),
            text=[f'${v:,.0f}' for v in br['total']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=11),
            hovertemplate='<b>%{x}</b><br>Revenue: <b>$%{y:,.0f}</b><extra></extra>'
        ))
        fig = apply_theme(fig, 280, legend=False)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        fig.update_xaxes(tickangle=0, tickfont=dict(color='#FFFFFF', size=11))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 2: Product + Payment ──
    r3, r4 = st.columns([55, 45], gap="medium")

    with r3:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>📦 Revenue per Product Line</div>",
                    unsafe_allow_html=True)
        pr = (df.groupby('product_line')['total'].sum()
                .sort_values(ascending=True).reset_index())
        colors = [PRODUCT_COLOR_MAP.get(p, '#1883FF') for p in pr['product_line']]
        fig = go.Figure(go.Bar(
            x=pr['total'], y=pr['product_line'], orientation='h',
            marker=dict(color=colors, cornerradius=5,
                        line=dict(color='rgba(255,255,255,0.05)', width=0.5)),
            text=[f'${v:,.0f}' for v in pr['total']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=11.5),
            hovertemplate='<b>%{y}</b><br>Revenue: <b>$%{x:,.0f}</b><extra></extra>'
        ))
        fig = apply_theme(fig, 320, legend=False)
        fig.update_xaxes(tickprefix='$', tickformat=',.0f')
        fig.update_yaxes(tickfont=dict(color='#FFFFFF', size=11))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r4:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>💳 Payment Method Distribution</div>",
                    unsafe_allow_html=True)
        pay = df['payment_method'].value_counts().reset_index()
        pay.columns = ['method', 'count']
        fig = go.Figure(go.Pie(
            labels=pay['method'], values=pay['count'], hole=0.58,
            marker=dict(colors=['#1883FF', '#004EE0', '#99CAFF'],
                        line=dict(color='#042E7B', width=3)),
            textinfo='label+percent', textfont=dict(color='#FFFFFF', size=12),
            hovertemplate='<b>%{label}</b><br>%{value} trx (%{percent})<extra></extra>'
        ))
        fig.add_annotation(
            text=f"<b>{tot_trx:,}</b><br><span style='font-size:11'>Transaksi</span>",
            x=0.5, y=0.5, showarrow=False, font=dict(color='white', size=20)
        )
        fig = apply_theme(fig, 320)
        fig.update_layout(legend=dict(orientation='v', x=1.02, y=0.5,
                                      font=dict(color='#FFFFFF', size=11)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 3: City + Member vs Normal ──
    r5, r6 = st.columns(2, gap="medium")

    with r5:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>🏙️ Revenue per City</div>",
                    unsafe_allow_html=True)
        cy = (df.groupby('city')['total'].sum()
                .reset_index().sort_values('total', ascending=False))
        fig = go.Figure(go.Bar(
            x=cy['city'], y=cy['total'],
            marker=dict(color=['#1883FF', '#00E676', '#FFD600'],
                        cornerradius=6, line=dict(color='rgba(255,255,255,0.08)', width=0.5)),
            text=[f'${v:,.0f}' for v in cy['total']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=12),
            hovertemplate='<b>%{x}</b><br>Revenue: <b>$%{y:,.0f}</b><extra></extra>'
        ))
        fig = apply_theme(fig, 300, legend=False)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        fig.update_xaxes(tickangle=0, tickfont=dict(color='#FFFFFF', size=12))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with r6:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>👥 Member vs Normal Contribution</div>",
                    unsafe_allow_html=True)
        ct = (df.groupby('customer_type')
                .agg(Revenue=('total', 'sum'), Transactions=('total', 'count'))
                .reset_index())
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Revenue ($)', x=ct['customer_type'], y=ct['Revenue'],
            marker=dict(color=['#1883FF', '#FFD600'], cornerradius=5),
            yaxis='y', offsetgroup=1,
            text=[f'${v:,.0f}' for v in ct['Revenue']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=11),
            hovertemplate='<b>%{x}</b><br>Revenue: $%{y:,.0f}<extra></extra>'
        ))
        fig.add_trace(go.Bar(
            name='Transactions', x=ct['customer_type'], y=ct['Transactions'],
            marker=dict(color=['#99CAFF', '#FF6D00'], cornerradius=5),
            yaxis='y2', offsetgroup=2,
            hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
        ))
        fig.update_layout(
            yaxis=dict(title='Revenue ($)', title_font=dict(color='#FFFFFF'),
                       tickprefix='$', tickformat=',.0f', tickfont=dict(color='#FFFFFF')),
            yaxis2=dict(title='Transactions', overlaying='y', side='right',
                        title_font=dict(color='#FFFFFF'), tickfont=dict(color='#FFFFFF')),
            barmode='group'
        )
        fig = apply_theme(fig, 300)
        fig.update_xaxes(tickangle=0, tickfont=dict(color='#FFFFFF', size=12))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
