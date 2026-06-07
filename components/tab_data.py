# ─────────────────────────────────────────
# components/tab_data.py — Tab 4: Data Table + CRUD
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
from datetime import datetime
from database import (
    load_data_for_delete,
    insert_transaction,
    delete_by_ctid,
    invalidate_cache,
)
from config import DEFAULT_PRODUCTS


def render(df: pd.DataFrame, all_products: list, all_pays: list, all_cities: list):
    """Render Tab 4 dengan 3 sub-tab: View / Tambah / Hapus."""
    st.markdown("<div class='section-hdr'>📋 Transaction Data Table</div>",
                unsafe_allow_html=True)

    dt1, dt2, dt3 = st.tabs(["📋 View Data", "➕ Tambah Data", "🗑️ Hapus Data"])

    with dt1:
        _render_view(df, all_products, all_pays, all_cities)

    with dt2:
        _render_add(all_products, all_cities)

    with dt3:
        _render_delete()


# ─────────────────────────────────────────
# VIEW DATA
# ─────────────────────────────────────────
def _render_view(df, all_products, all_pays, all_cities):
    fa, fb, fc = st.columns(3, gap="small")
    with fa:
        f_city = st.multiselect("🏙️ City", all_cities, default=all_cities, key='tc')
    with fb:
        f_prod = st.multiselect("📦 Product", all_products, default=all_products, key='tp')
    with fc:
        f_pay  = st.multiselect("💳 Payment", all_pays, default=all_pays, key='tpa')

    df_show = df[
        df['city'].isin(f_city) &
        df['product_line'].isin(f_prod) &
        df['payment_method'].isin(f_pay)
    ].copy()

    cols = [c for c in ['branch','city','customer_type','gender','product_line',
                         'unit_price','quantity','total','payment_method','order_date']
            if c in df_show.columns]
    df_disp = df_show[cols].copy()
    if 'total'      in df_disp.columns: df_disp['total']      = df_disp['total'].apply(lambda x: f'${x:,.2f}')
    if 'unit_price' in df_disp.columns: df_disp['unit_price'] = df_disp['unit_price'].apply(lambda x: f'${x:,.2f}')

    st.markdown(f"""
    <div style='color:#99CAFF; font-size:13px; font-weight:600; margin:8px 0;'>
        Menampilkan <span style='color:white;'>{len(df_disp):,}</span> transaksi
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df_disp, use_container_width=True, height=420,
                 column_config={
                     'branch':         st.column_config.TextColumn('Branch',       width='small'),
                     'city':           st.column_config.TextColumn('City'),
                     'customer_type':  st.column_config.TextColumn('Customer Type'),
                     'gender':         st.column_config.TextColumn('Gender',       width='small'),
                     'product_line':   st.column_config.TextColumn('Product Line'),
                     'unit_price':     st.column_config.TextColumn('Unit Price'),
                     'quantity':       st.column_config.NumberColumn('Qty',        width='small'),
                     'total':          st.column_config.TextColumn('Total Revenue'),
                     'payment_method': st.column_config.TextColumn('Payment'),
                     'order_date':     st.column_config.DateColumn('Date'),
                 })
    csv_dl = df_show.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv_dl, "ocean_data.csv", "text/csv")


# ─────────────────────────────────────────
# TAMBAH DATA
# ─────────────────────────────────────────
def _render_add(all_products, all_cities):
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0A2F85,#0D3FA3);
                border:1px solid rgba(24,131,255,0.3); border-radius:12px;
                padding:20px; margin-bottom:16px;'>
        <div style='color:#99CAFF; font-size:13px; font-weight:700;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;'>
            ➕ Tambah Transaksi Baru
        </div>
        <div style='color:#C8DEFF; font-size:12px;'>
            Isi semua field di bawah untuk menambah data ke database
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("add_form", clear_on_submit=True):
        n1, n2, n3 = st.columns(3)
        with n1:
            n_branch   = st.selectbox("🏢 Branch",        ['A', 'B', 'C'])
            n_city     = st.selectbox("🏙️ City",          ['Yangon', 'Mandalay', 'Naypyitaw'])
            n_custtype = st.selectbox("👤 Customer Type", ['Member', 'Normal'])
        with n2:
            n_gender   = st.selectbox("⚧ Gender",         ['Male', 'Female'])
            n_product  = st.selectbox("📦 Product Line",  all_products or DEFAULT_PRODUCTS)
            n_payment  = st.selectbox("💳 Payment",       ['Ewallet', 'Cash', 'Credit card'])
        with n3:
            n_uprice   = st.number_input("💲 Unit Price",  min_value=0.0, step=0.5, format="%.2f")
            n_qty      = st.number_input("📦 Quantity",    min_value=1, max_value=20, step=1)
            n_date     = st.date_input("📅 Order Date",   value=datetime.today())

        n_tax   = n_uprice * n_qty * 0.05
        n_total = n_uprice * n_qty + n_tax

        st.markdown(f"""
        <div style='background:rgba(24,131,255,0.1); border:1px solid rgba(24,131,255,0.3);
                    border-radius:8px; padding:12px; margin:8px 0;'>
            <span style='color:#99CAFF; font-size:13px;'>
                💰 Tax: <b style='color:white;'>${n_tax:,.2f}</b> &nbsp;|&nbsp;
                💵 Total: <b style='color:#00E676; font-size:15px;'>${n_total:,.2f}</b>
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.form_submit_button("✅ Simpan Data", use_container_width=True):
            ok = insert_transaction({
                'branch':        n_branch,
                'city':          n_city,
                'customer_type': n_custtype,
                'gender':        n_gender,
                'product_line':  n_product,
                'unit_price':    n_uprice,
                'quantity':      n_qty,
                'tax':           n_tax,
                'total':         n_total,
                'order_date':    n_date.strftime('%m/%d/%Y'),
                'payment_method': n_payment,
            })
            if ok:
                st.success(f"✅ Data berhasil ditambahkan! Total: ${n_total:,.2f}")
                invalidate_cache()
                st.rerun()


# ─────────────────────────────────────────
# HAPUS DATA — 1 BARIS via ctid
# ─────────────────────────────────────────
def _render_delete():
    st.markdown("""
    <div style='background:linear-gradient(135deg,#3D0A0A,#5C0A0A);
                border:1px solid rgba(255,23,68,0.3); border-radius:12px;
                padding:16px; margin-bottom:20px;'>
        <div style='color:#FF8A80; font-size:13px; font-weight:700;
                    text-transform:uppercase; letter-spacing:1px;'>
            🗑️ Hapus Data Transaksi
        </div>
        <div style='color:#FFCDD2; font-size:12px; margin-top:4px;'>
            Cari & pilih <b>1 baris</b> yang ingin dihapus.
            Data yang dihapus <b>tidak dapat dikembalikan</b>.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Load fresh (TTL=5 detik, koneksi baru) ──
    df_fresh = load_data_for_delete()
    if df_fresh.empty:
        st.warning("Tidak ada data di database.")
        return

    # ── Filter Panel ──
    st.markdown("""
    <div style='color:#99CAFF; font-size:12px; font-weight:700;
                text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>
        🔍 Filter & Cari Data
    </div>
    """, unsafe_allow_html=True)

    sf1, sf2, sf3, sf4 = st.columns(4)
    with sf1:
        s_city   = st.selectbox("🏙️ City",    ['Semua'] + sorted(df_fresh['city'].dropna().unique()),         key='del_city')
    with sf2:
        s_branch = st.selectbox("🏢 Branch",  ['Semua'] + sorted(df_fresh['branch'].dropna().unique()),       key='del_branch')
    with sf3:
        s_prod   = st.selectbox("📦 Product", ['Semua'] + sorted(df_fresh['product_line'].dropna().unique()), key='del_prod')
    with sf4:
        s_pay    = st.selectbox("💳 Payment", ['Semua'] + sorted(df_fresh['payment_method'].dropna().unique()),key='del_pay')

    sf5, sf6 = st.columns(2)
    with sf5:
        s_cust   = st.selectbox("👤 Cust Type",['Semua'] + sorted(df_fresh['customer_type'].dropna().unique()),key='del_cust')
    with sf6:
        s_gender = st.selectbox("⚧ Gender",   ['Semua'] + sorted(df_fresh['gender'].dropna().unique()),       key='del_gender')

    s_search = st.text_input(
        "🔎 Pencarian Bebas",
        placeholder="Contoh: Food, Yangon, Ewallet, Member...",
        key='del_search'
    )

    # ── Apply Filter ──
    dff = df_fresh.copy()
    if s_city   != 'Semua': dff = dff[dff['city']           == s_city]
    if s_branch != 'Semua': dff = dff[dff['branch']         == s_branch]
    if s_prod   != 'Semua': dff = dff[dff['product_line']   == s_prod]
    if s_pay    != 'Semua': dff = dff[dff['payment_method'] == s_pay]
    if s_cust   != 'Semua': dff = dff[dff['customer_type']  == s_cust]
    if s_gender != 'Semua': dff = dff[dff['gender']         == s_gender]

    if s_search.strip():
        mask = pd.Series(False, index=dff.index)
        for col in ['city','branch','product_line','payment_method','customer_type','gender']:
            if col in dff.columns:
                mask |= dff[col].astype(str).str.contains(s_search.strip(), case=False, na=False)
        dff = dff[mask]

    # ── Counter ──
    st.markdown(f"""
    <div style='background:rgba(24,131,255,0.1); border:1px solid rgba(24,131,255,0.25);
                border-radius:8px; padding:10px 14px; margin:10px 0;
                color:#C8DEFF; font-size:13px;'>
        📊 Ditemukan <b style='color:white; font-size:15px;'>{len(dff):,}</b> baris
        dari total <b style='color:white;'>{len(df_fresh):,}</b> data.
        Pilih <b style='color:#FFD600;'>1 baris</b> untuk dihapus.
    </div>
    """, unsafe_allow_html=True)

    if len(dff) == 0:
        st.info("😕 Tidak ada data yang cocok. Coba ubah filter.")
        return

    # ── Tabel Preview ──
    show_limit = min(100, len(dff))
    dff_reset  = dff.reset_index(drop=True)

    disp_cols = [c for c in ['branch','city','customer_type','gender','product_line',
                               'unit_price','quantity','total','payment_method','order_date']
                 if c in dff_reset.columns]
    df_show = dff_reset[disp_cols].copy()
    if 'total'      in df_show.columns: df_show['total']      = df_show['total'].apply(lambda x: f'${x:,.2f}' if pd.notna(x) else '-')
    if 'unit_price' in df_show.columns: df_show['unit_price'] = df_show['unit_price'].apply(lambda x: f'${x:,.2f}' if pd.notna(x) else '-')
    df_show.index = df_show.index + 1  # mulai dari 1

    st.markdown("<div style='color:#99CAFF; font-size:12px; margin-bottom:6px;'>👆 Lihat tabel, lalu pilih baris di selector di bawah:</div>",
                unsafe_allow_html=True)
    st.dataframe(df_show.head(show_limit), use_container_width=True,
                 height=min(400, 50 + show_limit * 35),
                 column_config={
                     'branch':         st.column_config.TextColumn('Branch',       width='small'),
                     'city':           st.column_config.TextColumn('City'),
                     'customer_type':  st.column_config.TextColumn('Cust. Type'),
                     'gender':         st.column_config.TextColumn('Gender',       width='small'),
                     'product_line':   st.column_config.TextColumn('Product Line', width='large'),
                     'unit_price':     st.column_config.TextColumn('Unit Price'),
                     'quantity':       st.column_config.NumberColumn('Qty',        width='small'),
                     'total':          st.column_config.TextColumn('Total'),
                     'payment_method': st.column_config.TextColumn('Payment'),
                     'order_date':     st.column_config.DateColumn('Date'),
                 })

    if len(dff) > 100:
        st.caption(f"⚠️ Menampilkan 100 dari {len(dff)} hasil. Persempit filter.")

    # ── Selector ──
    st.markdown("""
    <div style='background:rgba(255,23,68,0.08); border:1px solid rgba(255,23,68,0.25);
                border-radius:10px; padding:16px; margin-top:14px;'>
        <div style='color:#FF8A80; font-size:12px; font-weight:700;
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>
            🎯 Pilih Baris yang Akan Dihapus
        </div>
    """, unsafe_allow_html=True)

    option_labels = []
    for i, row in dff_reset.head(show_limit).iterrows():
        date_str  = str(row.get('order_date',''))[:10]
        total_str = f"${row['total']:,.2f}" if pd.notna(row.get('total')) else 'N/A'
        option_labels.append(
            f"#{i+1} | {row.get('branch','?')} — {row.get('city','?')} | "
            f"{row.get('product_line','?')} | {total_str} | {date_str} | "
            f"{row.get('payment_method','?')}"
        )

    sel_label = st.selectbox(
        "Pilih baris (#No | Branch — City | Product | Total | Date | Payment):",
        options=option_labels, key='del_row_select'
    )
    sel_idx   = option_labels.index(sel_label)
    sel_row   = dff_reset.iloc[sel_idx]
    sel_ctid  = sel_row.get('row_id', None)

    # ── Preview Baris ──
    total_val = sel_row.get('total', 0)
    total_val = float(total_val) if pd.notna(total_val) else 0.0

    st.markdown(f"""
    <div style='background:rgba(255,23,68,0.12); border:1px solid rgba(255,23,68,0.4);
                border-radius:8px; padding:14px; margin:12px 0;'>
        <div style='color:#FF8A80; font-size:12px; font-weight:700; margin-bottom:8px;'>
            ⚠️ PREVIEW — Baris yang akan dihapus:
        </div>
        <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px;'>
            <div style='color:#FFCDD2; font-size:12px;'>🏢 Branch: <b style='color:white;'>{sel_row.get('branch','?')}</b></div>
            <div style='color:#FFCDD2; font-size:12px;'>🏙️ City: <b style='color:white;'>{sel_row.get('city','?')}</b></div>
            <div style='color:#FFCDD2; font-size:12px;'>👤 Type: <b style='color:white;'>{sel_row.get('customer_type','?')}</b></div>
            <div style='color:#FFCDD2; font-size:12px;'>📦 Product: <b style='color:white;'>{sel_row.get('product_line','?')}</b></div>
            <div style='color:#FFCDD2; font-size:12px;'>💰 Total: <b style='color:#FF6D00; font-size:14px;'>${total_val:,.2f}</b></div>
            <div style='color:#FFCDD2; font-size:12px;'>💳 Payment: <b style='color:white;'>{sel_row.get('payment_method','?')}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Konfirmasi + Tombol ──
    cc, bc = st.columns([3, 1])
    with cc:
        confirm = st.checkbox(
            "✅ Saya yakin ingin menghapus 1 baris data ini (tidak dapat dikembalikan)",
            key='del_confirm'
        )
    with bc:
        hapus = st.button("🗑️ HAPUS 1 BARIS", type="primary",
                          disabled=not confirm, use_container_width=True)

    if hapus and confirm:
        if not sel_ctid:
            st.error("❌ row_id (ctid) tidak ditemukan.")
            return
        deleted = delete_by_ctid(sel_ctid)
        if deleted == 1:
            st.success(f"""✅ **1 baris berhasil dihapus!**
- Branch: {sel_row.get('branch','?')} — {sel_row.get('city','?')}
- Product: {sel_row.get('product_line','?')}
- Total: ${total_val:,.2f}""")
            invalidate_cache()
            st.rerun()
        else:
            st.error("❌ Gagal hapus. Data mungkin sudah berubah, coba refresh.")
