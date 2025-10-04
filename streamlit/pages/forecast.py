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

# === CUSTOM CSS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .block-container {
        padding-top: 1rem;
        max-width: 100%;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    .main .block-container {
        max-width: 100%;
    }
    
    .week-selector {
        background-color: #f0f8ff;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #0e4194;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: 600;
        color: #24292e;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0e4194;
    }
    
    .info-box {
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 4px;
    }
    
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: #0a3275;
        box-shadow: 0 4px 8px rgba(14, 65, 148, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# === SESSION STATE ===
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Prediksi 30 Hari'

# === NAVIGATION MENU (FIXED) ===
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang"],
    icons=["house", "map", "graph-up", "book", "info-circle"],
    menu_icon="cast",
    default_index=2,  # Index 2 = Prediksi 30 Hari
    orientation="horizontal",
    key="main_menu",  # Tambahkan key unik
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

# FIXED: Handle navigation dengan benar untuk semua halaman
if selected != st.session_state.current_page:
    st.session_state.current_page = selected
    
    if selected == "Beranda":
        st.switch_page("home.py")
    elif selected == "Deteksi Zona Ikan":
        st.switch_page("pages/hasil_deteksi.py")
    elif selected == "Tutorial":
        st.switch_page("pages/tutorial.py")  # Jika ada
    elif selected == "Tentang":
        st.switch_page("pages/tentang.py")  # Jika ada
    # Untuk "Prediksi 30 Hari" tidak perlu switch karena sudah di halaman ini

# === JUDUL HALAMAN ===
st.title("🌊 Peta Potensi Ikan & Zona Bahaya - Prediksi Mingguan")

# === PILIH BULAN DAN MINGGU ===
current_date = datetime.now()
current_month = current_date.month
current_year = current_date.year

st.markdown('<div class="week-selector">', unsafe_allow_html=True)
col_month, col_week = st.columns([2, 3])

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
        "📊 Pilih Minggu Prediksi",
        options=[1, 2, 3, 4],
        format_func=lambda x: f"Minggu ke-{x} ({calendar.month_name[selected_month]})",
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

st.info(f"📈 **Prediksi untuk:** {week_dates[selected_week-1]} | **Dataset:** fish_potential_variant_{selected_week}.csv")

# === LOAD DATA ===
try:
    csv_path = csv_files[selected_week]
    df = pd.read_csv(csv_path)
    st.success(f"✅ Data berhasil dimuat dari variant_{selected_week}.csv")
except FileNotFoundError:
    st.error(f"❌ File tidak ditemukan: {csv_path}")
    st.info(f"💡 **Pastikan struktur folder benar:**\n\n"
            f"Lokasi yang dicari: `{csv_path}`\n\n"
            f"Silakan buat folder `data` di direktori yang sama dengan script ini, "
            f"kemudian letakkan file CSV di dalamnya.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error membaca file: {str(e)}")
    st.stop()

# Validasi kolom
required_cols = {"lat", "lon", "skor", "ikan"}
if not required_cols.issubset(df.columns):
    st.error(f"CSV harus mengandung kolom: {required_cols}")
    st.stop()

# Fungsi alasan potensi
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
df_filtered = df[df['skor'] > 0.4].copy()

# === SIDEBAR CONTROLS ===
st.sidebar.header("🔍 Navigasi Laut")

basemap_option = st.sidebar.selectbox(
    "Pilih Basemap",
    ["OpenStreetMap", "Esri Satellite"],
    help="Pilih jenis peta dasar yang ingin digunakan"
)

# GPS Detection
loc = get_geolocation()
if loc is not None and "coords" in loc:
    default_start_lat = loc["coords"]["latitude"]
    default_start_lon = loc["coords"]["longitude"]
    st.sidebar.success("📍 GPS berhasil dideteksi!")
else:
    default_start_lat = df_filtered.lat.mean()
    default_start_lon = df_filtered.lon.mean()
    st.sidebar.warning("⚠️ GPS tidak terdeteksi, menggunakan koordinat default")

# Input koordinat
st.sidebar.subheader("📍 Koordinat Posisi Awal")
start_lat = st.sidebar.number_input(
    "Latitude Awal", 
    value=float(default_start_lat), 
    format="%.6f",
    help="Koordinat latitude posisi Anda saat ini"
)
start_lon = st.sidebar.number_input(
    "Longitude Awal", 
    value=float(default_start_lon), 
    format="%.6f",
    help="Koordinat longitude posisi Anda saat ini"
)

st.sidebar.subheader("🎯 Koordinat Tujuan")
end_lat = st.sidebar.number_input(
    "Latitude Tujuan", 
    value=float(df_filtered.lat.mean()), 
    format="%.6f",
    help="Koordinat latitude tempat tujuan"
)
end_lon = st.sidebar.number_input(
    "Longitude Tujuan", 
    value=float(df_filtered.lon.mean()), 
    format="%.6f",
    help="Koordinat longitude tempat tujuan"
)

if st.sidebar.button("🔄 Refresh GPS"):
    st.rerun()

# === KONTROL LAYER ===
st.markdown('<h2 class="section-header">🗺️ Peta Interaktif</h2>', unsafe_allow_html=True)
st.subheader("🎛️ Kontrol Layer")

col1, col2, col3 = st.columns(3)

# Heatmap controls
with col1:
    st.markdown("**🔥 Heatmap**")
    ikan_types = df_filtered['ikan'].unique()
    ikan_types_clean = [ikan for ikan in ikan_types if "Zona Bahaya" not in ikan]
    
    heatmap_toggles = {}
    for ikan in ikan_types_clean:
        heatmap_toggles[ikan] = st.checkbox(f"{ikan}", value=True, key=f"heat_{ikan}_{selected_week}")
    
    show_bahaya_heatmap = st.checkbox("🌊 Zona Bahaya", value=True, key=f"heat_bahaya_{selected_week}")

# Marker ikan controls
with col2:
    st.markdown("**📍 Marker Ikan**")
    show_ikan_markers = st.checkbox("Tampilkan Marker Ikan", value=False, key=f"marker_ikan_{selected_week}")
    
    marker_ikan_toggles = {}
    if show_ikan_markers:
        for ikan in ikan_types_clean:
            marker_ikan_toggles[ikan] = st.checkbox(f"• {ikan}", value=True, key=f"marker_{ikan}_{selected_week}")

# Marker bahaya dan rute
with col3:
    st.markdown("**🚫 Marker Bahaya**")
    show_bahaya_markers = st.checkbox("Tampilkan Marker Bahaya", value=False, key=f"marker_bahaya_{selected_week}")
    
    st.markdown("**🧭 Rute**")
    show_route = st.checkbox("Tampilkan Rute", value=True, key=f"show_route_{selected_week}")

# === GENERATE MAP ===
if basemap_option == "Esri Satellite":
    tiles_url = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    attr = "Tiles &copy; Esri"
else:
    tiles_url = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    attr = "&copy; OpenStreetMap contributors"

map_center = [(start_lat + end_lat) / 2, (start_lon + end_lon) / 2]
m = folium.Map(location=map_center, zoom_start=8, tiles=None)

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
                <b>Periode:</b> {week_dates[selected_week-1]}<br>
                <b>Jenis Ikan:</b> {row['ikan']}<br>
                <b>Latitude:</b> {row['lat']:.4f}<br>
                <b>Longitude:</b> {row['lon']:.4f}<br>
                <b>Skor Potensi:</b> {row['skor']:.4f}<br>
                <b>Alasan:</b> {row['alasan']}
                """
                folium.Marker(
                    location=[row['lat'], row['lon']],
                    popup=folium.Popup(popup_html, max_width=320),
                    icon=folium.Icon(color="blue", icon="info-sign")
                ).add_to(m)

# Marker bahaya
if show_bahaya_markers:
    bahaya_df = df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)]
    for _, row in bahaya_df.iterrows():
        popup_html = f"""
        <b>Periode:</b> {week_dates[selected_week-1]}<br>
        <b>Jenis:</b> {row['ikan']}<br>
        <b>Latitude:</b> {row['lat']:.4f}<br>
        <b>Longitude:</b> {row['lon']:.4f}<br>
        <b>Skor:</b> {row['skor']:.4f}<br>
        <b>Keterangan:</b> {row['alasan']}
        """
        folium.Marker(
            location=[row['lat'], row['lon']],
            popup=folium.Popup(popup_html, max_width=320),
            icon=folium.Icon(color="red", icon="warning-sign")
        ).add_to(m)

# Rute
if show_route:
    folium.Marker([start_lat, start_lon], popup="📍 Titik Awal", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker([end_lat, end_lon], popup="🎯 Titik Tujuan", icon=folium.Icon(color="blue", icon="flag")).add_to(m)
    folium.PolyLine(
        locations=[[start_lat, start_lon], [end_lat, end_lon]],
        color="cyan",
        weight=4,
        opacity=0.8,
        dash_array="10"
    ).add_to(m)

# Tampilkan peta
st_data = st_folium(m, width=1200, height=600, key=f"map_{selected_month}_{selected_week}")

# === INFO PANEL ===
st.markdown("---")
col_info1, col_info2 = st.columns(2)

with col_info1:
    st.subheader("ℹ️ Informasi Koordinat")
    distance_km = ((end_lat-start_lat)**2 + (end_lon-start_lon)**2)**0.5 * 111
    st.info(f"""
    **Periode Prediksi:** {week_dates[selected_week-1]}
    
    **Dataset:** fish_potential_variant_{selected_week}.csv
    
    **Basemap:** {basemap_option}
    
    **Posisi Awal:** {start_lat:.6f}, {start_lon:.6f}
    
    **Tujuan:** {end_lat:.6f}, {end_lon:.6f}
    
    **Jarak Estimasi:** ≈ {distance_km:.1f} km
    """)

with col_info2:
    st.subheader("📊 Status Layer Aktif")
    
    active_heatmaps = sum([1 for v in heatmap_toggles.values() if v]) + (1 if show_bahaya_heatmap else 0)
    active_markers_ikan = sum([1 for v in marker_ikan_toggles.values() if v]) if show_ikan_markers else 0
    active_markers_bahaya = 1 if show_bahaya_markers else 0
    
    st.metric("🔥 Heatmap Aktif", active_heatmaps)
    st.metric("📍 Marker Ikan Aktif", active_markers_ikan)
    st.metric("🚫 Marker Bahaya Aktif", active_markers_bahaya)
    st.metric("🧭 Rute", "Aktif" if show_route else "Nonaktif")

# === PERBANDINGAN MINGGU ===
st.markdown('<h2 class="section-header">📊 Perbandingan Prediksi Mingguan</h2>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([f"📅 Minggu ke-{i}" for i in range(1, 5)])

tabs = [tab1, tab2, tab3, tab4]
for i, tab in enumerate(tabs, 1):
    with tab:
        try:
            df_week = pd.read_csv(csv_files[i])
            if required_cols.issubset(df_week.columns):
                df_week_filtered = df_week[df_week['skor'] > 0.4]
                
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                with col_stat1:
                    st.metric("Total Titik Data", len(df_week_filtered))
                with col_stat2:
                    total_ikan = len(df_week_filtered[~df_week_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
                    st.metric("Titik Potensi Ikan", total_ikan)
                with col_stat3:
                    avg_score = df_week_filtered['skor'].mean()
                    st.metric("Rata-rata Skor", f"{avg_score:.3f}")
                
                if i == selected_week:
                    st.success(f"✅ Sedang menampilkan minggu ke-{i}")
            else:
                st.error(f"❌ File minggu ke-{i} tidak memiliki kolom yang sesuai")
                
        except FileNotFoundError:
            st.error(f"❌ File variant_{i}.csv tidak ditemukan")
        except Exception as e:
            st.error(f"❌ Error membaca file minggu ke-{i}: {str(e)}")

# === DATA SUMMARY ===
st.markdown('<h2 class="section-header">📈 Ringkasan Data</h2>', unsafe_allow_html=True)

col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.metric("Total Titik Data", len(df_filtered))

with col_stat2:
    total_ikan = len(df_filtered[~df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
    st.metric("Titik Potensi Ikan", total_ikan)

with col_stat3:
    total_bahaya = len(df_filtered[df_filtered['ikan'].str.contains("Zona Bahaya", case=False, na=False)])
    st.metric("Zona Bahaya", total_bahaya)

with col_stat4:
    avg_score = df_filtered['skor'].mean()
    st.metric("Rata-rata Skor", f"{avg_score:.3f}")

# === PANDUAN ===
with st.expander("📖 Panduan Penggunaan"):
    st.markdown("""
    ### Cara Menggunakan Aplikasi:
    
    **1. Pemilihan Periode:**
    - Pilih bulan dan minggu yang ingin dilihat
    - Sistem akan memuat data dari CSV yang sesuai
    
    **2. Navigasi:**
    - Gunakan menu di atas untuk berpindah halaman
    - Input koordinat awal dan tujuan di sidebar
    - Klik "Refresh GPS" untuk update lokasi
    
    **3. Kontrol Layer:**
    - Default: Heatmap aktif, marker nonaktif
    - Toggle checkbox untuk mengaktifkan/menonaktifkan layer
    - Setiap jenis ikan dapat dikontrol terpisah
    
    **4. Interpretasi:**
    - Heatmap: Biru (rendah) → Merah (tinggi)
    - Marker Biru: Potensi ikan
    - Marker Merah: Zona bahaya
    - Garis Cyan: Rute navigasi
    
    **5. Struktur Folder:**
    - Pastikan file CSV berada di folder `data/` 
    - Struktur: `project_root/data/fish_potential_variant_X.csv`
    """)

