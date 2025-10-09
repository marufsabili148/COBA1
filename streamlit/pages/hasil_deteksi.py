import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from streamlit_option_menu import option_menu
import os

# === KONFIGURASI HALAMAN ===
st.set_page_config(
    page_title="SAILOR - Deteksi Zona Ikan",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === CUSTOM CSS - COPERNICUS STYLE (CONSISTENT WITH HOME.PY) ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset with Inter Font */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: clamp(1rem, 3vw, 2rem);
        padding-bottom: clamp(1rem, 3vw, 2rem);
        padding-left: clamp(0.5rem, 2vw, 1rem);
        padding-right: clamp(0.5rem, 2vw, 1rem);
        max-width: 1400px;
    }
    
    /* Page Header - Responsive */
    .page-header {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        padding: clamp(1.5rem, 4vw, 2rem) 0 clamp(1rem, 3vw, 1.5rem) 0;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 1px solid #e1e4e8;
        text-align: center;
    }
    
    .page-title {
        font-size: clamp(1.8rem, 5vw, 2.5rem) !important;
        font-weight: 600 !important;
        color: #0e4194;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif !important;
    }
    
    .page-subtitle {
        font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
        color: #586069;
        font-weight: 400;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Buttons - Responsive */
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: clamp(0.5rem, 2vw, 0.75rem) clamp(1.25rem, 3vw, 1.5rem);
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.2s ease;
        with col1:
            st.markdown('<div class="control-card">', unsafe_allow_html=True)
            # Gunakan expander agar bisa klik buka/tutup seperti accordion
            with st.expander('🔥 Layer Heatmap', expanded=False):
                st.write('Pilih layer heatmap yang ingin ditampilkan:')
                # opsi per-jenis
                heatmap_mode = st.radio(
                    'Mode Heatmap',
                    ['Semua', 'Per Jenis', 'Zona Bahaya'],
                    index=0,
                    key='heatmap_mode_radio'
                )

                heatmap_toggles = {}
                if heatmap_mode in ('Semua', 'Per Jenis'):
                    st.write('Pilih jenis ikan untuk heatmap:')
                    for ikan in ikan_types_clean:
                        default_val = True if heatmap_mode == 'Semua' else True
                        heatmap_toggles[ikan] = st.checkbox(f'{ikan}', value=default_val, key=f'heat_{ikan}')

                # Toggle untuk heatmap zona bahaya
                if heatmap_mode == 'Zona Bahaya':
                    show_bahaya_heatmap = True
                else:
                    show_bahaya_heatmap = st.checkbox('🌊 Zona Bahaya', value=True, key='heat_bahaya')
            st.markdown('</div>', unsafe_allow_html=True)
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        margin: clamp(0.75rem, 2vw, 1rem) 0;
        border-radius: 4px;
    }
    
    .info-box h4 {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(1rem, 2.5vw, 1.15rem) !important;
    }
    
    .info-box p {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
    }
    
    /* Metrics - Responsive */
    [data-testid="stMetricValue"] {
        font-size: clamp(1.4rem, 4vw, 1.8rem) !important;
        font-weight: 600 !important;
        color: #0e4194;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
        color: #586069;
        font-weight: 500;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f6f8fa;
        border-radius: 4px;
        font-weight: 500 !important;
        color: #24292e;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
    }
    
    /* Control Cards - Responsive */
    .control-card {
        background: white;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        margin-bottom: 1rem;
    }
    
    .control-card-title {
        font-size: clamp(1rem, 2.5vw, 1.1rem) !important;
        font-weight: 600 !important;
        color: #24292e;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Input Fields */
    .stNumberInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #e1e4e8;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 4px;
        border: 1px solid #e1e4e8;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Checkbox */
    with col2:
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        # Expander untuk Marker Ikan (klik untuk buka/tutup)
        with st.expander('📍 Marker Ikan', expanded=False):
            st.write('Pengaturan marker titik hasil deteksi:')
            marker_mode = st.radio(
                'Mode Marker',
                ['Semua', 'Per Jenis', 'Tidak ada'],
                index=0,
                key='marker_mode_radio'
            )

            show_ikan_markers = False
            marker_ikan_toggles = {}
            if marker_mode == 'Semua':
                show_ikan_markers = True
                for ikan in ikan_types_clean:
                    marker_ikan_toggles[ikan] = True
            elif marker_mode == 'Per Jenis':
                show_ikan_markers = True
                st.write('Pilih jenis ikan yang ingin ditampilkan marker:')
                for ikan in ikan_types_clean:
                    marker_ikan_toggles[ikan] = st.checkbox(f'• {ikan}', value=True, key=f'marker_{ikan}')
            else:
                show_ikan_markers = False
        st.markdown('</div>', unsafe_allow_html=True)
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .page-header {
            margin: -0.5rem -0.5rem 1.5rem -0.5rem;
            padding: 1.5rem 1rem;
        }
        
        .control-card {
        # Ensure menu indicator syncs on load
        st.session_state.current_page = 'Deteksi Zona Ikan'
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Deteksi Zona Ikan'

# === NAVIGATION - single option_menu with unique key ===
nav_options = ["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang", "Feedback"]
current = st.session_state.get('current_page', 'Deteksi Zona Ikan')
default_index = nav_options.index(current) if current in nav_options else nav_options.index('Deteksi Zona Ikan')
selected = option_menu(
    menu_title=None,
    options=nav_options,
    icons=["house", "map", "graph-up", "book", "info-circle", "chat-dots"],
    menu_icon="cast",
    default_index=default_index,
    orientation="horizontal",
    key="main_nav",
    styles={
        "container": {"padding": "0", "background-color": "transparent", "border-bottom": "1px solid #e1e4e8"},
        "icon": {"color": "#586069", "font-size": "clamp(14px, 3vw, 16px)"},
        "nav-link": {"font-size": "clamp(0.75rem, 2vw, 0.95rem)", "text-align": "center", "margin": "0", "padding": "clamp(10px, 2vw, 14px) clamp(12px, 3vw, 24px)", "color": "#24292e", "font-weight": "500", "border-bottom": "3px solid transparent", "--hover-color": "#f6f8fa", "font-family": "Inter, sans-serif"},
        "nav-link-selected": {"background-color": "transparent", "border-bottom": "3px solid #0e4194", "color": "#0e4194"},
    }
)

# Only switch if user selected a different page
if selected != st.session_state.get('current_page', 'Deteksi Zona Ikan'):
    st.session_state.current_page = selected
    if selected == "Beranda":
        st.switch_page("home.py")
    elif selected == "Deteksi Zona Ikan":
        pass
    elif selected == "Prediksi 30 Hari":
        st.switch_page("pages/forecast.py")
    elif selected == "Tutorial":
        st.switch_page("pages/tutorial.py")
    elif selected == "Tentang":
        st.switch_page("home.py")
    elif selected == "Feedback":
        st.switch_page("pages/feedback.py")

st.session_state.current_page = selected

# === MAPPING CSV FILES (RELATIVE PATH) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
csv_files = {
    1: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_1.csv"),
    2: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_2.csv"), 
    3: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_3.csv"),
    4: os.path.join(PROJECT_ROOT, "csv", "fish_potential_variant_4.csv")
}

# Default: gunakan variant 1
csv_path = csv_files[1]

try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}")
    st.stop()

# Tambahkan alasan sederhana
def alasan_potensi(row):
    if "Zona Bahaya" in row['ikan']:
        return "Lokasi ini terdeteksi berbahaya karena kondisi cuaca/gelombang."
    elif row['skor'] > 0.9:
        return "Sangat potensial: kondisi lingkungan optimal (suhu, plankton, arus)."
    elif row['skor'] > 0.75:
        return "Potensial tinggi: sebagian besar parameter mendukung."
    elif row['skor'] > 0.5:
        return "Potensial sedang: hanya sebagian parameter sesuai."
    else:
        return "Potensial rendah: sedikit parameter yang mendukung."

df['alasan'] = df.apply(alasan_potensi, axis=1)

# Filter hanya skor > 0.4
df_filtered = df[df['skor'] > 0.4].copy()

# === SIDEBAR CONTROLS ===
st.sidebar.markdown("### 🔍 Kontrol Navigasi")

# Pilih basemap
basemap_option = st.sidebar.selectbox(
    "Pilih Basemap",
    ["OpenStreetMap", "Esri Satellite"]
)

# Inisialisasi session state untuk menyimpan koordinat GPS
if 'gps_lat' not in st.session_state:
    st.session_state.gps_lat = None
if 'gps_lon' not in st.session_state:
    st.session_state.gps_lon = None
if 'gps_detected' not in st.session_state:
    st.session_state.gps_detected = False

# Defensive: ensure start/end and route keys exist and are coercible to float/bool
if 'start_lat' not in st.session_state:
    st.session_state['start_lat'] = None
if 'start_lon' not in st.session_state:
    st.session_state['start_lon'] = None
if 'end_lat' not in st.session_state:
    st.session_state['end_lat'] = None
if 'end_lon' not in st.session_state:
    st.session_state['end_lon'] = None
if 'show_route' not in st.session_state:
    st.session_state['show_route'] = True

# Helper to coerce floats safely
def _safe_float(v, fallback):
    # Try to coerce v first, then fallback. If both fail or are None, return 0.0
    for candidate in (v, fallback):
        try:
            if candidate is None:
                continue
            return float(candidate)
        except Exception:
            continue
    return 0.0

# Ambil GPS live user
loc = get_geolocation()
if loc is not None and "coords" in loc:
    # Update session state dengan koordinat GPS
    st.session_state.gps_lat = loc["coords"]["latitude"]
    st.session_state.gps_lon = loc["coords"]["longitude"]
    st.session_state.gps_detected = True
    st.sidebar.success("📍 GPS berhasil terdeteksi!")
    st.sidebar.info(f"Lat: {st.session_state.gps_lat:.6f}, Lon: {st.session_state.gps_lon:.6f}")
    # If start coordinates haven't been set by user yet, populate them from GPS
    if st.session_state.get('start_lat') is None:
        st.session_state['start_lat'] = st.session_state.gps_lat
    if st.session_state.get('start_lon') is None:
        st.session_state['start_lon'] = st.session_state.gps_lon
else:
    if not st.session_state.gps_detected:
        st.sidebar.warning("⚠️ GPS tidak terdeteksi, menggunakan koordinat default")

# Tentukan nilai default untuk input
if st.session_state.gps_detected and st.session_state.gps_lat is not None:
    default_start_lat = st.session_state.gps_lat
    default_start_lon = st.session_state.gps_lon
else:
    default_start_lat = df_filtered.lat.mean()
    default_start_lon = df_filtered.lon.mean()

# Input koordinat manual
st.sidebar.markdown("#### 📍 Posisi Awal")
st.sidebar.caption("GPS terdeteksi - ubah manual jika perlu" if st.session_state.gps_detected else "Masukkan koordinat manual")

# Compute safe start coords (avoid None)
_start_val = st.session_state.get('start_lat')
if _start_val is None:
    _start_val = default_start_lat
_start_val = _safe_float(_start_val, default_start_lat)
_lon_val = st.session_state.get('start_lon')
if _lon_val is None:
    _lon_val = default_start_lon
_lon_val = _safe_float(_lon_val, default_start_lon)

# If a pending target was set by a map click, move it into the sidebar 'Tujuan' fields now
_pending = st.session_state.get('pending_target')
if _pending:
    try:
        p_lat, p_lon = _pending
        st.session_state['end_lat'] = float(p_lat)
        st.session_state['end_lon'] = float(p_lon)
        # clear pending flag
        st.session_state['pending_target'] = None
        st.sidebar.success("➡️ Tujuan otomatis diisi dari peta")
    except Exception:
        pass

start_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(_start_val), 
    format="%.6f",
    help="Koordinat latitude posisi Anda saat ini (terisi otomatis dari GPS)",
    key="start_lat"
)
start_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(_lon_val), 
    format="%.6f",
    help="Koordinat longitude posisi Anda saat ini (terisi otomatis dari GPS)",
    key="start_lon"
)

