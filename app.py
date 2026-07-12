import os
import io
import boto3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from werkzeug.utils import secure_filename
# pyrefly: ignore [missing-import]
from moto import mock_aws
from config import Config
from services.s3_service import S3Service

# 1. Inisialisasi Objek Flask & Konfigurasi
app = Flask(__name__)
app.config.from_object(Config)

# 2. Mengaktifkan Simulator AWS S3 Lokal Menggunakan Moto (RAM-Based)
mock_s3 = mock_aws()
mock_s3.start()

# 3. Membuat Wadah/Bucket Otomatis Saat Aplikasi Menyala
s3_client = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name=Config.AWS_REGION
)
try:
    s3_client.create_bucket(Bucket=Config.AWS_BUCKET_NAME)
    print(f"[*] Sukses membuat Local Bucket: '{Config.AWS_BUCKET_NAME}'")
except Exception as e:
    print(f"[!] Gagal inisialisasi Local Bucket: {str(e)}")


# -------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------

def allowed_file(filename: str) -> bool:
    """Validasi format ekstensi berkas dokumen."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def login_required(f):
    """Decorator: Melindungi route agar hanya bisa diakses saat sudah login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Silakan login terlebih dahulu untuk mengakses halaman ini.", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# -------------------------------------------------------------------------
