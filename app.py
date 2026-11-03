import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Auto Invoice Club Renang", layout="wide")

# --- FUNGSI TERBILANG OTOMATIS (RUPIAH) ---
def terbilang(n):
    angka = ["", "Satu", "Dua", "Tiga", "Empat", "Lima", "Enam", "Tujuh", "Delapan", "Sembilan", "Sepuluh", "Sebelas"]
    if n < 12: return angka[int(n)]
    elif n < 20: return terbilang(n - 10) + " Belas"
    elif n < 100: return terbilang(n // 10) + (" Puluh " + terbilang(n % 10) if n % 10 != 0 else " Puluh")
    elif n < 200: return "Seratus " + terbilang(n - 100)
    elif n < 1000: return terbilang(n // 100) + " Ratus " + terbilang(n % 100)
    elif n < 2000: return "Seribu " + terbilang(n - 1000)
    elif n < 1000000: return terbilang(n // 1000) + " Ribu " + terbilang(n % 1000)
    elif n < 1000000000: return terbilang(n // 1000000) + " Juta " + terbilang(n % 1000000)
    else: return str(n)

def format_rupiah(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# --- CSS UNTUK PRINT A4 ---
st.markdown("""
    <style>
    .invoice-box { max-width: 800px; margin: auto; padding: 30px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0,0,0,0.15); font-size: 16px; line-height: 24px; font-family: Arial, sans-serif; color: #000; background-color: #fff; }
    .header-title { text-align: center; font-weight: bold; font-size: 24px; margin-bottom: 0px; }
    .sub-title { text-align: center; font-weight: bold; font-size: 16px; margin-bottom: 20px; border-bottom: 2px solid #000; padding-bottom: 10px; }
    table { width: 100%; line-height: inherit; text-align: left; border-collapse: collapse; margin-bottom: 20px; }
    table td, table th { padding: 8px; vertical-align: top; border: 1px solid #ddd; }
    .no-border td { border: none; padding: 4px 8px; }
    .signature-box { margin-top: 40px; display: flex; justify-content: space-between; text-align: center; }
    .footer-note { margin-top: 30px; font-size: 12px; text-align: center; font-style: italic; }
    @media print {
        body * { visibility: hidden; }
        .invoice-box, .invoice-box * { visibility: visible; }
        .invoice-box { position: absolute; left: 0; top: 0; width: 100%; border: none; box-shadow: none; padding: 0; }
        .stApp { background-color: white; }
    }
    </style>
""", unsafe_allow_html=True)

col_input, col_preview = st.columns([1, 2])

# Inisialisasi variabel perhitungan
jml_peserta = 0
total_bayar = 0

with col_input:
    st.header("📂 1. Upload Data Kehadiran")
    uploaded_file = st.file_uploader("Upload File Rekap Excel (.xlsx / .xls)", type=["xlsx", "xls"])
    
    st.header("📝 2. Pengaturan Invoice")
    tarif_per_orang = st.number_input("Tarif per Kehadiran (Rp)", value=20000, step=5000)
    
    # PROSES EXCEL OTOMATIS
    default_club_name = "Nama Club..."
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            
            # Asumsi perhitungan: menghitung baris yang ada nama siswanya (mengabaikan baris kosong atau footer 'JUMLAH')
            # Mencari kolom yang mengandung kata 'NAMA'
            col_nama = [col for col in df.columns if 'NAMA' in str(col).upper()]
            if col_nama:
                valid_rows = df[df[col_nama[0]].notna()]
                # Singkirkan baris rekapitulasi bawah jika ada kata "JUMLAH"
                valid_rows = valid_rows[~valid_rows[col_nama[0]].astype(str).str.contains("JUMLAH", case=False)]
                jml_peserta = len(valid_rows)
            else:
                # Jika tidak ada kolom nama, kurangi 1 baris untuk footer jumlah
                jml_peserta = max(0, len(df) - 1)
                
            total_bayar = jml_peserta * tarif_per_orang
            st.success(f"✅ Data Terbaca! Total Peserta: **{jml_peserta} orang** | Total Tagihan: **{format_rupiah(total_bayar)}**")
            
            # Ambil nama club dari nama file
            default_club_name = uploaded_file.name.replace(".xlsx", "").replace(".xls", "").replace("REKAP KEHADIRAN", "").replace("LAPORAN KEHADIRAN", "").replace("OKTOBER 2026", "").strip().upper()
            
        except Exception as e:
            st.error(f"Gagal membaca data Excel: {e}")
    else:
        st.info("Silakan upload file Excel untuk menghitung otomatis.")

    # Form lanjutan
    no_invoice = st.text_input("No. Invoice", f"INV/KCW/{datetime.today().year}/{datetime.today().month:02d}-XXX")
    tgl_bayar = st.date_input("Tanggal Pembayaran", datetime.today())
    nama_club = st.text_input("Nama Club Renang", default_club_name)
    nama_pj = st.text_input("Nama Penanggung Jawab", "Bpk/Ibu ...")
    no_kontak = st.text_input("Nomor Kontak", "-")
    periode = st.text_input("Periode Latihan", "Oktober 2026")
    
    # Allow manual override for totals if needed
    total_bayar = st.number_input("Total Pembayaran Akhir (Rp)", value=total_bayar)
    
    metode = st.radio("Metode Pembayaran", ["Tunai", "Transfer", "QRIS"])
    petugas = st.text_input("Nama Penerima/Petugas", "Admin KCW")

# Konversi angka ke huruf
teks_terbilang = (terbilang(total_bayar) + " Rupiah").strip().title()

cb_tunai = "☑" if metode == "Tunai" else "☐"
cb_transfer = "☑" if metode == "Transfer" else "☐"
cb_qris = "☑" if metode == "QRIS" else "☐"

with col_preview:
    st.header("📄 3. Preview & Cetak")
    if uploaded_file is None:
        st.warning("Menunggu data diupload...")
    
    st.caption("💡 Tekan **Ctrl + P** (Windows) atau **Cmd + P** (Mac) untuk mencetak atau simpan ke PDF. Area input di kiri tidak akan ikut tercetak.")
    
    html_content = f"""<div class="invoice-box">
<div class="header-title">KAUMPANDAK CITY WATERPARK</div>
<div class="sub-title">BUKTI PEMBAYARAN BULANAN CLUB RENANG <br> | INVOICE PEMBAYARAN DITERIMA |</div>
<table class="no-border" style="margin-bottom: 20px;">
<tr><td width="30%"><strong>NO. INVOICE</strong></td><td width="5%">:</td><td>{no_invoice}</td></tr>
<tr><td><strong>STATUS PEMBAYARAN</strong></td><td>:</td><td><strong>LUNAS ✓</strong></td></tr>
<tr><td><strong>TANGGAL PEMBAYARAN</strong></td><td>:</td><td>{tgl_bayar.strftime("%d / %m / %Y")}</td></tr>
</table>
<strong>DITERIMA DARI:</strong>
<table class="no-border" style="margin-bottom: 20px;">
<tr><td width="30%">Nama Club Renang</td><td width="5%">:</td><td>{nama_club}</td></tr>
<tr><td>Nama Penanggung Jawab</td><td>:</td><td>{nama_pj}</td></tr>
<tr><td>Nomor Kontak</td><td>:</td><td>{no_kontak}</td></tr>
</table>
<strong>RINCIAN PEMBAYARAN:</strong>
<table>
<tr style="background-color: #f2f2f2;"><th width="5%">NO.</th><th width="45%">KETERANGAN</th><th width="15%" style="text-align: center;">JML PESERTA</th><th width="15%" style="text-align: center;">PERIODE</th><th width="20%" style="text-align: right;">TOTAL</th></tr>
<tr><td style="text-align: center;">1</td><td>Pembayaran bulanan club renang</td><td style="text-align: center;">{jml_peserta} orang</td><td style="text-align: center;">{periode}</td><td style="text-align: right;">{format_rupiah(total_bayar)}</td></tr>
</table>
<table class="no-border">
<tr><td width="30%"><strong>METODE PEMBAYARAN</strong></td><td width="5%">:</td><td>{cb_tunai} Tunai &nbsp;&nbsp;&nbsp; {cb_transfer} Transfer &nbsp;&nbsp;&nbsp; {cb_qris} QRIS</td></tr>
<tr><td>Keterangan / Referensi</td><td>:</td><td>-</td></tr>
<tr><td><strong>TOTAL DIBAYARKAN</strong></td><td>:</td><td><strong>{format_rupiah(total_bayar)}</strong></td></tr>
<tr><td><strong>Terbilang</strong></td><td>:</td><td><em>{teks_terbilang}</em></td></tr>
</table>
<p style="margin-top:20px;">Terima kasih telah memilih Kaumpandak City Waterpark sebagai tempat latihan club renang Anda.</p>
<div class="signature-box">
<div><p>PENERIMA / PETUGAS</p><br><br><br><p>( <strong>{petugas}</strong> )</p></div>
<div><p>PENGELOLA KAUMPANDAK CITY WATERPARK</p><br><br><br><p>( ........................................ )</p></div>
</div>
<div class="footer-note">Dokumen ini merupakan bukti pembayaran yang sah setelah pembayaran diterima oleh pihak Kaumpandak City Waterpark.</div>
</div>"""

    st.markdown(html_content, unsafe_allow_html=True)
