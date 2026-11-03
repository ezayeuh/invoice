import streamlit as st
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="Auto Invoice Club Renang", layout="wide")

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

# --- CSS PREVIEW DI LAYAR STREAMLIT ---
st.markdown("""
    <style>
    .preview-box { max-width: 800px; margin: auto; padding: 20px; border: 1px solid #eee; box-shadow: 0 0 10px rgba(0,0,0,0.15); font-size: 13px; line-height: 18px; font-family: Arial, sans-serif; color: #000; background-color: #fff; }
    .header-title { text-align: center; font-weight: bold; font-size: 20px; margin-bottom: 0px; }
    .sub-title { text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 10px; border-bottom: 2px solid #000; padding-bottom: 5px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 8px; font-size: 13px; }
    table td, table th { padding: 4px 6px; vertical-align: top; border: 1px solid #ddd; }
    .no-border td { border: none; padding: 2px 6px; }
    .signature-box { margin-top: 15px; display: flex; justify-content: space-between; text-align: center; font-size: 13px; }
    .footer-note { margin-top: 8px; font-size: 10px; text-align: center; font-style: italic; }
    
    .payment-info { background-color: #f9f9f9; padding: 8px 10px; border-radius: 4px; border: 1px dashed #ccc; margin-top: 6px; font-size: 12px; line-height: 16px; }
    .payment-container { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
    .payment-left { flex: 1.2; }
    .payment-right { flex: 0.8; text-align: center; }
    </style>
""", unsafe_allow_html=True)

col_input, col_preview = st.columns([1, 2])

jml_peserta = 0
total_bayar = 0

with col_input:
    st.header("📂 1. Upload Data")
    uploaded_file = st.file_uploader("Upload Excel (.xlsx/.xls)", type=["xlsx", "xls"])
    
    st.header("📝 2. Pengaturan")
    status_pembayaran = st.radio("Status Dokumen", ["LUNAS", "BELUM LUNAS"], horizontal=True)
    tarif_per_orang = st.number_input("Tarif per Kehadiran (Rp)", value=20000, step=5000)
    
    default_club_name = "Nama Club..."
    if uploaded_file is not None:
        try:
            df_raw = pd.read_excel(uploaded_file, header=None)
            header_row_idx = -1
            for i in range(min(20, len(df_raw))):
                if df_raw.iloc[i].astype(str).str.upper().str.contains('NAMA').any():
                    header_row_idx = i
                    break
            
            if header_row_idx != -1:
                df_raw.columns = df_raw.iloc[header_row_idx]
                df = df_raw.iloc[header_row_idx + 1:].reset_index(drop=True)
                col_nama = [col for col in df_raw.columns if 'NAMA' in str(col).upper()]
                valid_rows = df[df[col_nama[0]].notna()]
                valid_rows = valid_rows[~valid_rows[col_nama[0]].astype(str).str.contains("JUMLAH|NAMA", case=False)]
                jml_peserta = len(valid_rows)
            else:
                jml_peserta = max(0, len(df_raw) - 1)
                
            total_bayar = jml_peserta * tarif_per_orang
            st.success(f"✅ Data Terbaca! Peserta: **{jml_peserta}** | Tagihan: **{format_rupiah(total_bayar)}**")
            default_club_name = uploaded_file.name.replace(".xlsx", "").replace(".xls", "").replace("REKAP KEHADIRAN", "").replace("LAPORAN KEHADIRAN", "").replace("OKTOBER 2026", "").strip().upper()
        except Exception as e:
            st.error(f"Gagal membaca Excel: {e}")

    no_invoice = st.text_input("No. Invoice", f"INV/KCW/{datetime.today().year}/{datetime.today().month:02d}-XXX")
    tgl_bayar = st.date_input("Tanggal Dokumen", datetime.today())
    nama_club = st.text_input("Nama Club Renang", default_club_name)
    nama_pj = st.text_input("Nama Penanggung Jawab", "Bpk/Ibu ...")
    no_kontak = st.text_input("Nomor Kontak", "-")
    
    keterangan_tabel = st.text_input("Keterangan di Tabel", "Pembayaran bulanan club renang")
    periode = st.text_input("Periode Latihan", "Oktober 2026")
    total_bayar = st.number_input("Total Pembayaran Akhir (Rp)", value=total_bayar)
    
    if status_pembayaran == "LUNAS":
        metode = st.radio("Metode Pembayaran", ["Tunai", "Transfer", "QRIS"], horizontal=True)
        referensi = st.text_input("Keterangan / Ref. Pembayaran", "-")
    else:
        metode = "Transfer"
        referensi = "-"
        
    petugas = st.text_input("Penerima/Petugas", "Admin KCW")

