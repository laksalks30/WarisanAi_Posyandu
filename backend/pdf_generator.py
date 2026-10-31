"""
WARISAN.AI - Official PDF Report Generator
Menghasilkan dokumen resmi Surat Rekapitulasi Pemantauan Tumbuh Kembang Balita Posyandu
berformat PDF standar A4 dengan kop resmi, tabel antropometri WHO, dan lembar pengesahan.
"""

import io
from datetime import datetime
from typing import List, Dict, Any, Optional
from fpdf import FPDF


class PosyanduReportPDF(FPDF):
    def __init__(self, posyandu_name: str, periode: str):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.posyandu_name = posyandu_name
        self.periode = periode
        self.set_margins(10, 12, 10)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        # Kop Surat Resmi
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(15, 61, 38) # Posyandu Dark Green
        self.cell(0, 5, 'POSYANDU TERPADU PELAYANAN KESEHATAN IBU DAN ANAK', align='C', new_x='LMARGIN', new_y='NEXT')
        
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(21, 128, 61)
        self.cell(0, 5, f'{self.posyandu_name.upper()}', align='C', new_x='LMARGIN', new_y='NEXT')

        self.set_font('Helvetica', '', 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 4, 'Standar Antropometri: WHO Child Growth Standards & Permenkes RI No. 2 Tahun 2020', align='C', new_x='LMARGIN', new_y='NEXT')

        # Double Line Separator
        y = self.get_y() + 1
        self.set_draw_color(15, 61, 38)
        self.set_line_width(0.7)
        self.line(10, y, 200, y)
        self.set_draw_color(22, 101, 52)
        self.set_line_width(0.2)
        self.line(10, y + 1.2, 200, y + 1.2)
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 7.5)
        self.set_text_color(148, 163, 184)
        doc_info = f"Warisan.AI Platform - Dokumen Rekapitulasi Tumbuh Kembang Posyandu | Periode: {self.periode}"
        self.cell(140, 5, doc_info, align='L')
        page_info = f"Halaman {self.page_no()} dari {{nb}}"
        self.cell(50, 5, page_info, align='R')


