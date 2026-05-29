
# =========================================================
# IMPORT LIBRARY
# =========================================================
import streamlit as st
import pandas as pd
from datetime import datetime

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Aplikasi Tiket Konser",
    page_icon="🎫",
    layout="wide"
)

# =========================================================
# STYLE CSS
# =========================================================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.kotak {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# CLASS NODE
# =========================================================
class TicketNode:

    def __init__(self, kode, nama, konser,
                 lokasi, kategori, seat,
                 harga, jumlah, total,
                 status, waktu):

        self.kode = kode
        self.nama = nama
        self.konser = konser
        self.lokasi = lokasi
        self.kategori = kategori
        self.seat = seat
        self.harga = harga
        self.jumlah = jumlah
        self.total = total
        self.status = status
        self.waktu = waktu
        self.next = None

# =========================================================
# DATA KONSER
# =========================================================
konser_data = {

    "Coldplay World Tour": {
        "lokasi": "Jakarta International Stadium",
        "tanggal": "12 Juni 2026",
        "vip": 2500000,
        "regular": 1200000,
        "stok": 150,
        "genre": "Pop Rock",
        "guest": "Special Guest DJ"
    },

    "NIKI Live Concert": {
        "lokasi": "ICE BSD",
        "tanggal": "20 Juli 2026",
        "vip": 1800000,
        "regular": 850000,
        "stok": 100,
        "genre": "R&B",
        "guest": "Reality Club"
    },

    "Taylor Swift Eras Tour": {
        "lokasi": "Gelora Bung Karno",
        "tanggal": "10 Agustus 2026",
        "vip": 3500000,
        "regular": 2000000,
        "stok": 200,
        "genre": "Pop",
        "guest": "Sabrina Carpenter"
    }

}

# =========================================================
# CLASS LINKED LIST
# =========================================================
class TicketLinkedList:

    def __init__(self):
        self.head = None

    # =====================================================
    # TAMBAH DATA
    # =====================================================
    def tambah_tiket(self, kode, nama, konser,
                     lokasi, kategori, seat,
                     harga, jumlah, total,
                     status, waktu):

        node_baru = TicketNode(
            kode,
            nama,
            konser,
            lokasi,
            kategori,
            seat,
            harga,
            jumlah,
            total,
            status,
            waktu
        )

        if self.head is None:
            self.head = node_baru

        else:

            current = self.head

            while current.next:
                current = current.next

            current.next = node_baru

    # =====================================================
    # TAMPILKAN DATA
    # =====================================================
    def tampilkan_data(self):

        data = []

        current = self.head

        while current:

            data.append({
                "Kode": current.kode,
                "Nama": current.nama,
                "Konser": current.konser,
                "Seat": current.seat,
                "Kategori": current.kategori,
                "Jumlah": current.jumlah,
                "Total": f"Rp {current.total:,}",
                "Status": current.status,
                "Waktu": current.waktu
            })

            current = current.next

        return data

    # =====================================================
    # CEK SEAT
    # =====================================================
    def cek_seat(self, konser, seat, kode=None):

        current = self.head

        while current:

            if (
                current.konser == konser and
                current.seat == seat and
                current.kode != kode
            ):

                return True

            current = current.next

        return False

    # =====================================================
    # HAPUS DATA
    # =====================================================
    def hapus_tiket(self, kode):

        current = self.head
        prev = None

        while current:

            if current.kode == kode:

                # =========================================
                # KEMBALIKAN STOK
                # =========================================
                konser_data[current.konser]["stok"] += current.jumlah

                if prev:
                    prev.next = current.next

                else:
                    self.head = current.next

                return True

            prev = current
            current = current.next

        return False

    # =====================================================
    # UPDATE DATA
    # =====================================================
    def update_tiket(self, kode, konser_baru,
                     lokasi_baru, kategori_baru,
                     seat_baru, harga_baru,
                     jumlah_baru):

        current = self.head

        while current:

            if current.kode == kode:

                # =========================================
                # JIKA SUDAH LUNAS
                # =========================================
                if current.status == "Lunas":

                    return "lunas"

                # =========================================
                # VALIDASI STOK
                # =========================================
                if jumlah_baru > konser_data[konser_baru]["stok"]:

                    return "stok_habis"

                # =========================================
                # VALIDASI SEAT
                # =========================================
                if self.cek_seat(
                    konser_baru,
                    seat_baru,
                    kode
                ):

                    return "seat_digunakan"

                # =========================================
                # KEMBALIKAN STOK LAMA
                # =========================================
                konser_data[current.konser]["stok"] += current.jumlah

                # =========================================
                # KURANGI STOK BARU
                # =========================================
                konser_data[konser_baru]["stok"] -= jumlah_baru

                # =========================================
                # UPDATE DATA
                # =========================================
                current.konser = konser_baru
                current.lokasi = lokasi_baru
                current.kategori = kategori_baru
                current.seat = seat_baru
                current.harga = harga_baru
                current.jumlah = jumlah_baru
                current.total = harga_baru * jumlah_baru

                return "berhasil"

            current = current.next

        return "tidak ditemukan"

