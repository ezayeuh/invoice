import streamlit as st
import pandas as pd
from datetime import datetime
import base64

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

# --- CSS PREVIEW BERWARNA & ELEGAN ---
st.markdown("""
    <style>
    .preview-box * { box-sizing: border-box; }
    .preview-box { 
        width: 100%; 
        max-width: 680px; 
        aspect-ratio: 1 / 1.414;
        margin: auto; 
        padding: 25px 35px; 
        border: 1px solid #e0e0e0; 
        border-top: 10px solid #008CBA;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
        font-size: 13.5px; 
        line-height: 20px; 
        font-family: 'Segoe UI', Arial, sans-serif; 
        color: #333; 
        background-color: #fff; 
        overflow-x: hidden;
    }
    .header-title { text-align: center; font-weight: 900; font-size: 24px; color: #005f8c; margin-bottom: 4px; letter-spacing: 0.5px; }
    .sub-title { text-align: center; font-weight: bold; font-size: 13.5px; background-color: #008CBA; color: #fff; margin-bottom: 15px; padding: 6px; border-radius: 4px; }
    table.main-table { width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 13.5px; table-layout: fixed; word-wrap: break-word; }
    table.main-table td, table.main-table th { padding: 7px 8px; vertical-align: top; border: 1px solid #ddd; }
    table.main-table th { background-color: #008CBA; color: #ffffff; border: 1px solid #007a99; }
    .no-border td { border: none; padding: 3px 6px; }
    .signature-box { margin-top: 25px; display: flex; justify-content: space-between; text-align: center; font-size: 13.5px; }
    .footer-note { margin-top: 15px; font-size: 10px; text-align: center; font-style: italic; color: #666; border-top: 1px dashed #ccc; padding-top: 8px; }
    .label-header { color: #005f8c; font-weight: bold; font-size: 14px; text-transform: uppercase; margin-bottom: 4px; display: inline-block;}
    
    @media print {
        * {
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }
    }
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

    no_invoice = st.text_input("No. Invoice", f"INV-KCW-{datetime.today().year}-{datetime.today().month:02d}-XXX")
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

cb_tunai = "&#9745;" if metode == "Tunai" else "&#9744;"
cb_transfer = "&#9745;" if metode == "Transfer" else "&#9744;"
cb_qris = "&#9745;" if metode == "QRIS" else "&#9744;"

qris_direct_url = "https://lh3.googleusercontent.com/d/1JOS14LsBavoY1RujGfkQ15Z30AMTHRR4"

clean_club = "".join(c for c in nama_club if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_")
clean_inv = "".join(c for c in no_invoice if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_")
safe_filename = f"{clean_club}_{clean_inv}.pdf"

if status_pembayaran == "LUNAS":
    judul_dokumen = "BUKTI PEMBAYARAN BULANAN CLUB RENANG <br> INVOICE PEMBAYARAN DITERIMA"
    label_status = '<span style="background-color: #28a745 !important; color: white !important; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;">LUNAS &check;</span>'
    label_tanggal = "TANGGAL PEMBAYARAN"
    label_penerima = "DITERIMA DARI:"
    teks_penutup = "Terima kasih telah memilih Kaumpandak City Waterpark sebagai tempat latihan club renang Anda."
    teks_footer = "Dokumen ini merupakan bukti pembayaran yang sah setelah pembayaran diterima oleh pihak pengelola."

    metode_pembayaran_html = f"""<table class="no-border" style="margin-bottom: 8px;"><tr><td width="30%"><strong>METODE PEMBAYARAN</strong></td><td width="5%">:</td><td>{cb_tunai} Tunai &nbsp;&nbsp; {cb_transfer} Transfer &nbsp;&nbsp; {cb_qris} QRIS</td></tr><tr><td>Keterangan / Ref. Pembayaran</td><td>:</td><td>{referensi}</td></tr><tr><td><strong>TOTAL DIBAYAR</strong></td><td>:</td><td><strong style="color: #008CBA !important; font-size: 14.5px;">{format_rupiah(total_bayar)}</strong></td></tr><tr><td><strong>Terbilang</strong></td><td>:</td><td><em>{teks_terbilang}</em></td></tr></table>"""
    info_pembayaran_html = ""
    penutup_html = f"""<p style="margin-top:10px; margin-bottom: 10px; font-weight: bold; color: #005f8c !important;">{teks_penutup}</p>"""
else:
    judul_dokumen = "TAGIHAN PEMBAYARAN BULANAN CLUB RENANG <br> INVOICE MENUNGGU PEMBAYARAN"
    label_status = '<span style="background-color: #dc3545 !important; color: white !important; padding: 4px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important;">BELUM LUNAS &#9203;</span>'
    label_tanggal = "TANGGAL INVOICE"
    label_penerima = "DITAGIHKAN KEPADA:"
    teks_penutup = "Terima kasih atas perhatian dan kerjasamanya."
    teks_footer = "Dokumen ini merupakan rincian tagihan resmi yang diterbitkan oleh manajemen Kaumpandak City Waterpark."

    metode_pembayaran_html = f"""<table class="no-border" style="margin-bottom: 8px;"><tr><td width="30%"><strong>TOTAL TAGIHAN</strong></td><td width="5%">:</td><td><strong style="color: #dc3545 !important; font-size: 14.5px;">{format_rupiah(total_bayar)}</strong></td></tr><tr><td><strong>Terbilang</strong></td><td>:</td><td><em>{teks_terbilang}</em></td></tr></table>"""

    # --- FIX TOTAL: Menggunakan tabel fix murni dengan vertical-align: middle agar 100% sejajar rata tengah ---
    info_pembayaran_html = f"""
    <p style="margin-top:6px; margin-bottom: 4px; font-weight: bold;">Mohon segera melakukan pelunasan tagihan melalui informasi pembayaran di bawah ini:</p>
    <table style="width: 100%; border-collapse: collapse; background-color: #f4f9fc !important; border: 1px solid #cce4ec; border-left: 5px solid #008CBA !important; margin-bottom: 10px;">
        <tr>
            <td style="width: 55%; padding: 12px 14px; vertical-align: middle !important; border: none; border-right: 1px solid #cce4ec; font-size: 12px; line-height: 18px;">
                <span style="font-weight: bold; color: #005f8c !important;">&#128179; TRANSFER BANK:</span><br>
                &bull; Bank BCA<br>
                &bull; No. Rek: <b>1234567890</b><br>
                &bull; a.n. Kaumpandak City Waterpark
            </td>
            <td style="width: 45%; padding: 12px 14px; vertical-align: middle !important; border: none; text-align: center; font-size: 12px;">
                <span style="font-weight: bold; color: #005f8c !important;">&#128241; PEMBAYARAN QRIS:</span><br>
                <img src="{qris_direct_url}" width="50" style="margin-top: 3px; border: 1px solid #ccc; padding: 2px; background: #fff; border-radius: 4px;"><br>
                <span style="font-size: 8.5px; color: #666;">Scan untuk Membayar</span>
            </td>
        </tr>
    </table>
    """
    penutup_html = f"""<p style="margin-top:8px; margin-bottom: 8px;">{teks_penutup}</p>"""

isi_invoice = f"""<div class="preview-box"><div class="header-title">KAUMPANDAK CITY WATERPARK</div><div class="sub-title">{judul_dokumen}</div><table class="no-border" style="margin-bottom: 12px;"><tr><td width="30%"><strong>NO. INVOICE</strong></td><td width="5%">:</td><td>{no_invoice}</td></tr><tr><td><strong>STATUS PEMBAYARAN</strong></td><td>:</td><td>{label_status}</td></tr><tr><td><strong>{label_tanggal}</strong></td><td>:</td><td>{tgl_bayar.strftime("%d %b %Y")}</td></tr></table><span class="label-header">{label_penerima}</span><table class="no-border" style="margin-bottom: 12px; border-left: 3px solid #008CBA; background-color: #fcfcfc !important;"><tr><td width="30%">Nama Club Renang</td><td width="5%">:</td><td><strong>{nama_club}</strong></td></tr><tr><td>Nama Penanggung Jawab</td><td>:</td><td>{nama_pj}</td></tr><tr><td>Nomor Kontak</td><td>:</td><td>{no_kontak}</td></tr></table><span class="label-header">RINCIAN PEMBAYARAN:</span><table class="main-table"><tr><th width="8%" style="text-align: center; white-space: nowrap;">NO.</th><th width="37%">KETERANGAN</th><th width="15%" style="text-align: center;">PESERTA</th><th width="15%" style="text-align: center;">PERIODE</th><th width="25%" style="text-align: right; padding-right: 15px;">TOTAL</th></tr><tr><td style="text-align: center;">1</td><td>{keterangan_tabel}</td><td style="text-align: center;">{jml_peserta} orang</td><td style="text-align: center;">{periode}</td><td style="text-align: right; padding-right: 15px;">{format_rupiah(total_bayar)}</td></tr></table>{metode_pembayaran_html}{info_pembayaran_html}{penutup_html}<div class="signature-box"><div><p>PENERIMA / PETUGAS</p><br><br><br><p>( <strong>{petugas}</strong> )</p></div><div><p>PENGELOLA KAUMPANDAK CITY WATERPARK</p><br><br><br><p>( ........................................ )</p></div></div><div class="footer-note">{teks_footer}</div></div>"""
isi_invoice_js = isi_invoice.replace('\n', ' ').replace('\r', '').replace('"', '\\"')

with col_preview:
    st.header("📄 3. Preview & Cetak")

    js_print_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
    body {{ margin: 0; padding: 0; font-family: Arial, sans-serif; }}
    .btn-print {{
        background-color: #008CBA; border: none; color: white; padding: 12px 24px;
        text-align: center; text-decoration: none; display: block; font-size: 16px;
        font-weight: bold; margin: 0; cursor: pointer; border-radius: 6px;
        width: 100%; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;
    }}
    .btn-print:hover {{ background-color: #007399; }}
    </style>
    </head>
    <body>
    <button class="btn-print" onclick="printInvoice()">🖨️ CETAK INVOICE SEKARANG (PRINT)</button>
    <script>
    function printInvoice() {{
        var printWindow = window.open('', '_blank');
        printWindow.document.write('<html><head><meta charset="utf-8"><title>{safe_filename}</title>');
        printWindow.document.write('<style>');
        printWindow.document.write('* {{ box-sizing: border-box; -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }}');
        printWindow.document.write('@page {{ size: A4 portrait; margin: 10mm; }} ');
        printWindow.document.write('body {{ font-family: "Segoe UI", Arial, sans-serif; color: #333; padding: 0; margin: 0; font-size: 13.5px; line-height: 20px; }} ');
        printWindow.document.write('.preview-box {{ width: 100% !important; max-width: 100% !important; border: none !important; border-top: 10px solid #008CBA !important; box-shadow: none !important; padding: 10px !important; margin: 0 !important; border-radius: 0 !important; }} ');
        printWindow.document.write('.header-title {{ text-align: center; font-weight: 900; font-size: 24px; color: #005f8c; margin-bottom: 4px; letter-spacing: 0.5px; }} ');
        printWindow.document.write('.sub-title {{ text-align: center; font-weight: bold; font-size: 13.5px; background-color: #008CBA !important; color: #fff !important; margin-bottom: 15px; padding: 6px; border-radius: 4px; }} ');
        printWindow.document.write('table.main-table {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; font-size: 13.5px; table-layout: fixed; word-wrap: break-word; }} ');
        printWindow.document.write('table.main-table td, table.main-table th {{ padding: 7px 8px; vertical-align: top; border: 1px solid #ddd; }} ');
        printWindow.document.write('table.main-table th {{ background-color: #008CBA !important; color: #ffffff !important; border: 1px solid #007a99; }} ');
        printWindow.document.write('.no-border td {{ border: none; padding: 3px 6px; }} ');
        printWindow.document.write('.signature-box {{ margin-top: 25px; display: flex; justify-content: space-between; text-align: center; font-size: 13.5px; }} ');
        printWindow.document.write('.footer-note {{ margin-top: 15px; font-size: 10px; text-align: center; font-style: italic; color: #666; border-top: 1px dashed #ccc; padding-top: 8px; }}');
        printWindow.document.write('.label-header {{ color: #005f8c; font-weight: bold; font-size: 14px; text-transform: uppercase; margin-bottom: 4px; display: inline-block; }}');
        printWindow.document.write('</style></head><body onload="document.title=&quot;{safe_filename}&quot;; window.print(); window.close();">');
        printWindow.document.write("{isi_invoice_js}");
        printWindow.document.write('</body></html>');
        printWindow.document.close();
    }}
    </script>
    </body>
    </html>
    """

    b64_iframe = base64.b64encode(js_print_code.encode('utf-8')).decode('utf-8')
    st.markdown(f'<iframe src="data:text/html;base64,{b64_iframe}" width="100%" height="70" style="border:none; overflow:hidden;" scrolling="no"></iframe>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="preview-box">{isi_invoice}</div>', unsafe_allow_html=True)