teks_terbilang = (terbilang(total_bayar) + " Rupiah").strip().title()
cb_tunai = "☑" if metode == "Tunai" else "☐"
cb_transfer = "☑" if metode == "Transfer" else "☐"
cb_qris = "☑" if metode == "QRIS" else "☐"

qris_direct_url = "https://lh3.googleusercontent.com/d/1ieFAk4P8UMt_I0Ue30ztC7JPX9RTi1Rz"

if status_pembayaran == "LUNAS":
    judul_dokumen = "BUKTI PEMBAYARAN BULANAN CLUB RENANG <br> | INVOICE PEMBAYARAN DITERIMA |"
    label_status = "<strong>LUNAS ✓</strong>"
    label_tanggal = "TANGGAL PEMBAYARAN"
    teks_penutup = "Terima kasih telah memilih Kaumpandak City Waterpark sebagai tempat latihan club renang Anda."
    teks_footer = "Dokumen ini merupakan bukti pembayaran yang sah setelah pembayaran diterima oleh pihak Kaumpandak City Waterpark."
    
    metode_pembayaran_html = f"""
    <table class="no-border" style="margin-bottom: 4px;">
    <tr><td width="30%"><strong>METODE PEMBAYARAN</strong></td><td width="5%">:</td><td>{cb_tunai} Tunai &nbsp;&nbsp; {cb_transfer} Transfer &nbsp;&nbsp; {cb_qris} QRIS</td></tr>
    <tr><td>Keterangan / Referensi</td><td>:</td><td>{referensi}</td></tr>
    <tr><td><strong>TOTAL DIBAYAR</strong></td><td>:</td><td><strong>{format_rupiah(total_bayar)}</strong></td></tr>
    <tr><td><strong>Terbilang</strong></td><td>:</td><td><em>{teks_terbilang}</em></td></tr>
    </table>
    """
    info_pembayaran_html = ""
    penutup_html = f"""<p style="margin-top:6px; margin-bottom: 6px;">{teks_penutup}</p>"""
else:
    judul_dokumen = "TAGIHAN PEMBAYARAN BULANAN CLUB RENANG <br> | INVOICE MENUNGGU PEMBAYARAN |"
    label_status = "<strong>BELUM LUNAS ⏳</strong>"
    label_tanggal = "TANGGAL INVOICE"
    teks_penutup = "Mohon segera melakukan pelunasan tagihan melalui informasi pembayaran di bawah ini. Terima kasih."
    teks_footer = "Dokumen ini merupakan rincian tagihan resmi yang diterbitkan oleh manajemen Kaumpandak City Waterpark."
    
    metode_pembayaran_html = f"""
    <table class="no-border" style="margin-bottom: 4px;">
    <tr><td width="30%"><strong>TOTAL TAGIHAN</strong></td><td width="5%">:</td><td><strong>{format_rupiah(total_bayar)}</strong></td></tr>
    <tr><td><strong>Terbilang</strong></td><td>:</td><td><em>{teks_terbilang}</em></td></tr>
    </table>
    """
    info_pembayaran_html = f"""
    <div class="payment-info">
        <div style="font-weight: bold; margin-bottom: 2px; border-bottom: 1px solid #ddd; padding-bottom: 2px;">INFORMASI PEMBAYARAN:</div>
        <div class="payment-container">
            <div class="payment-left"><b>Transfer Bank:</b><br>• Bank BCA | No. Rek: <b>1234567890</b><br>• a.n. Kaumpandak City Waterpark</div>
            <div class="payment-right"><b>QRIS:</b><br><img src='{qris_direct_url}' width='45' style='margin-top: 2px;'><br><span style='font-size: 8px; color: #555;'>Scan untuk Bayar</span></div>
        </div>
    </div>
    """
    penutup_html = f"""<p style="margin-top:6px; margin-bottom: 6px;">{teks_penutup}</p>"""

