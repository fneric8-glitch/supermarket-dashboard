# ─────────────────────────────────────────
# components/tab_map.py — Tab 3: Branch Map
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import CITY_COORDS, BRANCH_LABEL, PRODUCT_COLOR_MAP


def apply_theme(fig, h=340, legend=True):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E3F2FF', family='Inter', size=12),
        height=h, margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(bgcolor='rgba(13,63,163,0.7)', bordercolor='rgba(153,202,255,0.3)',
                    borderwidth=1, font=dict(color='#FFFFFF', size=11)) if legend else dict(visible=False),
        hoverlabel=dict(bgcolor='#0A2F85', bordercolor='#1883FF',
                        font=dict(color='white', size=12))
    )
    fig.update_xaxes(gridcolor='rgba(153,202,255,0.08)', color='#E3F2FF',
                     tickfont=dict(color='#FFFFFF', size=11))
    fig.update_yaxes(gridcolor='rgba(153,202,255,0.08)', color='#E3F2FF',
                     tickfont=dict(color='#FFFFFF', size=11))
    return fig


def render(df: pd.DataFrame):
    if df.empty:
        st.warning("Tidak ada data.")
        return

    st.markdown("<div class='section-hdr'>🗺️ Branch Location Map — Myanmar</div>",
                unsafe_allow_html=True)

    # ── Hitung stats per kota ──
    city_st = (df.groupby('city')
                 .agg(Revenue=('total','sum'), Transactions=('total','count'),
                      Avg_Order=('total','mean'), Total_Qty=('quantity','sum'))
                 .reset_index())

    map_rows = []
    for _, r in city_st.iterrows():
        if r['city'] in CITY_COORDS:
            map_rows.append({**r.to_dict(), **CITY_COORDS[r['city']]})
    map_df = pd.DataFrame(map_rows)

    if map_df.empty:
        st.warning("Data kota tidak ditemukan di CITY_COORDS.")
        return

    # ── City Info Cards ──
    cols = st.columns(len(map_df), gap="medium")
    for col, row in zip(cols, map_df.itertuples()):
        with col:
            st.markdown(f"""
            <div class='map-card' style='border-top:3px solid {row.color};'>
                <div class='map-branch'>🏪 Branch {row.branch} — {row.city}</div>
                <div class='map-rev' style='color:{row.color};'>${row.Revenue:,.0f}</div>
                <div class='map-meta'>
                    📍 {row.desc}<br>
                    🧾 {row.Transactions} transaksi &nbsp;|&nbsp; 📦 {int(row.Total_Qty)} qty<br>
                    💵 Avg: ${row.Avg_Order:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # ── Geo Map ──
    fig_map = go.Figure()
    for _, r in map_df.iterrows():
        sz = max(30, r['Revenue'] / 1200)
        fig_map.add_trace(go.Scattergeo(
            lat=[r['lat']], lon=[r['lon']],
            mode='markers+text',
            marker=dict(size=sz, color=r['color'], opacity=0.88,
                        line=dict(width=3, color='white'), symbol='circle'),
            text=f" {r['city']}",
            textposition='top right',
            textfont=dict(color='white', size=14, family='Inter'),
            name=f"Branch {r['branch']} — {r['city']}",
            hovertemplate=(
                f"<b>🏪 Branch {r['branch']} — {r['city']}</b><br>"
                f"📍 {r['desc']}<br>"
                f"💰 Revenue: <b>${r['Revenue']:,.0f}</b><br>"
                f"🧾 Transactions: {r['Transactions']}<br>"
                f"📦 Total Qty: {int(r['Total_Qty'])}<br>"
                f"💵 Avg Order: ${r['Avg_Order']:,.0f}"
                "<extra></extra>"
            )
        ))
    fig_map.update_layout(
        geo=dict(
            scope='asia', center=dict(lat=19.5, lon=96.1), projection_scale=14,
            showland=True, landcolor='rgba(10,47,133,0.7)',
            showocean=True, oceancolor='rgba(4,46,123,0.95)',
            showcoastlines=True, coastlinecolor='rgba(153,202,255,0.5)', coastlinewidth=1.5,
            showlakes=True, lakecolor='rgba(24,131,255,0.2)',
            showcountries=True, countrycolor='rgba(153,202,255,0.4)', countrywidth=1,
            bgcolor='rgba(4,46,123,1)', framecolor='rgba(153,202,255,0.3)', framewidth=1,
        ),
        paper_bgcolor='rgba(4,46,123,1)', plot_bgcolor='rgba(4,46,123,1)',
        height=520, font=dict(color='#E3F2FF', family='Inter'),
        legend=dict(bgcolor='rgba(13,63,163,0.85)', bordercolor='rgba(153,202,255,0.35)',
                    borderwidth=1, font=dict(color='#FFFFFF', size=12),
                    x=0.01, y=0.98, title=dict(text='Branches', font=dict(color='#99CAFF'))),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.markdown("<div class='chart-wrap' style='padding:12px;'>", unsafe_allow_html=True)
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Branch Performance ──
    st.markdown("<div class='section-hdr'>📊 Branch Performance Comparison</div>",
                unsafe_allow_html=True)
    p1, p2 = st.columns([4, 6], gap="medium")

    with p1:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>🕸️ Performance Radar</div>",
                    unsafe_allow_html=True)
        cats         = ['Revenue', 'Transactions', 'Avg Order', 'Total Qty']
        r_colors     = [r['color'] for _, r in map_df.iterrows()]
        r_fills      = [c.replace('#', 'rgba(') + ',0.15)' if False else
                        f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.15)"
                        for c in r_colors]

        fig_r = go.Figure()
        for i, row in enumerate(map_df.itertuples()):
            vals = [
                row.Revenue      / map_df['Revenue'].max()      * 100,
                row.Transactions / map_df['Transactions'].max() * 100,
                row.Avg_Order    / map_df['Avg_Order'].max()    * 100,
                row.Total_Qty    / map_df['Total_Qty'].max()    * 100,
            ]
            vc = vals + [vals[0]]
            tc = cats + [cats[0]]
            fig_r.add_trace(go.Scatterpolar(
                r=vc, theta=tc, fill='toself', fillcolor=r_fills[i],
                line=dict(color=r_colors[i], width=2.5),
                name=f"Branch {row.branch} ({row.city})", opacity=1.0,
                hovertemplate=f"<b>Branch {row.branch} ({row.city})</b><br>%{{theta}}: <b>%{{r:.1f}}</b><extra></extra>"
            ))
            fig_r.add_trace(go.Scatterpolar(
                r=vc, theta=tc, mode='markers',
                marker=dict(color=r_colors[i], size=8, line=dict(color='white', width=1.5)),
                showlegend=False, hoverinfo='skip'
            ))
        fig_r.update_layout(
            polar=dict(
                bgcolor='rgba(4,46,123,0.6)',
                radialaxis=dict(color='#FFFFFF', gridcolor='rgba(153,202,255,0.25)',
                                tickfont=dict(color='#FFFFFF', size=10),
                                range=[0, 110], tickvals=[0,25,50,75,100],
                                ticktext=['0','25','50','75','100'],
                                linecolor='rgba(153,202,255,0.3)'),
                angularaxis=dict(color='#FFFFFF', gridcolor='rgba(153,202,255,0.2)',
                                 tickfont=dict(color='#FFFFFF', size=13),
                                 linecolor='rgba(153,202,255,0.3)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#FFFFFF', family='Inter'), height=380,
            margin=dict(l=50, r=50, t=50, b=50),
            legend=dict(bgcolor='rgba(13,63,163,0.8)', bordercolor='rgba(153,202,255,0.35)',
                        borderwidth=1, font=dict(color='#FFFFFF', size=11),
                        x=0.5, y=-0.12, xanchor='center', orientation='h')
        )
        st.plotly_chart(fig_r, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with p2:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>📦 Product Mix per Branch</div>",
                    unsafe_allow_html=True)
        bp = df.groupby(['branch', 'product_line'])['total'].sum().reset_index()
        bp['branch_label'] = bp['branch'].map(BRANCH_LABEL).fillna(bp['branch'])
        fig_bp = px.bar(
            bp, x='branch_label', y='total', color='product_line', barmode='stack',
            color_discrete_map=PRODUCT_COLOR_MAP,
            labels={'total': 'Revenue ($)', 'branch_label': 'Branch', 'product_line': 'Product'},
            custom_data=['product_line', 'branch_label']
        )
        fig_bp.update_traces(
            hovertemplate='<b>Product:</b> %{customdata[0]}<br>'
                          '<b>Branch:</b> %{customdata[1]}<br>'
                          '<b>Revenue:</b> $%{y:,.0f}<extra></extra>',
            textfont=dict(color='white')
        )
        fig_bp = apply_theme(fig_bp, 380)
        fig_bp.update_yaxes(tickprefix='$', tickformat=',.0f', tickfont=dict(color='#FFFFFF'))
        fig_bp.update_xaxes(tickangle=0, tickfont=dict(color='#FFFFFF', size=11))
        fig_bp.update_layout(
            legend=dict(title=dict(text='Product', font=dict(color='#FFFFFF')),
                        font=dict(color='#FFFFFF', size=11),
                        bgcolor='rgba(13,63,163,0.7)',
                        bordercolor='rgba(153,202,255,0.3)', borderwidth=1)
        )
        st.plotly_chart(fig_bp, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
