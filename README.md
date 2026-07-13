# 📂 Arsip ORMAWA - Sistem Manajemen Dokumen dengan Mock S3 Lokal

Aplikasi **Arsip ORMAWA** adalah platform web untuk mengelola arsip dokumen Organisasi Mahasiswa (ORMAWA). Dibangun dengan **Flask** dan menggunakan **moto** sebagai simulator AWS S3 lokal, sehingga tidak memerlukan akun AWS sungguhan.

Aplikasi ini cocok untuk pengembangan dan pembelajaran arsitektur cloud storage dengan S3, tanpa koneksi internet atau sumber daya AWS berbayar.

---

## 📋 Daftar Isi

1. [Ringkasan Project](#-ringkasan-project)
2. [Fitur Utama](#-fitur-utama)
3. [Arsitektur & Teknologi](#-arsitektur--teknologi)
4. [Prasyarat](#-prasyarat)
5. [Panduan Setup](#-panduan-setup)
6. [Struktur Folder](#-struktur-folder)
7. [Penjelasan File](#-penjelasan-file)
8. [Cara Menggunakan](#-cara-menggunakan)
9. [Troubleshooting](#-troubleshooting)

---

## 🎯 Ringkasan Project

Arsip ORMAWA menyediakan antarmuka web untuk mengunggah, mengelola, dan mengunduh dokumen organisasi. Semua data file disimpan dalam simulasi **S3 lokal** menggunakan `moto`.

Aplikasi mendukung:
- **Upload dokumen** dengan nama kustom dan kategori pilihan.
- **Edit metadata dokumen** dan ganti isi file.
- **Download dokumen** dari browser dengan mudah.
- **Hapus dokumen** yang tidak diperlukan.
- **Sidebar toggle**: Klik logo untuk membuka/menutup sidebar dan tampil lebih luas.
- **Filtering dan pencarian** dokumen berdasarkan nama atau kategori.
- **Dark theme elegans** dengan latar belakang pola jaringan organisasi yang animatif.
- **Dashboard ringkasan** dengan hero banner dan stat cards yang informatif.

---

## ✅ Fitur Utama

- **Dashboard Ringkasan**: Hero banner dengan statistik total dokumen, total kategori, dan ukuran penyimpanan. Tampilkan daftar dokumen terbaru.
- **Upload Dokumen**: Unggah file dengan kategori dan nama file pilihan (drag-drop support).
- **Edit Dokumen**: Perbarui nama, kategori, dan/atau ganti isi file dengan mudah.
- **File Replacement**: Saat mengganti dokumen, nama file baru tanpa ekstensi otomatis menggunakan ekstensi file lama.
- **Sidebar Toggle**: Klik logo untuk membuka/menutup sidebar. State tersimpan di localStorage untuk pengalaman pengguna yang lebih baik.
- **Dark Theme Elegan**: Desain modern dengan tema gelap yang indah, pola jaringan organisasi beranimasi, dan efek glassmorphic.
- **Responsive Design**: Tampilan sempurna di desktop dan mobile dengan layout yang fleksibel.
- **Form Centered**: Form upload dan edit ditampilkan di tengah halaman untuk fokus pengguna yang lebih baik.
- **Validasi Ekstensi**: Hanya menerima `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.jpg`, `.jpeg`, `.png`, `.zip`.

---

## 🏗️ Arsitektur & Teknologi

Aplikasi ini terdiri dari:
- **Flask** sebagai backend web dengan routing dan session management.
- **moto** sebagai simulator AWS S3 lokal tanpa memerlukan akun AWS.
- **Boto3** sebagai client AWS S3 untuk operasi penyimpanan.
- **Jinja2** untuk templates HTML dengan inheritance dan block extension.
- **HTML5 + CSS3** dengan custom properties untuk dark theme, animasi, dan responsivitas.
- **Bootstrap Icons v1.11.0** untuk ikon modern dan konsisten.
- **SVG Patterns** untuk latar belakang jaringan organisasi yang animatif.

### Arsitektur Aplikasi

```
Browser 
  → Flask Routes (app.py)
    → S3 Service Layer (services/s3_service.py)
      → moto S3 Mock (In-Memory Storage)
```

### Design System

Aplikasi menggunakan CSS custom properties untuk konsistensi visual:
- **Color Palette**: Indigo (#6366f1), Purple (#8b5cf6), Emerald (#10b981) dengan background gelap
- **Animations**: Cubic-bezier timing functions dan keyframe animations untuk smooth transitions
- **Layout**: CSS Grid dan Flexbox untuk responsive design
- **Effects**: Glassmorphism, gradient backgrounds, dan layered shadows

---

## 🧩 Prasyarat

- Python 3.8+
- `pip` terpasang
- Virtual environment direkomendasikan

---

## 🚀 Panduan Setup

Panduan ini menjelaskan langkah-langkah untuk menyiapkan lingkungan Python, menginstal dependensi, mengkonfigurasi aplikasi, dan menjalankan server Flask.

### 1. Buka terminal dan masuk ke direktori project

Buka PowerShell atau terminal lain, lalu jalankan:

```powershell
cd "d:\Tubes-Cloud\Tubes-Cloud ( Arsip ORMAWA )"
```

> Pastikan path yang digunakan sama dengan lokasi folder proyek Anda.

### 2. Buat virtual environment dan aktifkan

Virtual environment menjaga paket Python tetap terisolasi dari sistem utama.

**PowerShell**:

```powershell
python -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

**Command Prompt (CMD)**:

```cmd
python -m venv venv
.\venv\Scripts\activate.bat
```

Jika terminal menolak menjalankan skrip, jalankan `Set-ExecutionPolicy` terlebih dahulu seperti di atas.

### 3. Pasang dependensi

Setelah venv aktif, instal semua paket yang dibutuhkan:

```powershell
pip install -r requirements.txt
```

> Pastikan prompt terminal menampilkan `(venv)` di awal, ini menandakan environment sudah aktif.

### 4. Buat atau perbarui file `.env`

File `.env` berisi konfigurasi aplikasi dan credential mock untuk S3 lokal.

Buat file `.env` di root folder project jika belum ada, lalu isi dengan:

```env
AWS_ACCESS_KEY_ID=mock_access_key_lokal
AWS_SECRET_ACCESS_KEY=mock_secret_key_lokal
AWS_REGION=us-east-1
AWS_BUCKET_NAME=arsip-ormawa-lokal
FLASK_SECRET_KEY=kunci_rahasia_tugas_kuliah_123
AWS_ENDPOINT_URL=http://localhost:4566
LOGIN_USERNAME=admin
LOGIN_PASSWORD=ormawa2026
```

> Penjelasan singkat:
> - `AWS_*`: kredensial mock S3.
> - `AWS_BUCKET_NAME`: nama bucket lokal yang digunakan oleh aplikasi.
> - `FLASK_SECRET_KEY`: kunci rahasia untuk session Flask.
> - `LOGIN_USERNAME` / `LOGIN_PASSWORD`: akun admin default.

### 5. Jalankan aplikasi

Setelah dependensi dan konfigurasi siap, jalankan server Flask:

```powershell
python app.py
```

Aplikasi akan otomatis membuat bucket S3 lokal menggunakan `moto` saat pertama kali dijalankan.

### 6. Buka aplikasi di browser

Akses aplikasi melalui alamat:

```text
http://127.0.0.1:5000
```

Gunakan username dan password dari file `.env` untuk login.

---

## 📁 Struktur Folder

```text
Tubes-Cloud ( Arsip ORMAWA )/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── services/
│   └── s3_service.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── documents.html
│   ├── upload.html
│   └── edit.html
└── venv/
```

---

## 📄 Penjelasan File

- `app.py`: Entrypoint Flask dan route handling.
- `config.py`: Konfigurasi aplikasi dan daftar kategori dokumen.
- `services/s3_service.py`: Abstraksi operasi S3 (upload, download, delete, list, rename).
- `templates/`: Template Jinja2 untuk halaman UI.
- `.env`: Konfigurasi environment dan credential mock.
- `requirements.txt`: Daftar dependensi Python.

---

## 🛠️ Cara Menggunakan

1. **Login**: Gunakan kredensial di `.env` untuk masuk ke sistem.
2. **Dashboard**: Lihat ringkasan statistik dokumen dan akses dokumen terbaru.
3. **Toggle Sidebar**: Klik logo di sudut kiri atas untuk membuka/menutup sidebar. Posisi tersimpan otomatis.
4. **Upload Dokumen**: 
   - Buka halaman **Upload Dokumen**
   - Pilih kategori dari dropdown
   - Drag-drop atau klik untuk memilih file
   - Masukkan nama custom (opsional)
   - Klik "Mulai Upload"
5. **Kelola Dokumen**: Gunakan halaman **Daftar Dokumen** untuk:
   - 🔍 Cari dokumen berdasarkan nama
   - 📁 Filter berdasarkan kategori
   - 📥 Download file
   - ✏️ Edit nama, kategori, atau ganti file
   - 🗑️ Hapus dokumen
6. **Edit Dokumen**: Pada halaman **Edit**, Anda bisa:
   - Mengubah nama file tanpa menulis ekstensi,
   - Merubah kategori,
   - Mengganti file fisiknya.

---

## ⚠️ Troubleshooting

- `ModuleNotFoundError: No module named 'flask'`: Pastikan virtual environment aktif dan `pip install -r requirements.txt` sudah dijalankan.
- `Running scripts is disabled on this system`: Jalankan `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` di PowerShell.
- `Port 5000 already in use`: Hentikan proses lain atau jalankan `app.py` pada port berbeda.

---

## 📌 Catatan Penting

- Aplikasi ini menggunakan **moto** untuk memmock layanan AWS S3 secara lokal tanpa perlu akun AWS.
- Data dokumen hanya tersedia selama proses Flask berjalan dan tidak tersimpan di AWS asil.
- **Fitur Sidebar Toggle**: Posisi sidebar (buka/tutup) tersimpan di browser menggunakan localStorage, sehingga preferensi user teringat.
- **Dark Theme**: Aplikasi menggunakan dark theme dengan pola jaringan organisasi beranimasi untuk estetika modern.
- **Responsive Design**: Semua halaman responsif dan optimal di berbagai ukuran layar (desktop, tablet, mobile).
- **Form Centered**: Form upload dan edit ditampilkan terpusat untuk pengalaman pengguna yang lebih fokus dan elegan.
- **Logo Interaktif**: Saat sidebar collapsed, klik logo untuk toggle sidebar kembali (no hamburger button visible).

---

## 🎨 Peningkatan UI/UX

Aplikasi telah didesain ulang dengan fokus pada estetika dan user experience:

### Dark Theme Modern
- Background gelap (#0f172a) dengan gradient subtle untuk mengurangi kelelahan mata
- Text warna terang (#f1f5f9) untuk kontras optimal
- Accent colors: Indigo, Purple, Emerald untuk visual hierarchy

### Animasi & Transisi Smooth
- Cubic-bezier timing function untuk transisi natural
- 20-second drift animation untuk latar belakang pola jaringan
- Hover effects dengan scale dan shadow transforms
- Slide-down animation untuk alerts

### Responsive Layout
- Sidebar collapsible: 260px (expanded) → 60px (collapsed)
- Grid layout adaptive untuk desktop dan mobile
- Breakpoint 768px untuk tablet/mobile

### Fitur Accessibility
- Custom scrollbar dengan accent color
- Form labels dengan icon untuk clarity
- Color-coded badges untuk berbagai kategori dokumen
- Focus states dengan glow effect pada input fields

### Organizational Branding
- SVG pattern dengan jaringan organisasi (nodes dan connections)
- Hero banner di dashboard dengan organizational icons (👥 📊 🎯 📱)
- Consistent color scheme yang mencerminkan profesionalisme ORMAWA
