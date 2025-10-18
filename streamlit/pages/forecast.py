import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
import calendar
import os

# === KONFIGURASI STREAMLIT ===
st.set_page_config(
    layout="wide",
    page_title="SAILOR - Peta Potensi Ikan",
    page_icon="🌊",
    initial_sidebar_state="auto"
)

# Inject favicon from local sailor.png so browser tab shows the icon on this page
try:
    _fav = os.path.join(os.path.dirname(__file__), '..', 'img', 'sailor.png')
    with open(_fav, 'rb') as _f:
        _fb = __import__('base64').b64encode(_f.read()).decode()
    st.markdown(f'<link rel="icon" href="data:image/png;base64,{_fb}" type="image/png"/>', unsafe_allow_html=True)
except Exception:
    pass

# === CUSTOM CSS - RESPONSIVE & INTER FONT ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    .main .block-container {
        max-width: 100%;
        padding-bottom: 2rem;
    }
    
    /* Responsive Typography */
    h1 {
        font-size: clamp(1.5rem, 4vw, 2.5rem) !important;
        font-weight: 700 !important;
        font-family: 'Inter', sans-serif !important;
        line-height: 1.2 !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: clamp(1.2rem, 3vw, 1.8rem) !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    h3 {
        font-size: clamp(1rem, 2.5vw, 1.3rem) !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }
    
    .week-selector {
        background-color: #f0f8ff;
        padding: clamp(0.75rem, 2vw, 1rem);
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 4px solid #0e4194;
    }
    
    .section-header {
        font-size: clamp(1.2rem, 3vw, 1.8rem) !important;
        font-weight: 600 !important;
        color: #24292e;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0e4194;
        font-family: 'Inter', sans-serif !important;
    }
    
    .info-box {
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: clamp(0.75rem, 2vw, 1.5rem);
        margin: 1rem 0;
        border-radius: 4px;
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
    }
    
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: clamp(0.5rem, 2vw, 0.75rem) clamp(1rem, 3vw, 2rem);
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.2s ease;
        width: 100%;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        background-color: #0a3275;
        box-shadow: 0 4px 8px rgba(14, 65, 148, 0.2);
    }
    
    /* Responsive Columns */
    [data-testid="column"] {
        padding: 0.25rem !important;
    }
    
    /* Responsive Select/Input */
    .stSelectbox, .stNumberInput {
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }
    
    .stSelectbox > div > div {
        font-size: clamp(0.875rem, 2vw, 1rem) !important;
    }
    
    /* Responsive Metrics */
    [data-testid="stMetricValue"] {
        font-size: clamp(1rem, 3vw, 1.5rem) !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: clamp(0.75rem, 2vw, 0.875rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Responsive Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
        overflow-x: auto;
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: clamp(0.75rem, 2vw, 0.95rem) !important;
        padding: clamp(0.5rem, 2vw, 0.75rem) clamp(0.5rem, 2vw, 1rem) !important;
        white-space: nowrap;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Responsive Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        padding: 1rem 0.5rem;
    }
    
    .css-1d391kg .stNumberInput label,
    .css-1d391kg .stSelectbox label,
    [data-testid="stSidebar"] label {
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Responsive Checkbox */
    .stCheckbox {
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
    }
    
    .stCheckbox label {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Responsive Info/Warning/Success boxes */
    .stAlert {
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
        padding: clamp(0.5rem, 2vw, 1rem) !important;
    }
    
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        [data-testid="column"] {
            min-width: 100% !important;
            margin-bottom: 0.5rem;
        }
        
        .stButton > button {
            font-size: 0.875rem !important;
            padding: 0.6rem 1rem;
        }
        
        .week-selector {
            padding: 0.75rem;
        }
        
        /* Stack columns on mobile */
        .row-widget.stHorizontal {
            flex-direction: column;
        }
    }
    
    /* Extra Small Devices */
    @media (max-width: 480px) {
        h1 {
            font-size: 1.3rem !important;
        }
        
        .section-header {
            font-size: 1.1rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
    }
    
    /* Option Menu Responsive */
    .nav-link {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Prediksi 30 Hari'
st.session_state.current_page = 'Prediksi 30 Hari'

# === NAVIGATION MENU (UNIFIED) ===
nav_options = ["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang", "Feedback"]
current = st.session_state.get('current_page', 'Prediksi 30 Hari')
default_index = nav_options.index(current) if current in nav_options else nav_options.index('Prediksi 30 Hari')
selected = option_menu(
    menu_title=None,
    options=nav_options,
    icons=["house", "map", "graph-up", "book", "info-circle", "chat-dots"],
    menu_icon="cast",
    default_index=default_index,
    orientation="horizontal",
    key="main_nav",
    styles={
        "container": {"padding": "0", "background-color": "#ffffff", "border-bottom": "1px solid #e1e4e8"},
        "icon": {"color": "#586069", "font-size": "clamp(14px, 3vw, 16px)"},
        "nav-link": {"font-size": "clamp(0.75rem, 2vw, 0.95rem)", "text-align": "center", "margin": "0", "padding": "clamp(10px, 2vw, 14px) clamp(12px, 3vw, 24px)", "color": "#24292e", "font-weight": "500", "border-bottom": "3px solid transparent", "--hover-color": "#f6f8fa", "font-family": "Inter, sans-serif"},
        "nav-link-selected": {"background-color": "transparent", "border-bottom": "3px solid #0e4194", "color": "#0e4194"},
    }
)

# Only switch if different
if selected != st.session_state.get('current_page', 'Prediksi 30 Hari'):
    st.session_state.current_page = selected
    if selected == "Beranda":
        st.switch_page("home.py")
    elif selected == "Deteksi Zona Ikan":
        st.switch_page("pages/hasil_deteksi.py")
    elif selected == "Prediksi 30 Hari":
        pass
    elif selected == "Tutorial":
        st.switch_page("pages/tutorial.py")
    elif selected == "Tentang":
        st.switch_page("home.py")
    elif selected == "Feedback":
        st.switch_page("pages/feedback.py")

# sync
st.session_state.current_page = selected

# === JUDUL HALAMAN ===
st.title("🌊 Peta Potensi Ikan & Zona Bahaya")

# === PILIH BULAN DAN MINGGU ===
current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year

st.markdown('<div class="week-selector">', unsafe_allow_html=True)
col_month, col_week = st.columns([1, 1])

with col_month:
    selected_month = st.selectbox(
        "📅 Pilih Bulan",
        options=list(range(1, 13)),
        format_func=lambda x: calendar.month_name[x],
        index=current_month-1,
        help="Pilih bulan untuk melihat prediksi mingguan"
    )

with col_week:
    selected_week = st.selectbox(
        "📊 Pilih Minggu",
        options=[1, 2, 3, 4],
        format_func=lambda x: f"Minggu ke-{x}",
        help="Pilih minggu dalam bulan yang dipilih"
    )

st.markdown('</div>', unsafe_allow_html=True)

# === MAPPING CSV FILES (RELATIVE PATH) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Naik 1 level dari pages/ ke streamlit/
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# CSV ada di dalam streamlit/csv
csv_files = {
    1: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_1.csv"),
    2: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_2.csv"), 
    3: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_3.csv"),
    4: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_4.csv")
}

# Informasi periode
week_dates = []
for week in range(1, 5):
    start_date = datetime(current_year, selected_month, (week-1)*7 + 1)
    end_date = min(start_date + timedelta(days=6), 
                   datetime(current_year, selected_month, 
                           calendar.monthrange(current_year, selected_month)[1]))
    week_dates.append(f"{start_date.strftime('%d')}-{end_date.strftime('%d')} {calendar.month_name[selected_month]}")

st.info(f"📈 **Prediksi:** {week_dates[selected_week-1]} | **Dataset:** variant_{selected_week}.csv")

# === LOAD DATA ===
try:
    csv_path = csv_files[selected_week]
    df = pd.read_csv(csv_path)
    st.success(f"✅ Data berhasil dimuat")
except FileNotFoundError:
    st.error(f"❌ File tidak ditemukan: {csv_path}")
    st.info(f"💡 Pastikan file CSV ada di folder `csv/`")
    st.stop()
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.stop()

# Validasi kolom
required_cols = {"lat", "lon", "skor", "ikan"}
if not required_cols.issubset(df.columns):
    st.error(f"CSV harus mengandung kolom: {required_cols}")
    st.stop()

# Fungsi alasan potensi
def alasan_potensi(row):
    if "Zona Bahaya" in row['ikan']:
        return "Zona berbahaya karena kondisi cuaca/gelombang."
    elif row['skor'] > 0.9:
        return "Sangat potensial: kondisi lingkungan optimal."
    elif row['skor'] > 0.75:
        return "Potensial tinggi: parameter mendukung."
    elif row['skor'] > 0.5:
        return "Potensial sedang."
    else:
        return "Potensial rendah."

df['alasan'] = df.apply(alasan_potensi, axis=1)
df_filtered = df[df['skor'] > 0.4].copy()

# --- Pilih Titik Deteksi dari daftar (fallback jika klik marker tidak aktif) ---
try:
    detect_options = df_filtered[~df_filtered['ikan'].str.contains('Zona Bahaya', case=False, na=False)][['ikan','lat','lon','skor']].copy()
    detect_options['label'] = detect_options.apply(lambda r: f"{r['ikan']} — {r['lat']:.4f}, {r['lon']:.4f} — skor {r['skor']:.4f}", axis=1)
    detect_map = dict(zip(detect_options['label'].tolist(), detect_options[['lat','lon']].values.tolist()))
    sel_label = st.sidebar.selectbox('Pilih Titik Deteksi (daftar)', options=['-- Tidak memilih --'] + detect_options['label'].tolist())
    if sel_label and sel_label != '-- Tidak memilih --':
        if st.sidebar.button('➡️ Pilih Titik Ini dari Daftar'):
            lat, lon = detect_map[sel_label]
            st.session_state['pending_target'] = (float(lat), float(lon))
            route_key = f"show_route_{selected_week}"
            st.session_state[route_key] = True
            st.sidebar.success('➡️ Tujuan otomatis diisi dari daftar')
            st.experimental_rerun()
except Exception:
    pass

# === SIDEBAR CONTROLS ===
st.sidebar.header("🔍 Navigasi")

basemap_option = st.sidebar.selectbox(
    "Basemap",
    ["OpenStreetMap", "Esri Satellite"],
    help="Pilih jenis peta dasar"
)

# GPS Detection
loc = get_geolocation()
if loc is not None and "coords" in loc:
    default_start_lat = loc["coords"]["latitude"]
    default_start_lon = loc["coords"]["longitude"]
    st.sidebar.success("📍 GPS terdeteksi!")
    # Populate session start coords from GPS if not set
    if st.session_state.get('start_lat') is None:
        st.session_state['start_lat'] = default_start_lat
    if st.session_state.get('start_lon') is None:
        st.session_state['start_lon'] = default_start_lon
else:
    default_start_lat = df_filtered.lat.mean()
    default_start_lon = df_filtered.lon.mean()
    st.sidebar.warning("⚠️ GPS tidak terdeteksi")

# Input koordinat
st.sidebar.subheader("📍 Posisi Awal")
# Defensive defaults for coordinates in session_state
if 'start_lat' not in st.session_state:
    st.session_state['start_lat'] = None
if 'start_lon' not in st.session_state:
    st.session_state['start_lon'] = None
if 'end_lat' not in st.session_state:
    st.session_state['end_lat'] = None
if 'end_lon' not in st.session_state:
    st.session_state['end_lon'] = None

# Helper to coerce floats safely
def _safe_float_forecast(v, fallback):
    # Try to coerce v first, then fallback. If both fail or are None, return 0.0
    for candidate in (v, fallback):
        try:
            if candidate is None:
                continue
            return float(candidate)
        except Exception:
            continue
    return 0.0

# Compute safe start coords to avoid passing None to float()
_start_val = st.session_state.get('start_lat')
if _start_val is None:
    _start_val = default_start_lat
_start_val = _safe_float_forecast(_start_val, default_start_lat)
_lon_val = st.session_state.get('start_lon')
if _lon_val is None:
    _lon_val = default_start_lon
_lon_val = _safe_float_forecast(_lon_val, default_start_lon)

start_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(_start_val), 
    format="%.6f",
    key="start_lat"
)
start_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(_lon_val), 
    format="%.6f",
    key="start_lon"
)

# Option: auto-fill tujuan fields when user clicks a point on the map
auto_fill_on_click = st.sidebar.checkbox("Auto-fill Tujuan saat klik peta", value=True, key="auto_fill_on_click")

st.sidebar.subheader("🎯 Tujuan")
# Compute safe end coords
_end_val = st.session_state.get('end_lat')
if _end_val is None:
    _end_val = float(df_filtered.lat.mean())
_end_val = _safe_float_forecast(_end_val, float(df_filtered.lat.mean()))
_end_lon_val = st.session_state.get('end_lon')
if _end_lon_val is None:
    _end_lon_val = float(df_filtered.lon.mean())
_end_lon_val = _safe_float_forecast(_end_lon_val, float(df_filtered.lon.mean()))

end_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(_end_val), 
    format="%.6f",
    key="end_lat"
)
end_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(_end_lon_val), 
    format="%.6f",
    key="end_lon"
)

