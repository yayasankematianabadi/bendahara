import streamlit as st
from st_supabase_connection import SupabaseConnection
from login import show_login

# 1. SET WIDE MODE DEFAULT
st.set_page_config(
    page_title="Portal System", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. KONEKSI KE SUPABASE
conn = st.connection("supabase", type=SupabaseConnection)

# 3. INISIALISASI SESSION STATE DASAR
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "menu"

# --- LOGIKA NAVIGASI ---
if not st.session_state["authenticated"]:
    # Pastikan flag refresh direset saat belum login
    st.session_state["has_refreshed"] = False
    show_login(conn)
else:
    # --- LOGIKA AUTO-REFRESH SETELAH LOGIN ---
    # Menggunakan pengecekan yang lebih ketat untuk menghindari loop rerun
    if not st.session_state.get("has_refreshed", False):
        st.session_state["has_refreshed"] = True
        # Membersihkan resource cache sebelum rerun untuk memicu koneksi websocket baru
        st.cache_resource.clear()
        st.rerun()

    # SIDEBAR
    with st.sidebar:
        st.title("Informasi Akun")
        st.write(f"Logged in as:\n{st.session_state.get('user_email', 'User')}")
        st.divider()
        
        if st.button("🏠 Home Menu", key="side_home", use_container_width=True):
            st.session_state["current_page"] = "menu"
            st.rerun()
            
        if st.button("🚪 Logout", key="side_logout", use_container_width=True):
            try:
                conn.client.auth.sign_out()
            except:
                pass
            # Bersihkan semua state secara total
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # KONTEN UTAMA
    if st.session_state["current_page"] == "menu":
        st.title("Data")
        st.write("Harap upload dan proses data terlebih dahulu sebelum menarik report!")
        st.divider()

        col1 = st.columns(1)
        with col1:
            if st.button("📤\n\n\n\nMasukkan Data", key="btn_upload", use_container_width=True):
                st.session_state["current_page"] = "upload"
                st.rerun()

        st.title("Report")
        st.divider()
        col3 = st.columns(1)
        with col3:
            if st.button("📊\n\n\n\nReport Rekonsiliasi Transaksi Deposit dan Settlement", key="r1", use_container_width=True):
                st.session_state["current_page"] = "report_rekonsiliasi_transaksi_deposit_dan_settlement"
                st.rerun()

    elif st.session_state["current_page"] == "upload":
        show_upload_dashboard(conn)
