import streamlit as st
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(page_title="Tentang - SAilOR", page_icon="ℹ️", layout="wide")

# Inject favicon from local sailor.png so browser tab shows the icon on this page
try:
    import os, base64
    _fav = os.path.join(os.path.dirname(__file__), '..', 'img', 'sailor.png')
    with open(_fav, 'rb') as _f:
        _fb = base64.b64encode(_f.read()).decode()
    st.markdown(f'<link rel="icon" href="data:image/png;base64,{_fb}" type="image/png"/>', unsafe_allow_html=True)
except Exception:
    pass

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

st.markdown("## Tentang SAILOR")
st.markdown(
    "SAILOR adalah sistem informasi berbasis satelit dan kecerdasan buatan yang membantu nelayan dan peneliti mengidentifikasi zona penangkapan ikan yang potensial di wilayah Laut Jawa."
)

with st.expander("Tujuan dan Manfaat"):
    st.write("- Memberikan rekomendasi lokasi penangkapan ikan berbasis data satelit dan model AI\n- Meningkatkan efisiensi operasi penangkapan ikan dan keselamatan pelayaran\n- Menyediakan visualisasi interaktif untuk analisis cepat")

with st.expander("Detail Teknis"):
    st.write("- Dibangun dengan Streamlit\n- Peta interaktif menggunakan Folium dan streamlit-folium\n- Model prediksi: Random Forest (contoh)\n- Data contoh tersedia di folder `streamlit/csv`")

with st.expander("Tim Pengembang & Afiliasi"):
    st.markdown("**Teknik Komputer, Fakultas Teknik, Universitas Diponegoro**")
    st.markdown("**Oseanografi, Fakultas Perikanan dan Ilmu Kelautan, Universitas Diponegoro**")
    st.markdown("Anggota tim: M. Ma'ruf Sabili Riziq, Hasna Auliannisa Wahono, Nimas Ratri Kirana A.")

with st.expander("Kontak"):
    st.write("Email: sailor@undip.ac.id")
