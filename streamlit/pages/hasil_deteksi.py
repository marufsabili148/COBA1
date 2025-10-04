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

# === CUSTOM CSS - COPERNICUS STYLE ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Page Header */
    .page-header {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem 0 1.5rem 0;
        margin: -2rem -6rem 2rem -6rem;
        border-bottom: 1px solid #e1e4e8;
        text-align: center;
    }
    
    .page-title {
        font-size: 2.5rem;
        font-weight: 600;
        color: #0e4194;
        margin-bottom: 0.5rem;
    }
    
    .page-subtitle {
        font-size: 1.1rem;
        color: #586069;
        font-weight: 400;
    }
    
    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: 0.5rem 1.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #0a3275;
        box-shadow: 0 4px 8px rgba(14, 65, 148, 0.2);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #24292e;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0e4194;
    }
    
    /* Info Boxes */
    .info-box {
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: #0e4194;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #586069;
        font-weight: 500;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f6f8fa;
        border-radius: 4px;
        font-weight: 500;
        color: #24292e;
    }
    
    /* Checkbox */
    .stCheckbox {
        padding: 0.25rem 0;
    }
    
    /* Number Input */
    .stNumberInput > div > div > input {
        border-radius: 4px;
        border: 1px solid #e1e4e8;
    }
    
    /* Select Box */
    .stSelectbox > div > div > select {
        border-radius: 4px;
        border: 1px solid #e1e4e8;
    }
    
    /* Control Cards */
    .control-card {
        background: white;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .control-card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #24292e;
        margin-bottom: 1rem;
    }
    
    /* Stats Grid */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #24292e;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Headers */
    .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
        color: #0e4194;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    
    /* Text styling */
    p, span, div, label {
        font-family: 'Inter', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Deteksi Zona Ikan'

# === NAVIGATION ===
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang"],
    icons=["house", "map", "graph-up", "book", "info-circle"],
    menu_icon="cast",
    default_index=1,
    orientation="horizontal",
    styles={
        "container": {"padding": "0", "background-color": "#ffffff", "border-bottom": "1px solid #e1e4e8"},
        "icon": {"color": "#586069", "font-size": "16px"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "center",
            "margin": "0",
            "padding": "14px 24px",
            "color": "#24292e",
            "font-weight": "500",
            "border-bottom": "3px solid transparent",
            "--hover-color": "#f6f8fa",
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
    st.switch_page("Beranda.py")
elif selected == "Tentang":
    st.switch_page("Beranda.py")

# === PAGE HEADER ===
st.markdown("""
<div class="page-header">
    <h1 class="page-title">🌊 Deteksi Zona Ikan Real-Time</h1>
    <p class="page-subtitle">Visualisasi peta interaktif zona potensi ikan dan area berbahaya</p>
</div>
""", unsafe_allow_html=True)

# === BACA CSV ===
# Lokasi file hasil_deteksi.py
BASE_DIR = os.path.dirname(__file__)

# Naik 2 folder ke root project
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))

# Path CSV
csv_path = os.path.join(PROJECT_DIR, "csv", "fish_potential.csv")

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
st.markdown('<h3 class="section-header" style="font-size: 1.25rem; margin-top: 1rem;">🎛️ Kontrol Layer</h3>', unsafe_allow_html=True)

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