# =========================================================
# SESSION STATE
# =========================================================
if "tickets" not in st.session_state:
    st.session_state.tickets = TicketLinkedList()

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

# =========================================================
# LOGIN ADMIN
# =========================================================
USERNAME = "admin"
PASSWORD = "12345"

st.sidebar.subheader("🔐 Admin Panel")

admin_user = st.sidebar.text_input("Username Admin")
admin_pass = st.sidebar.text_input(
    "Password Admin",
    type="password"
)

if st.sidebar.button("Login Admin"):

    if admin_user == USERNAME and admin_pass == PASSWORD:

        st.session_state.admin_login = True
        st.sidebar.success("✅ Admin berhasil login")

    else:

        st.sidebar.error("❌ Login gagal")

# =========================================================
# LOGOUT ADMIN
# =========================================================
if st.session_state.admin_login:

    if st.sidebar.button("Logout Admin"):

        st.session_state.admin_login = False
        st.sidebar.success("✅ Logout berhasil")

# =========================================================
# HEADER
# =========================================================
st.title("🎫 Aplikasi Pemesanan Tiket Konser")
st.write("### Sistem Pemesanan Tiket Konser Online")

st.divider()

# =========================================================
# FORM USER
# =========================================================
st.sidebar.header("📝 Form Pemesanan")

nama = st.sidebar.text_input("👤 Nama Pembeli")

konser = st.sidebar.selectbox(
    "🎵 Pilih Konser",
    list(konser_data.keys())
)

kategori = st.sidebar.radio(
    "🎫 Kategori",
    ["VIP", "Regular"]
)

seat = st.sidebar.selectbox(
    "💺 Pilih Seat",
    [
        "A1", "A2", "A3",
        "B1", "B2", "B3",
        "C1", "C2", "C3"
    ]
)

jumlah = st.sidebar.number_input(
    "🔢 Jumlah Tiket",
    min_value=1,
    max_value=5,
    value=1
)

metode = st.sidebar.selectbox(
    "💳 Metode Pembayaran",
    ["QRIS", "Transfer Bank", "E-Wallet"]
)

submit = st.sidebar.button("🎟️ Pesan Tiket")

# =========================================================
# TAMPILAN KONSER
# =========================================================
st.header("🎤 Daftar Konser")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    st.subheader("Coldplay World Tour")
    st.write("📍 Jakarta International Stadium")
    st.write("📅 12 Juni 2026")
    st.write("🎵 Genre : Pop Rock")
    st.write("🎤 Guest Star : Special Guest DJ")
    st.write(f"🎫 Stok : {konser_data['Coldplay World Tour']['stok']}")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    st.subheader("NIKI Live Concert")
    st.write("📍 ICE BSD")
    st.write("📅 20 Juli 2026")
    st.write("🎵 Genre : R&B")
    st.write("🎤 Guest Star : Reality Club")
    st.write(f"🎫 Stok : {konser_data['NIKI Live Concert']['stok']}")

    st.markdown('</div>', unsafe_allow_html=True)

with col3:

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    st.subheader("Taylor Swift Eras Tour")
    st.write("📍 Gelora Bung Karno")
    st.write("📅 10 Agustus 2026")
    st.write("🎵 Genre : Pop")
    st.write("🎤 Guest Star : Sabrina Carpenter")
    st.write(f"🎫 Stok : {konser_data['Taylor Swift Eras Tour']['stok']}")

    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =========================================================
# PEMESANAN
# =========================================================
if submit:

    if nama == "":

        st.error("❌ Nama wajib diisi")

    else:

        # =============================================
        # VALIDASI STOK
        # =============================================
        if jumlah > konser_data[konser]["stok"]:

            st.error("❌ Stok tiket tidak cukup")

        # =============================================
        # VALIDASI SEAT
        # =============================================
        elif st.session_state.tickets.cek_seat(
            konser,
            seat
        ):

            st.error("❌ Seat sudah digunakan")

        else:

            if kategori == "VIP":
                harga = konser_data[konser]["vip"]

            else:
                harga = konser_data[konser]["regular"]

            total = harga * jumlah

            kode = f"TRX-{len(st.session_state.tickets.tampilkan_data()) + 1}"

            waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            status = "Pending"

            # =============================================
            # STOK BERKURANG
            # =============================================
            konser_data[konser]["stok"] -= jumlah

            st.session_state.tickets.tambah_tiket(
                kode,
                nama,
                konser,
                konser_data[konser]["lokasi"],
                kategori,
                seat,
                harga,
                jumlah,
                total,
                status,
                waktu
            )

            st.success("✅ Tiket berhasil dipesan!")

            st.balloons()

            st.subheader("🎫 E-Ticket")

            st.info(f'''
Kode Tiket : {kode}

Nama : {nama}

Konser : {konser}

Seat : {seat}

Kategori : {kategori}

Total Bayar : Rp {total:,}

Metode Pembayaran : {metode}

Status : {status}
''')

