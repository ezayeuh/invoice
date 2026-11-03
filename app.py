import streamlit as st
from datetime import datetime

# Konfigurasi halaman harus menjadi pemanggilan Streamlit pertama
st.set_page_config(page_title="Invoice Club Renang - KCW", layout="wide")

# --- CSS UNTUK TAMPILAN A4 & PRINT ---
st.markdown("""
    <style>
    .invoice-box {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
        font-size: 16px;
        line-height: 24px;
        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        color: #000;
        background-color: #fff;
    }
    .header-title {
        text-align: center;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 20px;
        border-bottom: 2px solid #000;
        padding-bottom: 10px;
    }
    table {
        width: 100%;
        line-height: inherit;
        text-align: left;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    table td, table th {
        padding: 8px;
        vertical-align: top;
        border: 1px solid #ddd;
    }
    .no-border td {
        border: none;
        padding: 4px 8px;
    }
    .signature-box {
        margin-top: 40px;
        display: flex;
        justify-content: space-between;
        text-align: center;
    }
    .footer-note {
        margin-top: 30px;
        font-size: 12px;
        text-align: center;
        font-style: italic;
    }
    /* Konfigurasi Cetak: Menyembunyikan UI Streamlit dan input, hanya menampilkan invoice-box */
    @media print {
        body * { visibility: hidden; }
        .invoice-box, .invoice-box * { visibility: visible; }
        .invoice-box { position: absolute; left: 0; top: 0; width: 100%; border: none; box-shadow: none; padding: 0; }
        .stApp { background-color: white; }
    }
    </style>
""", unsafe_allow_html=True)

# Membuat 2 kolom: Kolom kiri (1 bagian) untuk Input, Kolom kanan (2 bagian) untuk Preview
col_input, col_preview = st.columns([1, 2])

# --- KOLOM KIRI: INPUT DATA ---
with col_input:
    st.header("📝 Form Input")
    
    no_invoice = st.text_input("No. Invoice", "INV/KCW/2026/001")
    tgl_bayar = st.date_input("Tanggal Pembayaran", datetime.today())
    
    st.subheader("Data Club")
    nama_club = st.text_input("Nama Club Renang", "Club Renang Tirta")
    nama_pj = st.text_input("Nama Penanggung Jawab", "Bpk. Budi")
    no_kontak = st.text_input("Nomor Kontak", "0812-XXXX-XXXX")
    
    st.subheader("Rincian")
    jml_peserta = st.number_input("Jumlah Peserta", min_value=1, value=10)
    periode = st.text_input("Periode", "November 2026")
    total_bayar = st.number_input("Total Pembayaran (Rp)", min_value=0, value=500000, step=50000)
    terbilang = st.text_input("Terbilang", "Lima Ratus Ribu Rupiah")
    
    st.subheader("Pembayaran")
    metode = st.radio("Metode Pembayaran", ["Tunai", "Transfer", "QRIS"])
    referensi = st.text_input("Keterangan / Ref (Opsional)", "-")
    petugas = st.text_input("Nama Penerima/Petugas", "Admin KCW")

# Fungsi format angka ke format Rupiah
def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# Logika Checkbox Metode Pembayaran
cb_tunai = "☑" if metode == "Tunai" else "☐"
cb_transfer = "☑" if metode == "Transfer" else "☐"
cb_qris = "☑" if metode == "QRIS" else "☐"

# --- KOLOM KANAN: PREVIEW INVOICE ---
with col_preview:
    st.header("📄 Preview Invoice")
    st.caption("💡 Tekan **Ctrl + P** (Windows) atau **Cmd + P** (Mac) untuk mencetak atau menyimpan sebagai PDF. Area form akan disembunyikan otomatis saat dicetak.")
    
    html_content = f"""
    <div class="invoice-box">
        <div class="header-title">KAUMPANDAK CITY WATERPARK</div>
        <div class="sub-title">BUKTI PEMBAYARAN BULANAN CLUB RENANG <br> | INVOICE PEMBAYARAN DITERIMA |</div>
        
        <table class="no-border" style="margin-bottom: 20px;">
            <tr>
                <td width="30%"><strong>NO. INVOICE</strong></td>
                <td width="5%">:</td>
                <td>{no_invoice}</td>
            </tr>
            <tr>
                <td><strong>STATUS PEMBAYARAN</strong></td>
                <td>:</td>
                <td><strong>LUNAS ✓</strong></td>
            </tr>
            <tr>
                <td><strong>TANGGAL PEMBAYARAN</strong></td>
                <td>:</td>
                <td>{tgl_bayar.strftime("%d / %m / %Y")}</td>
            </tr>
        </table>

        <strong>DITERIMA DARI:</strong>
        <table class="no-border" style="margin-bottom: 20px;">
            <tr>
                <td width="30%">Nama Club Renang</td>
                <td width="5%">:</td>
                <td>{nama_club}</td>
            </tr>
            <tr>
                <td>Nama Penanggung Jawab</td>
                <td>:</td>
                <td>{nama_pj}</td>
            </tr>
            <tr>
                <td>Nomor Kontak</td>
                <td>:</td>
                <td>{no_kontak}</td>
            </tr>
        </table>

        <strong>RINCIAN PEMBAYARAN:</strong>
        <table>
            <tr style="background-color: #f2f2f2;">
                <th width="5%">NO.</th>
                <th width="45%">KETERANGAN</th>
                <th width="15%" style="text-align: center;">JML PESERTA</th>
                <th width="15%" style="text-align: center;">PERIODE</th>
                <th width="20%" style="text-align: right;">TOTAL</th>
            </tr>
            <tr>
                <td style="text-align: center;">1</td>
                <td>Pembayaran bulanan club renang</td>
                <td style="text-align: center;">{jml_peserta} orang</td>
                <td style="text-align: center;">{periode}</td>
                <td style="text-align: right;">{format_rupiah(total_bayar)}</td>
            </tr>
        </table>

        <table class="no-border">
            <tr>
                <td width="30%"><strong>METODE PEMBAYARAN</strong></td>
                <td width="5%">:</td>
                <td>{cb_tunai} Tunai &nbsp;&nbsp;&nbsp; {cb_transfer} Transfer &nbsp;&nbsp;&nbsp; {cb_qris} QRIS</td>
            </tr>
            <tr>
                <td>Keterangan / Referensi</td>
                <td>:</td>
                <td>{referensi}</td>
            </tr>
            <tr>
                <td><strong>TOTAL DIBAYARKAN</strong></td>
                <td>:</td>
                <td><strong>{format_rupiah(total_bayar)}</strong></td>
            </tr>
            <tr>
                <td><strong>Terbilang</strong></td>
                <td>:</td>
                <td><em>{terbilang}</em></td>
            </tr>
        </table>

        <p style="margin-top:20px;">Terima kasih telah memilih Kaumpandak City Waterpark sebagai tempat latihan club renang Anda.</p>

        <div class="signature-box">
            <div>
                <p>PENERIMA / PETUGAS</p>
                <br><br><br>
                <p>( <strong>{petugas}</strong> )</p>
            </div>
            <div>
                <p>PENGELOLA KAUMPANDAK CITY WATERPARK</p>
                <br><br><br>
                <p>( ........................................ )</p>
            </div>
        </div>

        <div class="footer-note">
            Dokumen ini merupakan bukti pembayaran yang sah setelah pembayaran diterima oleh pihak Kaumpandak City Waterpark.
        </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
