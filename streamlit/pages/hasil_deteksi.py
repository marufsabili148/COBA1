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
        width: 100%;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        background-color: #0a3275;
        box-shadow: 0 4px 8px rgba(14, 65, 148, 0.2);
    }
    
    /* Section Headers - Responsive */
    .section-header {
        font-size: clamp(1.3rem, 3.5vw, 1.5rem) !important;
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
    .stCheckbox {
        padding: 0.25rem 0;
    }
    
    .stCheckbox label {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #24292e;
        font-family: 'Inter', sans-serif !important;
    }
    
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Sidebar Headers */
    .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
        color: #0e4194;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(1rem, 2.5vw, 1.2rem) !important;
    }
    
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .page-header {
            margin: -0.5rem -0.5rem 1.5rem -0.5rem;
            padding: 1.5rem 1rem;
        }
        
        .control-card {
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Deteksi Zona Ikan'

# === NAVIGATION (CONSISTENT WITH HOME.PY) ===
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
            "background-color": "transparent", 
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
df = pd.read_csv(csv_path)

# Validasi kolom wajib
required_cols = {"lat", "lon", "skor", "ikan"}
if not required_cols.issubset(df.columns):
    st.error(f"CSV harus mengandung kolom: {required_cols}")
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

# Ambil GPS live user
loc = get_geolocation()
if loc is not None and "coords" in loc:
    default_start_lat = loc["coords"]["latitude"]
    default_start_lon = loc["coords"]["longitude"]
    st.sidebar.success("📍 GPS berhasil terdeteksi!")
else:
    default_start_lat = df_filtered.lat.mean()
    default_start_lon = df_filtered.lon.mean()
    st.sidebar.warning("⚠️ GPS tidak terdeteksi, menggunakan koordinat default")

# Input koordinat manual
st.sidebar.markdown("#### 📍 Posisi Awal")
start_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(default_start_lat), 
    format="%.6f",
    help="Koordinat latitude posisi Anda saat ini",
    key="start_lat"
)
start_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(default_start_lon), 
    format="%.6f",
    help="Koordinat longitude posisi Anda saat ini",
    key="start_lon"
)

st.sidebar.markdown("#### 🎯 Tujuan")
end_lat = st.sidebar.number_input(
    "Latitude", 
    value=float(df_filtered.lat.mean()), 
    format="%.6f",
    help="Koordinat latitude tujuan",
    key="end_lat"
)
end_lon = st.sidebar.number_input(
    "Longitude", 
    value=float(df_filtered.lon.mean()), 
    format="%.6f",
    help="Koordinat longitude tujuan",
    key="end_lon"
)

if st.sidebar.button("🔄 Refresh GPS"):
    st.rerun()

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
    
    heatmap_toggles = {}
    for ikan in ikan_types_clean:
        heatmap_toggles[ikan] = st.checkbox(f"{ikan}", value=True, key=f"heat_{ikan}")
    
    # Toggle untuk heatmap zona bahaya
    show_bahaya_heatmap = st.checkbox("🌊 Zona Bahaya", value=True, key="heat_bahaya")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-card-title">📍 Marker Ikan</div>', unsafe_allow_html=True)
    
    show_ikan_markers = st.checkbox("Tampilkan Marker Ikan", value=True, key="marker_ikan")
    
    # Detail marker per jenis ikan
    marker_ikan_toggles = {}
    if show_ikan_markers:
        for ikan in ikan_types_clean:
            marker_ikan_toggles[ikan] = st.checkbox(f"• {ikan}", value=True, key=f"marker_{ikan}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-card-title">🚫 Bahaya & Rute</div>', unsafe_allow_html=True)
    
    show_bahaya_markers = st.checkbox("Tampilkan Marker Bahaya", value=True, key="marker_bahaya")
    show_route = st.checkbox("Tampilkan Rute Navigasi", value=True, key="show_route")
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# === GENERATE MAP ===
# Set basemap
if basemap_option == "Esri Satellite":
    tiles_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community"
else:
    tiles_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attr = "&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> contributors"

# Inisialisasi peta
map_center = [(start_lat + end_lat) / 2, (start_lon + end_lon) / 2]
m = folium.Map(location=map_center, zoom_start=8, tiles=tiles_url, attr=attr)

# === HeatMap per jenis ikan ===
for ikan in ikan_types_clean:
    if heatmap_toggles[ikan]:
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

# === Gambar garis rute ===
if show_route:
    folium.Marker([start_lat, start_lon], popup="📍 Titik Awal (Posisi Anda)", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker([end_lat, end_lon], popup="🎯 Titik Tujuan", icon=folium.Icon(color="blue", icon="flag")).add_to(m)
    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        color="cyan",
        weight=4,
        opacity=0.8,
        dash_array="10"
    ).add_to(m)

# Tampilkan peta
st_data = st_folium(m, width=1200, height=600, returned_objects=["all_drawings"])

# === INFO PANEL ===
st.markdown("---")
st.markdown('<h2 class="section-header">ℹ️ Informasi Navigasi</h2>', unsafe_allow_html=True)

col_info1, col_info2 = st.columns(2)

with col_info1:
    st.markdown("""
    <div class="info-box">
        <h4 style="margin-top: 0; color: #0e4194;">📍 Koordinat</h4>
        <p style="margin: 0.5rem 0;"><strong>Posisi Awal:</strong> {:.6f}, {:.6f}</p>
        <p style="margin: 0.5rem 0;"><strong>Tujuan:</strong> {:.6f}, {:.6f}</p>
        <p style="margin: 0.5rem 0;"><strong>Jarak Estimasi:</strong> ≈ {:.1f} km</p>
    </div>
    """.format(start_lat, start_lon, end_lat, end_lon, 
               ((end_lat-start_lat)**2 + (end_lon-start_lon)**2)**0.5 * 111), 
    unsafe_allow_html=True)

with col_info2:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown('<h4 style="margin-top: 0; color: #0e4194;">📊 Statistik Layer Aktif</h4>', unsafe_allow_html=True)
    
    # Hitung layer yang aktif
    active_heatmaps = sum([1 for v in heatmap_toggles.values() if v]) + (1 if show_bahaya_heatmap else 0)
    active_markers_ikan = sum([1 for v in marker_ikan_toggles.values() if v]) if show_ikan_markers else 0
    active_markers_bahaya = 1 if show_bahaya_markers else 0
    
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