# If a pending map target exists, copy it to sidebar Tujuan
_pending = st.session_state.get('pending_target')
if _pending:
    try:
        p_lat, p_lon = _pending
        st.session_state['end_lat'] = float(p_lat)
        st.session_state['end_lon'] = float(p_lon)
        st.session_state['pending_target'] = None
        st.sidebar.success("➡️ Tujuan otomatis diisi dari peta")
        # update local variables so the UI shows immediately
        end_lat = st.session_state['end_lat']
        end_lon = st.session_state['end_lon']
    except Exception:
        pass

with st.sidebar.expander("DEBUG - session_state", expanded=False):
    st.write({
        'gps_detected': st.session_state.get('gps_detected'),
        'gps_lat': st.session_state.get('gps_lat'),
        'gps_lon': st.session_state.get('gps_lon'),
        'start_lat': st.session_state.get('start_lat'),
        'start_lon': st.session_state.get('start_lon'),
        'end_lat': st.session_state.get('end_lat'),
        'end_lon': st.session_state.get('end_lon')
    })

if st.sidebar.button("🔄 Refresh GPS"):
    st.rerun()

# === KONTROL LAYER (RESPONSIVE) ===
st.markdown('<h2 class="section-header">🗺️ Peta Interaktif</h2>', unsafe_allow_html=True)

