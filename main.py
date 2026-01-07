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
    "1. Alfian Rohman Rosyid, S.H., M.Pd.",
    "2. Sunaryah, S.Pd.",
    "3. Asari, S.T.",
    "4. Istuning Bayu Widari, S.Pd.",
    "5. Sri Astuti Handayani, S.Pd.",
    "6. Suroso, S.T.",
    "7. Agustina Wulandari, S.Pd.",
    "8. Muhammad Qodir",
    "9. Ahmad Muzaki, S.Pd.",
    "10. Herman Sulih Widianto, S.Pd.",
    "11. Nur Afifah, S.Pd.",
    "12. Wahyu Aji Tri Riswandhana, S.Kom.",
    "13. Vico Taufiqul Huda, S.Pd.",
    "14. Dyah Anggun Risky Wardani, S.Pd.",
    "15. Ismilatipah, S.Pd.",
    "16. Friska Setiaratna, S.Kom.",
    "17. Bagus Irawan Verdiono",
    "18. Wahyu Lailiyah, S.Pd.",
    "19. Nailatus Sa'adah, S.Psi.",
    "20. Anis Muflikhatur Rosidah, S.Psi.",
    "21. Bibin Abdul Harko Bintoro, S.Pd.",
    "22. Mochamad Yusak Nur Machmudi, S.Kom.",
    "23. Setia Budi",
    "24. Rizki Bima Prastyo",
    "25. Masyhuda, S.T.",
    "26. Seivudin, S.T.",
    "27. Muhammad Firmansyah, S.Kom",
    "28. Mokhammad Adam Naufal Nur Fatah, S.Kom",
    "29. Ika Wara Yuni Antisna, S.Pd",
    "30. Anisa Tata Ilahi, S.Psi",
    "31. Nursulaiman, M.Pd.",
    "32. Rizky Luhur W., S.Pd",
    "33. Muhammad Sulthon Aziz, S. Hum.",
    "34. Qurrotu Aina Al. Arofat, S.PdI",
    "35. Indri Dwi Setiani, S.Ak.",
    "36. Oktafia Ayu Setyoningrum, S.Ak.",
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

# --- FUNGSI KONEKSI (PERBAIKAN KUNCI OTOMATIS) ---
def connect_to_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    try:
        # 1. Cek apakah ini di Laptop (Ada file rahasia.json?)
        if os.path.exists(NAMA_FILE_KUNCI):
            creds = Credentials.from_service_account_file(NAMA_FILE_KUNCI, scopes=scopes)
        
        # 2. Jika tidak ada file, berarti di Internet (Pakai Secrets)
        elif "gcp_service_account" in st.secrets:
            # Ambil data dari Secrets dan buat salinannya (agar aman)
            creds_dict = dict(st.secrets["gcp_service_account"])
            
            # === BAGIAN PENTING: MEMBERSIHKAN KUNCI ===
            # Mengubah huruf "\n" menjadi tombol ENTER beneran
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        
        else:
            st.error("❌ File Kunci tidak ditemukan! Harap masukkan di Secrets.")
            st.stop()
            
        client = gspread.authorize(creds)
        sheet = client.open(NAMA_GOOGLE_SHEET).sheet1
        return sheet
        
    except Exception as e:
        st.error(f"❌ Gagal Konek ke Database: {e}")
        st.stop()

# --- TAMPILAN APLIKASI ---
if os.path.exists(NAMA_FILE_LOGO):
    st.image(NAMA_FILE_LOGO, width=150)
else:
    st.write("") 

st.title("🏫 Jurnal & Absensi Guru")
st.subheader("SMK Muhammadiyah 1 Ngoro")

with st.form("form_absensi"):
    col1, col2 = st.columns(2)
    with col1:
        nama = st.selectbox("Nama Guru", list_nama_guru)
    with col2:
        kelas = st.selectbox("Kelas", list_kelas)
    
    mapel = st.selectbox("Mata Pelajaran", list_mapel)
    materi = st.text_area("Materi / Aktivitas KBM", placeholder="Jelaskan kegiatan pembelajaran...")
    
    st.write("Bukti Foto Kegiatan:")
    gambar = st.camera_input("Ambil Foto")
    tombol_kirim = st.form_submit_button("Kirim Laporan")

# --- PROSES SIMPAN ---
if tombol_kirim:
    if not materi:
        st.warning("⚠️ Mohon lengkapi isian Materi!")
    else:
        with st.spinner("Sedang mengirim data..."):
            waktu = datetime.now()
            tgl = waktu.strftime("%Y-%m-%d")
            jam = waktu.strftime("%H:%M:%S")
            status_foto = "Ada Foto" if gambar else "Tanpa Foto"
            
            data_baru = [tgl, jam, nama, kelas, mapel, materi, status_foto]
            
            try:
                sheet = connect_to_sheet()
                sheet.append_row(data_baru)
                st.success(f"✅ Laporan berhasil dikirim!")
                st.balloons()
            except Exception as e:
                st.error(f"Gagal menyimpan data: {e}")