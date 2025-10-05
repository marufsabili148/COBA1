import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from streamlit_option_menu import option_menu
import os
import time

# === KONFIGURASI HALAMAN ===
st.set_page_config(
    page_title="SAILOR - Deteksi Zona Ikan",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === CUSTOM CSS - RESPONSIVE & INTER FONT ===
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
        padding: clamp(1.5rem, 3vw, 2rem) clamp(1rem, 2vw, 2rem) clamp(1rem, 2vw, 1.5rem);
        margin: -1rem -1rem 1.5rem -1rem;
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
        font-size: clamp(0.9rem, 2.5vw, 1.1rem) !important;
        color: #586069;
        font-weight: 400;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        padding: clamp(0.5rem, 2vw, 1rem);
    }
    
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {
        color: #0e4194;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
    }
    
    [data-testid="stSidebar"] label {
        font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Buttons - Responsive */
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: clamp(0.5rem, 2vw, 0.6rem) clamp(1rem, 2.5vw, 1.5rem);
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
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
    
    /* Section Headers - Responsive */
    .section-header {
        font-size: clamp(1.2rem, 3.5vw, 1.5rem) !important;
        font-weight: 600 !important;
        color: #24292e;
        margin: clamp(1.5rem, 3vw, 2rem) 0 clamp(0.75rem, 2vw, 1rem) 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0e4194;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Info Boxes - Responsive */
    .info-box {
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .info-box h4 {
        font-size: clamp(1rem, 2.5vw, 1.2rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .info-box p {
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Metrics - Responsive */
    [data-testid="stMetricValue"] {
        font-size: clamp(1.3rem, 3.5vw, 1.8rem) !important;
        font-weight: 600 !important;
        color: #0e4194;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: clamp(0.75rem, 2vw, 0.9rem) !important;
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
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Checkbox - Responsive */
    .stCheckbox {
        padding: 0.25rem 0;
    }
    
    .stCheckbox label {
        font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Number Input & Select Box - Fixed Overlap */
    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label {
        display: block !important;
        margin-bottom: 0.5rem !important;
        font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
    }
    
    .stNumberInput > div,
    .stSelectbox > div {
        width: 100% !important;
    }
    
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {
        border-radius: 4px;
        border: 1px solid #e1e4e8;
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        font-family: 'Inter', sans-serif !important;
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
        font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
        font-weight: 600 !important;
        color: #24292e;
        margin-bottom: 1rem;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #24292e;
        font-family: 'Inter', sans-serif !important;
    }
    
    p, span, div, label, a {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Responsive Columns */
    [data-testid="column"] {
        padding: clamp(0.25rem, 1vw, 0.5rem) !important;
    }
    
    /* Option Menu Responsive */
    .nav-link {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
    }
    
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .page-header {
            margin: -0.5rem -0.5rem 1rem -0.5rem;
            padding: 1.5rem 1rem 1rem;
        }
        
        [data-testid="column"] {
            min-width: 100% !important;
            margin-bottom: 0.5rem;
        }
        
        .control-card {
            padding: 1rem;
        }
        
        .row-widget.stHorizontal {
            flex-direction: column;
        }
    }
    
    /* Extra Small Devices */
    @media (max-width: 480px) {
        .page-title {
            font-size: 1.5rem !important;
        }
        
        .page-subtitle {
            font-size: 0.85rem !important;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Deteksi Zona Ikan'
if 'use_gps' not in st.session_state:
    st.session_state.use_gps = False
if 'gps_lat' not in st.session_state:
    st.session_state.gps_lat = None
if 'gps_lon' not in st.session_state:
    st.session_state.gps_lon = None
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()

# === NAVIGATION - RESPONSIVE ===
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang"],
    icons=["house", "map", "graph-up", "book", "info-circle"],
    menu_icon="cast",
    default_index=1,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "0", 
            "background-color": "#ffffff", 
            "border-bottom": "1px solid #e1e4e8"
        },
        "icon": {
            "color": "#586069", 
            "font-size": "clamp(14px, 3vw, 16px)"
        },
        "nav-link": {
            "font-size": "clamp(0.75rem, 2vw, 0.95rem)",
            "text-align": "center",
            "margin": "0",
            "padding": "clamp(10px, 2vw, 14px) clamp(12px, 3vw, 24px)",
            "color": "#24292e",
            "font-weight": "500",
            "border-bottom": "3px solid transparent",
            "--hover-color": "#f6f8fa",
            "font-family": "Inter, sans-serif",
        },
        "nav-link-selected": {
            "background-color": "transparent",
            "border-bottom": "3px solid #0e4194",
            "color": "#0e4194",
        },
    }
)

# Handle navigation
if selected == "Beranda":
    st.switch_page("home.py")
elif selected == "Prediksi 30 Hari":
    st.switch_page("pages/forecast.py")
elif selected == "Tutorial":
    st.switch_page("home.py")
elif selected == "Tentang":
    st.switch_page("home.py")

# === PAGE HEADER ===
st.markdown("""
<div class="page-header">
    <h1 class="page-title">🌊 Deteksi Zona Ikan Real-Time</h1>
    <p class="page-subtitle">Visualisasi peta interaktif zona potensi ikan dan area berbahaya</p>
</div>
""", unsafe_allow_html=True)

# === LOAD CSV WITH UPDATED PATH ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
csv_path = os.path.join(PROJECT_ROOT, "csv", "fish_potential.csv")

try:
    df = pd.read_csv(csv_path)
    st.success(f"✅ Data berhasil dimuat dari fish_potential.csv")
except FileNotFoundError:
    st.error(f"❌ File tidak ditemukan: {csv_path}")
    st.info(f"💡 Pastikan file CSV ada di folder `streamlit/csv/`")
    st.stop()
except Exception as e:
    st.error(f"❌ Error: {str(e)}")
    st.stop()

# Validasi kolom wajib
required_cols = {"lat", "lon", "skor", "ikan"}
if not required_cols.issubset(df.columns):
    st.error(f"CSV harus mengandung kolom: {required_cols}")
    st.stop()

# Tambahkan alasan
def alasan_potensi(row):
    if "Zona Bahaya" in row['ikan']:
        return "Lokasi berbahaya karena kondisi cuaca/gelombang."
    elif row['skor'] > 0.9:
        return "Sangat potensial: kondisi optimal."
    elif row['skor'] > 0.75:
        return "Potensial tinggi: parameter mendukung."
    elif row['skor'] > 0.5:
        return "Potensial sedang."
    else:
        return "Potensial rendah."

df['alasan'] = df.apply(alasan_potensi, axis=1)
df_filtered = df[df['skor'] > 0.4].copy()

# === SIDEBAR CONTROLS ===
st.sidebar.markdown("### 🔍 Kontrol Navigasi")

basemap_option = st.sidebar.selectbox(
    "Pilih Basemap",
    ["OpenStreetMap", "Esri Satellite"]
)

# === GPS DETECTION WITH AUTO-REFRESH ===
st.sidebar.markdown("---")
st.sidebar.markdown("### 🛰️ Kontrol GPS")

use_auto_gps = st.sidebar.checkbox(
    "Gunakan GPS Otomatis", 
    value=st.session_state.use_gps,
    help="Aktifkan untuk tracking posisi real-time dengan auto-refresh setiap 10 detik"
)
st.session_state.use_gps = use_auto_gps

# Ambil koordinat GPS
if use_auto_gps:
    loc = get_geolocation()
    if loc is not None and "coords" in loc:
        st.session_state.gps_lat = loc["coords"]["latitude"]
        st.session_state.gps_lon = loc["coords"]["longitude"]
        default_start_lat = st.session_state.gps_lat
        default_start_lon = st.session_state.gps_lon
        st.sidebar.success("📍 GPS terdeteksi dan aktif!")
        
        # Tampilkan countdown untuk refresh berikutnya
        elapsed = time.time() - st.session_state.last_refresh
        remaining = max(0, 10 - int(elapsed))
        st.sidebar.info(f"🔄 Refresh berikutnya dalam: {remaining} detik")
        
    else:
        if st.session_state.gps_lat is not None:
            default_start_lat = st.session_state.gps_lat
            default_start_lon = st.session_state.gps_lon
        else:
            default_start_lat = df_filtered.lat.mean()
            default_start_lon = df_filtered.lon.mean()
        st.sidebar.warning("⚠️ Menunggu sinyal GPS...")
else:
    if st.session_state.gps_lat is not None:
        default_start_lat = st.session_state.gps_lat
        default_start_lon = st.session_state.gps_lon
    else:
        default_start_lat = df_filtered.lat.mean()
        default_start_lon = df_filtered.lon.mean()
    st.sidebar.info("ℹ️ Mode manual - GPS dinonaktifkan")

st.sidebar.markdown("---")
st.sidebar.markdown("#### 📍 Posisi Awal")

start_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(default_start_lat), 
    format="%.6f",
    key="start_lat",
    disabled=use_auto_gps,
    help="Koordinat latitude posisi awal (otomatis dari GPS atau input manual)"
)
start_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(default_start_lon), 
    format="%.6f",
    key="start_lon",
    disabled=use_auto_gps,
    help="Koordinat longitude posisi awal (otomatis dari GPS atau input manual)"
)

# Update session state jika manual
if not use_auto_gps:
    st.session_state.gps_lat = start_lat
    st.session_state.gps_lon = start_lon

st.sidebar.markdown("#### 🎯 Tujuan")
end_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(df_filtered.lat.mean()), 
    format="%.6f",
    key="end_lat",
    help="Koordinat latitude tujuan"
)
end_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(df_filtered.lon.mean()), 
    format="%.6f",
    key="end_lon",
    help="Koordinat longitude tujuan"
)

if st.sidebar.button("🔄 Refresh Manual"):
    st.session_state.last_refresh = time.time()
    st.rerun()

# === MAIN MAP SECTION ===
st.markdown('<h2 class="section-header">🗺️ Peta Interaktif</h2>', unsafe_allow_html=True)

# === KONTROL LAYER (RESPONSIVE) ===
with st.expander("🎛️ Kontrol Layer", expanded=True):
    col_heat, col_marker = st.columns(2)
    
    with col_heat:
        st.markdown("**🔥 Heatmap**")
        ikan_types = df_filtered['ikan'].unique()
        ikan_types_clean = [ikan for ikan in ikan_types if "Zona Bahaya" not in ikan]
        
        heatmap_toggles = {}
        for ikan in ikan_types_clean:
            heatmap_toggles[ikan] = st.checkbox(f"{ikan}", value=True, key=f"heat_{ikan}")
        
        show_bahaya_heatmap = st.checkbox("🌊 Zona Bahaya", value=True, key="heat_bahaya")
    
    with col_marker:
        st.markdown("**📍 Marker**")
        show_ikan_markers = st.checkbox("Marker Ikan", value=True, key="marker_ikan")
        show_bahaya_markers = st.checkbox("Marker Bahaya", value=True, key="marker_bahaya")
        show_route = st.checkbox("Rute Navigasi", value=True, key="show_route")
        
        marker_ikan_toggles = {}
        if show_ikan_markers:
            for ikan in ikan_types_clean:
                marker_ikan_toggles[ikan] = st.checkbox(f"• {ikan}", value=True, key=f"marker_{ikan}")

st.markdown("---")

# === GENERATE MAP ===
if basemap_option == "Esri Satellite":
    tiles_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri"
else:
    tiles_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attr = "&copy; OpenStreetMap contributors"

map_center = [(start_lat + end_lat) / 2, (start_lon + end_lon) / 2]
m = folium.Map(location=map_center, zoom_start=8, tiles=tiles_url, attr=attr)

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

# Rute
if show_route:
    folium.Marker([start_lat, start_lon], popup="📍 Awal", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker([end_lat, end_lon], popup="🎯 Tujuan", icon=folium.Icon(color="blue", icon="flag")).add_to(m)
    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        color="cyan",
        weight=4,
        opacity=0.8,
        dash_array="10"
    ).add_to(m)

# === MARKER GPS AKTIF ===
if use_auto_gps and st.session_state.gps_lat is not None:
    folium.Marker(
        [start_lat, start_lon],
        popup="🧭 Posisi Anda Saat Ini (GPS Live)",
        icon=folium.Icon(color="darkgreen", icon="user", prefix='fa'),
        tooltip="Lokasi GPS Real-Time"
    ).add_to(m)
    
    # Circle untuk radius akurasi
    folium.Circle(
        location=[start_lat, start_lon],
        radius=50,
        color='green',
        fill=True,
        fillColor='green',
        fillOpacity=0.2,
        popup="Radius akurasi GPS (~50m)"
    ).add_to(m)

# Tampilkan peta dengan ukuran responsif
st_data = st_folium(m, width=None, height=500, returned_objects=[])

# === INFO PANEL (RESPONSIVE) ===
st.markdown("---")

with st.expander("ℹ️ Informasi Navigasi", expanded=False):
    distance_km = ((end_lat-start_lat)**2 + (end_lon-start_lon)**2)**0.5 * 111
    
    col1, col2 = st.columns(2)
    with col1:
        gps_status = "🟢 GPS Aktif" if use_auto_gps else "🔴 Manual"
        st.markdown(f"""
        **📍 Koordinat**
        - Status: {gps_status}
        - Posisi: {start_lat:.6f}, {start_lon:.6f}
        - Tujuan: {end_lat:.6f}, {end_lon:.6f}
        """)
    
    with col2:
        st.markdown(f"""
        **📊 Layer Aktif**
        - Heatmap: {sum([1 for v in heatmap_toggles.values() if v]) + (1 if show_bahaya_heatmap else 0)}
        - Marker: {(sum([1 for v in marker_ikan_toggles.values() if v]) if show_ikan_markers else 0) + (1 if show_bahaya_markers else 0)}
        """)
    
    st.info(f"**Jarak Estimasi:** ≈ {distance_km:.1f} km")

# === DATA SUMMARY (RESPONSIVE GRID) ===
st.markdown("---")
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
    st.metric("Avg Skor", f"{avg_score:.3f}")

# === PANDUAN ===
st.markdown("---")
with st.expander("📖 Panduan Penggunaan"):
    st.markdown("""
    ### Cara Menggunakan:
    
    **1. GPS Otomatis (Recommended)**
    - Centang "Gunakan GPS Otomatis" di sidebar
    - Izinkan akses lokasi saat browser meminta
    - Posisi akan diupdate otomatis setiap 10 detik
    - Marker hijau tua dengan ikon user menunjukkan posisi real-time Anda
    
    **2. Mode Manual**
    - Nonaktifkan GPS otomatis
    - Input koordinat secara manual di sidebar
    - Klik "Refresh Manual" untuk update peta
    
    **3. Kontrol Layer**
    - Toggle checkbox untuk show/hide layer tertentu
    - Heatmap menampilkan gradasi intensitas potensi
    - Marker biru = lokasi ikan
    - Marker merah = zona bahaya
    
    **4. Interpretasi Warna Heatmap:**
    - Biru = Rendah | Hijau = Sedang | Oranye = Tinggi | Merah = Sangat Tinggi
    
    **5. Navigasi**
    - Garis cyan = rute estimasi
    - Marker hijau = posisi awal
    - Marker biru = tujuan
    - Marker hijau tua + circle = GPS aktif
    
    **6. Basemap**
    - OpenStreetMap (standar) = Detail jalan dan topografi
    - Esri Satellite = Citra satelit real
    """)

# === AUTO-REFRESH GPS (10 DETIK) ===
if use_auto_gps:
    elapsed = time.time() - st.session_state.last_refresh
    if elapsed >= 10:
        st.session_state.last_refresh = time.time()
        time.sleep(0.1)  # Small delay untuk stabilitas
        st.rerun()
