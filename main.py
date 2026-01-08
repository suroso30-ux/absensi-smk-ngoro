import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import os

# --- KONFIGURASI ---
NAMA_FILE_KUNCI = "rahasia.json"
NAMA_GOOGLE_SHEET = "Database Absensi Guru"
NAMA_FILE_LOGO = "logo.png"

st.set_page_config(page_title="Absensi SMK Muhammadiyah 1 Ngoro", page_icon="📝")

# --- DATA GURU ---
list_nama_guru = [
    "Alfian Rohman Rosyid, S.H., M.Pd.",
    "Sunaryah, S.Pd.",
    "Asari, S.T.",
    "Istuning Bayu Widari, S.Pd.",
    "Sri Astuti Handayani, S.Pd.",
    "Suroso, S.T.",
    "Agustina Wulandari, S.Pd.",
    "Muhammad Qodir",
    "Ahmad Muzaki, S.Pd.",
    "Herman Sulih Widianto, S.Pd.",
    "Nur Afifah, S.Pd.",
    "Wahyu Aji Tri Riswandhana, S.Kom.",
    "Vico Taufiqul Huda, S.Pd.",
    "Dyah Anggun Risky Wardani, S.Pd.",
    "Ismilatipah, S.Pd.",
    "Friska Setiaratna, S.Kom.",
    "Bagus Irawan Verdiono",
    "Wahyu Lailiyah, S.Pd.",
    "Nailatus Sa'adah, S.Psi.",
    "Anis Muflikhatur Rosidah, S.Psi.",
    "Bibin Abdul Harko Bintoro, S.Pd.",
    "Mochamad Yusak Nur Machmudi, S.Kom.",
    "Setia Budi",
    "Rizki Bima Prastyo",
    "Masyhuda, S.T.",
    "Seivudin, S.T.",
    "Muhammad Firmansyah, S.Kom",
    "Mokhammad Adam Naufal Nur Fatah, S.Kom",
    "Ika Wara Yuni Antisna, S.Pd",
    "Anisa Tata Ilahi, S.Psi",
    "Nursulaiman, M.Pd.",
    "Rizky Luhur W., S.Pd",
    "Muhammad Sulthon Aziz, S. Hum.",
    "Qurrotu Aina Al. Arofat, S.PdI",
    "Indri Dwi Setiani, S.Ak.",
    "Oktafia Ayu Setyoningrum, S.Ak.",
    "Lainnya"
]

# --- DATA KELAS ---
list_kelas = [
    "X-TKR 1", "X-TKR 2", "X-TKR 3", 
    "X-TSM 1", "X-TSM 2", 
    "X-TKJ",
    "XI-TKR 1", "XI-TKR 2",
    "XI-TSM 1", "XI-TSM 2",
    "XI-TKJ",
    "XII-TKR 1", "XII-TKR 2",
    "XII-TSM 1", "XII-TSM 2",
    "XII-TKJ",
    "Lainnya"
]

# --- DATA MAPEL ---
list_mapel = [
    "Pendidikan Agama Islam dan Budi Pekerti",
    "Pendidikan Pancasila",
    "Bahasa Indonesia",
    "Matematika",
    "Sejarah",
    "Bahasa Inggris",
    "Seni Budaya / Seni Musik",
    "PJOK (Penjasorkes)",
    "Bahasa Jawa",
    "Informatika",
    "Projek IPAS",
    "Kewirausahaan / PKK",
    "Bimbingan Konseling (BK)",
    "Dasar-dasar Teknik Otomotif",
    "Teknik Kendaraan Ringan (TKR)",
    "Teknik Sepeda Motor (TSM)",
    "Dasar Teknik Jaringan Komputer & Telkom",
    "Teknik Komputer dan Jaringan (TKJ)",
    "Koding dan Kecerdasan Artifisial",
    "Kemuhammadiyahan dan Bahasa Arab",
    "Lainnya"
]

# --- FUNGSI KONEKSI ---
def connect_to_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    try:
        if os.path.exists(NAMA_FILE_KUNCI):
            creds = Credentials.from_service_account_file(NAMA_FILE_KUNCI, scopes=scopes)
        
        elif "gcp_service_account" in st.secrets:
            # Ambil data dari Secrets
            creds_dict = dict(st.secrets["gcp_service_account"])
            
            # --- PERBAIKAN PENTING ---
            # Kode ini mengubah "\n" (tulisan) menjadi ENTER (tombol)
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        
        else:
            st.error("❌ File Kunci tidak ditemukan! Cek Secrets.")
            st.stop()
            
        client = gspread.authorize(creds)
        sheet = client.open(NAMA_GOOGLE_SHEET).sheet1
        return sheet
        
    except Exception as e:
        st.error(f"❌ Error Detail: {e}")
        st.stop()

# --- TAMPILAN APLIKASI ---
if os.path.exists(NAMA_FILE_LOGO):
    st.image(NAMA_FILE_LOGO, width=150)

st.title("🏫 Jurnal & Absensi Guru")
st.subheader("SMK Muhammadiyah 1 Ngoro")

with st.form("form_absensi"):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.selectbox("Nama Guru", list_nama_guru)
    with col2:
        kelas = st.selectbox("Kelas", list_kelas)
    
    mapel = st.selectbox("Mata Pelajaran", list_mapel)
    materi = st.text_area("Materi / Aktivitas KBM", placeholder="Isi kegiatan...")
    
    st.write("Bukti Foto:")
    gambar = st.camera_input("Ambil Foto")
    tombol_kirim = st.form_submit_button("Kirim Laporan")

# --- PROSES SIMPAN ---
if tombol_kirim:
    if not materi:
        st.warning("⚠️ Mohon lengkapi Materi!")
    else:
        with st.spinner("Mengirim data..."):
            waktu = datetime.now()
            tgl = waktu.strftime("%Y-%m-%d")
            jam = waktu.strftime("%H:%M:%S")
            status_foto = "Ada Foto" if gambar else "Tanpa Foto"
            
            data_baru = [tgl, jam, nama, kelas, mapel, materi, status_foto]
            
            try:
                sheet = connect_to_sheet()
                sheet.append_row(data_baru)
                st.success(f"✅ Berhasil!")
                st.balloons()
            except Exception as e:
                st.error(f"Gagal: {e}")