# Option: auto-fill tujuan fields when user clicks a point on the map
auto_fill_on_click = st.sidebar.checkbox("Auto-fill Tujuan saat klik peta", value=True, key="auto_fill_on_click")

st.sidebar.markdown("#### 🎯 Tujuan")
# Compute safe end coords (avoid None)
_end_val = st.session_state.get('end_lat')
if _end_val is None:
    _end_val = float(df_filtered.lat.mean())
_end_val = _safe_float(_end_val, float(df_filtered.lat.mean()))
_end_lon_val = st.session_state.get('end_lon')
if _end_lon_val is None:
    _end_lon_val = float(df_filtered.lon.mean())
_end_lon_val = _safe_float(_end_lon_val, float(df_filtered.lon.mean()))

end_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(_end_val), 
    format="%.6f",
    help="Koordinat latitude tujuan",
    key="end_lat"
)
end_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(_end_lon_val), 
    format="%.6f",
    help="Koordinat longitude tujuan",
    key="end_lon"
)

# Debug panel to inspect session state during interactive testing
with st.sidebar.expander("DEBUG - session_state", expanded=False):
    st.write({
        'gps_detected': st.session_state.get('gps_detected'),
        'gps_lat': st.session_state.get('gps_lat'),
        'gps_lon': st.session_state.get('gps_lon'),
        'start_lat': st.session_state.get('start_lat'),
        'start_lon': st.session_state.get('start_lon'),
        'end_lat': st.session_state.get('end_lat'),
        'end_lon': st.session_state.get('end_lon'),
        'show_route': st.session_state.get('show_route')
    })

