# 🚀 Gemini Mode Argon Suite v2.7 (`gemini-mode-argon`)

[English](README.md) | **Bahasa Indonesia**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Antigravity](https://img.shields.io/badge/Antigravity-Plugin-green.svg)](https://github.com/google)
[![Reasoning](https://img.shields.io/badge/Reasoning-Frontier--Grade-orange.svg)](#)
[![Version](https://img.shields.io/badge/Version-2.7.1-emerald.svg)](#)

Mesin operasional dan penalaran berkinerja tinggi untuk **Google Antigravity**, dirancang khusus untuk mengangkat **Gemini 3.8 Flash** ke kedalaman kognitif, akurasi diagnostik, spesialisasi peran otonom, dan eksekusi terminal mandiri setara **Gemini 4 Argon** melalui **Spesifikasi Paritas Argon v2.7**, **Subagent Native Mandiri (`agents/`)**, dan **Pagar Lifecycle Deterministik Lintas-Surface (`hooks.json`)**.

---

## 🌟 Fitur Utama & Arsitektur Paritas Argon v2.7

* **Pagar Penegakan Deterministik Lintas-Surface (`hooks.json` — Antigravity 2.0 App & IDE/Cascade):** Menegakkan kontrak kognitif Argon secara fisik saat `/gemini-mode-argon` berstatus **`ON`**, dan menjaga **100% Zero-Interference (`< 3ms` no-op)** saat berstatus **`OFF`**:
  * **`PreInvocation` Hook:** Menginjeksi pengingat CoT 4-Ketukan, lokasi dinamis direktori `skills/`, dan State Ledger aktif **1 kali per giliran pesan pengguna**, ditambah monitor kesehatan `/compact` yang **sadar-`CHECKPOINT`** (otomatis ter-reset setelah pengguna menjalankan `/compact`).
  * **`PreToolUse` Hook:** Menegakkan `read-before-write` yang **aman terhadap *1-to-1 parallel tool batch*** baik pada tool App (`read_file`/`edit_file`/`write_file`) maupun IDE (`view_file`/`replace_file_content`/`multi_replace_file_content`/`write_to_file`) melalui parsing boolean `coerce_bool` deterministik, mengunci mode *read-only* saat peran `reviewer` aktif, membungkus test runner poliglot tunggal dengan `( export PYTHONUNBUFFERED=1; set -o pipefail; cmd 2>&1 | tail -n 80 )`, serta meminta konfirmasi untuk perintah destruktif/publikasi (termasuk flag global `git -C` dan penghapus database seperti `prisma migrate reset` / `dropdb`).
  * **`PostToolUse` Hook (*Photographic State Ledger*):** Secara otomatis mengekstrak daftar file yang dimodifikasi beserta simbol *top-level* utama (`class`/`interface`/`struct`/`fn` dalam format `file:Symbol` lintas bahasa Java, C#, Kotlin, Dart, Python, TS/JS, Go, Rust, Ruby, dan SQL) ke `scratch/argon_state.json` tanpa membebani kuota output Flash.
  * **`Stop` Hook (*Exit-Code-0 Auto-Healing Gate*):** Melacak urutan tuple `(step_idx, call_idx)` lintas ekosistem bahasa (`pytest`, `vitest`, `cargo`, `go`, `dotnet`, `rspec`, `phpunit`, `swift`, `ctest`, dll.), menghormati status `fullyIdle: false` Reactive Wakeup untuk subagent dan proses latar belakang, serta mencegah agen berhenti prematur apabila perubahan kode sumber belum dites **ATAU** apabila tes verifikasi terakhir masih gagal (`Command exited with code != 0`).
* **Subagent Native Mandiri (`agents/`):** Bebas ketergantungan plugin pihak ketiga untuk *Horizontal Compute Scale-Out* pada tugas multi-file (Blast Radius $> 3$ file):
  * **`argon-investigator`:** Spesialis survei kode paralel *read-only* dan pemburu akar masalah berbasis falsifikasi hipotesis.
  * **`argon-coder`:** Pekerja implementasi bedah 4-Ketukan dengan pembuktian `Exit Code 0`.
* **Hemat Anggaran Konteks Global (`rules/AGENTS.md` ~13 KB):** Aturan inti berdensitas tinggi menyisakan >70% kuota global `defaultRulesBudget` (`20.000` token) Antigravity untuk aturan proyek dan plugin lainnya.
* **Ritme Eksekusi 4-Ketukan & Adaptive Multi-Turn Pre-Flight Delta:** Menampilkan Pre-Flight 3–5 poin penuh pada Turn 1 dan meringkasnya menjadi 1 baris `> 🎯 **Pre-Flight Delta [<role>]:**` pada giliran lanjutan di lingkup yang sama (maksimal $\le 15\%$ framing dan minimal $\ge 85\%$ implementasi utuh).

---

## 🏛 Gambaran Arsitektur

```
                                      [Prompt Pengguna]
                                            │
                     ┌──────────────────────┴──────────────────────┐
                     ▼                                             ▼
         [Jalur 1: Auto-Level]                         [Jalur 2: Auto-Role]
      (Kalibrasi Penalaran & Ritme)                 (Spesialisasi Peran Otonom)
   ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
   │ • low    : Cepat / System 1 (<1s)│        │ • engineer   : Koding bedah      │
   │ • medium : 4-Beat CoT (1-3s)     │        │ • architect  : Makro & ADR       │
   │ • high   : Refleksi & Healing    │        │ • reviewer   : Audit zero-trust  │
   │ • auto   : Pemicu Deterministik  │        │ • tester     : QA & hermetic mock│
   └──────────────────────────────────┘        │ • dba        : SQL & EXPLAIN     │
                     │                         │ • devops     : SRE & CI/CD       │
                     ▼                         │ • researcher : Riset sumber data │
       [Subagent Native Mandiri]               │ • general    : Analisis umum     │
   ┌──────────────────────────────────┐        ├──────────────────────────────────┤
   │ • argon-investigator (Read-Only) │        │ • ui-designer: Figma & Tokens    │
   │ • argon-coder (Surgical Worker)  │        │ • vector-des.: Affinity & SVG    │
   └──────────────────────────────────┘        │ • 3d-designer: Blender & glTF    │
                                               │ • motion-des.: Video & Easing    │
                                               ├──────────────────────────────────┤
                                               │ • trader     : Sentinel & Quant  │
                                               ├──────────────────────────────────┤
                                               │ • Hibrida    : [peran1 + peran2] │
                                               └──────────────────────────────────┘
```

---

## ⚙️ Rekomendasi Konfigurasi Optimal

1. **Mesin (UI Antigravity):** Set model ke **`Gemini 3.8 Flash (High)`** (pastikan `python3` tersedia pada `PATH` sistem untuk eksekusi lifecycle hooks).
2. **Disiplin Kerja (Plugin):** Aktifkan sekali per sesi dengan `/gemini-mode-argon on`.

---

## 📦 Panduan Instalasi & Pengujian

Pasang ke dalam direktori plugin Antigravity lokal Anda:

```bash
git clone https://github.com/diinggos/gemini-mode-argon.git ~/.gemini/config/plugins/gemini-mode-argon
```

Buka kembali Antigravity atau mulai percakapan baru. Jalankan 29 skenario suite pengujian otomatis end-to-end:

```bash
python3 -m unittest discover -s ~/.gemini/config/plugins/gemini-mode-argon/tests -v
```

---

## 🕹 Panduan Perintah Slash

### 1. Kontrol Utama
* `/gemini-mode-argon on` (atau `/gemini-mode-argon`): Mengaktifkan Full-Auto Mode (*Auto-Role* + *Auto-Level* + *Active Hooks*).
* `/gemini-mode-argon off`: Menonaktifkan plugin (*Zero-Interference mode*) dan kembali ke perilaku bawaan asisten.
* `/gemini-mode-argon token-saver [on|off]`: Mengaktifkan/menonaktifkan mode hemat token tanpa basa-basi (`| ⚡ **token-saver: ON**`).

### 2. Override Tingkat Penalaran (Level)
* `/gemini-mode-argon level [auto | low | medium | high]`

### 3. Override Peran Tertentu (Role)
* `/gemini-mode-argon role auto` *(default)* atau `/gemini-mode-argon-<peran> [on|off]`:
  * **Suite Teknikal (8):** `engineer`, `architect`, `reviewer`, `tester`, `dba`, `devops`, `researcher`, `general`.
  * **Suite Kreatif (4):** `ui-designer`, `vector-designer`, `3d-designer`, `motion-designer`.
  * **Suite Finansial & Kuantitatif (1):** `trader`.

---

## 📋 Protokol Adaptive Pre-Flight & Multi-Turn Delta

| Peran | Poin | Langkah Protokol Pre-Flight | Fokus & Target Keamanan |
| :--- | :---: | :--- | :--- |
| **`engineer`** | 3–4 | `1. Pinned Scope & Blast Radius` → `2. Invariants & Kontrak` → `3. Edge-Cases & Null Safety` → `4. Tes Verifikasi` | Baca paralel di awal, bebas regresi, tes terminal non-interaktif |
| **`dba`** | 4–5 | `1. Pinned DB & Target Query` → `2. Lock & Blast Radius` → `3. Strategi Indeks` → `4. Rencana Rollback` → `5. Cek EXPLAIN` | Bebas lock tabel, urutan composite index, keamanan data mutlak |
| **`architect`** | 3–4 | `1. Pinned Baseline & De-Anchoring` → `2. Batas Domain` → `3. Matriks Triad & Math` → `4. Rekomendasi ADR` | Anti-dikotomi biner, eksplorasi "Jalan Tengah" (OSS/Headless), kalkulasi RPS/GB |
| **`devops`** | 4–5 | `1. Pinned Env Scope` → `2. Keamanan Secrets & Non-Root` → `3. Kesehatan Layer/Pipeline` → `4. Rencana Rollback` → `5. Smoke Check` | Container non-root, proteksi kebocoran rahasia, rollback otomatis |
| **`tester`** | 3–4 | `1. Pinned Fungsi & Framework` → `2. Partisi Ekivalensi` → `3. Injeksi Fault` → `4. Isolasi Hermetic Mock` | Anti-bias happy-path, pengujian batas negatif, isolasi mock hermetik |
| **`reviewer`** | 3–4 | `1. Pinned Batas Audit` → `2. Risiko OWASP & Konkurensi` → `3. Blast Radius` → `4. Target Skor Kesiapan` | Bersifat read-only, verifikasi caller hulu, skor kesiapan (1–10) |
| **`researcher`** | 3–4 | `1. Pinned Lingkup & Versi` → `2. Hirarki Sumber Primer` → `3. Depresi & Versi API` → `4. Bukti Ter-grounding` | Nol halusinasi, grounded pada Context7/sumber resmi, verifikasi semver |
| **`general`** | 3–4 | `1. Pinned Baseline & Cek Bingkai` → `2. Ruang Solusi Ortogonal` → `3. Mekanisme Kausal` → `4. Keputusan Tegas` | Dekomposisi first-principles, sintesis Pareto, anti-sikofansi |
| **`ui-designer`** | 3–4 | `1. Pinned Viewport & Kerapatan` → `2. Hierarki & WCAG` → `3. Pemetaan Token Semantik` → `4. 5 Micro-States & Kasus Ekstrim` | W3C Design Tokens, kontras WCAG (4.5:1), touch target (44px), Figma Auto-Layout |
| **`vector-designer`** | 3–4 | `1. Pinned Kanvas/ViewBox` → `2. Geometri & Boolean` → `3. Kerapatan & Presisi Node` → `4. Format & Budget Byte` | Affinity Designer MCP (`localhost:6767/sse`), Bézier curve economics, SVG presisi |
| **`3d-designer`** | 3–4 | `1. Pinned Target Output` → `2. Topologi & Budget Poli` → `3. Strategi Shader PBR` → `4. Pencahayaan & Staging` | Scripting headless Blender `bpy`, topologi quad bersih, realisme PBR, kompresi glTF Draco |
| **`motion-designer`** | 3–4 | `1. Pinned FPS & Durasi Frame` → `2. Kurva Easing Fisika` → `3. Hierarki Layer & Keyframe` → `4. Budget Performa & Encoding` | Video programatis Remotion, pipeline FFmpeg, easing fisika cubic-bezier, animasi Lottie |
| **`trader`** | 5 | `1. Pinned Akun & Status DEFCON` → `2. Market Regime & Makro` → `3. Cuaca & Lot Math` → `4. Mikrostruktur & SMC` → `5. Gate Lifecycle` | Layer 0 AI Sentinel (DEFCON 1/3/5), lot size deterministik Python, MT5/Binance MCP |

> 💡 **Tugas Ringan / Kasual (`low`):** **Zero Pre-Flight** — langsung jawab instan dan ramah tanpa beban checklist (< 1 detik).

---

## 💡 Contoh Penggunaan Nyata (Turn 1 Pre-Flight Penuh vs Turn 2 Delta)

### Turn 1 — Perbaikan Bug Awal (`engineer` pada level `high`)
```markdown
> 🟢 **gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2**

### Argon [engineer] Pre-Flight
- Pinned Scope & Blast Radius: `src/auth/jwt.ts:L42-L68` (`verifyAccessToken`) -> dipanggil oleh `src/middleware/requireAuth.ts`.
- Invariants & Kontrak: Pertahankan tipe return `AuthClaims` dan kode HTTP 401 `TOKEN_EXPIRED`.
- Edge-Cases & Null Safety: Tangani klaim `exp` kosong, toleransi waktu (`clockTolerance: 5`), dan header Bearer rusak.
- Tes Verifikasi Konkret: `CI=true npx vitest run src/auth/jwt.test.ts`

**Root-Cause Delta:** `verifyAccessToken` menganggap nilai timestamp numerik `0` sebagai falsy dan melewati validasi kedaluwarsa saat `clockTolerance` tidak diset.

[... Diff bedah 100% utuh & bukti kelulusan Vitest (Exit Code 0) ...]
```

### Turn 2 — Tindak Lanjut pada Lingkup yang Sama (`Pre-Flight Delta`)
```markdown
> 🟢 **gemini-mode-argon [AUTO: engineer] [high] | Strike: 0/2**
> 🎯 **Pre-Flight Delta [engineer]:** Kontrak `AuthClaims` (`src/auth/jwt.ts`) -> Tambah validasi klaim `aud` + unit test negatif -> `CI=true npx vitest run src/auth/jwt.test.ts`

[... Implementasi langsung & verifikasi Exit Code 0 tanpa pengulangan checklist panjang ...]
```

---

## 🧪 Matriks Suite Pengujian End-to-End

Paket ini dilengkapi dengan **29 pengujian unit dan integrasi otomatis komprehensif** (`tests/test_hooks.py`) untuk memverifikasi determinisme penegakan sistem:

| Kategori | Cakupan & Kontrak yang Terverifikasi | Pengujian |
| :--- | :--- | :---: |
| **Zero-Interference** | 100% no-op saat `OFF` (latensi < 0.003 ms), cache parsing transkrip inkremental sub-milidetik, nol mutasi tool, keluar bersih. | `test_01`, `test_29` |
| **Command Parser** | Pemindai slash command berantai, normalisasi token (misal `/gemini-mode-argon /token-saver`), override peran, dan reset kunci reviewer. | `test_02`, `test_22`, `test_28` |
| **Lifecycle Hooks** | Deduplikasi giliran `PreInvocation`, monitor `/compact` sadar-CHECKPOINT, keamanan batch `PreToolUse` read-before-write, ekstraksi ledger `PostToolUse`, dan auto-healing Exit-Code-0 pada `Stop`. | `test_03`–`test_09`, `test_11`–`test_13`, `test_17`, `test_23`, `test_27` |
| **Paritas Surface** | Kompatibilitas lintas-surface antara Antigravity App (`read_file`, `edit_file`) dan IDE/Cascade (`view_file`, `replace_file_content`). | `test_16` |
| **Pengurai Poliglot** | Ekstraksi simbol multibahasa lintas Java, C#, Kotlin, Dart, Python, TS/JS, Go, Rust, Ruby, dan SQL. | `test_24`, `test_26` |
| **Higiene & Keamanan** | 0 unused import AST, 0 path hardcoded lokal, proteksi perintah destruktif/publish, dan kontras logo dual-theme (skor 100/100). | `test_10`, `test_14`, `test_15`, `test_18`–`test_21`, `test_25` |

---

## 🧩 Menambahkan Peran Kustom (*Extensibility Guide*)

1. Buat direktori skill baru: `skills/gemini-mode-argon-<peran-baru>/SKILL.md` lengkap dengan YAML frontmatter (`name`, `description`), pola **Universal Triad**, **Response Blueprint (`A`, `B`, atau `C`)**, serta **3–5 poin Pre-Flight Checklist**.
2. Daftarkan `<peran-baru>` ke `VALID_ROLES` di `scripts/argon_core.py` dan tambahkan 1 baris ringkas pada tabel Dispatcher di `rules/AGENTS.md` (pastikan ukuran `rules/AGENTS.md` tetap `< 24.000 bytes`).
3. Jalankan `python3 -m unittest discover -s tests -v` untuk memverifikasi pengenalan slash command `/gemini-mode-argon-<peran-baru> on`.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah [Lisensi MIT](LICENSE) - lihat file LICENSE untuk informasi selengkapnya.
