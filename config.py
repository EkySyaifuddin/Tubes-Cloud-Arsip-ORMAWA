import os
from dotenv import load_dotenv

# Membaca file .env
load_dotenv()

class Config:
    # Konfigurasi Utama Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-key-jika-env-kosong')
    
    # Konfigurasi AWS S3
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION', 'ap-southeast-1')
    AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
    AWS_ENDPOINT_URL = os.getenv('AWS_ENDPOINT_URL')
    
    # Kategori Dokumen yang Diizinkan (Sesuai Spesifikasi)
    CATEGORIES = ['Proposal', 'LPJ', 'Surat', 'Notulen', 'Dokumentasi', 'SK']
    
    # Batasan Validasi File
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'xlsx', 'pptx', 'jpg', 'jpeg', 'png', 'zip'}
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024  # Maksimal 20 MB dalam ukuran bytes
    
    # Kredensial Login Sistem
    LOGIN_USERNAME = os.getenv('LOGIN_USERNAME', 'admin')
    LOGIN_PASSWORD = os.getenv('LOGIN_PASSWORD', 'ormawa2026')