col_btn1, col_btn2 = st.sidebar.columns(2)
with col_btn1:
    if st.button("🔄 Refresh GPS", use_container_width=True):
        st.session_state.gps_detected = False
        st.rerun()
with col_btn2:
    if st.button("📍 Gunakan GPS", use_container_width=True):
        if st.session_state.gps_detected and st.session_state.gps_lat is not None:
            # Force update dengan rerun
            st.rerun()
        else:
            st.sidebar.error("GPS belum terdeteksi")

# === MAIN MAP SECTION ===
st.markdown('<h2 class="section-header">🗺️ Peta Interaktif</h2>', unsafe_allow_html=True)

# === KONTROL LAYER ===
st.markdown('<h3 class="section-header" style="font-size: clamp(1.1rem, 3vw, 1.25rem); margin-top: 1rem;">🎛️ Kontrol Layer</h3>', unsafe_allow_html=True)

# Buat kolom untuk toggle controls
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-card-title">🔥 Layer Heatmap</div>', unsafe_allow_html=True)
    
    # Toggle untuk heatmap per jenis ikan
    ikan_types = df_filtered['ikan'].unique()
    ikan_types_clean = [ikan for ikan in ikan_types if "Zona Bahaya" not in ikan]
    
    # Dropdown untuk memilih layer heatmap: Semua / Per jenis / Zona Bahaya
    heatmap_mode = st.selectbox(
        "Mode Heatmap",
        ["Semua", "Per Jenis", "Zona Bahaya"],
        index=0,
        key="heatmap_mode",
        help="Pilih apakah menampilkan semua heatmap, per jenis ikan, atau hanya zona bahaya"
    )

    heatmap_toggles = {}
    if heatmap_mode in ("Semua", "Per Jenis"):
        for ikan in ikan_types_clean:
            default_val = True if heatmap_mode == "Semua" else True
            heatmap_toggles[ikan] = st.checkbox(f"{ikan}", value=default_val, key=f"heat_{ikan}")

    # Toggle untuk heatmap zona bahaya
    show_bahaya_heatmap = True if heatmap_mode == "Zona Bahaya" else st.checkbox("🌊 Zona Bahaya", value=True, key="heat_bahaya")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-card-title">📍 Marker Ikan</div>', unsafe_allow_html=True)
    # Dropdown untuk memilih marker ikan: Semua / Per jenis / Tidak ada
    marker_mode = st.selectbox(
        "Mode Marker",
        ["Semua", "Per Jenis", "Tidak ada"],
        index=0,
        key="marker_mode",
        help="Pilih apakah menampilkan semua marker, memilih per jenis ikan, atau tidak menampilkan marker"
    )

    show_ikan_markers = False
    marker_ikan_toggles = {}
    if marker_mode == "Semua":
        show_ikan_markers = True
        for ikan in ikan_types_clean:
            marker_ikan_toggles[ikan] = True
    elif marker_mode == "Per Jenis":
        show_ikan_markers = True
        for ikan in ikan_types_clean:
            marker_ikan_toggles[ikan] = st.checkbox(f"• {ikan}", value=True, key=f"marker_{ikan}")
    else:
        show_ikan_markers = False
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-card-title">🚫 Bahaya & Rute</div>', unsafe_allow_html=True)
    
    show_bahaya_markers = st.checkbox("Tampilkan Marker Bahaya", value=st.session_state.get('marker_bahaya', True), key="marker_bahaya")
    show_route = st.checkbox("Tampilkan Rute Navigasi", value=st.session_state.get('show_route', True), key="show_route")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

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
            st.session_state['show_route'] = True
            st.sidebar.success('➡️ Tujuan otomatis diisi dari daftar')
            st.experimental_rerun()