# =========================================================
# UPDATE TIKET USER
# =========================================================
st.divider()

st.subheader("✏️ Update Tiket")

kode_update = st.text_input("Masukkan Kode Tiket")

konser_baru = st.selectbox(
    "Pilih Konser Baru",
    list(konser_data.keys())
)

kategori_baru = st.radio(
    "Kategori Baru",
    ["VIP", "Regular"],
    key="update"
)

seat_baru = st.selectbox(
    "Seat Baru",
    ["A1", "A2", "B1", "B2", "C1", "C2"],
    key="seat_update"
)

jumlah_baru = st.number_input(
    "Jumlah Baru",
    min_value=1,
    max_value=5,
    value=1,
    key="jumlah_update"
)

if st.button("Update Tiket"):

    if kategori_baru == "VIP":
        harga_baru = konser_data[konser_baru]["vip"]

    else:
        harga_baru = konser_data[konser_baru]["regular"]

    hasil = st.session_state.tickets.update_tiket(
        kode_update,
        konser_baru,
        konser_data[konser_baru]["lokasi"],
        kategori_baru,
        seat_baru,
        harga_baru,
        jumlah_baru
    )

    if hasil == "berhasil":

        st.success("✅ Tiket berhasil diupdate!")

    elif hasil == "lunas":

        st.error(
            "❌ Tiket tidak bisa diupdate karena sudah lunas!"
        )

    elif hasil == "seat_digunakan":

        st.error("❌ Seat sudah digunakan")

    elif hasil == "stok_habis":

        st.error("❌ Stok tiket tidak cukup")

    else:

        st.error("❌ Kode tiket tidak ditemukan")

# =========================================================
# ADMIN PANEL
# =========================================================
if st.session_state.admin_login:

    st.divider()

    st.header("📊 Data Pemesanan")

    data = st.session_state.tickets.tampilkan_data()

    if data:

        cari = st.text_input("🔍 Cari Nama")

        if cari:

            hasil = []

            for item in data:

                if cari.lower() in item["Nama"].lower():
                    hasil.append(item)

            df = pd.DataFrame(hasil)

        else:

            df = pd.DataFrame(data)

        st.dataframe(df, use_container_width=True)

        # =============================================
        # STATISTIK
        # =============================================
        total_pembeli = len(data)

        total_penghasilan = 0

        current = st.session_state.tickets.head

        while current:

            total_penghasilan += current.total
            current = current.next

        st.metric(
            "💰 Total Penghasilan",
            f"Rp {total_penghasilan:,}"
        )

        st.metric(
            "👥 Total Pembeli",
            total_pembeli
        )

        # =============================================
        # KONFIRMASI PEMBAYARAN
        # =============================================
        st.divider()

        st.subheader("💳 Konfirmasi Pembayaran")

        kode_bayar = st.text_input(
            "Masukkan Kode Tiket Pembayaran"
        )

        if st.button("Konfirmasi Pembayaran"):

            current = st.session_state.tickets.head

            ditemukan = False

            while current:

                if current.kode == kode_bayar:

                    current.status = "Lunas"

                    ditemukan = True

                    break

                current = current.next

            if ditemukan:

                st.success(
                    "✅ Status pembayaran berhasil diubah menjadi Lunas"
                )

            else:

                st.error("❌ Kode tiket tidak ditemukan")

        # =============================================
        # HAPUS DATA
        # =============================================
        st.divider()

        st.subheader("🗑️ Hapus Tiket")

        kode_hapus = st.text_input("Kode Tiket")

        if st.button("Hapus Tiket"):

            hasil = st.session_state.tickets.hapus_tiket(
                kode_hapus
            )

            if hasil:

                st.success("✅ Tiket berhasil dihapus")

            else:

                st.error("❌ Kode tiket tidak ditemukan")

else:

    st.info(
        "👤 User hanya dapat memesan dan update tiket."
    )

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "© 2026 | Developed by MANIS - UAS Struktur Data"
)

