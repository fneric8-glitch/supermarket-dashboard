# ─────────────────────────────────────────
# database.py — Koneksi DB & semua fungsi data
# ─────────────────────────────────────────

import streamlit as st
import pandas as pd
import psycopg2
import os
from config import DB_CONFIG


# ── Buat koneksi baru (tidak di-cache, agar selalu fresh) ──
def new_conn():
    """Buka koneksi PostgreSQL baru."""
    return psycopg2.connect(**DB_CONFIG)


@st.cache_resource
def get_conn():
    """Koneksi cached untuk cek availability."""
    try:
        return new_conn()
    except Exception:
        return None


# ── Load data utama (cached 30 detik) ──
@st.cache_data(ttl=30)
def load_data() -> pd.DataFrame:
    """
    Load semua data dari supermarket_sales.
    Fallback ke CSV jika DB tidak tersedia.
    """
    try:
        conn = new_conn()
        df = pd.read_sql("SELECT * FROM supermarket_sales", conn)
        conn.close()
    except Exception as e:
        st.warning(f"⚠️ DB tidak tersedia, fallback ke CSV: {e}")
        df = _load_csv()
    return _clean(df)


# ── Load data fresh untuk fitur Delete (cached 5 detik) ──
@st.cache_data(ttl=5)
def load_data_for_delete() -> pd.DataFrame:
    """
    Load data dengan ctid (PostgreSQL row pointer) untuk keperluan hapus 1 baris.
    TTL sangat pendek agar selalu sinkron setelah INSERT/DELETE.
    """
    try:
        conn = new_conn()
        df = pd.read_sql(
            "SELECT ctid::text AS row_id, * FROM supermarket_sales ORDER BY order_date DESC",
            conn
        )
        conn.close()
        return _clean(df)
    except Exception as e:
        st.error(f"❌ Gagal load data untuk delete: {e}")
        return pd.DataFrame()


# ── INSERT 1 transaksi baru ──
def insert_transaction(data: dict) -> bool:
    """
    Insert 1 baris transaksi baru ke DB.
    data: dict dengan key = nama kolom.
    Return True jika sukses.
    """
    sql = """
        INSERT INTO supermarket_sales
            (branch, city, customer_type, gender, product_line,
             unit_price, quantity, tax, total, order_date, payment_method)
        VALUES
            (%(branch)s, %(city)s, %(customer_type)s, %(gender)s, %(product_line)s,
             %(unit_price)s, %(quantity)s, %(tax)s, %(total)s, %(order_date)s, %(payment_method)s)
    """
    try:
        conn = new_conn()
        cur  = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"❌ INSERT gagal: {e}")
        return False


# ── DELETE 1 baris by ctid ──
def delete_by_ctid(ctid: str) -> int:
    """
    Hapus tepat 1 baris berdasarkan ctid PostgreSQL.
    Return jumlah baris yang dihapus (harusnya 1).
    """
    try:
        conn = new_conn()
        cur  = conn.cursor()
        cur.execute(
            "DELETE FROM supermarket_sales WHERE ctid = %s::tid",
            (ctid,)
        )
        deleted = cur.rowcount
        conn.commit()
        conn.close()
        return deleted
    except Exception as e:
        st.error(f"❌ DELETE gagal: {e}")
        return 0


# ── Invalidate semua cache data ──
def invalidate_cache():
    """Clear semua cache data agar re-fetch dari DB."""
    st.cache_data.clear()


# ── PRIVATE: Load dari CSV (fallback) ──
def _load_csv() -> pd.DataFrame:
    for path in ["DATABASE_SUPERMARKET.csv", "supermarket_sales.csv"]:
        if os.path.exists(path):
            raw = open(path, encoding='utf-8', errors='ignore').read(500)
            sep = ';' if raw.count(';') > raw.count(',') else ','
            return pd.read_csv(path, sep=sep)
    return pd.DataFrame()


# ── PRIVATE: Bersihkan & standarisasi kolom ──
def _clean(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df.columns = [c.lower().strip().replace(' ', '_') for c in df.columns]
    rename_map = {
        'date':           'order_date',
        'payment':        'payment_method',
        'customer_type_': 'customer_type',
    }
    df.rename(columns=rename_map, inplace=True)
    for col in ['total', 'quantity', 'unit_price', 'tax']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    if 'order_date' in df.columns:
        df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
        df['month_name'] = df['order_date'].dt.strftime('%b %Y')
        df['month_sort'] = df['order_date'].dt.to_period('M').astype(str)
    return df
