# 🚀 Gemini Mode Argon Suite v2.0 (`gemini-mode-argon`)

[English](README.md) | **Bahasa Indonesia**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/google)
[![Reasoning](https://img.shields.io/badge/Reasoning-Frontier--Grade-orange.svg)](#)
[![Version](https://img.shields.io/badge/Version-2.1.0-emerald.svg)](#)

Mesin operasional dan penalaran berkinerja tinggi untuk **Google Antigravity**, dirancang untuk menghadirkan disiplin penalaran kelas *frontier*, spesialisasi peran otomatis (*Autonomous Role Dispatching*), dan eksekusi terminal mandiri (*Terminal Auto-Healing*) ke dalam alur kerja agen berbasis Gemini dengan **Spesifikasi Paritas Argon v2.0**.

---

## 🌟 Fitur Utama & Arsitektur Paritas Argon v2.0

* **Arsitektur Dua Jalur (Two-Track Architecture):** Memisahkan **Kalibrasi Tingkat Penalaran** (`low`, `medium`, `high`, `auto`) dari **Spesialisasi Peran** (13 domain lintas suite teknikal, kreatif, dan finansial).
* **Stateful Cognitive Anchor & Telemetri Strike:** Baris pertama badge status aktif kini mencantumkan telemetri kegagalan (`| Strike: <0-2>/2`) secara transparan untuk mencegah amnesia konteks antar-turn percakapan.
* **Komposisi Peran Hibrida (Hybrid Role Composition):** Menggabungkan 2 spesialisasi teknis (misal: `[AUTO: trader + dba]` atau `[AUTO: devops + reviewer]`) secara dinamis saat instruksi melintasi dua domain tanpa terdegradasi ke peran umum.
* **Pivot Dinamis di Tengah Giliran (Mid-Flight Dynamic Pivot):** Membatalkan keterikatan hipotesis awal seketika saat inspeksi berkas atau terminal menemukan kompleksitas arsitektur tersembunyi.
* **Eskalasi Level Deterministik:** Batasan tegas pemilihan level penalaran (`low` <15 baris tanpa mutasi berkas, `medium` untuk audit/desain, `high` untuk koding/migrasi/risiko finansial).
* **3 Blueprint Output Sesuai Domain (Aturan Asimetri Token 15/85):** Alokasi kuota token ketat: maksimal $\le 15\%$ token untuk Pre-Flight dan framing struktural; minimal $\ge 85\%$ token dialokasikan untuk implementasi kode teknis utuh (*Affirmative Completeness*) pada Blueprint A (Makro), B (Rekayasa), dan C (Audit/Gate).
* **Anti-Reward-Hacking Gate:** Auto-healing terminal melarang keras pelemahan assertion unit test, penghapusan test yang gagal, atau penambahan supresi tipe demi mengejar exit code 0 palsu.
* **Zero-Strike MCP & CLI Graceful Fallback:** Otomatis beralih menghasilkan artefak kode mandiri produksi jika server MCP eksternal (Figma, Affinity Designer, Blender bpy, MT5/Binance) sedang luring (*offline*).
* **Eksekusi Terminal Bersih Konteks:** Menggunakan pipa dan flag non-interaktif (`CI=true`, `--quiet`, `| tail -n 80`) agar buffer memori prompt tidak tertimbun log terminal masif.

---

## 🏛 Gambaran Arsitektur

```
                                      [Prompt Pengguna]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
         [Jalur 1: Auto-Level]                         [Jalur 2: Auto-Role]
      (Kalibrasi Tingkat Penalaran)                  (Spesialisasi Peran Otonom)
   ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
   │ • low    : Cepat / System 1 (<1s)│        │ • engineer   : Koding bedah      │
   │ • medium : CoT Seimbang (1-3s)   │        │ • architect  : Makro & ADR       │
   │ • high   : Refleksi & Auto-Heal  │        │ • reviewer   : Audit zero-trust  │
   │ • auto   : Heuristik Deterministik│       │ • tester     : QA & hermetic mock│
   └──────────────────────────────────┘        │ • dba        : SQL & EXPLAIN     │
                                               │ • devops     : SRE & CI/CD       │
                                               │ • researcher : Riset sumber data │
                                               │ • general    : Analisis umum     │
                                               ├──────────────────────────────────┤
                                               │ • ui-designer: Figma & Tokens    │
                                               │ • vector-des.: Affinity & SVG    │
                                               │ • 3d-designer: Blender & glTF    │
                                               │ • motion-des.: Video & Easing    │
                                               ├──────────────────────────────────┤
                                               │ • trader     : Sentinel & Quant  │
                                               ├──────────────────────────────────┤
                                               │ • Hibrida    : [peran1 + peran2] │
                                               └──────────────────────────────────┘
```

---

## ⚙️ Rekomendasi Konfigurasi Optimal

Untuk kombinasi kecepatan throughput dan kedalaman logika terbaik:

1. **Mesin (UI Antigravity):** Set model ke **`Gemini 3.8 Flash (High)`**
   * Memberikan alokasi kuota token penalaran (*Chain-of-Thought*) maksimal tanpa penalti latensi (tetap sangat responsif).
2. **Disiplin Kerja (Plugin):** Biarkan pada mode **`auto`**
   * Aktifkan dengan perintah: `/gemini-mode-argon on`
   * Bekerja adaptif: menjawab instan untuk pertanyaan biasa, dan otomatis mengeluarkan daya penuh *Pre-Flight + Auto-Healing* saat koding rumit.

---

## 📦 Panduan Instalasi

Pasang ke dalam direktori Antigravity lokal Anda dengan menjalankan satu perintah ini di terminal:

```bash
git clone https://github.com/diinggos/gemini-mode-argon.git ~/.gemini/config/plugins/gemini-mode-argon
```

Buka kembali Antigravity atau mulai percakapan baru. Sistem akan langsung mendeteksi dan memuat plugin secara otomatis.

---

## 🕹 Panduan Perintah Slash

### 1. Kontrol Utama
* `/gemini-mode-argon on` (atau cukup `/gemini-mode-argon`): Mengaktifkan Full-Auto Mode (*Auto-Role* + *Auto-Level*).
* `/gemini-mode-argon off`: Menonaktifkan plugin dan kembali ke perilaku bawaan asisten.
* `/gemini-mode-argon token-saver [on|off]`: Mengaktifkan/menonaktifkan mode hemat token tanpa basa-basi (`| token-saver: ON`), hanya mengeluarkan checklist Pre-Flight dan kode produksi utuh.

### 2. Override Tingkat Penalaran (Level)
* `/gemini-mode-argon level auto`: Eskalasi dinamis berdasarkan heuristik deterministik *(default)*.
* `/gemini-mode-argon level low`: Mode cepat System 1; tanpa overhead Pre-Flight (< 1 detik).
* `/gemini-mode-argon level medium`: Mode System 2 seimbang dengan Pre-Flight ringkas 3–5 poin (1–3 detik).
* `/gemini-mode-argon level high`: Reflexion System 2 mendalam dengan eksekusi terminal dan auto-healing mandiri (5–10 detik).

### 3. Override Peran Tertentu (Role)
* `/gemini-mode-argon role auto`: Deteksi peran otonom *(default)*.
* **Suite Teknikal:**
  * `/gemini-mode-argon-engineer on`: Kunci ke mode Principal Software Engineer.
  * `/gemini-mode-argon-architect on`: Kunci ke mode Principal Systems Architect.
  * `/gemini-mode-argon-reviewer on`: Kunci ke mode Read-Only Security Auditor & Reviewer.
  * `/gemini-mode-argon-tester on`: Kunci ke mode QA & Test Automation Specialist.
  * `/gemini-mode-argon-dba on`: Kunci ke mode Database Administrator & SQL Performance.
  * `/gemini-mode-argon-devops on`: Kunci ke mode SRE & Infrastructure Automation.
  * `/gemini-mode-argon-researcher on`: Kunci ke mode Peneliti Teknis & Verifikasi Fakta.
  * `/gemini-mode-argon-general on`: Kunci ke mode Pemecah Masalah Lintas Domain.
* **Suite Kreatif:**
  * `/gemini-mode-argon-ui-designer on`: Kunci ke mode Principal UI/UX & Design Systems.
  * `/gemini-mode-argon-vector-designer on`: Kunci ke mode Precision Vector & Affinity Designer.
  * `/gemini-mode-argon-3d-designer on`: Kunci ke mode 3D Artist & Blender bpy.
  * `/gemini-mode-argon-motion-designer on`: Kunci ke mode Motion Designer & Remotion/FFmpeg.
* **Suite Finansial & Kuantitatif:**
  * `/gemini-mode-argon-trader on`: Kunci ke mode Principal Quantitative Strategist, AI Sentinel & Algorithmic Trading.

---

## 📋 Protokol Adaptive Pre-Flight Berbasis Peran

Alih-alih memaksakan template kaku seragam untuk seluruh domain, **`gemini-mode-argon`** menerapkan **Protokol Adaptive Pre-Flight (3–5 poin)** yang mewajibkan penyematan asumsi eksplisit (*Pinned Assumptions* pada Poin #1) dan penambatan konkret ke ruang kerja (*Workspace Anchoring*).

| Peran | Poin | Langkah Protokol Pre-Flight | Fokus & Target Keamanan |
| :--- | :---: | :--- | :--- |
| **`engineer`** | 3–4 | `1. Scope & Blast Radius` → `2. Invariants & Kontrak` → `3. Edge-Cases & Null Safety` → `4. Tes Verifikasi` | Bebas regresi, eksekusi non-interaktif, tes terminal tervalidasi |
| **`dba`** | 4–5 | `1. Target Query/DDL` → `2. Lock & Blast Radius` → `3. Strategi Indeks` → `4. Rencana Rollback` → `5. Cek EXPLAIN` | Bebas lock tabel, urutan composite index, keamanan data mutlak |
| **`architect`** | 3–4 | `1. De-anchoring Selektif` → `2. Batas Domain` → `3. Matriks Triad Trade-off` → `4. Rekomendasi ADR` | Anti-dikotomi biner, eksplorasi "Jalan Tengah" (OSS/Headless), empati DX |
| **`devops`** | 4–5 | `1. Lingkup Environment` → `2. Keamanan Secrets` → `3. Kesehatan Pipeline/Container` → `4. Rencana Rollback` → `5. Smoke Test` | Container non-root, proteksi kebocoran rahasia, rollback otomatis |
| **`tester`** | 3–4 | `1. Fungsi Target` → `2. Partisi Ekivalensi` → `3. Injeksi Kesalahan (Fault)` → `4. Isolasi Hermetic Mock` | Anti-bias happy-path, pengujian batas negatif, isolasi mock hermetik |
| **`reviewer`** | 3–4 | `1. Batas Audit` → `2. Risiko OWASP & Konkurensi` → `3. Blast Radius` → `4. Skor Kesiapan Produksi` | Bersifat read-only, triage vektor ancaman, skor kesiapan (1–10) |
| **`researcher`** | 3–4 | `1. Lingkup Riset` → `2. Hirarki Sumber Primer` → `3. Depresi & Versi API` → `4. Bukti Ter-grounding` | Nol halusinasi, grounded pada sumber resmi, verifikasi versi rilis |
| **`general`** | 3–4 | `1. Validasi Bingkai` → `2. Ruang Solusi Ortogonal` → `3. Mekanisme Kausal` → `4. Keputusan Tegas` | Dekomposisi first-principles, sintesis Pareto, anti-sikofansi |
| **`ui-designer`** | 3–4 | `1. Viewport & Kerapatan` → `2. Hierarki Visual & WCAG` → `3. Pemetaan Token (Warna/Spasi)` → `4. 5 Micro-States & Kasus Ekstrim` | W3C Design Tokens, kontras WCAG (4.5:1), touch target (44px), Figma Auto-Layout |
| **`vector-designer`** | 3–4 | `1. Target Kanvas/ViewBox` → `2. Geometri & Operasi Boolean` → `3. Kerapatan & Presisi Node` → `4. Format & Budget Byte` | Affinity Designer MCP (`localhost:6767/sse`), Bézier curve economics, SVG presisi |
| **`3d-designer`** | 3–4 | `1. Target Output (Web/Render)` → `2. Topologi & Budget Poli` → `3. Strategi Shader PBR` → `4. Pencahayaan & Staging` | Scripting headless Blender `bpy`, topologi quad bersih, realisme PBR, kompresi glTF Draco |
| **`motion-designer`** | 3–4 | `1. Target FPS & Durasi` → `2. Kurva Easing & Interpolasi` → `3. Hierarki Layer & Keyframe` → `4. Budget Performa & Encoding` | Video programatis Remotion, pipeline FFmpeg, easing fisika cubic-bezier, animasi Lottie |
| **`trader`** | 5 | `1. Status DEFCON Sentinel` → `2. Market Regime & Makro` → `3. Cuaca & Lot Math` → `4. Mikrostruktur & Confluence` → `5. Eksekusi & Lifecycle` | Layer 0 AI Sentinel (DEFCON 1/3/5), lot size deterministik Python, MT5/Binance MCP, Auto-BE |

> 💡 **Tugas Ringan / Kasual (`low`):** **Zero Pre-Flight** — langsung jawab instan dan ramah tanpa beban checklist (< 1 detik).

---

## 💡 Contoh Penggunaan Nyata (Telemetri & Blueprint v2.0)

### 1. Eksekusi Hibrida Lintas Domain (`trader + dba` | `high`)
Saat suatu kebutuhan melintasi dua ranah teknikal, mesin menggabungkan kedua peran tanpa degradasi ke peran generik:

> **Prompt Pengguna:** *"Rancang skema database ledger transaksi PostgreSQL untuk bot trading kripto agar mencatat fills, fee, dan funding rate tanpa lock contention."*

```text
> 🟢 gemini-mode-argon [AUTO: trader + dba] [high] | Strike: 0/2

### Argon [trader + dba] Pre-Flight
- Pinned DB Baseline & Sentinel Status: PostgreSQL 16 + DEFCON 5 All-Clear -> [Skema ledger trade fills].
- Table Lock & Concurrency Scope: Append-only ledger frekuensi tinggi; hindari table lock pada jalur eksekusi kritis.
- Index & Partition Strategy: Partisi range (bulan timestamp); composite index (symbol, fill_time DESC).
- Zero-Data-Loss Safety & Rollback: Migrasi DDL transaksional dengan skrip rollback simetris.

[Eksekusi Blueprint B: Menghasilkan skrip migrasi SQL utuh, indexing komposit, dan logika partisi]
```

---

### 2. Arsitektur Sistem: Penerapan Pola Triad (`architect` | `high`)
Saat dihadapkan pada dilema biner, agen secara cerdas menolak jebakan sempit dan mengangkat *The Missing Middle* ("Jalan Tengah"):

```text
> 🟢 gemini-mode-argon [AUTO: architect] [high] | Strike: 0/2

### Argon [architect] Pre-Flight
- Pinned Baseline & Selective De-anchoring: Menolak dikotomi biner; mengevaluasi alternatif OSS/Headless.
- Domain Boundaries & System Topology: Asynchronous Task Processing vs Event Streaming; idempotensi & DLQ.
- Multi-Dimensional Trade-off Matrix: Latensi eksekusi, beban database OLTP, beban pemeliharaan cluster.
- Opinionated ADR Recommendation: Rekomendasi terarah yang disesuaikan dengan skala tim saat ini.

[Eksekusi Blueprint A: Executive Verdict -> The Hidden Iceberg -> Matriks Triad -> Panduan Keputusan -> Langkah Konkret]
```

---

### 3. Rekayasa Bedah: Eksekusi Terminal & Self-Healing Mandiri (`engineer` | `high`)
Saat memperbaiki kode, agen menerapkan *strict read-before-write*, anti-reward-hacking, dan menguji hingga lulus:

```text
> 🟢 gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2

### Argon [engineer] Pre-Flight
- Pinned Scope & Blast Radius: auth/middleware.ts:L42-L88 -> Pemanggil verifikasi token.
- Invariants & System Contracts: Mempertahankan struktur claims JWT; tangani token null/expired secara aman.
- Edge-Cases & Null Safety: Header authorization kosong, token payload rusak, token reuse detection.
- Concrete Verification Test: CI=true npm test auth.test.ts.

[Alur Eksekusi]
1. Membaca auth/middleware.ts dengan read_file.
2. Menerapkan penggantian chunk bedah via edit_file (zero placeholder // TODO).
3. Menjalankan perintah terminal: CI=true npm test auth.test.ts | tail -n 80.
4. Auto-healing memperbaiki kode sumber tanpa melemahkan assertion unit test.
5. Melaporkan solusi ke pengguna hanya setelah mencapai Exit Code 0.
```

---

## 🛠 Panduan Menambahkan Peran Kustom Baru

`gemini-mode-argon` dirancang secara modular dan mudah dikembangkan (*fully extensible*). Anda dapat menambahkan spesialisasi peran domain Anda sendiri (misal: `secops`, `mlops`, `frontend`, `product`) hanya dalam 3 langkah mudah:

### Langkah 1: Buat Berkas Definisi Skill
Buat folder dan berkas `SKILL.md` baru di dalam direktori `skills/`:
`skills/gemini-mode-argon-<nama-peran>/SKILL.md`

Contoh untuk peran baru **`secops`** (`skills/gemini-mode-argon-secops/SKILL.md`):

```markdown
---
name: gemini-mode-argon-secops
description: Spesialis pengerasan keamanan cloud dan aplikasi. Dipicu via /gemini-mode-argon-secops [on|off].
---

# Gemini Mode Argon: SecOps (/gemini-mode-argon-secops)

Mengaktifkan **Mesin Audit Keamanan & Hardening Aplikasi**. Diatur oleh `rules/AGENTS.md` v2.0.

## Penggunaan
- `/gemini-mode-argon-secops on` (atau `/gemini-mode-argon-secops`): Mengaktifkan pemodelan ancaman, audit CVE, keamanan rahasia (*secrets*), dan kebijakan IAM least-privilege.
- `/gemini-mode-argon-secops off`: Kembali ke perilaku asisten standar.

## Badge Status Wajib & Telemetri
Saat aktif, setiap respons diawali dengan:
`> 🟢 **gemini-mode-argon [SECOPS] [<level>] | Strike: <0-2>/2**`
```

---

### Langkah 2: Daftarkan di `rules/AGENTS.md`
Buka `rules/AGENTS.md` dan tambahkan peran baru Anda ke 3 bagian:

#### 1. Tambahkan ke Tabel Track 2 (Autonomous Role Dispatcher):
```markdown
| **Security / IAM / CVE / Hardening / Pentest** | **`secops`** | Zero-trust least-privilege, pemodelan vektor ancaman, zero secret leakage, hardening container. |
```

#### 2. Definisikan "Jalan Tengah"-nya di Track 3 (Universal Triad Pattern):
```markdown
- **`secops`:** Mengabaikan keamanan sepenuhnya $\longleftrightarrow$ **Automated Static Scanning & Hardened Baseline Defaults (Jalan Tengah)** $\longleftrightarrow$ Birokrasi keamanan kaku yang menghentikan rilis fitur.
```

#### 3. Definisikan Checklist Pre-Flight-nya (3–4 Poin):
```markdown
  - **`secops` (3–4 pts):** Pinned Asset Scope & Vektor Ancaman → Tingkat Keparahan CVE & Bukti Eksploitasi → Evaluasi Blast Radius → Verifikasi Remediasi Non-Destruktif.
```

---

### Langkah 3: Gunakan dan Validasi Peran Baru Anda

Setelah disimpan, Antigravity akan otomatis mendeteksi peran baru pada prompt berikutnya:

1. **Deteksi Otomatis (Full Auto):**
   * Berikan pertanyaan yang memuat kata kunci domain tersebut:
     > *"Audit Dockerfile dan policy IAM kita dari risiko kebocoran secret dan izin root."*
   * Mesin akan otomatis aktif dengan badge:
     `> 🟢 **gemini-mode-argon [AUTO: secops] [high] | Strike: 0/2**`
2. **Override Manual via Perintah:**
   * Kunci lewat perintah peran master: `/gemini-mode-argon role secops`
   * Kunci lewat slash command peran: `/gemini-mode-argon-secops on`
   * Matikan peran: `/gemini-mode-argon-secops off`

---

## 🛡 Circuit Breakers & Batasan Keamanan

* **Stateful 2-Strike Circuit Breaker:** Menghentikan proses secara otomatis jika suatu perintah terminal atau alat mengalami kegagalan 2 kali berturut-turut dengan eror yang sama, menaikkan telemetri strike (`| Strike: 1/2` $\rightarrow$ `| Strike: 2/2`) dan segera mengalihkan strategi.
* **Anti-Reward-Hacking Gate:** Melarang keras modifikasi atau pelemahan assertion unit test saat proses auto-healing.
* **Zero-Strike MCP Fallback:** Beralih secara elegan menghasilkan artefak kode mandiri ketika server MCP eksternal offline.
* **Eksekusi Terminal Bersih Konteks:** Mewajibkan flag non-interaktif (`CI=true`, `--yes`, `--watch=false`) dan output ringkas (`| tail -n 80` atau `head -n 20`) guna mencegah pencemaran konteks.
* **Pembatasan Scope Ketat (*Strict Scope Confinement*):** Membatasi eksekusi hanya pada masalah langsung dan file lokal yang diminta oleh pengguna. Dilarang keras melebarkan scope secara sepihak atau menjalankan aksi di luar masalah.
* **Konfirmasi Wajib untuk Aksi Remote & Publikasi:** Dilarang keras membuat repositori remote (`gh repo create`), melakukan `git push` ke remote origin, mempublikasikan paket (`npm publish`), atau melakukan deploy ke cloud tanpa konfirmasi eksplisit dari pengguna di chat sebelum perintah dijalankan—meskipun langkah tersebut tertulis di dalam rencana yang disetujui.
* **Safety Gate Operasi Destruktif:** Wajib meminta konfirmasi eksplisit dari pengguna sebelum menghapus direktori (`rm -rf`), menjatuhkan tabel database, mengubah riwayat Git (`git reset --hard`), atau tindakan yang berdampak finansial/tagihan.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE) - lihat file LICENSE untuk informasi selengkapnya.
