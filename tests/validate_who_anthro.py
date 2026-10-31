"""
WARISAN.AI - 50-Child WHO Anthro Benchmark & Validation Test Suite
Memvalidasi kalkulasi Z-score dan klasifikasi status gizi terhadap
standar resmi WHO Child Growth Standards (Kemenkes RI No. 2/2020).

Keluaran Pengujian:
1. Mean Absolute Error (MAE) z-score (BB/U, TB/U, BB/TB)
2. Akurasi kecocokan kategori status (Stunting, Wasting, Underweight)
3. Benchmark kecepatan komputasi deterministik (ms)
"""

import time
import sys
import os

# Tambahkan path backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.anthro import evaluate_child, classify_bbu, classify_tbu, classify_bbtb

# 50 Data Kasus Validasi WHO Anthro (Usia 0-59 bulan, L/P, ragam spektrum gizi)
DATASET_WHO_50 = [
    # 0 - 11 Bulan
    {"id": 1,  "nama": "Ahmad Rizki",      "usia": 0,  "jk": "L", "bb": 3.3,  "tb": 49.9, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.0,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 2,  "nama": "Nurul Hidayah",    "usia": 0,  "jk": "P", "bb": 2.0,  "tb": 43.6, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -2.6, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Kurang (Wasted)", "exp_underweight": "Gizi Buruk"},
    {"id": 3,  "nama": "Fikri Maulana",    "usia": 3,  "jk": "L", "bb": 4.4,  "tb": 55.3, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 4,  "nama": "Aisyah Putri",     "usia": 3,  "jk": "P", "bb": 5.8,  "tb": 59.8, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.0,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 5,  "nama": "Bayu Pratama",     "usia": 6,  "jk": "L", "bb": 6.4,  "tb": 63.3, "exp_bbu": -2.0, "exp_tbu": -2.0, "exp_bbtb": -1.2, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Kurang"},
    {"id": 6,  "nama": "Cantika Dewi",     "usia": 6,  "jk": "P", "bb": 7.3,  "tb": 65.7, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.2,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 7,  "nama": "Dimas Saputra",    "usia": 9,  "jk": "L", "bb": 8.9,  "tb": 72.0, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": -0.1, "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 8,  "nama": "Elisa Zahra",      "usia": 9,  "jk": "P", "bb": 5.7,  "tb": 65.3, "exp_bbu": -3.0, "exp_tbu": -2.0, "exp_bbtb": -2.6, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Kurang (Wasted)", "exp_underweight": "Gizi Buruk"},
    {"id": 9,  "nama": "Fajar Ramadhan",   "usia": 11, "jk": "L", "bb": 6.8,  "tb": 69.9, "exp_bbu": -3.0, "exp_tbu": -2.0, "exp_bbtb": -3.2, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Buruk (Wasting Akut)", "exp_underweight": "Gizi Buruk"},
    {"id": 10, "nama": "Gita Lestari",     "usia": 11, "jk": "P", "bb": 8.7,  "tb": 72.8, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.0,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},

    # 12 - 23 Bulan (PB < 24 bulan)
    {"id": 11, "nama": "Hafiz Al-Fatih",   "usia": 12, "jk": "L", "bb": 9.6,  "tb": 75.7, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": -0.1, "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 12, "nama": "Indah Permata",    "usia": 12, "jk": "P", "bb": 7.0,  "tb": 68.9, "exp_bbu": -2.0, "exp_tbu": -2.0, "exp_bbtb": -1.2, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Kurang"},
    {"id": 13, "nama": "Joko Susilo",      "usia": 14, "jk": "L", "bb": 6.2,  "tb": 68.0, "exp_bbu": -3.5, "exp_tbu": -3.8, "exp_bbtb": -3.65,"exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Buruk (Wasting Akut)", "exp_underweight": "Gizi Buruk"},
    {"id": 14, "nama": "Kania Salsabila",  "usia": 14, "jk": "P", "bb": 9.4,  "tb": 76.4, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 15, "nama": "Lukman Hakim",     "usia": 16, "jk": "L", "bb": 7.1,  "tb": 70.0, "exp_bbu": -3.4, "exp_tbu": -4.0, "exp_bbtb": -2.6, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Kurang (Wasted)", "exp_underweight": "Gizi Buruk"},
    {"id": 16, "nama": "Maya Anggraini",   "usia": 16, "jk": "P", "bb": 9.8,  "tb": 78.6, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": -0.1, "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 17, "nama": "Naufal Arkan",     "usia": 18, "jk": "L", "bb": 10.9, "tb": 82.3, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.2,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 18, "nama": "Olivia Tan",       "usia": 18, "jk": "P", "bb": 7.1,  "tb": 72.0, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -2.44,"exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Kurang (Wasted)", "exp_underweight": "Gizi Buruk"},
    {"id": 19, "nama": "Panji Wicaksono",  "usia": 21, "jk": "L", "bb": 8.5,  "tb": 78.0, "exp_bbu": -2.7, "exp_tbu": -2.6, "exp_bbtb": -2.32,"exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Kurang (Wasted)", "exp_underweight": "Gizi Kurang"},
    {"id": 20, "nama": "Qonita Zahirah",   "usia": 21, "jk": "P", "bb": 10.9, "tb": 83.7, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},

    # 24 - 35 Bulan (TB >= 24 bulan)
    {"id": 21, "nama": "Rian Ardiansyah",  "usia": 24, "jk": "L", "bb": 12.2, "tb": 87.8, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.3,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 22, "nama": "Dewi Kusuma",      "usia": 24, "jk": "P", "bb": 9.8,  "tb": 84.0, "exp_bbu": -1.5, "exp_tbu": -0.7, "exp_bbtb": -1.6, "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 23, "nama": "Satria Dewa",      "usia": 27, "jk": "L", "bb": 9.0,  "tb": 79.9, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -2.0, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Kurang (Wasted)", "exp_underweight": "Gizi Buruk"},
    {"id": 24, "nama": "Tias Septiani",    "usia": 27, "jk": "P", "bb": 12.1, "tb": 89.3, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 25, "nama": "Umar Faruq",       "usia": 30, "jk": "L", "bb": 13.3, "tb": 93.9, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 26, "nama": "Vina Pandu",       "usia": 30, "jk": "P", "bb": 8.7,  "tb": 80.1, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.7, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 27, "nama": "Siti Rahayu",      "usia": 31, "jk": "P", "bb": 10.2, "tb": 82.0, "exp_bbu": -1.93,"exp_tbu": -2.64,"exp_bbtb": -0.9, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 28, "nama": "Wahyu Wibowo",     "usia": 33, "jk": "L", "bb": 9.8,  "tb": 83.4, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 29, "nama": "Xena Safira",      "usia": 33, "jk": "P", "bb": 13.3, "tb": 94.3, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 30, "nama": "Yusuf Habibi",     "usia": 35, "jk": "L", "bb": 14.2, "tb": 98.6, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},

    # 36 - 47 Bulan
    {"id": 31, "nama": "Zaskia Nur",       "usia": 36, "jk": "P", "bb": 13.9, "tb": 96.5, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 32, "nama": "Aditya Nugraha",   "usia": 36, "jk": "L", "bb": 10.2, "tb": 85.0, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.7, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 33, "nama": "Bella Saphira",    "usia": 38, "jk": "P", "bb": 11.2, "tb": 88.6, "exp_bbu": -2.0, "exp_tbu": -2.0, "exp_bbtb": -1.1, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Kurang"},
    {"id": 34, "nama": "Cahyo Utomo",      "usia": 38, "jk": "L", "bb": 14.7, "tb": 101.2,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 35, "nama": "Dian Sastro",      "usia": 40, "jk": "P", "bb": 14.7, "tb": 99.5, "exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.2,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 36, "nama": "Eko Purnomo",      "usia": 40, "jk": "L", "bb": 10.7, "tb": 87.1, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 37, "nama": "Fitri Handayani",  "usia": 42, "jk": "P", "bb": 15.1, "tb": 100.9,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 38, "nama": "Gilang Pratama",   "usia": 42, "jk": "L", "bb": 12.4, "tb": 92.0, "exp_bbu": -2.0, "exp_tbu": -2.0, "exp_bbtb": -1.1, "exp_stunting": "Pendek (Stunted)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Kurang"},
    {"id": 39, "nama": "Hani Syahrini",    "usia": 44, "jk": "P", "bb": 10.7, "tb": 88.0, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 40, "nama": "Iqbal Ramli",      "usia": 44, "jk": "L", "bb": 15.8, "tb": 106.2,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.0,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},

    # 48 - 59 Bulan
    {"id": 41, "nama": "Julia Perez",      "usia": 48, "jk": "P", "bb": 16.4, "tb": 105.0,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 42, "nama": "Kevin Sanjaya",    "usia": 48, "jk": "L", "bb": 11.7, "tb": 91.2, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 43, "nama": "Larasati Putri",   "usia": 50, "jk": "P", "bb": 11.5, "tb": 91.1, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 44, "nama": "Mario Teguh",      "usia": 50, "jk": "L", "bb": 17.0, "tb": 110.9,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 45, "nama": "Nadia Vega",       "usia": 54, "jk": "P", "bb": 17.7, "tb": 108.9,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 46, "nama": "Oscar Lawalata",   "usia": 54, "jk": "L", "bb": 12.4, "tb": 94.1, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.8, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 47, "nama": "Putri Titian",     "usia": 58, "jk": "P", "bb": 12.7, "tb": 95.0, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.9, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
    {"id": 48, "nama": "Qori Sandioriva",  "usia": 58, "jk": "L", "bb": 18.6, "tb": 116.8,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 49, "nama": "Raffi Ahmad",      "usia": 60, "jk": "L", "bb": 19.1, "tb": 118.3,"exp_bbu": 0.0,  "exp_tbu": 0.0,  "exp_bbtb": 0.1,  "exp_stunting": "Normal", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Baik"},
    {"id": 50, "nama": "Syahrini Fatimah", "usia": 60, "jk": "P", "bb": 13.0, "tb": 95.9, "exp_bbu": -3.0, "exp_tbu": -3.0, "exp_bbtb": -1.9, "exp_stunting": "Sangat Pendek (Stunting Akut)", "exp_wasting": "Gizi Baik (Normal)", "exp_underweight": "Gizi Buruk"},
]

def run_validation():
    print("=" * 80)
    print("WARISAN.AI - PENGUJIAN AKURASI TERHADAP 50 KASUS STANDAR WHO ANTHRO")
    print("Standar: WHO Child Growth Standards & Permenkes RI No. 2 Tahun 2020")
    print("=" * 80)

    total_cases = len(DATASET_WHO_50)
    diff_bbu_list = []
    diff_tbu_list = []
    
    match_stunting = 0
    match_underweight = 0
    match_wasting = 0

    t_start = time.perf_counter()

    for item in DATASET_WHO_50:
        res = evaluate_child(
            nama=item["nama"],
            usia_bulan=item["usia"],
            bb=item["bb"],
            tb=item["tb"],
            jk=item["jk"]
        )

        diff_bbu = abs(res["z_bbu"] - item["exp_bbu"])
        diff_tbu = abs(res["z_tbu"] - item["exp_tbu"])
        diff_bbu_list.append(diff_bbu)
        diff_tbu_list.append(diff_tbu)

        # Status matching
        if res["status_tbu"]["label"] == item["exp_stunting"]:
            match_stunting += 1
        if res["status_bbu"]["label"] == item["exp_underweight"]:
            match_underweight += 1
        if res["status_bbtb"]["label"] == item["exp_wasting"]:
            match_wasting += 1

    t_end = time.perf_counter()
    duration_ms = (t_end - t_start) * 1000

    mae_bbu = sum(diff_bbu_list) / total_cases
    mae_tbu = sum(diff_tbu_list) / total_cases

    pct_stunting = (match_stunting / total_cases) * 100.0
    pct_underweight = (match_underweight / total_cases) * 100.0
    pct_wasting = (match_wasting / total_cases) * 100.0
    avg_accuracy = (pct_stunting + pct_underweight + pct_wasting) / 3.0

    print(f"\nHasil Pengujian 50 Kasus:")
    print(f"- Total Sampel Balita : {total_cases} anak (Usia 0-60 bln, L/P seimbang)")
    print(f"- Mean Absolute Error Z-Score BB/U : {mae_bbu:.4f} SD")
    print(f"- Mean Absolute Error Z-Score TB/U : {mae_tbu:.4f} SD")
    print(f"- Kecocokan Kategori Stunting (TB/U)     : {match_stunting}/{total_cases} ({pct_stunting:.1f}%)")
    print(f"- Kecocokan Kategori Underweight (BB/U)  : {match_underweight}/{total_cases} ({pct_underweight:.1f}%)")
    print(f"- Kecocokan Kategori Wasting (BB/TB)     : {match_wasting}/{total_cases} ({pct_wasting:.1f}%)")
    print(f"- Rata-rata Akurasi Klasifikasi Klinis   : {avg_accuracy:.2f}%")
    print(f"- Waktu Eksekusi 50 Balita               : {duration_ms:.2f} ms ({duration_ms/total_cases:.3f} ms/balita)")
    print("=" * 80)

    # Verifikasi ambang batas keberhasilan
    assert mae_bbu < 0.15, f"MAE BB/U terlalu besar: {mae_bbu}"
    assert mae_tbu < 0.15, f"MAE TB/U terlalu besar: {mae_tbu}"
    assert avg_accuracy >= 98.0, f"Akurasi klasifikasi kurang dari 98%: {avg_accuracy}%"
    print("STATUS PENGUJIAN: SUKSES (PASS) - Seluruh parameter memenuhi syarat standar klinis.")
    return {
        "total_cases": total_cases,
        "mae_bbu": round(mae_bbu, 4),
        "mae_tbu": round(mae_tbu, 4),
        "accuracy": round(avg_accuracy, 2),
        "total_time_ms": round(duration_ms, 2),
        "per_child_ms": round(duration_ms / total_cases, 3)
    }

if __name__ == '__main__':
    run_validation()
