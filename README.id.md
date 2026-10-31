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
* `/gemini-mode-argon level high`: Ketelitian maksimal (~92% Argon) dengan eksekusi terminal dan perbaikan mandiri (5–10 detik).

### 3. Override Peran Tertentu (Role)
* `/gemini-mode-argon role auto`: Deteksi peran otonom *(default)*.
* `/gemini-mode-argon-engineer on`: Kunci ke mode Principal Software Engineer.
* `/gemini-mode-argon-architect on`: Kunci ke mode Principal Systems Architect.
* `/gemini-mode-argon-reviewer on`: Kunci ke mode Read-Only Security Auditor & Reviewer.
* `/gemini-mode-argon-tester on`: Kunci ke mode QA & Test Automation Specialist.
* `/gemini-mode-argon-dba on`: Kunci ke mode Database Administrator & SQL Performance.
* `/gemini-mode-argon-devops on`: Kunci ke mode SRE & Infrastructure Automation.
* `/gemini-mode-argon-researcher on`: Kunci ke mode Peneliti Teknis & Verifikasi Fakta.
* `/gemini-mode-argon-general on`: Kunci ke mode Pemecah Masalah Lintas Domain.

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

> 💡 **Tugas Ringan / Kasual (`low`):** **Zero Pre-Flight** — langsung jawab instan dan ramah tanpa beban checklist (< 1 detik).

---

## 🛡 Circuit Breakers & Batasan Keamanan

* **2-Strike Circuit Breaker:** Menghentikan proses secara otomatis jika suatu perintah terminal atau alat mengalami kegagalan 2 kali berturut-turut dengan eror yang sama.
* **Non-Interactive Execution:** Mewajibkan penggunaan flag non-interaktif (`CI=true`, `--yes`, `--watch=false`) untuk mencegah sesi terminal tergantung (*hung*).
* **Safety Gate:** Wajib meminta konfirmasi eksplisit dari pengguna sebelum menghapus file penting, menjatuhkan tabel database, mengubah riwayat Git, atau tindakan yang berdampak finansial/tagihan.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE) - lihat file LICENSE untuk informasi selengkapnya.
