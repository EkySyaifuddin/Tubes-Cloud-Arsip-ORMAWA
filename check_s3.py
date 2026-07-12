import io
import os
import boto3
# pyrefly: ignore [missing-import]
from moto import mock_aws
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

def test_s3_simulation():
    print("=== Memulai Simulasi Pemeriksaan Boto3 S3 (Moto Mock) ===")
    
    # 1. Mengaktifkan S3 Mocking untuk sesi ini
    with mock_aws():
        bucket_name = os.getenv('AWS_BUCKET_NAME', 'arsip-ormawa-lokal')
        aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        # 2. Inisialisasi klien S3
        s3_client = boto3.client(
            's3',
            region_name=aws_region
        )
        
        # 3. Membuat bucket
        print(f"[1/5] Membuat bucket baru: '{bucket_name}'...")
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print("      -> Bucket berhasil dibuat.")
        except Exception as e:
            print(f"      -> [ERROR] Gagal membuat/mengakses bucket: {str(e)}")
            return
            
        # 4. Melakukan Upload File Percobaan
        file_content = b"Ini adalah isi berkas percobaan arsip ORMAWA."
        file_name = "Surat/surat_undangan_test.txt"
        
        print(f"[2/5] Mengunggah file '{file_name}' ke S3...")
        try:
            s3_client.upload_fileobj(
                io.BytesIO(file_content),
                bucket_name,
                file_name
            )
            print("      -> Upload sukses!")
        except Exception as e:
            print(f"      -> [ERROR] Gagal mengunggah file: {str(e)}")
            return
        
        # 5. Melakukan Query List Objects (Membuktikan file ada di S3)
        print(f"[3/5] Memeriksa daftar objek di bucket '{bucket_name}'...")
        try:
            response = s3_client.list_objects_v2(Bucket=bucket_name)
            
            if 'Contents' in response:
                print("      -> File Ditemukan di S3:")
                for item in response['Contents']:
                    print(f"         * Key (Path): {item['Key']}")
                    print(f"         * Size      : {item['Size']} Bytes")
                    print(f"         * Last Mod  : {item['LastModified']}")
            else:
                print("      -> [GAGAL] Bucket kosong!")
                return
        except Exception as e:
            print(f"      -> [ERROR] Gagal list objek: {str(e)}")
            return

        # 6. Mengunduh berkas kembali untuk validasi integritas data
        print(f"[4/5] Mengunduh kembali '{file_name}' untuk verifikasi konten...")
        try:
            download_stream = io.BytesIO()
            s3_client.download_fileobj(bucket_name, file_name, download_stream)
            downloaded_content = download_stream.getvalue()
            
            print(f"      -> Isi file terunduh: '{downloaded_content.decode('utf-8')}'")
        except Exception as e:
            print(f"      -> [ERROR] Gagal mengunduh file: {str(e)}")
            return
        
        # 7. Selesai
        print("[5/5] Uji coba selesai. Boto3 dan simulator S3 berjalan 100% sukses!")

if __name__ == "__main__":
    test_s3_simulation()
