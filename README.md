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
- Upload dokumen dengan nama kustom.
- Edit metadata dokumen dan ganti isi file.
- Download dokumen dari browser.
- Hapus dokumen.
- Sidebar yang bisa disembunyikan/ditampilkan.
- Filtering dan pencarian dokumen berdasarkan nama atau kategori.

---

## ✅ Fitur Utama

- **Dashboard Ringkasan**: Total dokumen, total kategori, ukuran penyimpanan, dan daftar dokumen terbaru.
- **Upload Dokumen**: Unggah file dengan kategori dan nama file pilihan.
- **Edit Dokumen**: Perbarui nama, kategori, dan/atau ganti isi file.
- **File Replacement**: Saat mengganti dokumen, nama file baru tanpa ekstensi otomatis menggunakan ekstensi file lama.
- **Hide / Unhide Sidebar**: Sidebar dapat disembunyikan untuk tampilan lebih luas.
- **Validasi Ekstensi**: Hanya menerima `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.jpg`, `.jpeg`, `.png`, `.zip`.

---

## 🏗️ Arsitektur & Teknologi

Aplikasi ini terdiri dari:
- **Flask** sebagai backend web.
- **moto** sebagai simulator AWS S3 lokal.
- **Boto3** sebagai client AWS S3.
- **Jinja2** untuk templates HTML.
- **Bootstrap** untuk layout dan styling UI.

### Arsitektur Sederhana

Browser → Flask (`app.py`) → Service S3 lokal (`services/s3_service.py`) → moto S3 mock

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

1. Login menggunakan kredensial di `.env`.
2. Buka halaman **Upload** untuk menambahkan dokumen.
3. Gunakan halaman **Documents** untuk mencari, mengunduh, mengedit, atau menghapus file.
4. Pada halaman **Edit**, Anda bisa:
   - mengubah nama file tanpa menulis ekstensi,
   - merubah kategori,
   - mengganti file fisiknya.

---

## ⚠️ Troubleshooting

- `ModuleNotFoundError: No module named 'flask'`: Pastikan virtual environment aktif dan `pip install -r requirements.txt` sudah dijalankan.
- `Running scripts is disabled on this system`: Jalankan `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` di PowerShell.
- `Port 5000 already in use`: Hentikan proses lain atau jalankan `app.py` pada port berbeda.

---

## 📌 Catatan Penting

- Aplikasi ini menggunakan **moto** untuk memmock layanan AWS S3 secara lokal.
- Data dokumen hanya tersedia selama proses Flask berjalan dan tidak tersimpan di AWS asli.
- Fitur `file edit` sudah diperbarui untuk memungkinkan nama baru tanpa ekstensi dan mengganti isi file bila diunggah ulang.