except Exception:
    pass

# === GENERATE MAP ===
# Set basemap
if basemap_option == "Esri Satellite":
    tiles_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
else:
    tiles_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attr = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"

# Inisialisasi peta
# Compute safe map center using coerced floats to avoid NoneType errors
_map_s_lat = _safe_float(st.session_state.get('start_lat', _start_val), _start_val)
_map_s_lon = _safe_float(st.session_state.get('start_lon', _lon_val), _lon_val)
_map_e_lat = _safe_float(st.session_state.get('end_lat', _end_val), _end_val)
_map_e_lon = _safe_float(st.session_state.get('end_lon', _end_lon_val), _end_lon_val)
map_center = [(_map_s_lat + _map_e_lat) / 2, (_map_s_lon + _map_e_lon) / 2]
m = folium.Map(location=map_center, zoom_start=8, tiles=tiles_url, attr=attr)

# === HeatMap per jenis ikan ===
if heatmap_mode in ("Semua", "Per Jenis"):
    for ikan in ikan_types_clean:
        if heatmap_toggles.get(ikan, False):
            subdf = df_filtered[df_filtered['ikan'] == ikan]
            heat_data = [
                [row['lat'], row['lon'], row['skor']]
                for _, row in subdf.iterrows()
            ]
            if heat_data:
                HeatMap(
                    heat_data,
                    min_opacity=0.1,
                    max_zoom=9,
                    radius=12,
                    blur=15,
                    gradient={0.1: "blue", 0.4: "lime", 0.7: "orange", 1: "red"}
                ).add_to(m)