# AUTENTIKASI
# -------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Halaman login sistem."""
    # Jika sudah login, langsung ke dashboard
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if username == Config.LOGIN_USERNAME and password == Config.LOGIN_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            flash(f"Selamat datang, {username}! Anda berhasil masuk.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Username atau password salah. Coba lagi.", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Menghapus sesi login dan kembali ke halaman login."""
    session.clear()
    flash("Anda telah berhasil keluar dari sistem.", "success")
    return redirect(url_for('login'))


# -------------------------------------------------------------------------
# LAYER RUTING WEB (FLASK ROUTES) - DILINDUNGI LOGIN
# -------------------------------------------------------------------------

@app.route('/')
@login_required
def dashboard():
    """Menampilkan statistik ringkasan arsip dokumen dari S3."""
    try:
        s3_service = S3Service()
        stats = s3_service.get_dashboard_stats()
    except Exception as e:
        app.logger.error(f"Error Dashboard: {str(e)}")
        flash("Gagal terhubung dengan layanan S3 Cloud lokal.", "danger")
        stats = {'total_documents': 0, 'total_categories': 0, 'total_storage': "0.00 MB", 'category_counts': {}, 'recent_documents': []}
    return render_template('dashboard.html', stats=stats)


@app.route('/documents')
@login_required
def documents():
    """Menampilkan seluruh dokumen dengan filter pencarian berkas."""
    search_query = request.args.get('search', '').strip().lower()
    category_filter = request.args.get('category', '').strip()

    s3_service = S3Service()
    all_files = s3_service.list_files()
    filtered_files = []

    for file in all_files:
        match_search = search_query in file['filename'].lower() if search_query else True
        match_category = file['category'] == category_filter if category_filter else True

        if match_search and match_category:
            filtered_files.append(file)

    return render_template('documents.html', files=filtered_files, categories=Config.CATEGORIES)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Memproses inputan dokumen baru dari user menuju S3."""
    if request.method == 'POST':
        if 'document_file' not in request.files:
            flash("Form rusak, file tidak terdeteksi.", "danger")
            return redirect(request.url)

        file = request.files['document_file']
        category = request.form.get('category')

        if not category or category not in Config.CATEGORIES:
            flash("Silakan pilih kategori dokumen resmi.", "warning")
            return redirect(request.url)

        if file.filename == '':
            flash("Anda belum memilih berkas apa pun.", "warning")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Format berkas ditolak oleh sistem keamanan!", "danger")
            return redirect(request.url)

        custom_name = request.form.get('custom_filename', '').strip()
        if custom_name:
            filename_base = secure_filename(custom_name)
            if not filename_base:
                flash("Nama berkas tidak valid.", "warning")
                return redirect(request.url)
            if '.' not in filename_base and '.' in file.filename:
                filename_base = f"{filename_base}.{file.filename.rsplit('.', 1)[1]}"
            filename = filename_base
        else:
            filename = secure_filename(file.filename)

        # Mengirimkan berkas via service layer
        s3_service = S3Service()
        success = s3_service.upload_file(file, category, filename)

        if success:
            flash(f"Berkas '{filename}' berhasil masuk ke cloud cluster.", "success")
            return redirect(url_for('documents'))
        else:
            flash("Gagal mengunggah dokumen ke S3.", "danger")

    return render_template('upload.html', categories=Config.CATEGORIES)


@app.route('/download/<path:s3_key>')
@login_required
def download(s3_key):
    """Mengunduh file langsung secara biner (stream) dari memori S3."""
    s3_service = S3Service()
    file_stream = io.BytesIO()

    success = s3_service.download_file(s3_key, file_stream)

    if success:
        file_stream.seek(0)
        filename = s3_key.split('/')[-1]
        return send_file(file_stream, as_attachment=True, download_name=filename, max_age=0)
    else:
        flash("Gagal mengambil data dari server cloud.", "danger")
        return redirect(url_for('documents'))


@app.route('/delete/<path:s3_key>', methods=['POST'])
@login_required
def delete(s3_key):
    """Menghapus objek berkas di dalam S3 cluster."""
    s3_service = S3Service()
    success = s3_service.delete_file(s3_key)

    if success:
        flash("Dokumen sukses dihapus dari penyimpanan.", "success")
    else:
        flash("Gagal menghapus berkas dokumen.", "danger")
    return redirect(url_for('documents'))


@app.route('/edit/<path:s3_key>', methods=['GET', 'POST'])
@login_required
def edit(s3_key):
    """Menampilkan form edit metadata dokumen dan memproses rename objek S3."""
    s3_service = S3Service()
    file = s3_service.get_file(s3_key)
    if not file:
        flash("Dokumen tidak ditemukan.", "danger")
        return redirect(url_for('documents'))

    if request.method == 'POST':
        custom_name = request.form.get('custom_filename', '').strip()
        category = request.form.get('category')
        uploaded_file = request.files.get('document_file')
        file_replacement = uploaded_file and uploaded_file.filename != ''

        if category not in Config.CATEGORIES:
            flash("Kategori dokumen tidak valid.", "warning")
            return redirect(request.url)

        target_filename = file['filename']
        if custom_name:
            filename_base = secure_filename(custom_name)
            if not filename_base:
                flash("Nama berkas tidak valid.", "warning")
                return redirect(request.url)
            if '.' not in filename_base:
                extension = None
                if file_replacement and '.' in uploaded_file.filename:
                    extension = uploaded_file.filename.rsplit('.', 1)[1]
                elif '.' in file['filename']:
                    extension = file['filename'].rsplit('.', 1)[1]
                if extension:
                    filename_base = f"{filename_base}.{extension}"
            target_filename = filename_base
        elif file_replacement:
            target_filename = secure_filename(uploaded_file.filename)
            if not target_filename:
                flash("Nama berkas dari file upload tidak valid.", "warning")
                return redirect(request.url)

        if not allowed_file(target_filename):
            flash("Format berkas ditolak oleh sistem keamanan!", "danger")
            return redirect(request.url)

        new_key = f"{category}/{target_filename}"
        if new_key != s3_key and s3_service.file_exists(new_key):
            flash("Berkas dengan nama tersebut sudah ada. Gunakan nama lain.", "warning")
            return redirect(request.url)

        if file_replacement:
            success = s3_service.upload_file(uploaded_file, category, target_filename)
            if not success:
                flash("Gagal mengunggah file baru ke S3.", "danger")
                return redirect(request.url)
            if new_key != s3_key:
                s3_service.delete_file(s3_key)
        elif new_key != s3_key:
            success = s3_service.rename_file(s3_key, new_key)
            if not success:
                flash("Gagal memperbarui dokumen.", "danger")
                return redirect(request.url)
        else:
            flash("Tidak ada perubahan yang disimpan.", "info")
            return redirect(request.url)

        flash(f"Dokumen berhasil diperbarui menjadi '{target_filename}'.", "success")
        return redirect(url_for('documents'))

    return render_template('edit.html', file=file, categories=Config.CATEGORIES)


# 5. Menjalankan Server Lokal Flask
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)