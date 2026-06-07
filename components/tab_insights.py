# ─────────────────────────────────────────
# components/tab_insights.py — Tab 5: Insights & Recommendations
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def apply_theme(fig, h=260, legend=True):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E3F2FF', family='Inter', size=12),
        height=h, margin=dict(l=12, r=12, t=36, b=12),
        legend=dict(bgcolor='rgba(13,63,163,0.7)', bordercolor='rgba(153,202,255,0.3)',
                    borderwidth=1, font=dict(color='#FFFFFF', size=11)) if legend else dict(visible=False),
        hoverlabel=dict(bgcolor='#0A2F85', bordercolor='#1883FF', font=dict(color='white', size=12))
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

    st.markdown("<div class='section-hdr'>💡 Insights & Recommendations</div>",
                unsafe_allow_html=True)

    # ── Hitung metrik ──
    best_prod  = df.groupby('product_line')['total'].sum().idxmax()
    best_rev   = df.groupby('product_line')['total'].sum().max()
    worst_prod = df.groupby('product_line')['total'].sum().idxmin()
    best_city  = df.groupby('city')['total'].sum().idxmax()
    best_pay   = df['payment_method'].value_counts().idxmax()
    mem_rev    = df[df['customer_type'] == 'Member']['total'].sum()
    norm_rev   = df[df['customer_type'] == 'Normal']['total'].sum()
    mem_pct    = mem_rev / (mem_rev + norm_rev) * 100 if (mem_rev + norm_rev) > 0 else 0

    i1, i2 = st.columns(2, gap="medium")

    # ── Insights ──
    with i1:
        insights = [
            ("🏆 Top Product Line",
             f"<b>{best_prod}</b> adalah product line terlaris dengan revenue <b>${best_rev:,.0f}</b>. Pertahankan stok dan promo untuk kategori ini."),
            ("🏙️ Branch Terbaik",
             f"<b>{best_city}</b> menghasilkan revenue tertinggi. Strategi marketing di kota ini sangat efektif dan bisa dijadikan benchmark."),
            ("💳 Metode Pembayaran",
             f"<b>{best_pay}</b> adalah metode pembayaran paling populer. Pastikan sistem payment ini selalu tersedia dan smooth."),
            ("👥 Customer Segmentation",
             f"Member berkontribusi <b>{mem_pct:.1f}%</b> dari total revenue. "
             + ("Program loyalty sudah sangat efektif! 🎉" if mem_pct > 50 else "Perlu tingkatkan konversi Normal → Member.")),
            ("⚠️ Perlu Perhatian",
             f"<b>{worst_prod}</b> memiliki revenue terendah. Pertimbangkan bundle promo atau evaluasi pricing strategy."),
        ]
        for title, text in insights:
            st.markdown(f"""
            <div class='ins-card'>
                <div class='ins-title'>{title}</div>
                <div class='ins-text'>{text}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Recommendations ──
    with i2:
        recs = [
            ("🚀 Ekspansi Member Program",
             "Tingkatkan insentif membership — diskon eksklusif, poin reward, early access produk baru. Target 60%+ Member dalam 6 bulan."),
            ("📱 Digital Payment Push",
             f"Karena {best_pay} dominan, pertimbangkan cashback eksklusif dan edukasi penggunaan e-payment ke customer lama."),
            ("🕐 Waktu Promosi Optimal",
             "Ada pola seasonal di data. Optimalkan flash sale di periode peak demand untuk maksimalkan revenue per transaksi."),
            ("🏪 Cross-Branch Strategy",
             "Bagikan best practice dari branch terbaik ke branch lain. Standarisasi SOP yang terbukti meningkatkan konversi."),
            ("📦 Product Mix Optimization",
             f"Fokus inventory pada {best_prod} dan bundle dengan {worst_prod} untuk mendongkrak penjualan keduanya."),
            ("🌐 Online Integration",
             "Pertimbangkan click & collect atau delivery untuk perluas jangkauan di luar 3 kota existing."),
        ]
        for title, text in recs:
            st.markdown(f"""
            <div class='rec-card'>
                <div class='rec-title'>{title}</div>
                <div class='rec-text'>{text}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Summary Charts ──
    st.markdown("<div class='section-hdr' style='margin-top:24px;'>📊 Summary Charts</div>",
                unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3, gap="medium")

    with s1:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>📈 Monthly Revenue</div>",
                    unsafe_allow_html=True)
        tr = (df.groupby('month_sort')
                .agg(Revenue=('total','sum'), mn=('month_name','first'))
                .reset_index().sort_values('month_sort'))
        fig = go.Figure(go.Scatter(
            x=tr['mn'], y=tr['Revenue'], mode='lines+markers',
            line=dict(color='#1883FF', width=3),
            marker=dict(size=8, color='#99CAFF', line=dict(width=2, color='#1883FF')),
            fill='tozeroy', fillcolor='rgba(24,131,255,0.12)',
            hovertemplate='%{x}: <b>$%{y:,.0f}</b><extra></extra>'
        ))
        fig = apply_theme(fig, legend=False)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with s2:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>👥 Customer Type</div>",
                    unsafe_allow_html=True)
        cp = df['customer_type'].value_counts().reset_index()
        cp.columns = ['type', 'count']
        fig = go.Figure(go.Pie(
            labels=cp['type'], values=cp['count'], hole=0.55,
            marker=dict(colors=['#1883FF','#FFD600'], line=dict(color='#042E7B', width=3)),
            textinfo='label+percent', textfont=dict(color='#FFFFFF', size=12),
        ))
        fig = apply_theme(fig)
        fig.update_layout(legend=dict(font=dict(color='#FFFFFF', size=11)))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with s3:
        st.markdown("<div class='chart-wrap'><div class='chart-title'>⚧ Revenue by Gender</div>",
                    unsafe_allow_html=True)
        gr = df.groupby('gender')['total'].sum().reset_index()
        fig = go.Figure(go.Bar(
            x=gr['gender'], y=gr['total'],
            marker=dict(color=['#F50057','#1883FF'], cornerradius=6),
            text=[f'${v:,.0f}' for v in gr['total']],
            textposition='outside', textfont=dict(color='#FFFFFF', size=12),
            hovertemplate='%{x}: <b>$%{y:,.0f}</b><extra></extra>'
        ))
        fig = apply_theme(fig, legend=False)
        fig.update_yaxes(tickprefix='$', tickformat=',.0f')
        fig.update_xaxes(tickangle=0, tickfont=dict(color='#FFFFFF', size=12))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
