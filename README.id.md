# 🚀 Gemini Mode Argon Suite (`gemini-mode-argon`)

[English](README.md) | **Bahasa Indonesia**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/google)
[![Reasoning](https://img.shields.io/badge/Reasoning-Frontier--Grade-orange.svg)](#)

Mesin operasional dan penalaran berkinerja tinggi untuk **Google Antigravity**, dirancang untuk menghadirkan disiplin penalaran kelas *frontier*, spesialisasi peran otomatis (*Autonomous Role Dispatching*), dan eksekusi terminal mandiri (*Terminal Auto-Healing*) ke dalam alur kerja agen berbasis Gemini.

---

## 🌟 Fitur Utama

* **Arsitektur Dua Jalur (Two-Track Architecture):** Memisahkan **Kalibrasi Tingkat Penalaran** (`low`, `medium`, `high`, `auto`) dari **Spesialisasi Peran** (8 domain teknis).
* **Auto-Role Otonom:** Mengklasifikasikan prompt pengguna secara dinamis untuk menentukan arketipe rekayasa perangkat lunak terbaik secara instan.
* **Protokol Pre-Flight 4-Poin:** Menjalankan checklist verifikasi wajib sebelum mensintesis solusi atau memodifikasi file kode.
* **Terminal Auto-Healing (Level High):** Menjalankan pengujian di terminal secara mandiri, menangkap eror secara langsung, dan memperbaikinya sendiri secara berulang hingga mencapai exit code 0.
* **Universal Triad Pattern & Arsitektur 5-Blok:** Secara naluriah memetakan "Jalan Tengah" (*The Missing Middle*) di semua peran dan menyajikan solusi dengan ritme 5-blok native Argon yang tegas dan terstruktur.
* **Frontier Fluid Rigor & Anti-Anchoring:** Membongkar dikotomi biner secara anggun dengan empati developer nyata (relasi database lokal vs friksi sinkronisasi webhook, batas biaya MAU).
* **Zero Overhead pada Tugas Ringan:** Respons System 1 instan (< 1 detik) untuk obrolan kasual, dan otomatis eskalasi ke System 2 (*Chain-of-Thought* mendalam) untuk rekayasa teknis yang rumit.

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
   │ • low    : Cepat / System 1 (<1s)│        │ • engineer   : Koding & refaktor │
   │ • medium : CoT Seimbang (1-3s)   │        │ • architect  : Makro & ADR       │
   │ • high   : Refleksi & Auto-Heal  │        │ • reviewer   : Audit zero-trust  │
   │ • auto   : Eskalasi Dinamis      │        │ • tester     : QA & hermetic mock│
   └──────────────────────────────────┘        │ • dba        : SQL & EXPLAIN     │
                                               │ • devops     : SRE & CI/CD       │
                                               │ • researcher : Riset sumber data │
                                               │ • general    : Analisis umum     │
                                               ├──────────────────────────────────┤
                                               │ • ui-designer: Figma & Tokens    │
                                               │ • vector-des.: Affinity & SVG    │
                                               │ • 3d-designer: Blender & glTF    │
                                               │ • motion-des.: Video & Easing    │
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

### 2. Override Tingkat Penalaran (Level)
* `/gemini-mode-argon level auto`: Eskalasi dinamis sesuai bobot tugas *(bawaan/default)*.
* `/gemini-mode-argon level low`: Mode cepat System 1; tanpa overhead Pre-Flight (< 1 detik).
* `/gemini-mode-argon level medium`: Mode System 2 seimbang dengan Pre-Flight ringkas (1–3 detik).
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

---

## 📋 Protokol Adaptive Pre-Flight Berbasis Peran

Alih-alih memaksakan 4-poin kaku seragam untuk seluruh domain, **`gemini-mode-argon`** menerapkan **Protokol Adaptive Pre-Flight (3–5 poin)** yang beradaptasi secara dinamis sesuai kebutuhan dan profil risiko spesifik dari peran yang sedang aktif.

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

> 💡 **Tugas Ringan / Kasual (`low`):** **Zero Pre-Flight** — langsung jawab instan dan ramah tanpa beban checklist (< 1 detik).

---

## 💡 Contoh Penggunaan Nyata

Berikut adalah bagaimana `gemini-mode-argon` merespons skenario teknis di dunia nyata:

### 1. Arsitektur Sistem: Penerapan Pola Triad (`architect` | `high`)
Saat dihadapkan pada dilema biner, agen secara cerdas menolak jebakan sempit dan mengangkat *The Missing Middle* ("Jalan Tengah"):

> **Prompt Pengguna:** *"Aplikasi kami mulai lambat karena banyak proses asynchronous (email, kompresi gambar, webhook sync). Apakah sebaiknya kami buat background queue sendiri pakai Cron Job polling database, atau langsung pasang Apache Kafka / RabbitMQ?"*

```text
> 🟢 gemini-mode-argon [AUTO: architect] [high]

### Argon [architect] Pre-Flight
- Selective De-anchoring & Spectrum Check: Menolak dikotomi biner; mengevaluasi alternatif OSS/Headless.
- Domain Boundaries & System Topology: Asynchronous Task Processing vs Event Streaming; idempotensi & DLQ.
- Multi-Dimensional Trade-off Matrix: Latensi eksekusi, beban database OLTP, beban pemeliharaan cluster.
- Opinionated ADR Recommendation: Rekomendasi terarah yang disesuaikan dengan skala tim saat ini.

[Executive Verdict]
Untuk 95% aplikasi web modern, jangan gunakan Cron Job polling database, dan jangan terburu-buru memasang Apache Kafka. Pilihan paling pragmatis dan teruji di industri adalah "Jalan Tengah": gunakan antrean berbasis Redis (BullMQ/Sidekiq/Celery) atau PostgreSQL FOR UPDATE SKIP LOCKED.

[The Hidden Iceberg]
- Cron DB Polling: Memicu race condition, eksekusi ganda, dan beban I/O konstan pada database produksi Anda.
- Apache Kafka: Dirancang untuk event streaming skala masif, bukan antrean tugas background (sulit per-task retry/delay).

[Matriks Komparasi Triad]
| Dimensi Evaluasi | 1. Custom Cron + DB Polling | 2. Jalan Tengah (Redis / SKIP LOCKED) | 3. Enterprise Broker (Kafka) |
| Waktu & Latensi | Rawan bug, jeda 1m+ | Instan (<10ms), siap dalam hitungan jam | Berpekan-pekan konfigurasi cluster |
| Beban DB Produksi | Tinggi (lock contention) | Nol (Redis) / Minimal (SKIP LOCKED) | Nol (cluster broker terisolasi) |
| Fitur Antrean Bawaan | Wajib koding manual | Bawaan library (retry backoff, DLQ) | Butuh arsitektur custom rumit |

[Empati Rekayasa Nyata]
- Queue Isolation: Pisahkan worker kompresi gambar (CPU-bound) dari antrean email notifikasi (latensi kritis).
```

---

### 2. Rekayasa Bedah: Eksekusi Terminal & Self-Healing Mandiri (`engineer` | `high`)
Saat memperbaiki bug atau mengimplementasikan fitur, agen menerapkan *strict read-before-write* dan berulang kali menguji hingga exit code 0:

> **Prompt Pengguna:** *"Test suite auth kita gagal dengan TypeError di middleware refresh token, tolong perbaiki dan pastikan semua test lulus."*

```text
> 🟢 gemini-mode-argon [AUTO: engineer] [high]

### Argon [engineer] Pre-Flight
- Target Scope & Blast Radius: auth/middleware.ts & logika verifikasi token.
- Invariants & System Contracts: Mempertahankan struktur claims JWT; tangani token null/expired secara aman.
- Edge-Cases & Null Safety: Header authorization kosong, token payload rusak, token reuse detection.
- Concrete Verification Test: CI=true npm test auth.test.ts.

[Alur Eksekusi]
1. Membaca auth/middleware.ts dengan read_file (mempertahankan komentar/docstring).
2. Menerapkan penggantian chunk bedah via edit_file (zero placeholder // TODO).
3. Menjalankan perintah terminal: CI=true npm test auth.test.ts.
4. Menangkap exit code dan stderr: jika assertion gagal, agen menganalisis eror dan memperbaiki kode kembali.
5. Melaporkan solusi ke pengguna hanya setelah mencapai Exit Code 0.
```

---

### 3. Kueri Ringan / Kasual: Zero Pre-Flight Overhead (< 1s) (`general` | `low`)
Pertanyaan cepat dan sederhana langsung dijawab tanpa checklist birokrasi:

> **Prompt Pengguna:** *"Bagaimana cara convert string ke integer di Go?"*

```text
> 🟢 gemini-mode-argon [AUTO: general] [low]

Gunakan package standar `strconv.Atoi`:

package main

import (
    "fmt"
    "strconv"
)

func main() {
    i, err := strconv.Atoi("42")
    if err != nil {
        panic(err)
    }
    fmt.Println(i) // 42
}

*(Zero Pre-Flight checklist overhead, respons System 1 instan).*
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

Mengaktifkan **Mesin Audit Keamanan & Hardening Aplikasi**.

## Penggunaan
- `/gemini-mode-argon-secops on` (atau `/gemini-mode-argon-secops`): Mengaktifkan pemodelan ancaman, audit CVE, keamanan rahasia (*secrets*), dan kebijakan IAM least-privilege.
- `/gemini-mode-argon-secops off`: Kembali ke perilaku asisten standar.

## Badge Status Wajib
Saat aktif, setiap respons diawali dengan:
`> 🟢 **gemini-mode-argon-secops: ON**`
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
  - **`secops` (3–4 pts):** Batas Vektor Ancaman → Tingkat Keparahan CVE & Bukti Eksploitasi → Evaluasi Blast Radius → Verifikasi Remediasi Non-Destruktif.
```

---

### Langkah 3: Gunakan dan Validasi Peran Baru Anda

Setelah disimpan, Antigravity akan otomatis mendeteksi peran baru pada prompt berikutnya:

1. **Deteksi Otomatis (Full Auto):**
   * Berikan pertanyaan yang memuat kata kunci domain tersebut:
     > *"Audit Dockerfile dan policy IAM kita dari risiko kebocoran secret dan izin root."*
   * Mesin akan otomatis aktif dengan badge:
     `> 🟢 **gemini-mode-argon [AUTO: secops] [high]**`
2. **Override Manual via Perintah:**
   * Kunci lewat perintah peran master: `/gemini-mode-argon role secops`
   * Kunci lewat slash command peran: `/gemini-mode-argon-secops on`
   * Matikan peran: `/gemini-mode-argon-secops off`

---

## 🛡 Circuit Breakers & Batasan Keamanan

* **2-Strike Circuit Breaker:** Menghentikan proses secara otomatis jika suatu perintah terminal atau alat mengalami kegagalan 2 kali berturut-turut dengan eror yang sama.
* **Non-Interactive Execution:** Mewajibkan penggunaan flag non-interaktif (`CI=true`, `--yes`, `--watch=false`) untuk mencegah sesi terminal tergantung (*hung*).
* **Safety Gate:** Wajib meminta konfirmasi eksplisit dari pengguna sebelum menghapus file penting, menjatuhkan tabel database, mengubah riwayat Git, atau tindakan yang berdampak finansial/tagihan.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE) - lihat file LICENSE untuk informasi selengkapnya.
