import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client
import json

# === KONFIGURASI HALAMAN ===
st.set_page_config(
    page_title="SAILOR - Feedback Nelayan",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# === SUPABASE CONFIGURATION ===
SUPABASE_URL = "https://kkeiwnrziuisnrloltwh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtrZWl3bnJ6aXVpc25ybG9sdHdoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk2MjU4NDAsImV4cCI6MjA3NTIwMTg0MH0.v9tF5xmhxTFi2SRYrh-UwdtErYXJOYjU1EZ_UvUAtbk"

try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as e:
    st.error(f"Error koneksi Supabase: {e}")

# === CUSTOM CSS ===
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    
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
    
    .stButton > button {
        background-color: #0e4194;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 4px;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        background-color: #0a3275;
        box-shadow: 0 4px 8px rgba(14, 65, 148, 0.2);
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #24292e;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #0e4194;
    }
    
    .info-card {
        background: #f6f8fa;
        border-left: 4px solid #0e4194;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #155724;
    }
    
    .textarea-container {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# === PAGE HEADER ===
st.markdown("""
<div class="page-header">
    <h1 class="page-title">📝 Feedback Validasi Lapangan</h1>
    <p class="page-subtitle">Bantu kami meningkatkan akurasi prediksi dengan pengalaman Anda di lapangan</p>
</div>
""", unsafe_allow_html=True)

# === PENJELASAN ===
st.markdown('<h2 class="section-header">ℹ️ Mengapa Feedback Anda Penting?</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #0e4194; margin-top: 0;">🎯 Validasi Data</h3>
        <p>Pengalaman Anda membantu memvalidasi akurasi prediksi zona ikan yang kami buat</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #0e4194; margin-top: 0;">📊 Peningkatan Model</h3>
        <p>Data lapangan digunakan untuk melatih dan meningkatkan model AI kami</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card">
        <h3 style="color: #0e4194; margin-top: 0;">🤝 Kolaborasi</h3>
        <p>Membangun sistem yang benar-benar bermanfaat bagi nelayan Indonesia</p>
    </div>
    """, unsafe_allow_html=True)

# === FORM FEEDBACK ===
st.markdown("---")
st.markdown('<h2 class="section-header">📋 Form Feedback</h2>', unsafe_allow_html=True)

with st.form("feedback_form", clear_on_submit=True):
    # Informasi Nelayan
    st.markdown("### 👤 Informasi Nelayan")
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        nama_nelayan = st.text_input("Nama Lengkap*", placeholder="Masukkan nama Anda")
        no_telepon = st.text_input("No. Telepon/WhatsApp*", placeholder="08xxxxxxxxxx")
        asal_daerah = st.text_input("Asal Daerah/Pelabuhan*", placeholder="Contoh: Pelabuhan Muara Baru, Jakarta")
    
    with col_info2:
        jenis_kapal = st.selectbox(
            "Jenis Kapal",
            ["Kapal Kecil (< 5 GT)", "Kapal Sedang (5-30 GT)", "Kapal Besar (> 30 GT)", "Perahu Tradisional"]
        )
        pengalaman_melaut = st.selectbox(
            "Pengalaman Melaut",
            ["< 1 tahun", "1-5 tahun", "5-10 tahun", "10-20 tahun", "> 20 tahun"]
        )
        alat_tangkap = st.text_input("Alat Tangkap Utama", placeholder="Contoh: Jaring insang, Pancing, Rawai")
    
    st.markdown("---")
    
    # Data Penangkapan
    st.markdown("### 🎣 Data Penangkapan Ikan")
    
    col_catch1, col_catch2 = st.columns(2)
    
    with col_catch1:
        tanggal_tangkap = st.date_input("Tanggal Penangkapan*", value=datetime.now())
        waktu_tangkap = st.time_input("Waktu Penangkapan*", value=None)
        
        st.markdown("#### 📍 Koordinat Lokasi Penangkapan*")
        latitude = st.number_input("Latitude", format="%.6f", value=0.0, step=0.000001)
        longitude = st.number_input("Longitude", format="%.6f", value=0.0, step=0.000001)
    
    with col_catch2:
        jenis_ikan = st.multiselect(
            "Jenis Ikan yang Ditangkap*",
            ["Tuna", "Cakalang", "Tongkol", "Lemuru", "Kembung", "Tenggiri", "Kakap", "Baronang", "Kerapu", "Lainnya"]
        )
        
        if "Lainnya" in jenis_ikan:
            jenis_ikan_lainnya = st.text_input("Sebutkan jenis ikan lainnya", placeholder="Pisahkan dengan koma")
        else:
            jenis_ikan_lainnya = ""
        
        jumlah_tangkapan = st.number_input("Estimasi Jumlah Tangkapan (kg)*", min_value=0.0, step=0.5)
        
        kualitas_tangkapan = st.select_slider(
            "Kualitas Hasil Tangkapan",
            options=["Sangat Buruk", "Buruk", "Cukup", "Baik", "Sangat Baik"]
        )
    
    st.markdown("---")
    
    # Kondisi Lingkungan
    st.markdown("### 🌊 Kondisi Lingkungan Saat Penangkapan")
    
    col_env1, col_env2, col_env3 = st.columns(3)
    
    with col_env1:
        kondisi_cuaca = st.selectbox(
            "Kondisi Cuaca",
            ["Cerah", "Berawan", "Mendung", "Hujan Ringan", "Hujan Lebat", "Badai"]
        )
        tinggi_gelombang = st.selectbox(
            "Tinggi Gelombang",
            ["< 0.5 meter", "0.5 - 1 meter", "1 - 2 meter", "2 - 3 meter", "> 3 meter"]
        )
    
    with col_env2:
        kecepatan_angin = st.selectbox(
            "Kecepatan Angin",
            ["Tenang (< 5 knot)", "Ringan (5-10 knot)", "Sedang (10-20 knot)", "Kencang (20-30 knot)", "Sangat Kencang (> 30 knot)"]
        )
        kejernihan_air = st.selectbox(
            "Kejernihan Air",
            ["Sangat Jernih", "Jernih", "Agak Keruh", "Keruh", "Sangat Keruh"]
        )
    
    with col_env3:
        suhu_permukaan = st.number_input("Suhu Permukaan Air (°C)", min_value=20.0, max_value=35.0, value=28.0, step=0.1)
        kedalaman_penangkapan = st.number_input("Kedalaman Penangkapan (meter)", min_value=0.0, step=1.0)
    
    st.markdown("---")
    
    # Validasi Prediksi SAILOR
    st.markdown("### ✅ Validasi Prediksi SAILOR")
    
    menggunakan_sailor = st.radio(
        "Apakah Anda menggunakan aplikasi SAILOR untuk menentukan lokasi penangkapan?*",
        ["Ya", "Tidak"]
    )
    
    if menggunakan_sailor == "Ya":
        akurasi_prediksi = st.select_slider(
            "Seberapa akurat prediksi SAILOR dengan hasil tangkapan Anda?*",
            options=["Sangat Tidak Akurat", "Tidak Akurat", "Cukup Akurat", "Akurat", "Sangat Akurat"]
        )
    else:
        akurasi_prediksi = "Tidak Menggunakan"
    
    st.markdown("---")
    
    # Catatan Tambahan
    st.markdown("### 📝 Catatan dan Saran")
    
    catatan_tambahan = st.text_area(
        "Catatan Tambahan",
        placeholder="Ceritakan pengalaman Anda, kondisi khusus yang Anda temui, atau saran untuk pengembangan aplikasi...",
        height=150
    )
    
    saran_fitur = st.text_area(
        "Saran Fitur Baru",
        placeholder="Fitur apa yang Anda harapkan dari aplikasi SAILOR?",
        height=100
    )
    
    # Persetujuan
    st.markdown("---")
    persetujuan = st.checkbox(
        "Saya setuju data ini digunakan untuk pengembangan dan penelitian aplikasi SAILOR*",
        value=False
    )
    
    # Submit Button
    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("📤 Kirim Feedback")
    
    if submitted:
        # Validasi input wajib
        if not nama_nelayan or not no_telepon or not asal_daerah:
            st.error("Mohon lengkapi semua informasi nelayan yang bertanda *")
        elif latitude == 0.0 or longitude == 0.0:
            st.error("Mohon masukkan koordinat lokasi penangkapan yang valid")
        elif not jenis_ikan:
            st.error("Mohon pilih minimal satu jenis ikan yang ditangkap")
        elif jumlah_tangkapan == 0:
            st.error("Mohon masukkan jumlah tangkapan")
        elif not persetujuan:
            st.error("Mohon centang persetujuan penggunaan data")
        else:
            # Siapkan data untuk dikirim
            feedback_data = {
                "nama_nelayan": nama_nelayan,
                "no_telepon": no_telepon,
                "asal_daerah": asal_daerah,
                "jenis_kapal": jenis_kapal,
                "pengalaman_melaut": pengalaman_melaut,
                "alat_tangkap": alat_tangkap,
                "tanggal_tangkap": tanggal_tangkap.strftime("%Y-%m-%d"),
                "waktu_tangkap": waktu_tangkap.strftime("%H:%M:%S") if waktu_tangkap else None,
                "latitude": latitude,
                "longitude": longitude,
                "jenis_ikan": json.dumps(jenis_ikan),
                "jenis_ikan_lainnya": jenis_ikan_lainnya,
                "jumlah_tangkapan": jumlah_tangkapan,
                "kualitas_tangkapan": kualitas_tangkapan,
                "kondisi_cuaca": kondisi_cuaca,
                "tinggi_gelombang": tinggi_gelombang,
                "kecepatan_angin": kecepatan_angin,
                "kejernihan_air": kejernihan_air,
                "suhu_permukaan": suhu_permukaan,
                "kedalaman_penangkapan": kedalaman_penangkapan,
                "menggunakan_sailor": menggunakan_sailor,
                "akurasi_prediksi": akurasi_prediksi,
                "catatan_tambahan": catatan_tambahan,
                "saran_fitur": saran_fitur,
                "created_at": datetime.now().isoformat()
            }
            
            try:
                # Kirim ke Supabase
                response = supabase.table("feedback_nelayan").insert(feedback_data).execute()
                
                st.markdown("""
                <div class="success-box">
                    <h3 style="margin-top: 0;">✅ Feedback Berhasil Dikirim!</h3>
                    <p>Terima kasih atas kontribusi Anda untuk pengembangan aplikasi SAILOR.</p>
                    <p>Data Anda akan sangat membantu kami meningkatkan akurasi prediksi zona ikan.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.balloons()
                
            except Exception as e:
                st.error(f"Terjadi kesalahan saat mengirim data: {str(e)}")
                st.info("Silakan coba lagi atau hubungi tim pengembang jika masalah berlanjut.")

# === FOOTER INFO ===
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #586069; padding: 2rem 0;">
    <p><strong>Kontak Tim Pengembang SAILOR</strong></p>
    <p>Email: sailor@example.com | WhatsApp: +62 xxx-xxxx-xxxx</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        Data yang Anda kirimkan akan dijaga kerahasiaannya dan hanya digunakan untuk pengembangan aplikasi
    </p>
</div>
""", unsafe_allow_html=True)
