import streamlit as st
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(page_title="SAILOR - Tutorial", page_icon="📘", layout="wide")

# Ensure menu indicator syncs on load
st.session_state.current_page = 'Tutorial'

# === NAVBAR ===
nav_options = ["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang", "Feedback"]
current = st.session_state.get('current_page', 'Tutorial')
default_index = nav_options.index(current) if current in nav_options else nav_options.index('Tutorial')
selected = option_menu(
    menu_title=None,
    options=nav_options,
    icons=["house", "map", "graph-up", "book", "info-circle", "chat-dots"],
    menu_icon="cast",
    default_index=default_index,
    orientation="horizontal",
    key="main_nav",
)

if selected != st.session_state.get('current_page', 'Tutorial'):
    st.session_state.current_page = selected
    if selected == "Beranda":
        st.switch_page("home.py")
    elif selected == "Deteksi Zona Ikan":
        st.switch_page("pages/hasil_deteksi.py")
    elif selected == "Prediksi 30 Hari":
        st.switch_page("pages/forecast.py")
    elif selected == "Tentang":
        st.switch_page("home.py")
    elif selected == "Feedback":
        st.switch_page("pages/feedback.py")

st.session_state.current_page = selected

# Konten placeholder tutorial (sudah diterjemahkan ke Bahasa Indonesia)
st.title("📘 Panduan & Tutorial")
st.write("Konten tutorial sedang disiapkan. Halaman ini berfungsi sebagai panduan singkat dan contoh penggunaan.")

with st.expander("2. Menggunakan Navigasi GPS"):
    st.markdown("""
    **Langkah-langkah:**
    1. Klik pada titik koordinat di peta yang ingin Anda tuju
    2. Koordinat akan otomatis terisi pada kolom 'Koordinat Tujuan'
    3. Posisi awal otomatis terdeteksi dari GPS perangkat Anda
    4. Aktifkan toggle 'Gunakan GPS' untuk pembaruan otomatis
    5. Atau gunakan tombol 'Refresh GPS' untuk pembaruan manual
    """)

with st.expander("3. Melihat Prediksi 30 Hari"):
    st.markdown("""
    **Langkah-langkah:**
    1. Pilih 'Prediksi 30 Hari' dari menu navigasi
    2. Pilih bulan dan minggu yang ingin ditampilkan
    3. Sistem akan menampilkan prediksi secara otomatis
    4. Pilih jenis ikan menggunakan filter yang tersedia
    5. Unduh data dalam format CSV jika diperlukan
    """)

with st.expander("4. Memahami Zona Bahaya"):
    st.markdown("""
    **Indikator Zona Bahaya:**
    - Gelombang Tinggi: Hs > 2.5 meter (berbahaya untuk melaut)
    - Perairan Dangkal: Kedalaman < 10 meter (risiko kandas)

    Zona bahaya ditandai dengan warna merah pada peta. Hindari area ini saat melaut.
    """)

with st.expander("5. Parameter yang Digunakan"):
    st.markdown("""
    **Parameter Oseanografi:**
    - Suhu Permukaan Laut (SST/thetao)
    - Klorofil-a (chl)
    - Tinggi Gelombang (Hs)
    - Kedalaman (deptho)
    """)

st.markdown('<h2 class="section-header">Pertanyaan yang Sering Diajukan</h2>', unsafe_allow_html=True)

with st.expander("Apakah SAILOR gratis?"):
    st.markdown("Ya, SAILOR disediakan sebagai demo gratis untuk nelayan dan pemangku kepentingan.")

with st.expander("Seberapa akurat prediksi SAILOR?"):
    st.markdown("Model Random Forest menunjukkan RMSE 0.002816 dan MAE 0.002245.")

with st.expander("Dapatkah digunakan di luar Laut Jawa?"):
    st.markdown("Saat ini hanya mendukung wilayah Laut Jawa; dukungan wilayah lain menyusul.")

with st.expander("Apa jika GPS tidak terdeteksi?"):
    st.markdown("Pastikan browser memperbolehkan akses lokasi atau masukkan koordinat secara manual.")