# Mobile-friendly: Use expander for controls on small screens
with st.expander("🎛️ Kontrol Layer", expanded=True):
    # Heatmap controls
    st.markdown("**🔥 Heatmap**")
    ikan_types = df_filtered['ikan'].unique()
    ikan_types_clean = [ikan for ikan in ikan_types if "Zona Bahaya" not in ikan]
    
    heatmap_toggles = {}
    cols_heat = st.columns(2)
    for idx, ikan in enumerate(ikan_types_clean):
        with cols_heat[idx % 2]:
            heatmap_toggles[ikan] = st.checkbox(f"{ikan}", value=True, key=f"heat_{ikan}_{selected_week}")
    
    show_bahaya_heatmap = st.checkbox("🌊 Zona Bahaya", value=True, key=f"heat_bahaya_{selected_week}")
    
    st.markdown("---")
    
    # Marker controls
    st.markdown("**📍 Marker**")
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        show_ikan_markers = st.checkbox("Marker Ikan", value=False, key=f"marker_ikan_{selected_week}")
    
    with col_m2:
        show_bahaya_markers = st.checkbox("Marker Bahaya", value=False, key=f"marker_bahaya_{selected_week}")
    
    marker_ikan_toggles = {}
    if show_ikan_markers:
        cols_marker = st.columns(2)
        for idx, ikan in enumerate(ikan_types_clean):
            with cols_marker[idx % 2]:
                marker_ikan_toggles[ikan] = st.checkbox(f"• {ikan}", value=True, key=f"marker_{ikan}_{selected_week}")
    
    st.markdown("---")
    st.markdown("**🧭 Rute**")
    show_route = st.checkbox("Tampilkan Rute", value=st.session_state.get(f"show_route_{selected_week}", False), key=f"show_route_{selected_week}")

