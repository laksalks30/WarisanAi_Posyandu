# 👶 Warisan.AI — Posyandu Gizi Agent
### *Sistem Deteksi Dini Stunting & Malnutrisi Balita Berbasis WHO Growth Standards Menggunakan IBM Langflow & IBM Bob*

[![Theme](https://img.shields.io/badge/Hackathon-National%20Hackathon%20Hacktiv8%20x%20IBM-0f62fe)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![Category](https://img.shields.io/badge/Category-Healthcare%20%26%20Wellbeing-1a6b45)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![Technology](https://img.shields.io/badge/Powered%20By-IBM%20Langflow%20%26%20IBM%20Bob-8a3ffc)](https://github.com/laksalks30/WarisanAi_Posyandu)
[![Standard](https://img.shields.io/badge/Standard-WHO%20%26%20Permenkes%20No.2%2F2020-orange)](https://github.com/laksalks30/WarisanAi_Posyandu)

---

## 📌 Latar Belakang & Masalah
Prevalensi stunting di Indonesia saat ini mencapai **21,5%** (SKI 2023), sementara target nasional pemerintah adalah menurunkannya hingga **14%**. Posyandu adalah garda terdepan dalam pemantauan tumbuh kembang balita, namun menghadapi tantangan nyata di lapangan:
1. **Kompleksitas Perhitungan Z-Score:** Kader posyandu adalah relawan komunitas non-medis yang kesulitan menghitung dan menginterpretasikan kurva pertumbuhan multivariat (*BB/U*, *TB/U*, *BB/TB*) standar WHO.
2. **Keterlambatan Rujukan:** Pencatatan manual di buku KIA fisik membuat data baru direkap bulanan, sehingga balita yang mengalami gizi buruk akut atau indikasi stunting terlambat dirujuk ke Puskesmas.
3. **Kesenjangan Komunikasi:** Bahasa medis (misal: *z-score -2.8 SD*) membingungkan ibu balita, memicu kepanikan tanpa solusi nyata.

**Warisan.AI** hadir sebagai solusi komprehensif yang mengotomatisasi kalkulasi antropometri presisi tinggi dan mengorkestrasikan kecerdasan buatan (*AI Agent*) untuk triaging risiko, pembuatan rekomendasi gizi berbasis pangan lokal, serta otomasi pelaporan langsung ke Bidan Desa.

---

## 🚀 Fitur Utama
- **⚡ Automated WHO Anthropometric Engine:** Menghitung z-score presisi secara instan untuk 3 indeks utama (**BB/U**, **TB/U** untuk stunting, **BB/TB** untuk wasting/gizi buruk akut) berdasarkan WHO Child Growth Standards & Permenkes RI No. 2 Tahun 2020.
- **🛡️ AI Early Warning & Clinical Triaging:** Memilah balita menjadi 3 kategori risiko: *Aman*, *Perlu Pemantauan Khusus*, dan *Perlu Rujukan Cepat/Bahaya*.
- **💬 Mother-Friendly AI Explainer:** Menerjemahkan angka z-score medis menjadi narasi edukasi yang ramah, empatik, dan mudah dicerna oleh orang tua balita.
- **🥗 Actionable Nutrition & PMT Recommendation:** Menghasilkan saran intervensi nutrisi spesifik usia yang kaya protein hewani lokal (telur, lele, tempe, kelor).
- **📲 Direct WhatsApp Integration:** Memungkinkan kader posyandu mengirimkan rekapitulasi balita berisiko ke Bidan Desa atau pesan edukasi ke orang tua balita dalam sekali klik via WhatsApp.
- **📄 Instant Posyandu Report Generator:** Menghasilkan draf laporan formal Posyandu yang siap dicetak untuk evaluasi Puskesmas.

---

## 🏗️ Arsitektur Sistem & Integrasi IBM Ecosystem

```
┌────────────────────────────────────────────────────────┐
│                   Kader Posyandu                       │
│     (Input: Nama, Usia, BB, TB, Jenis Kelamin)         │
└──────────────────────────┬─────────────────────────────┘
                           │ HTTP / UI
┌──────────────────────────▼─────────────────────────────┐
│             Warisan.AI Frontend Application            │
│       - Real-time WHO Anthropometric Engine (Client)   │
│       - WhatsApp Action & Medical Report Generator     │
└──────────────────────────┬─────────────────────────────┘
                           │ Model Context Protocol (MCP)
┌──────────────────────────▼─────────────────────────────┐
│                 IBM Bob Environment                    │
│   - Agentic Orchestrator & Scaffolding Platform        │
│   - MCP Proxy (`mcp-proxy.exe`, streamable HTTP)       │
│   - Component Lifecycle & Diagnostics Validation       │
└──────────────────────────┬─────────────────────────────┘
                           │ JSON Payload / API
┌──────────────────────────▼─────────────────────────────┐
│               IBM Langflow Cognitive Agent             │
│   1. ChatInput: Menangkap data penimbangan posyandu    │
│   2. Prompt Template: Basis aturan antropometri klinis │
│   3. Language Model: Penalaran diagnostik komposit     │
│   4. ChatOutput: Laporan terstruktur & triaging risiko │
└────────────────────────────────────────────────────────┘
```

### Peran IBM Langflow
Langflow bertindak sebagai **Cognitive Layer** yang memproses penalaran data balita melalui pipeline alur kerja kognitif di [`warisan-ai-flow.json`](./warisan-ai-flow.json):
- Mengekstrak data balita dan membandingkannya dengan acuan deviasi standar WHO.
- Mendeteksi korelasi bahaya stunting (TB/U < -2SD) dan malnutrisi akut (BB/TB < -3SD).
- Memformulasikan teks laporan klinis dan rencana intervensi.

### Peran IBM Bob
IBM Bob bertindak sebagai **Agentic Development Partner & System Orchestrator**:
- Mengelola konfigurasi server MCP di [`.bob/mcp.json`](./.bob/mcp.json) untuk menghubungkan agen cerdas Langflow ke aplikasi klien.
- Melakukan rapid prototyping dan optimasi performa frontend ramah kader.
- Menguji akurasi matematika tabel referensi data antropometri balita umur 0–60 bulan.

---

## 📁 Struktur Direktori
```
BOB_HACKATON/
├── .bob/
│   ├── artifacts/               # Artefak dan output pendukung IBM Bob
│   └── mcp.json                 # Konfigurasi Model Context Protocol (MCP) server
├── warisan-ai-app/
│   └── index.html               # Aplikasi web antarmuka kader posyandu
├── warisan-ai-flow.json         # Workflow export IBM Langflow Agent
├── .gitignore                   # Konfigurasi file git ignore
└── README.md                    # Dokumentasi lengkap proyek
```

---

## 💻 Panduan Menjalankan Aplikasi

### 1. Prasyarat
- Browser modern (Chrome, Edge, Firefox, Safari).
- Python 3.x (opsional, untuk menjalankan server HTTP lokal).

### 2. Menjalankan Frontend
Clone repository ini dan jalankan server lokal:
```bash
git clone https://github.com/laksalks30/WarisanAi_Posyandu.git
cd WarisanAi_Posyandu

# Jalankan HTTP server dengan Python
python -m http.server 3000 --directory warisan-ai-app
```
Akses aplikasi melalui browser:
```
http://localhost:3000
```

### 3. Mengimpor Alur Kerja Langflow
1. Buka antarmuka **IBM Langflow** Anda.
2. Pilih **Import / Upload Flow**.
3. Pilih file `warisan-ai-flow.json`.
4. Jalankan Playground atau hubungkan via MCP endpoint ke IBM Bob.

---

## 📊 Dampak yang Diharapkan
- **Waktu Analisis:** Dipangkas dari 30–45 menit menjadi kurang dari 10 detik per posyandu.
- **Akurasi Deteksi:** Mengeliminasi 100% kesalahan pembacaan manual grafik KMS konvensional.
- **Rujukan Cepat (*Same-Day Referral*):** Balita berisiko stunting dan gizi buruk langsung teridentifikasi hari itu juga di meja Posyandu dan diteruskan ke Bidan Desa.

---

## 👥 Pengembang
Dikembangkan untuk **National Hackathon (Hacktiv8 x IBM)**.  
*Repositori:* [github.com/laksalks30/WarisanAi_Posyandu](https://github.com/laksalks30/WarisanAi_Posyandu)
