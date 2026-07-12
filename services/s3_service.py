import boto3
from botocore.exceptions import ClientError
from config import Config
from datetime import datetime

class S3Service:
    def __init__(self):
        # Menginisialisasi koneksi ke AWS S3 menggunakan credential dari config
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION,
            endpoint_url=Config.AWS_ENDPOINT_URL
        )
        self.bucket_name = Config.AWS_BUCKET_NAME

    def list_files(self):
        """Mengambil seluruh daftar file dari S3 Bucket secara real-time"""
        files = []
        try:
            # Menggunakan list_objects_v2 untuk mengambil isi bucket
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            
            # Jika bucket tidak kosong
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    
                    # S3 menggunakan '/' sebagai penanda folder (prefix)
                    if '/' in key:
                        category, filename = key.split('/', 1)
                    else:
                        category = 'Tanpa Kategori'
                        filename = key
                        
                    # Lewati jika key berupa folder kosong (hanya nama kategori dengan akhiran '/')
                    if not filename:
                        continue
                        
                    files.append({
                        'key': key,
                        'filename': filename,
                        'category': category,
                        'size': obj['Size'],              # Ukuran dalam bytes
                        'last_modified': obj['LastModified'] # Tanggal dari AWS
                    })
            # Urutkan file berdasarkan tanggal upload terbaru
            files.sort(key=lambda x: x['last_modified'], reverse=True)
        except ClientError as e:
            print(f"Error AWS S3: {e}")
        return files

    def upload_file(self, file_obj, category, filename):
        """Mengunggah file ke S3 dengan format: Kategori/NamaFile"""
        # Gabungkan kategori dan nama file menjadi S3 Object Key
        s3_key = f"{category}/{filename}"
        try:
            # Menggunakan upload_fileobj sesuai spesifikasi tugas
            self.s3_client.upload_fileobj(file_obj, self.bucket_name, s3_key)
            return True
        except ClientError as e:
            print(f"Gagal Upload: {e}")
            return False

    def download_file(self, s3_key, file_obj):
        """Mengunduh file dari S3 ke memori objek"""
        try:
            self.s3_client.download_fileobj(self.bucket_name, s3_key, file_obj)
            return True
        except ClientError as e:
            print(f"Gagal Download: {e}")
            return False

    def delete_file(self, s3_key):
        """Menghapus objek dari S3 berdasarkan Key-nya"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            print(f"Gagal Hapus: {e}")
            return False

    def file_exists(self, s3_key):
        """Memeriksa apakah objek sudah ada di bucket."""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            code = e.response.get('Error', {}).get('Code')
            if code in ('404', 'NoSuchKey', 'NotFound'):
                return False
            print(f"Error head_object: {e}")
            return False

    def get_file(self, s3_key):
        """Mengambil metadata file dari daftar objek berdasarkan key."""
        for file in self.list_files():
            if file['key'] == s3_key:
                return file
        return None

    def rename_file(self, old_key, new_key):
        """Mengganti nama objek S3 dengan menyalin lalu menghapus yang lama."""
        if old_key == new_key:
            return True

        try:
            copy_source = {'Bucket': self.bucket_name, 'Key': old_key}
            self.s3_client.copy_object(Bucket=self.bucket_name, CopySource=copy_source, Key=new_key)
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=old_key)
            return True
        except ClientError as e:
            print(f"Gagal Rename: {e}")
            return False

    def get_dashboard_stats(self):
        """Menghitung statistik real-time dari S3 untuk halaman utama Dashboard"""
        all_files = self.list_files()
        
        total_documents = len(all_files)
        total_bytes = sum(f['size'] for f in all_files)
        
        # Mengubah bytes menjadi MegaBytes (MB) dengan pembulatan 2 angka di belakang koma
        total_storage_mb = round(total_bytes / (1024 * 1024), 2)
        
        # Menghitung jumlah file unik per kategori
        category_counts = {cat: 0 for cat in Config.CATEGORIES}
        for f in all_files:
            if f['category'] in category_counts:
                category_counts[f['category']] += 1
                
        # Ambil 5 dokumen terbaru saja untuk dipajang
        recent_documents = all_files[:5]
        
        return {
            'total_documents': total_documents,
            'total_categories': len(Config.CATEGORIES),
            'total_storage': f"{total_storage_mb} MB",
            'category_counts': category_counts,
            'recent_documents': recent_documents
        }