# Susunan HTML Invoice Bersih
isi_invoice = f"""
<div class="header-title">KAUMPANDAK CITY WATERPARK</div>
<div class="sub-title">{judul_dokumen}</div>
<table class="no-border" style="margin-bottom: 6px;">
<tr><td width="30%"><strong>NO. INVOICE</strong></td><td width="5%">:</td><td>{no_invoice}</td></tr>
<tr><td><strong>STATUS PEMBAYARAN</strong></td><td>:</td><td>{label_status}</td></tr>
<tr><td><strong>{label_tanggal}</strong></td><td>:</td><td>{tgl_bayar.strftime("%d / %m / %Y")}</td></tr>
</table>
<strong>DITERIMA DARI:</strong>
<table class="no-border" style="margin-bottom: 6px;">
<tr><td width="30%">Nama Club Renang</td><td width="5%">:</td><td>{nama_club}</td></tr>
<tr><td>Nama Penanggung Jawab</td><td>:</td><td>{nama_pj}</td></tr>
<tr><td>Nomor Kontak</td><td>:</td><td>{no_kontak}</td></tr>
</table>
<strong>RINCIAN PEMBAYARAN:</strong>
<table>
<tr style="background-color: #f2f2f2;"><th width="5%">NO.</th><th width="45%">KETERANGAN</th><th width="15%" style="text-align: center;">JML PESERTA</th><th width="15%" style="text-align: center;">PERIODE</th><th width="20%" style="text-align: right;">TOTAL</th></tr>
<tr><td style="text-align: center;">1</td><td>{keterangan_tabel}</td><td style="text-align: center;">{jml_peserta} orang</td><td style="text-align: center;">{periode}</td><td style="text-align: right;">{format_rupiah(total_bayar)}</td></tr>
</table>
{metode_pembayaran_html}
{info_pembayaran_html}
{penutup_html}
<div class="signature-box">
<div><p>PENERIMA / PETUGAS</p><br><br><p>( <strong>{petugas}</strong> )</p></div>
<div><p>PENGELOLA KAUMPANDAK CITY WATERPARK</p><br><br><p>( ........................................ )</p></div>
</div>
<div class="footer-note">{teks_footer}</div>
"""

# Escape string agar aman dibaca oleh Javascript pembuka jendela baru
isi_invoice_js = isi_invoice.replace('\n', ' ').replace('\r', '').replace('"', '\\"')

with col_preview:
    st.header("📄 3. Preview & Cetak")
    
    # Tombol Cetak Menggunakan New Window (100% Bersih, Tanpa Blok Hitam, Pas A4)
    js_print_code = f"""
    <button onclick="printInvoice()" style="
        background-color: #008CBA; border: none; color: white; padding: 12px 24px;
        text-align: center; text-decoration: none; display: block; font-size: 16px;
        font-weight: bold; margin: 0px 0px 15px 0px; cursor: pointer; border-radius: 6px;
        width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); font-family: Arial, sans-serif;
    ">
        🖨️ CETAK INVOICE SEKARANG (PRINT)
    </button>
    
    <script>
    function printInvoice() {{
        var printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><title>Print Invoice KCW</title>');
        printWindow.document.write('<style>');
        printWindow.document.write('@page {{ size: A4 portrait; margin: 5mm; }} ');
        printWindow.document.write('body {{ font-family: Arial, sans-serif; color: #000; padding: 15px; font-size: 13px; line-height: 18px; }} ');
        printWindow.document.write('.header-title {{ text-align: center; font-weight: bold; font-size: 20px; margin-bottom: 0px; }} ');
        printWindow.document.write('.sub-title {{ text-align: center; font-weight: bold; font-size: 14px; margin-bottom: 10px; border-bottom: 2px solid #000; padding-bottom: 5px; }} ');
        printWindow.document.write('table {{ width: 100%; border-collapse: collapse; margin-bottom: 8px; font-size: 13px; }} ');
        printWindow.document.write('table td, table th {{ padding: 4px 6px; vertical-align: top; border: 1px solid #ddd; }} ');
        printWindow.document.write('.no-border td {{ border: none; padding: 2px 6px; }} ');
        printWindow.document.write('.signature-box {{ margin-top: 15px; display: flex; justify-content: space-between; text-align: center; font-size: 13px; }} ');
        printWindow.document.write('.footer-note {{ margin-top: 8px; font-size: 10px; text-align: center; font-style: italic; }}');
        printWindow.document.write('.payment-info {{ background-color: #f9f9f9; padding: 8px 10px; border-radius: 4px; border: 1px dashed #ccc; margin-top: 6px; font-size: 12px; line-height: 16px; }}');
        printWindow.document.write('.payment-container {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }}');
        printWindow.document.write('.payment-left {{ flex: 1.2; }}');
        printWindow.document.write('.payment-right {{ flex: 0.8; text-align: center; }}');
        printWindow.document.write('</style></head><body>');
        printWindow.document.write("{isi_invoice_js}");
        printWindow.document.write('<script>window.onload = function() {{ window.print(); window.close(); }}<\\/script>');
        printWindow.document.write('</body></html>');
        printWindow.document.close();
    }}
    </script>
    """
    
    components.html(js_print_code, height=70)
    
    # Preview di Web Streamlit
    st.markdown(f'<div class="preview-box">{isi_invoice}</div>', unsafe_allow_html=True)
