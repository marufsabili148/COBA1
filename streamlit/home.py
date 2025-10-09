import streamlit as st
from streamlit_option_menu import option_menu
import os
import base64


# === KONFIGURASI HALAMAN ===
st.set_page_config(
    page_title="SAILOR - Satellite-based AI Fish Detection",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Explicitly set current page for consistent menu indicator
st.session_state.current_page = 'Beranda'

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
    
    /* Navigation Bar - Responsive */
    .stApp > header {
        background-color: transparent;
    }
    
    /* Hero Section - Responsive */
    .hero-container {
        background: none;
        padding: clamp(2rem, 5vw, 4rem) clamp(1rem, 3vw, 2rem) clamp(1.5rem, 4vw, 3rem);
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 1px solid #e1e4e8;
    }
    
    .hero-content {
        max-width: 900px;
        margin: 0 auto;
        text-align: center;
        padding: 0 1rem;
    }
    
    .hero-title {
        font-size: clamp(2rem, 6vw, 3rem) !important;
        font-weight: 600 !important;
        color: #0e4194;
        margin-bottom: 1rem;
        line-height: 1.2;
        font-family: 'Inter', sans-serif !important;
    }
    
    .hero-subtitle {
        font-size: clamp(1rem, 3vw, 1.25rem) !important;
        color: #586069;
        font-weight: 400;
        line-height: 1.6;
        margin-bottom: 1.5rem;
        font-family: 'Inter', sans-serif !important;
    }
    
    .hero-description {
        color: #586069;
        font-size: clamp(0.9rem, 2.5vw, 1.05rem) !important;
        line-height: 1.7;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Buttons - Responsive */
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: clamp(0.6rem, 2vw, 0.75rem) clamp(1.5rem, 3vw, 2rem);
        font-size: clamp(0.9rem, 2vw, 1rem) !important;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.2s ease;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton > button:hover {
        background-color: #0a3275;
        box-shadow: 0 4px 8px rgba(14, 65, 148, 0.2);
    }
    
    /* Feature Grid - Responsive */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
        gap: clamp(1rem, 3vw, 2rem);
        margin: clamp(1.5rem, 3vw, 3rem) 0;
    }
    
    .feature-box {
        background: white;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: clamp(1.25rem, 3vw, 2rem);
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }
    
    .feature-icon {
        font-size: clamp(2rem, 5vw, 2.5rem);
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-heading {
        font-size: clamp(1.05rem, 2.5vw, 1.25rem) !important;
        font-weight: 600 !important;
        color: #24292e;
        margin-bottom: 0.75rem;
        font-family: 'Inter', sans-serif !important;
    }
    
    .feature-text {
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        color: #586069;
        line-height: 1.6;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Stats Section - Responsive */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));
        gap: clamp(1rem, 3vw, 2rem);
        margin: clamp(1.5rem, 3vw, 3rem) 0;
    }
    
    .stat-card {
        background: white;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: clamp(1.25rem, 3vw, 2rem);
        text-align: center;
    }
    
    .stat-number {
        font-size: clamp(1.8rem, 5vw, 2.5rem) !important;
        font-weight: 700 !important;
        color: #0e4194;
        display: block;
        margin-bottom: 0.5rem;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stat-label {
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
        color: #586069;
        font-weight: 400;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Section Headers - Responsive */
    .section-header {
        font-size: clamp(1.5rem, 4vw, 2rem) !important;
        font-weight: 600 !important;
        color: #24292e;
        margin: clamp(2rem, 4vw, 3rem) 0 clamp(1rem, 2vw, 1.5rem) 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0e4194;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Info Boxes - Responsive */
    .info-box {
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        margin: clamp(1rem, 2vw, 1.5rem) 0;
        border-radius: 4px;
    }
    
    .info-box-title {
        font-weight: 600 !important;
        color: #24292e;
        margin-bottom: 0.5rem;
        font-size: clamp(0.95rem, 2vw, 1.1rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .info-box-content {
        color: #586069;
        line-height: 1.6;
        font-size: clamp(0.85rem, 2vw, 0.95rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Links Section - Responsive */
    .links-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 250px), 1fr));
        gap: clamp(1rem, 2vw, 1.5rem);
        margin: clamp(1.5rem, 3vw, 2rem) 0;
    }
    
    .link-card {
        background: white;
        border: 1px solid #e1e4e8;
        border-radius: 8px;
        padding: clamp(1rem, 2.5vw, 1.5rem);
        transition: all 0.2s ease;
    }
    
    .link-card:hover {
        border-color: #0e4194;
        box-shadow: 0 4px 12px rgba(14, 65, 148, 0.1);
    }
    
    .link-title {
        font-weight: 600 !important;
        color: #0e4194;
        margin-bottom: 0.5rem;
        font-size: clamp(0.95rem, 2.5vw, 1.1rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Footer - Responsive */
    .footer-container {
        background: #24292e;
        color: #ffffff;
        padding: clamp(2rem, 4vw, 3rem) clamp(1rem, 3vw, 2rem);
        margin: clamp(2rem, 4vw, 4rem) -1rem -2rem -1rem;
    }
    
    .footer-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));
        gap: clamp(1.5rem, 3vw, 2rem);
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .footer-heading {
        font-size: clamp(1rem, 2.5vw, 1.1rem) !important;
        font-weight: 600 !important;
        margin-bottom: 1rem;
        color: #ffffff;
        font-family: 'Inter', sans-serif !important;
    }
    
    .footer-text {
        color: #959da5;
        line-height: 1.6;
        font-size: clamp(0.8rem, 2vw, 0.9rem) !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .footer-link {
        color: #959da5;
        text-decoration: none;
        transition: color 0.2s;
        font-family: 'Inter', sans-serif !important;
    }
    
    .footer-link:hover {
        color: #ffffff;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: #f6f8fa;
        border-radius: 4px;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #24292e;
        font-family: 'Inter', sans-serif !important;
    }
    
    h1 {
        font-size: clamp(1.5rem, 4vw, 2.5rem) !important;
    }
    
    h2 {
        font-size: clamp(1.3rem, 3.5vw, 2rem) !important;
    }
    
    h3 {
        font-size: clamp(1.1rem, 3vw, 1.5rem) !important;
    }
    
    p, div, span, label, a {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Option Menu Responsive */
    .nav-link {
        font-family: 'Inter', sans-serif !important;
        font-size: clamp(0.8rem, 2vw, 0.95rem) !important;
    }
    
    /* Mobile Optimization */
    @media (max-width: 768px) {
        .hero-container {
            margin: -0.5rem -0.5rem 1.5rem -0.5rem;
            padding: 1.5rem 1rem;
        }
        
        .footer-container {
            margin: 2rem -0.5rem -1rem -0.5rem;
            padding: 2rem 1rem;
        }
        
        .feature-grid, .stats-container, .links-grid {
            gap: 1rem;
        }
    }
    
    /* Extra Small Devices */
    @media (max-width: 480px) {
        .hero-title {
            font-size: 1.8rem !important;
        }
        
        .hero-subtitle {
            font-size: 0.95rem !important;
        }
        
        .stat-number {
            font-size: 1.6rem !important;
        }
        
        .feature-icon {
            font-size: 1.8rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# === NAVIGATION - RESPONSIVE ===
selected = option_menu(
    menu_title=None,
    options=["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang", "Feedback"],
    icons=["house", "map", "graph-up", "book", "info-circle", "chat-dots"],
    menu_icon="cast",
    default_index=["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang"].index(st.session_state.current_page),
    orientation="horizontal",
    key="main_nav",
    styles={
        "container": {
            "padding": "0", 
            "background-color": "transparent", 
            "border-bottom": "1px solid #333333"
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

# Handle navigation to other pages
if selected == "Deteksi Zona Ikan":
    st.session_state.current_page = selected
    st.switch_page("pages/hasil_deteksi.py")
elif selected == "Prediksi 30 Hari":
    st.session_state.current_page = selected
    st.switch_page("pages/forecast.py")
elif selected == "Feedback":
    st.session_state.current_page = selected
    st.switch_page("pages/feedback.py")

st.session_state.current_page = selected

# === HALAMAN BERANDA ===
if selected == "Beranda":
    # Hero Section
    # Try to load the local image and embed it as a base64 data URI so it renders inside the hero HTML
    image_path = os.path.join(os.path.dirname(__file__), "img", "sailor.png")
    try:
        with open(image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        # Perbesar sedikit supaya lebih proporsional di layout
        img_tag = f'<img src="data:image/png;base64,{b64}" alt="SAILOR" style="max-width:360px; width:55%; height:auto; margin-bottom:1rem;" />'
    except Exception:
        # Fallback to text if the image can't be read
        img_tag = '<h1 class="hero-title">SAILOR</h1>'

    st.markdown(f"""
    <div class="hero-container">
        <div class="hero-content">
            {img_tag}
            <p class="hero-subtitle">Sumber Daya Optimasi Lokasi Cerdas Berbasis Satelit</p>
            <p class="hero-description">
                Sistem deteksi zona ikan yang memanfaatkan data satelit dan kecerdasan buatan
                untuk mengidentifikasi zona penangkapan ikan yang potensial di Laut Jawa
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # CTA Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Mulai Deteksi Zona Ikan", use_container_width=True):
            st.switch_page("pages/hasil_deteksi.py")
    
    # Stats Section
    st.markdown('<h2 class="section-header">Key Statistics</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="stats-container">
            <div class="stat-card">
                <span class="stat-number">12.01M</span>
                <span class="stat-label">Perkiraan Potensi Ikan (ton/tahun)</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">Real-Time</span>
                <span class="stat-label">Data Satelit Copernicus</span>
            </div>
            <div class="stat-card">
                <span class="stat-number">6 Jenis</span>
                <span class="stat-label">Jenis Ikan Pelagis Terdeteksi</span>
            </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<h2 class="section-header">Features</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-box">
            <span class="feature-icon">🗺</span>
            <div class="feature-heading">Interactive Mapping</div>
            <div class="feature-text">
                Real-time visualization of potential fishing zones using satellite-based oceanographic data
            </div>
        </div>
        
        <div class="feature-box">
            <span class="feature-icon">🤖</span>
            <div class="feature-heading">AI Prediction</div>
            <div class="feature-text">
                30-day forecasting using Random Forest machine learning with high accuracy (RMSE: 0.002816)
            </div>
        </div>
        
        <div class="feature-box">
            <span class="feature-icon">⚠</span>
            <div class="feature-heading">Hazard Detection</div>
            <div class="feature-text">
                Automatic identification of dangerous zones based on wave height and shallow water conditions
            </div>
        </div>
        
        <div class="feature-box">
            <span class="feature-icon">🧭</span>
            <div class="feature-heading">GPS Navigation</div>
            <div class="feature-text">
                Direct navigation guidance to selected potential fishing locations with real-time tracking
            </div>
        </div>
        
        <div class="feature-box">
            <span class="feature-icon">🐟</span>
            <div class="feature-heading">Multi-Species Support</div>
            <div class="feature-text">
                Detection for 6 pelagic species: Tongkol, Cakalang, Tenggiri, Teri, Shortfin Scad, Spotted Sardinella
            </div>
        </div>
        
        <div class="feature-box">
            <span class="feature-icon">🔄</span>
            <div class="feature-heading">Automatic Updates</div>
            <div class="feature-text">
                Hourly automated processing of new Copernicus satellite data without manual intervention
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Useful Links
    st.markdown('<h2 class="section-header">Related Resources</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="links-grid">
        <div class="link-card">
            <div class="link-title">Ministry of Marine Affairs and Fisheries</div>
            <div class="feature-text">Official fisheries data and regulations</div>
            <a href="https://kkp.go.id" target="_blank" class="footer-link">Visit Website →</a>
        </div>
        
        <div class="link-card">
            <div class="link-title">BMKG Maritime Weather</div>
            <div class="feature-text">Weather forecasts and maritime conditions</div>
            <a href="https://www.bmkg.go.id" target="_blank" class="footer-link">Visit Website →</a>
        </div>
        
        <div class="link-card">
            <div class="link-title">Copernicus Marine Service</div>
            <div class="feature-text">Source of oceanographic satellite data</div>
            <a href="https://marine.copernicus.eu" target="_blank" class="footer-link">Visit Website →</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-container">
        <div class="footer-grid">
            <div>
                <div class="footer-heading">About SAILOR</div>
                <p class="footer-text">
                    A fish detection information system based on AI and satellite data to help fishermen 
                    find potential fishing zones in the Java Sea.
                </p>
            </div>
            <div>
                <div class="footer-heading">Contact</div>
                <p class="footer-text">
                    Team Awikwok<br>
                    Universitas Diponegoro<br>
                    Email: sailor@undip.ac.id
                </p>
            </div>
            <div>
                <div class="footer-heading">Quick Links</div>
                <p class="footer-text">
                    <a href="#" class="footer-link">User Guide</a><br>
                    <a href="#" class="footer-link">Fisher's Manual</a><br>
                    <a href="#" class="footer-link">FAQ</a><br>
                    <a href="#" class="footer-link">API Documentation</a>
                </p>
            </div>
        </div>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 2rem 0;">
        <p style="text-align: center; color: #959da5; font-size: clamp(0.8rem, 2vw, 0.9rem); font-family: Inter, sans-serif;">
            © 2025 SAILOR - Team Awikwok | Universitas Diponegoro | GEMASTIK XVIII
        </p>
    </div>
    """, unsafe_allow_html=True)

# === HALAMAN TUTORIAL ===
elif selected == "Tutorial":
    st.markdown('<h1 class="section-header">Panduan Pengguna</h1>', unsafe_allow_html=True)
    st.markdown("Panduan singkat penggunaan sistem SAILOR untuk membantu Anda memulai.")
    
    with st.expander("1. Mengakses Halaman Deteksi Zona Ikan", expanded=True):
        st.markdown("""
        **Langkah-langkah:**
        1. Pilih menu **'Deteksi Zona Ikan'** dari navigasi
        2. Tunggu sampai peta interaktif selesai dimuat
        3. Gunakan kotak centang untuk memilih jenis ikan yang ingin ditampilkan
        4. Gunakan kontrol layer untuk mengaktifkan/mematikan zona bahaya
        """)
    
    with st.expander("2. Menggunakan Navigasi GPS"):
        st.markdown("""
        **Langkah-langkah:**
        1. Klik pada titik koordinat di peta yang ingin Anda tuju
        2. Koordinat akan otomatis terisi pada kolom 'Koordinat Tujuan'
        3. Posisi awal otomatis terdeteksi dari GPS perangkat Anda
        4. Aktifkan toggle **'Gunakan GPS'** untuk pembaruan otomatis
        5. Atau gunakan tombol **'Refresh GPS'** untuk pembaruan manual
        """)
    
    with st.expander("3. Melihat Prediksi 30 Hari"):
        st.markdown("""
        **Langkah-langkah:**
        1. Pilih **'Prediksi 30 Hari'** dari menu navigasi
        2. Pilih bulan dan minggu yang ingin ditampilkan
        3. Sistem akan menampilkan prediksi secara otomatis
        4. Pilih jenis ikan menggunakan filter yang tersedia
        5. Unduh data dalam format CSV jika diperlukan
        """)
    
    with st.expander("4. Memahami Zona Bahaya"):
        st.markdown("""
        **Indikator Zona Bahaya:**
        - **Gelombang Tinggi**: Hs > 2.5 meter (berbahaya untuk penangkapan)
        - **Perairan Dangkal**: Kedalaman < 10 meter (risiko kandas)
        
        Zona bahaya ditandai dengan warna merah pada peta. Hindari area ini saat melaut.
        """)
    
    with st.expander("5. Parameter yang Digunakan"):
        st.markdown("""
        **Parameter Oseanografi:**
        - **Suhu Permukaan Laut (SST/thetao)**: Menentukan habitat ikan
        - **Klorofil-a (chl)**: Indikator produktivitas primer/makanan ikan
        - **Tinggi Gelombang (Hs)**: Untuk deteksi zona bahaya
        - **Kedalaman (deptho)**: Untuk deteksi perairan dangkal
        """)
    
    st.markdown('<h2 class="section-header">Pertanyaan yang Sering Diajukan</h2>', unsafe_allow_html=True)
    
    with st.expander("Apakah SAILOR gratis digunakan?"):
        st.markdown("Ya, SAILOR disediakan sebagai demo gratis untuk nelayan dan pemangku kepentingan perikanan.")
    
    with st.expander("Seberapa akurat prediksi SAILOR?"):
        st.markdown("Model Random Forest yang digunakan menunjukkan RMSE 0.002816 dan MAE 0.002245, mengindikasikan akurasi prediksi yang baik.")
    
    with st.expander("Dapatkah digunakan di luar Laut Jawa?"):
        st.markdown("Saat ini SAILOR mendukung wilayah Laut Jawa. Pengembangan untuk wilayah lain direncanakan di masa mendatang.")
    
    with st.expander("Apa yang harus dilakukan jika GPS tidak terdeteksi?"):
        st.markdown("Pastikan perizinan lokasi pada browser diberikan. Anda juga dapat memasukkan koordinat secara manual.")

# === HALAMAN TENTANG ===
elif selected == "Tentang":
    st.markdown('<h1 class="section-header">About SAILOR</h1>', unsafe_allow_html=True)
    
    # Responsive: Stack on mobile
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What is SAILOR?
        
        **SAILOR** (Satellite-based AI Intelligent Localization Optimization Resources) is a fisheries 
        information system based on satellite technology and artificial intelligence designed to help 
        fishermen find potential fishing zones in the Java Sea.
        
        ### Objectives
        
        To build a spatial information system based on oceanographic satellite data that can detect and 
        predict potential fishing grounds in the Java Sea automatically.
        
        ### SAILOR Advantages
        
        **Real-Time Data**: Uses Copernicus satellite data updated every hour
        
        **AI Prediction**: Random Forest machine learning model with high accuracy
        
        **Hazard Zones**: Automatic detection of dangerous areas for fisher safety
        
        **GPS Navigation**: Direct guidance to potential locations
        
        **Multi-Species**: Supports 6 pelagic fish species
        
        **Auto Processing**: Automatic system without manual intervention
        """)
    
    with col2:
        st.markdown("""
        <div class="info-box">
            <div class="info-box-title">Statistics</div>
            <div class="info-box-content">
                <strong>6 Fish Species</strong><br>
                Tongkol, Cakalang, Tenggiri, Teri, Shortfin Scad, Spotted Sardinella<br><br>
                
                <strong>2 Parameters</strong><br>
                Sea Surface Temperature, Chlorophyll-a<br><br>
                
                <strong>Model Accuracy</strong><br>
                RMSE: 0.002816<br>
                MAE: 0.002245
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">Development Team</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-box" style="text-align: center;">
            <div class="feature-heading">M. Ma'ruf Sabili Riziq</div>
            <p style="color: #586069; font-family: Inter, sans-serif;">21120123140123</p>
            <p style="color: #959da5; font-size: clamp(0.8rem, 2vw, 0.9rem); font-family: Inter, sans-serif;">Lead Developer</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-box" style="text-align: center;">
            <div class="feature-heading">Hasna Auliannisa Wahono</div>
            <p style="color: #586069; font-family: Inter, sans-serif;">21120123130078</p>
            <p style="color: #959da5; font-size: clamp(0.8rem, 2vw, 0.9rem); font-family: Inter, sans-serif;">Data Scientist</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-box" style="text-align: center;">
            <div class="feature-heading">Nimas Ratri Kirana A.</div>
            <p style="color: #586069; font-family: Inter, sans-serif;">26050122120033</p>
            <p style="color: #959da5; font-size: clamp(0.8rem, 2vw, 0.9rem); font-family: Inter, sans-serif;">UI/UX Designer</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<h2 class="section-header">Institution</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Universitas Diponegoro**
        
        Faculty of Science and Mathematics
        
        Informatics Study Program
        """)
    
    with col2:
        st.markdown("""
        **GEMASTIK XVIII**
        
        Category: Software Development
        
        Year: 2025
        """)
    
    st.markdown('<h2 class="section-header">References & Data Sources</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    - Copernicus Marine Environment Monitoring Service (CMEMS)
    - Ministry of Marine Affairs and Fisheries of Indonesia
    - Zainuddin et al. (2023) - Satellite-Based Ocean Color and Thermal Signatures
    - Putri et al. (2021) - Distribution of Small Pelagic Fish in Makassar Strait
    - Semedi et al. (2023) - Seasonal Migration Zone of Skipjack Tuna
    """)
    
    st.markdown('<h2 class="section-header">Contact Us</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Email**")
        st.markdown("sailor@undip.ac.id")
    
    with col2:
        st.markdown("**GitHub**")
        st.markdown("[github.com/sailor-project](https://github.com)")
    
    with col3:
        st.markdown("**Documentation**")
        st.markdown("[docs.sailor.id](https://docs.sailor.id)")