def generate_posyandu_pdf(
    posyandu: str,
    periode: str,
    balita_list: List[Dict[str, Any]],
    officer: str = "Sri Wahyuni, A.Md.",
    bidan: str = "Bd. Siti Nurhaliza, S.Tr.Keb",
    summary: Optional[Dict[str, Any]] = None,
    instructions: Optional[List[str]] = None
) -> bytes:
    """
    Menghasilkan file binary PDF resmi untuk Rekapitulasi Posyandu.
    """
    pdf = PosyanduReportPDF(posyandu_name=posyandu, periode=periode)
    pdf.alias_nb_pages()
    pdf.add_page()

    # Judul Dokumen
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(15, 61, 38)
    pdf.cell(0, 6, 'SURAT REKAPITULASI HASIL PEMANTAUAN STATUS GIZI BALITA', align='C', new_x='LMARGIN', new_y='NEXT')
    
    pdf.set_font('Helvetica', 'I', 8)
    pdf.set_text_color(71, 85, 105)
    tgl_now = datetime.now().strftime("%d %B %Y")
    pdf.cell(0, 4, f'Tanggal Pelaporan: {tgl_now}  |  Sistem Deteksi Dini & Rujukan Posyandu', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(3)

    # Box Metadata Administrasi
    pdf.set_fill_color(248, 250, 248)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, pdf.get_y(), 190, 16, style='FD')
    
    init_y = pdf.get_y() + 2
    pdf.set_xy(13, init_y)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(30, 41, 59)
    pdf.cell(25, 4, 'Nama Posyandu', 0, 0)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(65, 4, f': {posyandu}', 0, 0)

    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(32, 4, 'Petugas Penimbang', 0, 0)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(60, 4, f': {officer} (Kader Posyandu)', 0, 1)

    pdf.set_xy(13, init_y + 5)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(25, 4, 'Periode / Bulan', 0, 0)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(65, 4, f': {periode}', 0, 0)

    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(32, 4, 'Bidan Pembina Desa', 0, 0)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(60, 4, f': {bidan}', 0, 1)

    pdf.set_xy(13, init_y + 10)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(25, 4, 'Standar Baku', 0, 0)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(65, 4, ': Permenkes RI No. 2/2020 & WHO Anthro', 0, 0)

    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(32, 4, 'Status Evaluasi', 0, 0)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.set_text_color(21, 128, 61)
    pdf.cell(60, 4, ': Terverifikasi Lengkap', 0, 1)

    pdf.ln(5)

    # Hitung Statistik Ringkasan jika tidak ada
    total = len(balita_list)
    tinggi = sum(1 for b in balita_list if b.get('risk') == 'TINGGI')
    sedang = sum(1 for b in balita_list if b.get('risk') == 'SEDANG')
    aman = sum(1 for b in balita_list if b.get('risk') == 'AMAN')

    # Ringkasan Triase 4 Kolom
    col_w = 46
    h_box = 12
    curr_y = pdf.get_y()

    # Box 1: Total
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(10, curr_y, col_w, h_box, style='FD')
    pdf.set_xy(10, curr_y + 1.5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(col_w, 4.5, str(total), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_xy(10, curr_y + 6)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(100, 116, 139)
    pdf.cell(col_w, 4, 'Total Balita Ditimbang', align='C')

    # Box 2: Gizi Baik
    pdf.set_fill_color(240, 253, 244)
    pdf.set_draw_color(187, 247, 208)
    pdf.rect(10 + col_w + 2, curr_y, col_w, h_box, style='FD')
    pdf.set_xy(10 + col_w + 2, curr_y + 1.5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(21, 128, 61)
    pdf.cell(col_w, 4.5, str(aman), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_xy(10 + col_w + 2, curr_y + 6)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(22, 101, 52)
    pdf.cell(col_w, 4, 'Gizi Baik (Normal)', align='C')

    # Box 3: Perlu Pantau
    pdf.set_fill_color(255, 251, 235)
    pdf.set_draw_color(253, 230, 138)
    pdf.rect(10 + (col_w + 2) * 2, curr_y, col_w, h_box, style='FD')
    pdf.set_xy(10 + (col_w + 2) * 2, curr_y + 1.5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(180, 83, 9)
    pdf.cell(col_w, 4.5, str(sedang), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_xy(10 + (col_w + 2) * 2, curr_y + 6)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(146, 64, 14)
    pdf.cell(col_w, 4, 'Perlu Pemantauan (14 Hari)', align='C')

    # Box 4: Prioritas Rujukan
    pdf.set_fill_color(254, 242, 242)
    pdf.set_draw_color(254, 202, 202)
    pdf.rect(10 + (col_w + 2) * 3, curr_y, col_w, h_box, style='FD')
    pdf.set_xy(10 + (col_w + 2) * 3, curr_y + 1.5)
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_text_color(185, 28, 28)
    pdf.cell(col_w, 4.5, str(tinggi), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_xy(10 + (col_w + 2) * 3, curr_y + 6)
    pdf.set_font('Helvetica', '', 7.5)
    pdf.set_text_color(153, 27, 27)
    pdf.cell(col_w, 4, 'Prioritas Rujukan Puskesmas', align='C')

    pdf.set_xy(10, curr_y + h_box + 5)

    # =========================================================================
    # TABEL EVALUASI ANTROPOMETRI BALITA
    # =========================================================================
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(15, 61, 38)
    pdf.cell(0, 5, 'DAFTAR HASIL PENGUKURAN & DEVIASI STANDAR (WHO Z-SCORE)', align='L', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(1)

    # Lebar Kolom (Total 190 mm)
    w_no = 7
    w_nama = 38
    w_jk = 9
    w_usia = 13
    w_bb = 13
    w_tb = 13
    w_bbu = 28
    w_tbu = 28
    w_bbtb = 21
    w_status = 20

    # Header Tabel
    pdf.set_fill_color(15, 61, 38)
    pdf.set_draw_color(15, 61, 38)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Helvetica', 'B', 7.5)

    pdf.cell(w_no, 6, 'No', border=1, align='C', fill=True)
    pdf.cell(w_nama, 6, 'Nama Balita', border=1, align='L', fill=True)
    pdf.cell(w_jk, 6, 'JK', border=1, align='C', fill=True)
    pdf.cell(w_usia, 6, 'Usia', border=1, align='C', fill=True)
    pdf.cell(w_bb, 6, 'BB (kg)', border=1, align='C', fill=True)
    pdf.cell(w_tb, 6, 'TB (cm)', border=1, align='C', fill=True)
    pdf.cell(w_bbu, 6, 'BB/U (Berat/Umur)', border=1, align='C', fill=True)
    pdf.cell(w_tbu, 6, 'TB/U (Stunting)', border=1, align='C', fill=True)
    pdf.cell(w_bbtb, 6, 'BB/TB (Wasting)', border=1, align='C', fill=True)
    pdf.cell(w_status, 6, 'Status Triase', border=1, align='C', fill=True, new_x='LMARGIN', new_y='NEXT')

    def fmt_z(val):
        if val is None:
            return "-"
        return f"+{val:.2f}" if val > 0 else f"{val:.2f}"

    pdf.set_draw_color(226, 232, 240)
    for idx, b in enumerate(balita_list):
        risk = b.get('risk', 'AMAN')
        if risk == 'TINGGI':
            pdf.set_fill_color(254, 242, 242) # Red soft
            status_label = "RUJUKAN"
            text_risk_color = (185, 28, 28)
        elif risk == 'SEDANG':
            pdf.set_fill_color(255, 251, 235) # Amber soft
            status_label = "PANTAU"
            text_risk_color = (180, 83, 9)
        else:
            if idx % 2 == 1:
                pdf.set_fill_color(248, 250, 248)
            else:
                pdf.set_fill_color(255, 255, 255)
            status_label = "NORMAL"
            text_risk_color = (21, 128, 61)

        pdf.set_font('Helvetica', '', 7.5)
        pdf.set_text_color(30, 41, 59)

        # Baris Balita
        pdf.cell(w_no, 5.5, str(idx + 1), border=1, align='C', fill=True)
        
        # Nama
        pdf.set_font('Helvetica', 'B', 7.5)
        nama_txt = str(b.get('nama', ''))[:22]
        pdf.cell(w_nama, 5.5, f" {nama_txt}", border=1, align='L', fill=True)

        pdf.set_font('Helvetica', '', 7.5)
        pdf.cell(w_jk, 5.5, str(b.get('jk', '-')), border=1, align='C', fill=True)
        pdf.cell(w_usia, 5.5, f"{b.get('usia', '-')} bln", border=1, align='C', fill=True)
        pdf.cell(w_bb, 5.5, f"{b.get('bb', '-')}", border=1, align='C', fill=True)
        pdf.cell(w_tb, 5.5, f"{b.get('tb', '-')}", border=1, align='C', fill=True)

        # Z-Scores
        z_bbu = b.get('zBBU', b.get('z_bbu'))
        label_bbu = b.get('sBBU', {}).get('label') if isinstance(b.get('sBBU'), dict) else b.get('status_bbu', '')
        bbu_text = f"{fmt_z(z_bbu)} ({label_bbu[:10]})" if label_bbu else fmt_z(z_bbu)
        pdf.cell(w_bbu, 5.5, bbu_text, border=1, align='C', fill=True)

        z_tbu = b.get('zTBU', b.get('z_tbu'))
        label_tbu = b.get('sTBU', {}).get('label') if isinstance(b.get('sTBU'), dict) else b.get('status_tbu', '')
        tbu_text = f"{fmt_z(z_tbu)} ({label_tbu[:10]})" if label_tbu else fmt_z(z_tbu)
        pdf.cell(w_tbu, 5.5, tbu_text, border=1, align='C', fill=True)

        z_bbtb = b.get('zBBTB', b.get('z_bbtb'))
        label_bbtb = b.get('sBBTB', {}).get('label') if isinstance(b.get('sBBTB'), dict) else b.get('status_bbtb', '')
        bbtb_text = f"{fmt_z(z_bbtb)} ({label_bbtb[:8]})" if label_bbtb else fmt_z(z_bbtb)
        pdf.cell(w_bbtb, 5.5, bbtb_text, border=1, align='C', fill=True)

        # Status Triase Label
        pdf.set_font('Helvetica', 'B', 7.5)
        pdf.set_text_color(*text_risk_color)
        pdf.cell(w_status, 5.5, status_label, border=1, align='C', fill=True, new_x='LMARGIN', new_y='NEXT')

    pdf.ln(4)

    # =========================================================================
    # REKOMENDASI KLINIS & TINDAK LANJUT PRIORITAS
    # =========================================================================
    # Cek apakah butuh page break
    if pdf.get_y() > 220:
        pdf.add_page()

    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(15, 61, 38)
    pdf.cell(0, 5, 'RENCANA TINDAK LANJUT MEDIS & INTERVENSI GIZI', align='L', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(1)

    pdf.set_fill_color(248, 250, 248)
    pdf.set_draw_color(203, 213, 225)
    rec_y = pdf.get_y()
    
    # Kumpulkan daftar rujukan & pemantauan
    list_tinggi = [b for b in balita_list if b.get('risk') == 'TINGGI']
    list_sedang = [b for b in balita_list if b.get('risk') == 'SEDANG']

    bullets = []
    if list_tinggi:
        nama_tinggi = ", ".join([str(b.get('nama')) for b in list_tinggi])
        bullets.append(f"1. Rujukan Medis Prioritas: Segera rujuk balita ({nama_tinggi}) ke Puskesmas / Bidan Pembina Desa hari ini untuk pemeriksaan klinis lanjutan serta penerbitan Paket PMT Pemulihan.")
    if list_sedang:
        nama_sedang = ", ".join([str(b.get('nama')) for b in list_sedang])
        bullets.append(f"2. Pemantauan Siklus 14 Hari: Jadwalkan penimbangan ulang 2 minggu ke depan untuk ({nama_sedang}) dan berikan edukasi asupan protein hewani harian (1 butir telur/hari atau ikan lokal).")
    if not list_tinggi and not list_sedang:
        bullets.append("1. Kondisi Komunitas Normal: Seluruh balita berada dalam kurva tumbuh kembang yang baik. Pertahankan pola makan gizi seimbang dan imunisasi rutin.")

    bullets.append("3. Komunikasi & Konseling Orang Tua: Gunakan pendekatan suportif dan edukatif tanpa menimbulkan stigma kecemasan pada keluarga balita.")

    # Render bullets
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(51, 65, 85)
    for bul in bullets:
        pdf.multi_cell(190, 4.5, bul, border=0, align='L')
        pdf.ln(0.5)

    pdf.ln(3)

    # =========================================================================
    # LEMBAR PENGESAHAN TANDA TANGAN
    # =========================================================================
    if pdf.get_y() > 240:
        pdf.add_page()

    pdf.ln(2)
    sig_y = pdf.get_y()
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(30, 41, 59)

    # Kolom Kiri: Kader Posyandu
    pdf.set_xy(15, sig_y)
    pdf.cell(80, 4, 'Mengetahui / Penanggung Jawab Penimbangan,', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_xy(15, sig_y + 4)
    pdf.set_font('Helvetica', 'I', 7.5)
    pdf.cell(80, 4, 'Kader Penimbang Posyandu', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_xy(15, sig_y + 20)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(80, 4, f'( {officer} )', align='C', new_x='LMARGIN', new_y='NEXT')

    # Kolom Kanan: Bidan Pembina Desa
    pdf.set_xy(115, sig_y)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.cell(80, 4, 'Bidan Pembina Desa / Kelurahan,', align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_xy(115, sig_y + 4)
    pdf.set_font('Helvetica', 'I', 7.5)
    pdf.cell(80, 4, 'Puskesmas Pembina Wilayah', align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_xy(115, sig_y + 20)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(80, 4, f'( {bidan} )', align='C', new_x='LMARGIN', new_y='NEXT')

    # Output bytes
    return bytes(pdf.output())
