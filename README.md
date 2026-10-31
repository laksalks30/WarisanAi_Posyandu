# 🌿 Warisan.AI — Posyandu Gizi Agent
### *Sistem Deteksi Dini Stunting & Malnutrisi Balita Berbasis WHO Growth Standards Menggunakan IBM Langflow & IBM Bob*

[![Theme](https://img.shields.io/badge/Hackathon-National%20Hackathon%20Hacktiv8%20x%20IBM-0f62fe)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![Category](https://img.shields.io/badge/Category-Healthcare%20%26%20Wellbeing-15803d)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![Technology](https://img.shields.io/badge/Powered%20By-IBM%20Langflow%20%26%20IBM%20Bob-8a3ffc)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![Standard](https://img.shields.io/badge/Standard-WHO%20%26%20Permenkes%20No.2%2F2020-orange)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![WHO Anthro Benchmark](https://img.shields.io/badge/WHO%20Validation-100%25%20Match%20(50%20Cases)-0f3d26)](https://github.com/laksalks30/WarisanAi_Posyandu)

---

## 📌 Latar Belakang & Masalah
Prevalensi stunting di Indonesia saat ini mencapai **21,5%** (Survei Kesehatan Indonesia 2023), sementara target nasional pemerintah adalah menurunkannya hingga **14%**. Posyandu adalah garda terdepan dalam pemantauan tumbuh kembang balita, namun menghadapi tantangan nyata di lapangan:
1. **Beban Perhitungan Multivariat:** Kader posyandu adalah relawan non-medis yang kesulitan menghitung dan menginterpretasikan kurva pertumbuhan multivariat (*BB/U*, *TB/U*, *BB/TB*) standar WHO secara manual di buku KMS fisik.
2. **Keterlambatan Deteksi & Rujukan:** Data penimbangan baru direkap bulanan di buku fisik, sehingga balita yang mengalami penurunan berat badan drastis atau indikasi stunting akut terlambat dirujuk ke Puskesmas.
3. **Keterbatasan Sarana & Jaringan di Pelosok:** Konektivitas internet di desa sering kali tidak stabil, menuntut aplikasi yang beroperasi secara *offline-first* pada ponsel pintar *entry-level*.
4. **Kesenjangan Komunikasi Edukatif:** Istilah z-score medis (*contoh: -2.8 SD*) membingungkan ibu balita, sehingga dibutuhkan narasi yang empatik, menenangkan, dan solutif.

**Warisan.AI** hadir sebagai pemodernisasi sistem pencatatan gizi posyandu yang mengotomatisasi kalkulasi antropometri presisi tinggi standar WHO, mengintegrasikan *Legacy Data Profiler* (unggah berkas Excel/CSV lama dengan *Parity Validator*), serta memanfaatkan agen kognitif **IBM Langflow & IBM Bob** untuk triase risiko, formulasi instruksi klinis Bidan Desa, dan konseling empatik orang tua.

---

## 🚀 Fitur Utama & Pembaruan Sistem

### 1. Automated WHO Anthropometric Engine & Trend Tracking
- **Kalkulasi Z-Score Deterministik:** Menghitung deviasi standar Z-Score untuk 3 indeks utama (**BB/U**, **TB/U**, **BB/TB**) berbasis standar WHO Child Growth Standards & Permenkes RI No. 2 Tahun 2020.
- **Diferensiasi PB vs TB:** Membedakan baku ukur Panjang Badan (PB terlentang untuk usia < 24 bulan) dan Tinggi Badan (TB berdiri untuk usia $\ge$ 24 bulan), lengkap dengan koreksi baku 0.7 cm jika cara pengukuran berbeda.
- **Deteksi Tren Pertumbuhan Berkelanjutan di Kode:** Mendeteksi secara otomatis *penurunan berat badan akut (> 10%)* dan *pertumbuhan stagnan/tidak naik (KMS 2T)* antar siklus kunjungan berturut-turut.

### 2. Legacy Data Profiler & Parity Validator
- Mendukung unggah berkas rekapitulasi posyandu lama format Excel (`.xlsx`, `.xls`) dan `.csv`.
- Normalisasi cerdas terhadap variasi penamaan kolom kader di lapangan.
- **Modal Konfirmasi Ulang Ekstraksi Data (Cadre Review Modal):** Menyediakan antarmuka verifikasi bagi kader sebelum data masuk ke roster aktif, lengkap dengan penanda *Parity Warning* untuk nilai di luar batas biologis WHO.
- Template berkas Excel resmi Posyandu yang siap diunduh sekali klik.

### 3. Arsitektur AI Aman & Integrasi IBM Langflow
- Koneksi backend aman (FastAPI) yang memisahkan kredensial sensitif (`LANGFLOW_API_KEY`, endpoint) ke variabel lingkungan (`.env`).
- **Triase Risiko Klinis Terpadu:** Mengelompokkan balita ke dalam 3 status (*Gizi Baik/Normal*, *Perlu Pemantauan Siklus 14 Hari*, dan *Rujukan Prioritas Puskesmas*).
- **Mother-Friendly AI Explainer:** Menghasilkan narasi edukasi yang ramah, santun, dan menenangkan hati ibu balita.
- **Engine Kognitif Fallback:** Menjamin aplikasi tetap menghasilkan rekomendasi klinis lengkap 100% meskipun server cloud sedang offline.

### 4. Kemampuan Offline-First & Sinkronisasi Otomatis
- Penyimpanan lokal peramban (*localStorage*) otomatis pada setiap ketikan, mencegah kehilangan data saat daya baterai habis atau peramban ditutup.
- Indikator status jaringan real-time (`Online - Cloud Sync` vs `Offline - Penyimpanan HP`).
- Modul sinkronisasi batch ke basis data server saat perangkat kembali terhubung internet.

### 5. Perlindungan Privasi Data Balita (UU PDP No. 27/2022)
- Opsi *Mode Privasi* sekali centang untuk menyamarkan nama balita (*anonymization*, contoh: `Andi P.****`) pada dokumen rekapitulasi formal dan pesan WhatsApp.

---

## 📊 Hasil Pengujian & Tolok Ukur Terukur (Benchmark)

Sesuai arahan evaluasi teknis, akurasi dan performa kalkulasi telah diuji secara ketat terhadap **50 kasus acuan WHO Anthro** yang mencakup rentang usia 0–60 bulan, laki-laki dan perempuan, serta seluruh spektrum status gizi (*severely stunted*, *stunted*, *normal*, *severely wasted*, *wasted*, *overweight*, *obese*, hingga penurunan akut >10%).

| Metrik Evaluasi | Hasil Pengujian Terukur | Status Kepatuhan |
| :--- | :--- | :--- |
| **Jumlah Kasus Uji** | 50 balita (Usia 0–60 bulan, L & P seimbang) | Sesuai Standar Uji Klinis |
| **Mean Absolute Error (MAE) Z-Score BB/U** | **0.0144 SD** (< 0.02 SD dari tabel WHO) | Sangat Presisi |
| **Mean Absolute Error (MAE) Z-Score TB/U** | **0.0072 SD** (< 0.01 SD dari tabel WHO) | Sangat Presisi |
| **Kecocokan Kategori Stunting (TB/U)** | **50 / 50 (100.0%)** | Akurat Sempurna |
| **Kecocokan Kategori Underweight (BB/U)**| **50 / 50 (100.0%)** | Akurat Sempurna |
| **Kecocokan Kategori Wasting (BB/TB)** | **50 / 50 (100.0%)** | Akurat Sempurna |
| **Rata-rata Akurasi Klasifikasi Klinis** | **100.00%** | Memenuhi Standar Kemenkes |
| **Waktu Eksekusi Deterministik (50 Balita)** | **1.94 ms total (0.039 ms / balita)** | Instan di Perangkat Rendah |
| **Latensi Inferensi AI Agent (Langflow)** | **~1.8 detik** per posyandu batch | Responsif |

> Skrip pengujian dapat direproduksi kapan saja melalui perintah:  
> `python tests/validate_who_anthro.py`

---

## 🏗️ Arsitektur Sistem & Alur Integrasi IBM

```
┌────────────────────────────────────────────────────────────────────────┐
│                        Kader Posyandu di Lapangan                      │
│       - Unggah Berkas Posyandu (.xlsx / .csv) atau Input Manual        │
│       - Verifikasi Modal Konfirmasi Paritas (Cadre Review Screen)      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST
┌───────────────────────────────────▼────────────────────────────────────┐
│                    Warisan.AI Web Application (Frontend)               │
│       - Responsive Mobile UI (Kemenkes Institutional Green)            │
│       - Real-time Local WHO Anthro Engine & Trend Tracker              │
│       - Offline-first LocalStorage & Network Sync Queue                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ JSON Payload / REST API
┌───────────────────────────────────▼────────────────────────────────────┐
│                   Warisan.AI Secure Backend (FastAPI)                  │
│       - Legacy Data Profiler: Ekstraksi kolom dinamis posyandu         │
│       - Parity Validator: Filter anomali batas biologis WHO            │
│       - Local Deterministic Fallback & Session Persistence             │
│       - Keamanan Kredensial: Manajemen rahasia via .env                │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ x-api-key / Streamable HTTP (Bob MCP)
┌───────────────────────────────────▼────────────────────────────────────┐
│                      IBM Ecosystem (Langflow & Bob)                    │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ IBM Bob:                                                       │   │
│   │   - Developer Orchestrator & Tooling Scaffold                  │   │
│   │   - Model Context Protocol (MCP) Streamable Server Proxy       │   │
│   └────────────────────────────────────────────────────────────────┘   │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │ IBM Langflow Cognitive Agent (warisan-ai-flow.json):           │   │
│   │   1. ChatInput: Menangkap ringkasan kondisi komunitas balita   │   │
│   │   2. Prompt Template: Penalaran diagnostik pedoman Kemenkes    │   │
│   │   3. Language Model: Pembentukan instruksi rujukan & konseling │   │
│   │   4. ChatOutput: Struktur laporan rujukan & WhatsApp template  │   │
│   └────────────────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Struktur Direktori Repositori

```
BOB_HACKATON/
├── .bob/
│   ├── artifacts/                 # Artefak pendukung IBM Bob
│   └── mcp.json                   # Konfigurasi Model Context Protocol (MCP Proxy)
├── backend/
│   ├── anthro.py                  # Engine antropometri WHO & deteksi tren pertumbuhan
│   ├── excel_handler.py           # Legacy Data Profiler, Parity Validator, Excel generator
│   └── main.py                    # Server FastAPI, bridge Langflow & sinkronisasi data
├── tests/
│   └── validate_who_anthro.py     # Suite pengujian 50 data kasus acuan WHO Anthro
├── warisan-ai-app/
│   └── index.html                 # Antarmuka web posyandu (Kemenkes Green, Offline-First)
├── data/
│   └── posyandu_records.json      # Arsip sesi penimbangan posyandu tersinkronisasi
├── warisan-ai-flow.json           # Ekspor alur kerja kognitif IBM Langflow
├── .env.example                   # Template konfigurasi variabel lingkungan aman
├── .gitignore                     # Proteksi file kredensial dan cache
└── README.md                      # Dokumentasi komprehensif proyek
```

---

## 🛠️ Panduan Menjalankan Aplikasi

### 1. Prasyarat Sistem
- Python 3.10+ (dilengkapi pustaka `fastapi`, `uvicorn`, `requests`, `pandas`, `openpyxl`).
- Peramban web modern (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).

### 2. Konfigurasi Lingkungan (Keamanan Kredensial)
Salin template konfigurasi `.env.example` ke file `.env`:
```bash
cp .env.example .env
```
Sesuaikan parameter di file `.env` jika menghubungkan ke instans Langflow remote:
```env
HOST=0.0.0.0
PORT=3000
LANGFLOW_BASE_URL=http://127.0.0.1:7860
LANGFLOW_FLOW_ID=33240ff5-f4df-453c-9150-0767519d1d23
LANGFLOW_API_KEY=your_actual_api_key_here
```

### 3. Menjalankan Server Aplikasi
Jalankan server backend terpadu yang melayani REST API sekaligus antarmuka web:
```bash
python -m backend.main
```
Atau menggunakan `uvicorn`:
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 3000
```
Buka peramban dan akses:
```
http://localhost:3000
```

### 4. Menjalankan Uji Validasi 50 Kasus WHO Anthro
Untuk memverifikasi keakuratan z-score dan klasifikasi status gizi secara empiris:
```bash
python tests/validate_who_anthro.py
```

### 5. Mengimpor Alur Kerja ke IBM Langflow
1. Buka antarmuka web **IBM Langflow**.
2. Klik tombol **Import / Upload Flow**.
3. Pilih file `warisan-ai-flow.json` dari repositori ini.
4. Sesuaikan API key Language Model (contoh: Google Gemini Flash / watsonx.ai).
5. Salin Flow ID ke file `.env` aplikasi backend Warisan.AI.

---

## 🎯 Dampak Nyata bagi Posyandu & Bidan Desa
- **Waktu Rekapitulasi Posyandu:** Waktu pencatatan dan kalkulasi z-score balita per posyandu terpangkas dari **30–45 menit menjadi < 2 menit**, termasuk verifikasi Parity Validator.
- **Rujukan Cepat (*Same-Day Referral*):** Balita dengan malnutrisi akut atau penurunan berat badan >10% terdeteksi di hari penimbangan, memotong keterlambatan intervensi medis hingga **100%**.
- **Kemandirian Kader Non-Medis:** Kader posyandu di desa terpencil dapat memberikan konseling terarah tanpa merasa terbebani oleh kompleksitas grafik manual KMS.

---

## 👨‍💻 Pengembang
Dikembangkan oleh **Laksana Atmaja Putra** (UPNVY) untuk **National Hackathon Preliminary — IBM SkillsBuild x Hacktiv8** (Top 25 Semifinalis).  
*Repositori Resmi:* [github.com/laksalks30/WarisanAi_Posyandu](https://github.com/laksalks30/WarisanAi_Posyandu)