# === GENERATE MAP (RESPONSIVE SIZE) ===
if basemap_option == "Esri Satellite":
    tiles_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri"
else:
    tiles_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attr = "&copy; OpenStreetMap contributors"

_map_s_lat = _safe_float_forecast(st.session_state.get('start_lat', start_lat), start_lat)
_map_s_lon = _safe_float_forecast(st.session_state.get('start_lon', start_lon), start_lon)
_map_e_lat = _safe_float_forecast(st.session_state.get('end_lat', end_lat), end_lat)
_map_e_lon = _safe_float_forecast(st.session_state.get('end_lon', end_lon), end_lon)

# Prefer centering on the dataset's heatmap centroid (Java Sea area) unless a route is being shown.
# Use a sensible default for Java Sea if dataset is empty or centroids are invalid.
JAVA_SEA_CENTER = (-6.0, 111.0)
try:
    if not df_filtered.empty:
        df_center_lat = float(df_filtered['lat'].mean())
        df_center_lon = float(df_filtered['lon'].mean())
    else:
        df_center_lat, df_center_lon = JAVA_SEA_CENTER
except Exception:
    df_center_lat, df_center_lon = JAVA_SEA_CENTER

# If user requested a route and both endpoints are valid, center on the route midpoint.
use_route_center = False
if show_route and all(isinstance(x, float) for x in [_map_s_lat, _map_s_lon, _map_e_lat, _map_e_lon]):
    # Consider route center only when endpoints are non-trivial (not all zeros)
    if not (_map_s_lat == 0 and _map_s_lon == 0 and _map_e_lat == 0 and _map_e_lon == 0):
        use_route_center = True

