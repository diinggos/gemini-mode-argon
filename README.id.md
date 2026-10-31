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

Alih-alih memaksakan 4-poin kaku seragam untuk seluruh domain, **`gemini-mode-argon`** menerapkan **Protokol Adaptive Pre-Flight (3–5 poin)** yang beradaptasi secara dinamis sesuai kebutuhan dan profil risiko spesifik dari peran yang sedang aktif:

* **`engineer` (3–4 Poin):** Scope & Blast Radius $\to$ Invariants & Kontrak Sistem $\to$ Edge-Cases & Null Safety $\to$ Tes Verifikasi Konkret.
* **`dba` (4–5 Poin):** Target Query/DDL $\to$ Risiko Table Lock & Blast Radius $\to$ Strategi Indeks $\to$ **Rencana Rollback & Keamanan Data** $\to$ Validasi EXPLAIN.
* **`devops` (4–5 Poin):** Lingkup Lingkungan $\to$ Keamanan Secrets & Izin $\to$ Kesehatan Pipeline/Container $\to$ **Rencana Rollback** $\to$ Verifikasi Smoke Test.
* **`reviewer` (3–4 Poin):** Batas Audit $\to$ Vektor Ancaman (OWASP/Race Condition) $\to$ Blast Radius $\to$ Skor Kesiapan Produksi (*Production Readiness Score*).
* **`tester` (3–4 Poin):** Fungsi Target $\to$ Partisi Ekivalensi & Batas $\to$ Vektor Injeksi Kesalahan (*Fault Injection*) $\to$ Isolasi Hermetic Mock.
* **`architect` (3–4 Poin):** Batas Domain & Topologi Sistem $\to$ Matriks Trade-off & Non-Functional Req $\to$ Invariants $\to$ Keputusan Arsitektur (ADR).
* **`researcher` (3–4 Poin):** Lingkup Riset $\to$ Hirarki Kepercayaan Sumber Primer $\to$ Depresi & Perubahan Versi $\to$ Verifikasi Bukti Ter-grounding.
* **`general` (3–4 Poin):** Inti Masalah & Asumsi Tersembunyi $\to$ Mekanisme Kausal & Trade-off $\to$ Efek Tingkat Kedua (*"And then what?"*) $\to$ Metrik Keputusan.
* **Tugas Ringan / Kasual (`low`):** **Zero Pre-Flight** — langsung jawab instan dan ramah tanpa beban checklist.

---

## 🛡 Circuit Breakers & Batasan Keamanan

* **2-Strike Circuit Breaker:** Menghentikan proses secara otomatis jika suatu perintah terminal atau alat mengalami kegagalan 2 kali berturut-turut dengan eror yang sama.
* **Non-Interactive Execution:** Mewajibkan penggunaan flag non-interaktif (`CI=true`, `--yes`, `--watch=false`) untuk mencegah sesi terminal tergantung (*hung*).
* **Safety Gate:** Wajib meminta konfirmasi eksplisit dari pengguna sebelum menghapus file penting, menjatuhkan tabel database, mengubah riwayat Git, atau tindakan yang berdampak finansial/tagihan.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE) - lihat file LICENSE untuk informasi selengkapnya.