# === HeatMap zona bahaya ===
if show_bahaya_heatmap:
    bahaya_df = df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)]
    bahaya_heat = [
        [row['lat'], row['lon'], row['skor']]
        for _, row in bahaya_df.iterrows()
    ]
    if bahaya_heat:
        HeatMap(
            bahaya_heat,
            min_opacity=0.1,
            max_zoom=9,
            radius=14,
            blur=18,
            gradient={0.1: "blue", 0.4: "yellow", 0.7: "orange", 1: "red"}
        ).add_to(m)

# === Marker titik koordinat ikan ===
if show_ikan_markers:
    for ikan in ikan_types_clean:
        if marker_ikan_toggles.get(ikan, True):
            subdf = df_filtered[df_filtered['ikan'] == ikan]
            for _, row in subdf.iterrows():
                popup_html = f"""
                <b>Jenis Ikan:</b> {row['ikan']}<br>
                <b>Latitude:</b> {row['lat']:.4f}<br>
                <b>Longitude:</b> {row['lon']:.4f}<br>
                <b>Skor Potensi:</b> {row['skor']:.4f}<br>
                <b>Alasan:</b> {row['alasan']}
                """
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)

# === Marker titik koordinat zona bahaya ===
if show_bahaya_markers:
    bahaya_df = df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)]
    for _, row in bahaya_df.iterrows():
        popup_html = f"""
        <b>Jenis:</b> {row['ikan']}<br>
        <b>Latitude:</b> {row['lat']:.4f}<br>
        <b>Longitude:</b> {row['lon']:.4f}<br>
        <b>Skor:</b> {row['skor']:.4f}<br>
        <b>Keterangan:</b> {row['alasan']}
        """
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=300),
            icon=folium.Icon(color="red", icon="warning-sign")
        ).add_to(m)