if use_route_center:
    map_center = [(_map_s_lat + _map_e_lat) / 2, (_map_s_lon + _map_e_lon) / 2]
    zoom_start = 9
else:
    map_center = [df_center_lat, df_center_lon]
    # Wider zoom to show the Java Sea heatmap area
    zoom_start = 7

m = folium.Map(location=map_center, zoom_start=zoom_start, tiles=None)

folium.TileLayer(tiles=tiles_url, attr=attr, name=basemap_option, control=True).add_to(m)

# HeatMap per jenis ikan
for ikan in ikan_types_clean:
    if heatmap_toggles[ikan]:
        subdf = df_filtered[df_filtered['ikan'] == ikan]
        heat_data = [[row['lat'], row['lon'], row['skor']] for _, row in subdf.iterrows()]
        if heat_data:
            HeatMap(
                heat_data,
                min_opacity=0.1,
                max_zoom=9,
                radius=12,
                blur=15,
                gradient={0.1: "blue", 0.4: "lime", 0.7: "orange", 1: "red"}
            ).add_to(m)

# HeatMap zona bahaya
if show_bahaya_heatmap:
    bahaya_df = df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)]
    bahaya_heat = [[row['lat'], row['lon'], row['skor']] for _, row in bahaya_df.iterrows()]
    if bahaya_heat:
        HeatMap(
            bahaya_heat,
            min_opacity=0.1,
            max_zoom=9,
            radius=14,
            blur=18,
            gradient={0.1: "blue", 0.4: "yellow", 0.7: "orange", 1: "red"}
        ).add_to(m)

