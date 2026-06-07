# ─────────────────────────────────────────
# config.py — Semua konstanta, warna, mapping
# ─────────────────────────────────────────

# ── Database ──
DB_CONFIG = {
    "host":     "localhost",
    "port":     "5432",
    "database": "DATABASE_UAS_SQL_WEB",
    "user":     "ericfariz7",
    "password": "12345678910",
}

# ── Chart Colors ──
CHART_COLORS = [
    '#1883FF', '#004EE0', '#00E676',
    '#FFD600', '#FF6D00', '#F50057',
    '#99CAFF', '#E3F2FF'
]

PRODUCT_COLOR_MAP = {
    'Electronic accessories': '#1883FF',
    'Fashion accessories':    '#004EE0',
    'Food and beverages':     '#00E676',
    'Health and beauty':      '#FFD600',
    'Home and lifestyle':     '#FF6D00',
    'Sports and travel':      '#F50057',
}

# ── Branch Labels ──
BRANCH_LABEL = {
    'A': 'A (Yangon)',
    'B': 'B (Mandalay)',
    'C': 'C (Naypyitaw)',
}

# ── City Coordinates (Myanmar) ──
CITY_COORDS = {
    'Yangon': {
        'lat': 16.8661, 'lon': 96.1951,
        'branch': 'A',
        'desc': 'Largest city & commercial hub',
        'color': '#1883FF',
    },
    'Mandalay': {
        'lat': 21.9588, 'lon': 96.0891,
        'branch': 'B',
        'desc': 'Second largest city',
        'color': '#00E676',
    },
    'Naypyitaw': {
        'lat': 19.7633, 'lon': 96.0785,
        'branch': 'C',
        'desc': 'Capital of Myanmar',
        'color': '#FFD600',
    },
}

# ── Default Product List (fallback) ──
DEFAULT_PRODUCTS = [
    'Health and beauty',
    'Electronic accessories',
    'Home and lifestyle',
    'Sports and travel',
    'Food and beverages',
    'Fashion accessories',
]
