# Main JAKI Application - Frontend and Backend Logic
import streamlit as st
import os
from PIL import Image
import db_utils # Our database utility module
import time # For simulating progress

# --- Configuration ---
UPLOAD_DIR = "/home/ubuntu/jaki_app/uploads"
LOGO_PATH = "/home/ubuntu/jaki_app/logo_jaki.png" # Assuming logo is in the same directory
SUCCESS_IMAGE_PATH = "/home/ubuntu/jaki_app/success_icon.png" # Placeholder, replace with actual path if you have one
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
CATEGORIES = [
    "Pilih Kategori...",
    "Infrastruktur & Fasilitas Umum", 
    "Jalan Rusak", 
    "Sampah Liar", 
    "Penerangan Jalan Mati", 
    "Banjir & Genangan",
    "Pohon Tumbang",
    "Pelanggaran Ketertiban Umum",
    "Pengadaan Baru",
    "Lainnya"
]

# --- Helper Functions ---
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(uploaded_file):
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    try:
        filename = uploaded_file.name.replace(" ", "_").lower()
        if not allowed_file(filename):
            st.error(f"Tipe file tidak valid. Hanya {", ".join(ALLOWED_EXTENSIONS)} yang diizinkan.")
            return None

        file_path = os.path.join(UPLOAD_DIR, filename)
        counter = 1
        original_filename = filename
        name_part, ext_part = os.path.splitext(original_filename)
        while os.path.exists(file_path):
            filename = f"{name_part}_{counter}{ext_part}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            counter += 1
            
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    except Exception as e:
        st.error(f"Error saat menyimpan gambar: {e}")
        return None

# Initialize Database
db_utils.init_db()

# --- Load Custom CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide", page_title="JAKI - Lapor Masalah")
local_css("/home/ubuntu/jaki_app/style.css")

# --- Custom Header ---
# Using columns for better control over layout
col1, col2, col3 = st.columns([0.3, 0.4, 0.3])
with col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=100) # Adjusted width
    else:
        st.markdown("<span class=\"brand-name\">jaki</span>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style=\"text-align: right; margin-top: 20px;\"><span class=\"nav-links\">Fitur Tentang Kami Bantuan &nbsp;&nbsp;&nbsp; Bahasa Indonesia ⌄</span></div>", unsafe_allow_html=True)

st.markdown("<h2 class=\"page-title\">Laporkan Masalah di Sekitar Anda dengan JAKI</h2>", unsafe_allow_html=True)
# st.markdown("---_---_---") # Removed, CSS will handle spacing/borders if needed

# --- State Management ---
if "upload_complete" not in st.session_state:
    st.session_state.upload_complete = False
if "image_path" not in st.session_state:
    st.session_state.image_path = None
if "show_form" not in st.session_state:
    st.session_state.show_form = False
if "submission_success" not in st.session_state:
    st.session_state.submission_success = False
if "error_message" not in st.session_state:
    st.session_state.error_message = None

# --- Page 1: Upload Image ---
if not st.session_state.show_form and not st.session_state.submission_success:
    st.markdown("<h3 class=\"custom-h3\">Unggah gambar atau rekam video masalah yang ingin Anda laporkan</h3>", unsafe_allow_html=True)
    
    # Apply card styling to the uploader section
    with st.container(): # Use a container to apply card style if direct styling is hard
        # This is a conceptual application of a class. Streamlit doesn't directly support adding classes to all elements.
        # The style.css targets `section[data-testid="stFileUploadDropzone"]` which is more reliable.
        uploaded_file = st.file_uploader(
            "Drag & drop images, and Video or browser files on your computer", 
            type=list(ALLOWED_EXTENSIONS),
            label_visibility="collapsed"
        )

    if uploaded_file is not None:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Uploading Image...")
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        
        status_text.text("Upload Complete!")
        st.image(uploaded_file, width=200, use_column_width='auto')
        
    saved_path = save_uploaded_file(uploaded_file)
    if saved_path:
        st.session_state.image_path = saved_path
        st.session_state.upload_complete = True
        time.sleep(1)
        st.session_state.show_form = True
        st.rerun()
    else:
        st.session_state.error_message = "Gagal memproses file yang diunggah."
        st.session_state.upload_complete = False
        st.rerun()
    
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None # Clear after displaying

    # Centered Upload Button (cosmetic, actual upload is handled by file_uploader)
    # This button is more for visual consistency with the reference image
    # It doesn't perform the upload itself, st.file_uploader does.
    cols_button = st.columns([1,0.5,1])
    with cols_button[1]:
        if st.button("Upload", use_container_width=True, key="upload_button_visual") and uploaded_file is None:
            st.warning("Silakan pilih file untuk diunggah terlebih dahulu.")