# Marker ikan
if show_ikan_markers:
    for ikan in ikan_types_clean:
        if marker_ikan_toggles.get(ikan, True):
            subdf = df_filtered[df_filtered['ikan'] == ikan]
            for _, row in subdf.iterrows():
                popup_html = f"""
                <div style="font-family: Inter, sans-serif; font-size: 13px;">
                <b>Periode:</b> {week_dates[selected_week-1]}<br>
                <b>Jenis Ikan:</b> {row['ikan']}<br>
                <b>Lat:</b> {row['lat']:.4f}<br>
                <b>Lon:</b> {row['lon']:.4f}<br>
                <b>Skor:</b> {row['skor']:.4f}<br>
                <b>Alasan:</b> {row['alasan']}
                </div>
                """
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_html, max_width=280),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)

# Marker bahaya
if show_bahaya_markers:
    bahaya_df = df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)]
    for _, row in bahaya_df.iterrows():
        popup_html = f"""
        <div style="font-family: Inter, sans-serif; font-size: 13px;">
        <b>Periode:</b> {week_dates[selected_week-1]}<br>
        <b>Jenis:</b> {row['ikan']}<br>
        <b>Lat:</b> {row['lat']:.4f}<br>
        <b>Lon:</b> {row['lon']:.4f}<br>
        <b>Skor:</b> {row['skor']:.4f}<br>
        <b>Info:</b> {row['alasan']}
        </div>
        """
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=280),
            icon=folium.Icon(color="red", icon="warning-sign")
        ).add_to(m)

