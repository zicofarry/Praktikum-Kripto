import hashlib
import hmac

# BAGIAN 1: Hashing dengan SHA-256 (Tanpa Kunci)
# Digunakan untuk: Verifikasi integritas dokumen

print("=" * 65)
print("  SISTEM VERIFIKASI INTEGRITAS DOKUMEN AKADEMIK")
print("  Menggunakan SHA-256 dan HMAC-SHA256")
print("=" * 65)

# Contoh Data Dokumen Akademik (Hardcoded)
dokumen_transkrip = "Nama: Budi Santoso | NIM: 13522001 | IPK: 3.85 | Semester: 8"
dokumen_ijazah = "Universitas XYZ | Program Studi: Informatika | Lulus: 2026 | Predikat: Cum Laude"
dokumen_surat = "Surat Keterangan Aktif | NIM: 13522001 | Tahun Ajaran: 2025/2026"

# Dokumen yang sudah dimodifikasi (untuk simulasi tampering)
dokumen_transkrip_palsu = "Nama: Budi Santoso | NIM: 13522001 | IPK: 3.95 | Semester: 8"  # IPK diubah

print("\n" + "-" * 65)
print("BAGIAN 1: HASHING DENGAN SHA-256 (Verifikasi Integritas)")
print("-" * 65)

# Fungsi hashing SHA-256
def hash_sha256(data: str) -> str:
    """Menghitung hash SHA-256 dari string input."""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

# Hitung hash untuk setiap dokumen
hash_transkrip = hash_sha256(dokumen_transkrip)
hash_ijazah = hash_sha256(dokumen_ijazah)
hash_surat = hash_sha256(dokumen_surat)
hash_transkrip_palsu = hash_sha256(dokumen_transkrip_palsu)

print("\n[1] Dokumen Transkrip")
print(f"    Data Asli  : {dokumen_transkrip}")
print(f"    SHA-256    : {hash_transkrip}")

print("\n[2] Dokumen Ijazah")
print(f"    Data Asli  : {dokumen_ijazah}")
print(f"    SHA-256    : {hash_ijazah}")

print("\n[3] Dokumen Surat Keterangan")
print(f"    Data Asli  : {dokumen_surat}")
print(f"    SHA-256    : {hash_surat}")

# Simulasi Verifikasi Integritas
print("\n" + "-" * 65)
print("SIMULASI VERIFIKASI INTEGRITAS DOKUMEN")
print("-" * 65)

print("\n[!] Dokumen Transkrip ASLI:")
print(f"    Data  : {dokumen_transkrip}")
print(f"    Hash  : {hash_transkrip}")

print("\n[!] Dokumen Transkrip PALSU (IPK diubah dari 3.85 -> 3.95):")
print(f"    Data  : {dokumen_transkrip_palsu}")
print(f"    Hash  : {hash_transkrip_palsu}")

if hash_transkrip == hash_transkrip_palsu:
    print("\n    >> HASIL: Hash SAMA - Dokumen TIDAK berubah (identik)")
else:
    print("\n    >> HASIL: Hash BERBEDA - Dokumen TERDETEKSI telah dimodifikasi!")
    print("    >> PERINGATAN: Integritas dokumen terganggu!")

# BAGIAN 2: HMAC-SHA256 (Dengan Kunci Rahasia)
# Digunakan untuk: Autentikasi dokumen antar pihak

print("\n\n" + "-" * 65)
print("BAGIAN 2: HMAC-SHA256 (Autentikasi dengan Kunci Rahasia)")
print("-" * 65)

# Kunci rahasia yang dibagikan antara Fakultas dan Rektorat
kunci_rahasia = b"KunciRahasiaFakultasRektorat2026!"

# Dokumen resmi yang dikirim
dokumen_resmi = "Surat Rekomendasi | Dari: Dekan Fakultas Informatika | Untuk: Rektorat | Perihal: Beasiswa Mahasiswa Berprestasi"

def hitung_hmac_sha256(kunci: bytes, data: str) -> str:
    """Menghitung HMAC-SHA256 dari data dengan kunci rahasia."""
    return hmac.new(kunci, data.encode('utf-8'), hashlib.sha256).hexdigest()