# --- Page 2: Report Form ---
elif st.session_state.show_form and not st.session_state.submission_success:
    st.markdown("<h3 class=\"custom-h3\">Sistem AI JAKI telah menganalisis dan mengklasifikasikan laporan Anda secara otomatis.</h3>", unsafe_allow_html=True)
    st.markdown("<p style=\'text-align: center; font-size: smaller; color: #555;\'>Teknologi ini memastikan identifikasi masalah lebih cepat dan laporan diteruskan ke dinas terkait untuk segera ditindaklanjuti.</p>", unsafe_allow_html=True)

    if st.session_state.image_path:
        st.image(st.session_state.image_path, caption="Gambar Laporan", width=300, use_column_width='auto')
    else:
        st.warning("Tidak ada gambar yang diunggah. Silakan kembali dan unggah gambar.")
        if st.button("Kembali ke Unggah"):
            st.session_state.show_form = False
            st.session_state.upload_complete = False
            st.session_state.image_path = None
            st.rerun()
        st.stop()

    with st.form("report_form"):
        st.markdown("<span class=\"form-section-label\">Deskripsi Otomatis ✨</span>", unsafe_allow_html=True)
        description = st.text_area("", placeholder="Contoh: Jalan berlubang di area trotoar, berpotensi membahayakan pejalan kaki dan pengguna kendaraan.", height=100, label_visibility="collapsed")
        
        st.markdown("<span class=\"form-section-label\">Kategori Masalah ✨</span>", unsafe_allow_html=True)
        category = st.selectbox("", CATEGORIES, label_visibility="collapsed")

        st.markdown("<span class=\"form-section-label\">Lokasi ✨</span>", unsafe_allow_html=True)
        location_text = st.text_input("", placeholder="Contoh: Jl. Raya Bandung No. 123, RT 01/RW 02, Kel. Sukasari...", label_visibility="collapsed")
        
        # Geolocation JS - This is still experimental and might not reliably update the Streamlit input
        # For a production app, a custom component (e.g., streamlit-js-eval) is recommended.
        # st.markdown(""" 
        # <script>
        # function getLocationAndSetInput() {
        #     if (navigator.geolocation) {
        #         navigator.geolocation.getCurrentPosition(function(position) {
        #             const lat = position.coords.latitude;
        #             const lon = position.coords.longitude;
        #             const locationString = `Lat: ${lat.toFixed(6)}, Lon: ${lon.toFixed(6)}`;
        #             // Attempt to find and set the Streamlit input. This is highly unreliable.
        #             // The input element's ID is dynamically generated by Streamlit.
        #             // A more robust way is needed, e.g., passing it via query params or a custom component.
        #             try {
        #                 let inputs = document.querySelectorAll('input[type="text"]');
        #                 // Assuming the location input is the last one or has a specific placeholder
        #                 for (let i = 0; i < inputs.length; i++) {
        #                     if (inputs[i].placeholder.includes("Jl. Raya Bandung")) {
        #                         inputs[i].value = locationString;
        #                         // Trigger an event to let Streamlit know the input changed
        #                         const event = new Event('input', { bubbles: true });
        #                         inputs[i].dispatchEvent(event);
        #                         break;
        #                     }
        #                 }
        #             } catch (e) { console.error("Error setting location input: ", e); }
        #             console.log(locationString);
        #         }, function(error) {
        #             console.error("Error getting location: ", error.message);
        #         });
        #     } else {
        #         console.log("Geolocation is not supported by this browser.");
        #     }
        # }
        # // Call it if a button is clicked or automatically
        # // document.addEventListener('DOMContentLoaded', (event) => {
        # //     const geoButton = document.getElementById('get-location-button');
        # //     if(geoButton) { geoButton.onclick = getLocationAndSetInput; }
        # // });
        # </script>
        # """, unsafe_allow_html=True)
        # if st.button("Deteksi Lokasi Saya (Eksperimental)", key="get_location_button"):
        #    st.markdown("<script>getLocationAndSetInput();</script>", unsafe_allow_html=True)
        #    st.info("Mencoba mendeteksi lokasi... Hasil mungkin muncul di input lokasi jika berhasil, atau periksa konsol browser.")

        latitude_val = -6.175392 # Default Jakarta
        longitude_val = 106.827153

        col_cancel, col_submit = st.columns(2)
        with col_cancel:
            # Apply custom class for styling if st.form_submit_button doesn't accept `class_name`
            # We rely on the general .stButton > button[kind="secondary"] selector from CSS
            cancel_button = st.form_submit_button("Cancel", use_container_width=True)
        with col_submit:
            submitted = st.form_submit_button("Submit", type="primary", use_container_width=True)

        if cancel_button:
            st.session_state.show_form = False
            st.session_state.upload_complete = False
            st.session_state.image_path = None
            st.rerun()

        if submitted:
            if not description.strip() or category == "Pilih Kategori..." or not location_text.strip():
                st.error("Harap isi semua field yang wajib: Deskripsi, Kategori, dan Lokasi.")
            elif not st.session_state.image_path:
                st.error("Gambar tidak ditemukan. Silakan unggah ulang.")
            else:
                st.info("Memproses laporan Anda...")
                report_id = db_utils.add_report(
                    image_path=st.session_state.image_path,
                    category=category,
                    description=description,
                    latitude=latitude_val, 
                    longitude=longitude_val 
                )
                if report_id:
                    st.session_state.submission_success = True
                    st.session_state.show_form = False
                    st.rerun()
                else:
                    st.error("Gagal menyimpan laporan. Silakan coba lagi.")

# --- Page 3: Submission Success ---
elif st.session_state.submission_success:
    st.balloons()
    st.markdown("<div class=\"success-message-container\">", unsafe_allow_html=True)
    if os.path.exists(SUCCESS_IMAGE_PATH):
        st.image(SUCCESS_IMAGE_PATH, width=150)
    else: # Fallback if specific success image isn't found
        st.markdown("✅", unsafe_allow_html=True) # Simple checkmark emoji
    st.markdown("<h3>Laporan Berhasil Dikirim!</h3>", unsafe_allow_html=True)
    st.markdown("<p>Terima kasih! Laporan Anda telah berhasil dikirim dan akan segera diproses oleh dinas terkait. Anda dapat memantau perkembangan laporan ini melalui aplikasi JAKI.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Lapor Masalah Lain", type="primary"):
        st.session_state.upload_complete = False
        st.session_state.image_path = None
        st.session_state.show_form = False
        st.session_state.submission_success = False
        st.rerun()

# To run this app: streamlit run /home/ubuntu/jaki_app/app.py