# Rute (guarded)
_s_lat = _safe_float_forecast(st.session_state.get('start_lat', start_lat), start_lat)
_s_lon = _safe_float_forecast(st.session_state.get('start_lon', start_lon), start_lon)
_e_lat = _safe_float_forecast(st.session_state.get('end_lat', end_lat), end_lat)
_e_lon = _safe_float_forecast(st.session_state.get('end_lon', end_lon), end_lon)
if show_route and all(isinstance(x, float) for x in [_s_lat, _s_lon, _e_lat, _e_lon]):
    folium.Marker([_s_lat, _s_lon], popup="📍 Awal", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker([_e_lat, _e_lon], popup="🎯 Tujuan", icon=folium.Icon(color="blue", icon="flag")).add_to(m)
    folium.PolyLine(
        locations=[[_s_lat, _s_lon], [_e_lat, _e_lon]],
        color="cyan",
        weight=4,
        opacity=0.8,
        dash_array="10"
    ).add_to(m)

# Tampilkan peta dengan ukuran responsif
st_data = st_folium(m, width=None, height=500, key=f"map_{selected_month}_{selected_week}", returned_objects=["last_clicked"])

# Jika pengguna mengklik titik pada peta, tampilkan tombol "Menuju Titik Ini"
clicked = None
if isinstance(st_data, dict):
    clicked = st_data.get('last_clicked')

if clicked:
    # streamlit-folium memberikan {'lat':..., 'lng':...}
    try:
        lat = float(clicked.get('lat'))
        lon = float(clicked.get('lng'))
        st.markdown(f"**Koordinat terpilih:** {lat:.6f}, {lon:.6f}")
        if st.session_state.get('auto_fill_on_click', True):
            st.session_state['pending_target'] = (lat, lon)
            route_key = f"show_route_{selected_week}"
            if st.session_state.get('start_lat') is None and st.session_state.get('gps_lat') is not None:
                st.session_state['start_lat'] = st.session_state.get('gps_lat')
            if st.session_state.get('start_lon') is None and st.session_state.get('gps_lon') is not None:
                st.session_state['start_lon'] = st.session_state.get('gps_lon')
            st.session_state[route_key] = True
            st.session_state['route_just_set'] = True
            st.experimental_rerun()
        else:
            if st.button("➡️ Menuju Titik Ini"):
                st.session_state['pending_target'] = (lat, lon)
                route_key = f"show_route_{selected_week}"
                if st.session_state.get('start_lat') is None and st.session_state.get('gps_lat') is not None:
                    st.session_state['start_lat'] = st.session_state.get('gps_lat')
                if st.session_state.get('start_lon') is None and st.session_state.get('gps_lon') is not None:
                    st.session_state['start_lon'] = st.session_state.get('gps_lon')
                st.session_state[route_key] = True
                st.session_state['route_just_set'] = True
                st.experimental_rerun()
    except Exception:
        pass

# Auto-refresh: tambahkan pilihan di sidebar (JS reload)
auto_refresh = st.sidebar.checkbox("🔁 Auto Refresh", value=False)
refresh_interval = st.sidebar.number_input("Interval refresh (detik)", min_value=5, max_value=600, value=30, step=5)
if auto_refresh:
    from streamlit.components.v1 import html as st_html
    # reload halaman setelah interval (client-side)
    st_html(f"<script>setTimeout(()=>location.reload(), {int(refresh_interval)*1000});</script>", height=0)

# === INFO PANEL (RESPONSIVE) ===
st.markdown("---")

with st.expander("ℹ️ Informasi Koordinat", expanded=False):
    # Safely coerce coordinates to floats for presentation and distance calc
    _s_lat = _safe_float_forecast(st.session_state.get('start_lat', start_lat), start_lat)
    _s_lon = _safe_float_forecast(st.session_state.get('start_lon', start_lon), start_lon)
    _e_lat = _safe_float_forecast(st.session_state.get('end_lat', end_lat), end_lat)
    _e_lon = _safe_float_forecast(st.session_state.get('end_lon', end_lon), end_lon)
    distance_km = ((_e_lat-_s_lat)**2 + (_e_lon-_s_lon)**2)**0.5 * 111
    st.info(f"""
    **Periode:** {week_dates[selected_week-1]}
    
    **Dataset:** variant_{selected_week}.csv
    
    **Basemap:** {basemap_option}
    
    **Posisi Awal:** {_s_lat:.6f}, {_s_lon:.6f}
    
    **Tujuan:** {_e_lat:.6f}, {_e_lon:.6f}
    
    **Jarak:** ≈ {distance_km:.1f} km
    """)

# === DATA SUMMARY (RESPONSIVE GRID) ===
st.markdown('<h2 class="section-header">📈 Ringkasan Data</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Data", len(df_filtered))
    total_bahaya = len(df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
    st.metric("Zona Bahaya", total_bahaya)

with col2:
    total_ikan = len(df_filtered[~df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
    st.metric("Potensi Ikan", total_ikan)
    avg_score = df_filtered['skor'].mean()
    st.metric("Rata-rata Skor", f"{avg_score:.3f}")

# === PERBANDINGAN MINGGU (COMPACT) ===
st.markdown('<h2 class="section-header">📊 Perbandingan Mingguan</h2>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([f"W{i}" for i in range(1, 5)])

tabs = [tab1, tab2, tab3, tab4]
for i, tab in enumerate(tabs, 1):
    with tab:
        try:
            df_week = pd.read_csv(csv_files[i])
            if required_cols.issubset(df_week.columns):
                df_week_filtered = df_week[df_week['skor'] > 0.4]
                
                c1, c2 = st.columns(2)
                with c1:
                    st.metric("Total", len(df_week_filtered))
                with c2:
                    avg = df_week_filtered['skor'].mean()
                    st.metric("Avg", f"{avg:.3f}")
                
                if i == selected_week:
                    st.success(f"✅ Minggu ke-{i}")
            else:
                st.error(f"❌ File tidak sesuai")
                
        except FileNotFoundError:
            st.error(f"❌ File tidak ada")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# === PANDUAN ===
with st.expander("📖 Panduan"):
    st.markdown("""
    ### Cara Menggunakan:
    
    **1. Pilih Periode** - Bulan dan minggu
    
    **2. Kontrol Layer** - Toggle heatmap dan marker
    
    **3. Navigasi** - Input koordinat di sidebar
    
    **4. Interpretasi:**
    - Heatmap: Biru (rendah) → Merah (tinggi)
    - Marker Biru: Potensi ikan
    - Marker Merah: Zona bahaya
    - Garis Cyan: Rute
    """)