# === Marker Posisi Awal (SELALU TAMPIL jika GPS terdeteksi atau koordinat diinput) ===
# Tambahkan marker posisi awal dengan icon khusus untuk GPS
if st.session_state.gps_detected:
    _disp_s_lat = _safe_float(st.session_state.get('start_lat', start_lat), start_lat)
    _disp_s_lon = _safe_float(st.session_state.get('start_lon', start_lon), start_lon)
    folium.Marker(
        [_disp_s_lat, _disp_s_lon], 
        popup=f"📍 <b>Posisi Anda (GPS)</b><br>Lat: {_disp_s_lat:.6f}<br>Lon: {_disp_s_lon:.6f}", 
        icon=folium.Icon(color="green", icon="record", prefix='fa'),
        tooltip="Posisi Anda Saat Ini"
    ).add_to(m)
else:
    _disp_s_lat = _safe_float(st.session_state.get('start_lat', start_lat), start_lat)
    _disp_s_lon = _safe_float(st.session_state.get('start_lon', start_lon), start_lon)
    folium.Marker(
        [_disp_s_lat, _disp_s_lon], 
        popup=f"📍 <b>Posisi Awal (Manual)</b><br>Lat: {_disp_s_lat:.6f}<br>Lon: {_disp_s_lon:.6f}", 
        icon=folium.Icon(color="lightgreen", icon="map-marker", prefix='fa'),
        tooltip="Posisi Awal"
    ).add_to(m)

# === Gambar garis rute (guarded) ===
try:
    _start_lat = _safe_float(st.session_state.get('start_lat', start_lat), start_lat)
    _start_lon = _safe_float(st.session_state.get('start_lon', start_lon), start_lon)
    _end_lat = _safe_float(st.session_state.get('end_lat', end_lat), end_lat)
    _end_lon = _safe_float(st.session_state.get('end_lon', end_lon), end_lon)
except Exception:
    _start_lat, _start_lon, _end_lat, _end_lon = start_lat, start_lon, end_lat, end_lon

if show_route:
    # Only draw route if we have valid numeric coordinates
    if all(map(lambda x: isinstance(x, float), [_start_lat, _start_lon, _end_lat, _end_lon])):
        folium.Marker(
            [_end_lat, _end_lon], 
            popup=f"🎯 <b>Titik Tujuan</b><br>Lat: {_end_lat:.6f}<br>Lon: {_end_lon:.6f}", 
            icon=folium.Icon(color="blue", icon="flag"),
            tooltip="Tujuan"
        ).add_to(m)
        folium.PolyLine(
            locations=[[_start_lat, _start_lon], [_end_lat, _end_lon]],
            color="cyan",
            weight=4,
            opacity=0.8,
            dash_array="10",
            popup=f"Rute: {((_end_lat-_start_lat)**2 + (_end_lon-_start_lon)**2)**0.5 * 111:.1f} km"
        ).add_to(m)

# Tampilkan peta
st_data = st_folium(m, width=1200, height=600, returned_objects=["last_clicked", "all_drawings"])

# Tangani klik pada peta: jika ada titik diklik, tampilkan tombol untuk menavigasi ke titik tersebut
clicked = None
if isinstance(st_data, dict):
    clicked = st_data.get('last_clicked')

