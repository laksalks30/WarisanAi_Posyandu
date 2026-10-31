"""
WARISAN.AI - Legacy Data Profiler & Parity Validator
Modul pengolah data riwayat / lembar pencatatan posyandu format Excel & CSV.

Fitur:
- Pemetaan fleksibel ragam penamaan kolom kader Posyandu Indonesia.
- Parity Validator: Deteksi anomali biologis batas rentang WHO.
- Generator template resmi Posyandu (Excel .xlsx).
"""

import io
import re
import pandas as pd
from typing import List, Dict, Any, Tuple
from backend.anthro import validate_biometric_bounds, sanitize_name

# Sinonim nama kolom posyandu
COLUMN_SYNONYMS = {
    'nama': ['nama', 'nama balita', 'nama anak', 'nama lengkap', 'anak', 'nama_balita', 'balita'],
    'usia': ['usia', 'usia (bulan)', 'umur', 'umur (bulan)', 'umur (bln)', 'bln', 'bulan', 'usia_bulan', 'usia bulan', 'umur bulan'],
    'bb': ['bb', 'berat', 'berat badan', 'berat (kg)', 'bb (kg)', 'bb_kg', 'berat_badan', 'berat badan (kg)'],
    'tb': ['tb', 'tinggi', 'tinggi badan', 'tinggi (cm)', 'tb (cm)', 'panjang', 'panjang badan', 'pb', 'pb (cm)', 'tinggi badan (cm)', 'panjang badan (cm)'],
    'jk': ['jk', 'jenis kelamin', 'kelamin', 'sex', 'gender', 'l/p', 'l_p', 'lp', 'jenis kelamin (l/p)', 'jeniskelaminlp', 'jenis kelamin lp'],
    'bb_prev': ['bb lalu', 'bb bulan lalu', 'bb sebelumnya', 'berat lalu', 'bb_prev', 'prev_bb', 'bb_lalu', 'bb bulan lalu (kg)', 'berat bulan lalu (kg)']
}


def normalize_col(name: str) -> str:
    """Normalisasi string nama kolom untuk pencocokan toleran terhadap variasi kader."""
    raw = str(name).strip().lower()
    clean = re.sub(r'[^a-zA-Z0-9]', '', raw)
    
    # 1. Exact match on clean string
    for canonical, synonyms in COLUMN_SYNONYMS.items():
        for syn in synonyms:
            syn_clean = re.sub(r'[^a-zA-Z0-9]', '', syn.lower())
            if clean == syn_clean:
                return canonical
                
    # 2. Fuzzy substring check
    if 'kelamin' in raw or 'gender' in raw or raw == 'jk' or raw in ['l/p', 'lp']:
        return 'jk'
    if 'nama' in raw:
        return 'nama'
    if 'umur' in raw or 'usia' in raw or 'bln' in raw:
        return 'usia'
    if 'lalu' in raw or 'sebelum' in raw:
        return 'bb_prev'
    if 'berat' in raw or raw.startswith('bb'):
        return 'bb'
    if 'tinggi' in raw or 'panjang' in raw or raw.startswith('tb') or raw.startswith('pb'):
        return 'tb'
        
    return name


def parse_posyandu_file(file_bytes: bytes, filename: str) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Ekstrak data dari file Excel (.xlsx, .xls) atau CSV,
    lalu lakukan pemeriksaan Parity Validator.
    """
    warnings = []
    
    # Baca file
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(file_bytes))
        else:
            df = pd.read_excel(io.BytesIO(file_bytes))
    except Exception as e:
        raise ValueError(f"Gagal membaca berkas {filename}: {str(e)}")

    # Ganti nama kolom ke canonical
    new_cols = {}
    for col in df.columns:
        canonical = normalize_col(col)
        new_cols[col] = canonical
    df = df.rename(columns=new_cols)

    # Validasi kolom wajib
    required = ['nama', 'usia', 'bb', 'tb', 'jk']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib tidak ditemukan di berkas: {', '.join(missing)}. Pastikan ada kolom Nama, Usia, BB, TB, dan JK.")

    extracted = []
    for idx, row in df.iterrows():
        # Lewati baris kosong
        if pd.isna(row.get('nama')) and pd.isna(row.get('bb')):
            continue

        raw_nama = str(row.get('nama', '')).strip()
        nama = sanitize_name(raw_nama) if raw_nama else f"Balita #{idx+1}"

        # Parse Usia
        try:
            usia = int(float(row.get('usia', 0)))
        except (ValueError, TypeError):
            usia = 0

        # Parse BB
        try:
            bb = round(float(row.get('bb', 0.0)), 2)
        except (ValueError, TypeError):
            bb = 0.0

        # Parse TB
        try:
            tb = round(float(row.get('tb', 0.0)), 1)
        except (ValueError, TypeError):
            tb = 0.0

        # Parse JK
        raw_jk = str(row.get('jk', 'L')).strip().upper()
        jk = 'P' if ('P' in raw_jk or 'PEREMPUAN' in raw_jk) else 'L'

        # Parse BB Lalu (opsional)
        bb_prev = None
        if 'bb_prev' in df.columns and not pd.isna(row.get('bb_prev')):
            try:
                bb_prev = round(float(row.get('bb_prev')), 2)
            except (ValueError, TypeError):
                bb_prev = None

        # Parity Validator Check
        parity_issues = validate_biometric_bounds(usia, bb, tb)
        status = "WARNING" if parity_issues else "VALID"

        extracted.append({
            "id": idx + 1,
            "nama": nama,
            "usia": usia,
            "bb": bb,
            "tb": tb,
            "jk": jk,
            "bb_prev": bb_prev,
            "parity_status": status,
            "parity_issues": parity_issues
        })

    return extracted, warnings


def generate_posyandu_template_excel() -> bytes:
    """Menghasilkan file Excel template pencatatan posyandu resmi."""
    data = [
        {"Nama Balita": "Andi Pratama",    "Usia (Bulan)": 21, "BB (kg)": 8.5,  "TB (cm)": 78.0, "Jenis Kelamin (L/P)": "L", "BB Bulan Lalu (kg)": 8.4},
        {"Nama Balita": "Siti Rahayu",     "Usia (Bulan)": 31, "BB (kg)": 10.2, "TB (cm)": 82.0, "Jenis Kelamin (L/P)": "P", "BB Bulan Lalu (kg)": 10.1},
        {"Nama Balita": "Budi Santoso",    "Usia (Bulan)": 16, "BB (kg)": 7.1,  "TB (cm)": 70.0, "Jenis Kelamin (L/P)": "L", "BB Bulan Lalu (kg)": 7.3},
        {"Nama Balita": "Dewi Kusuma",     "Usia (Bulan)": 24, "BB (kg)": 9.8,  "TB (cm)": 84.0, "Jenis Kelamin (L/P)": "P", "BB Bulan Lalu (kg)": 9.6},
        {"Nama Balita": "Reza Firmansyah", "Usia (Bulan)": 14, "BB (kg)": 6.2,  "TB (cm)": 68.0, "Jenis Kelamin (L/P)": "L", "BB Bulan Lalu (kg)": 7.0},
    ]
    df = pd.DataFrame(data)
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Pencatatan_Posyandu')
    buf.seek(0)
    return buf.getvalue()