# Pengirim (Fakultas) menghitung HMAC
hmac_pengirim = hitung_hmac_sha256(kunci_rahasia, dokumen_resmi)

print("\n--- Sisi Pengirim (Fakultas) ---")
print(f"    Dokumen    : {dokumen_resmi}")
print(f"    Kunci      : {kunci_rahasia.decode()}")
print(f"    HMAC-SHA256: {hmac_pengirim}")

# Simulasi Penerima (Rektorat) memverifikasi
print("\n--- Sisi Penerima (Rektorat) ---")

# Dokumen diterima tanpa perubahan
hmac_penerima = hitung_hmac_sha256(kunci_rahasia, dokumen_resmi)
print("\n[Skenario 1] Dokumen diterima TANPA perubahan:")
print(f"    HMAC Pengirim : {hmac_pengirim}")
print(f"    HMAC Penerima : {hmac_penerima}")

if hmac.compare_digest(hmac_pengirim, hmac_penerima):
    print("    >> HASIL: HMAC COCOK - Dokumen AUTENTIK dan UTUH!")
else:
    print("    >> HASIL: HMAC TIDAK COCOK - Dokumen TIDAK autentik!")

# Dokumen dimodifikasi oleh pihak ketiga (man-in-the-middle)
dokumen_dimodifikasi = "Surat Rekomendasi | Dari: Dekan Fakultas Informatika | Untuk: Rektorat | Perihal: Beasiswa Semua Mahasiswa"
hmac_dokumen_palsu = hitung_hmac_sha256(kunci_rahasia, dokumen_dimodifikasi)

print("\n[Skenario 2] Dokumen DIMODIFIKASI oleh penyerang:")
print(f"    Dokumen Asli       : ...Perihal: Beasiswa Mahasiswa Berprestasi")
print(f"    Dokumen Dimodifikasi: ...Perihal: Beasiswa Semua Mahasiswa")
print(f"    HMAC Pengirim      : {hmac_pengirim}")
print(f"    HMAC Dok. Palsu    : {hmac_dokumen_palsu}")

if hmac.compare_digest(hmac_pengirim, hmac_dokumen_palsu):
    print("    >> HASIL: HMAC COCOK - Dokumen autentik")
else:
    print("    >> HASIL: HMAC TIDAK COCOK - Dokumen TERDETEKSI dipalsukan!")

# Penyerang mencoba dengan kunci berbeda
kunci_palsu = b"KunciPalsuPenyerang12345678901!"
hmac_kunci_palsu = hitung_hmac_sha256(kunci_palsu, dokumen_resmi)

print("\n[Skenario 3] Penyerang menggunakan KUNCI BERBEDA:")
print(f"    Kunci Asli   : {kunci_rahasia.decode()}")
print(f"    Kunci Palsu  : {kunci_palsu.decode()}")
print(f"    HMAC Asli    : {hmac_pengirim}")
print(f"    HMAC Palsu   : {hmac_kunci_palsu}")

if hmac.compare_digest(hmac_pengirim, hmac_kunci_palsu):
    print("    >> HASIL: HMAC COCOK - Dokumen autentik")
else:
    print("    >> HASIL: HMAC TIDAK COCOK - Kunci tidak valid, autentikasi GAGAL!")

# RINGKASAN
print("\n\n" + "=" * 65)
print("  RINGKASAN")
print("=" * 65)
print("""
  1. SHA-256 (Hash biasa):
     - Digunakan untuk menjaga INTEGRITAS data
     - Perubahan sekecil apapun menghasilkan hash yang berbeda total
     - Tidak menggunakan kunci (siapapun bisa menghitung)

  2. HMAC-SHA256 (Hash + Kunci):
     - Digunakan untuk AUTENTIKASI + INTEGRITAS
     - Membutuhkan kunci rahasia yang sama di kedua pihak
     - Melindungi dari pemalsuan yang disengaja (man-in-the-middle)
""")
print("=" * 65)