if clicked:
    try:
        lat = float(clicked.get('lat'))
        lon = float(clicked.get('lng') or clicked.get('lon') or clicked.get('lng') )
        st.markdown(f"**Koordinat terpilih:** {lat:.6f}, {lon:.6f}")
        # If auto-fill is enabled, immediately set pending target and rerun
        if st.session_state.get('auto_fill_on_click', True):
            st.session_state['pending_target'] = (lat, lon)
            if st.session_state.get('start_lat') is None and st.session_state.get('gps_lat') is not None:
                st.session_state['start_lat'] = st.session_state.get('gps_lat')
            if st.session_state.get('start_lon') is None and st.session_state.get('gps_lon') is not None:
                st.session_state['start_lon'] = st.session_state.get('gps_lon')
            st.session_state['show_route'] = True
            st.session_state['route_just_set'] = True
            st.experimental_rerun()
        else:
            if st.button("➡️ Menuju Titik Ini"):
                # update tujuan dan aktifkan rute
                # set pending target so sidebar picks it up immediately
                st.session_state['pending_target'] = (lat, lon)
                # ensure start coords exist (use GPS if available)
                if st.session_state.get('start_lat') is None and st.session_state.get('gps_lat') is not None:
                    st.session_state['start_lat'] = st.session_state.get('gps_lat')
                if st.session_state.get('start_lon') is None and st.session_state.get('gps_lon') is not None:
                    st.session_state['start_lon'] = st.session_state.get('gps_lon')
                st.session_state['show_route'] = True
                st.session_state['route_just_set'] = True
                st.experimental_rerun()
    except Exception:
        pass

# === INFO PANEL ===
st.markdown("---")
st.markdown('<h2 class="section-header">ℹ️ Informasi Navigasi</h2>', unsafe_allow_html=True)

col_info1, col_info2 = st.columns(2)

with col_info1:
    gps_status = "GPS Aktif 🟢" if st.session_state.gps_detected else "Manual 🔵"
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

# Default: gunakan variant 1
csv_path = csv_files[1]

# Baca CSV
try:
    df = pd.read_csv(csv_path)
except Exception as e:
    st.error(f"Gagal membaca file CSV: {e}")
    st.stop()
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Heatmap", active_heatmaps)
    with col_b:
        st.metric("Marker Ikan", active_markers_ikan)
    with col_c:
        st.metric("Marker Bahaya", active_markers_bahaya)
    
    st.markdown('</div>', unsafe_allow_html=True)

# === DATA SUMMARY ===
st.markdown("---")
st.markdown('<h2 class="section-header">📈 Ringkasan Data</h2>', unsafe_allow_html=True)

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    total_points = len(df_filtered)
    st.metric("Total Titik Data", total_points)

with col_stat2:
    total_ikan = len(df_filtered[~df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
    st.metric("Titik Potensi Ikan", total_ikan)

with col_stat3:
    total_bahaya = len(df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
    st.metric("Zona Bahaya", total_bahaya)

with col_stat4:
    avg_score = df_filtered['skor'].mean()
    st.metric("Rata-rata Skor", f"{avg_score:.3f}")

# === PANDUAN PENGGUNAAN ===
st.markdown("---")
with st.expander("📖 Panduan Penggunaan"):
    st.markdown("""
    ### Cara Menggunakan Aplikasi:
    
    **1. Input Koordinat:**
    - Masukkan latitude/longitude posisi awal di sidebar kiri
    - Masukkan koordinat tujuan yang diinginkan
    - Klik "🔄 Refresh GPS" untuk update lokasi otomatis
    
    **2. Kontrol Layer:**
    - Centang/hapus centang untuk menampilkan/menyembunyikan layer
    - Heatmap menunjukkan intensitas dengan gradasi warna
    - Marker biru = lokasi potensi ikan
    - Marker merah = zona bahaya
    
    **3. Interpretasi Warna Heatmap:**
    - Biru = Potensi rendah
    - Hijau = Potensi sedang  
    - Oranye = Potensi tinggi
    - Merah = Potensi sangat tinggi
    
    **4. Navigasi:**
    - Garis cyan putus-putus menunjukkan rute estimasi
    - Marker hijau = posisi awal
    - Marker biru = tujuan
    
    **5. Pilihan Basemap:**
    - OpenStreetMap = Peta standar dengan detail jalan dan topografi
    - Esri Satellite = Citra satelit untuk melihat kondisi geografis real
    """)

# Auto-refresh dengan tombol tambahan
if st.sidebar.button("🔄 Auto Refresh (30s)"):
    import time
    time.sleep(30)
    st.rerun()
