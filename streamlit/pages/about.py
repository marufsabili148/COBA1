import streamlit as st
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(page_title="Tentang - SAilOR", page_icon="ℹ️", layout="wide")

# Explicit current page to keep navbar indicator consistent
st.session_state.current_page = 'Tentang'

# === NAVBAR ===
nav_options = ["Beranda", "Deteksi Zona Ikan", "Prediksi 30 Hari", "Tutorial", "Tentang", "Feedback"]
current = st.session_state.get('current_page', 'Tentang')
default_index = nav_options.index(current) if current in nav_options else 0
selected = option_menu(
    menu_title=None,
    options=nav_options,
    icons=["house", "map", "graph-up", "book", "info-circle", "chat-dots"],
    menu_icon="cast",
    default_index=default_index,
    orientation="horizontal",
    key="main_nav",
)

if selected != current:
    st.session_state.current_page = selected
    st.experimental_rerun()

st.markdown("## Tentang SAiLOR")
st.markdown(
    "SAiLOR adalah aplikasi demo yang memanfaatkan data satelit untuk membantu mendeteksi zona penangkapan ikan yang potensial. Halaman ini berisi informasi singkat tentang tujuan dan teknologi yang digunakan."
)

with st.expander("Detail Teknis"):
    st.write("- Dibangun dengan Streamlit\n- Navigasi menggunakan streamlit_option_menu\n- Data contoh tersedia di folder csv/")

with st.expander("Kontak & Lisensi"):
    st.write("Ini adalah versi demo; tidak ada kontak resmi. Gunakan untuk tujuan pengujian dan pengembangan.")
