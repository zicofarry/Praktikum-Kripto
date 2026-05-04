import ctypes
import os

# 1. Muat (Load) Shared Library C yang sudah kita kompilasi tadi
# Gunakan 'keccak.so' jika Anda di Linux/Mac
lib_path = os.path.abspath("keccak.dll") 
keccak_lib = ctypes.CDLL(lib_path)

# 2. Definisikan tipe argumen (Signature) agar Python tidak salah mengirim tipe memori ke C
keccak_lib.Keccak.argtypes = [
    ctypes.c_uint,                  # rate
    ctypes.c_uint,                  # capacity
    ctypes.c_char_p,                # input (pointer ke string/bytes)
    ctypes.c_ulonglong,             # inputByteLen
    ctypes.c_ubyte,                 # delimitedSuffix
    ctypes.POINTER(ctypes.c_ubyte), # output (pointer ke array byte)
    ctypes.c_ulonglong              # outputByteLen
]

def hitung_SHA3_256_via_C(pesan):
    # Ubah string Python menjadi bytes (C-string)
    input_bytes = pesan.encode('utf-8')
    input_len = len(input_bytes)
    
    # Siapkan "ruang kosong" di memori untuk diisi oleh fungsi C
    # Karena SHA3-256 butuh 32 byte, kita buat array C berukuran 32
    output_buffer = (ctypes.c_ubyte * 32)()
    
    # 3. Panggil fungsi C-nya!
    keccak_lib.Keccak(
        1088,           # rate
        512,            # capacity
        input_bytes,    # data input
        input_len,      # panjang input
        0x06,           # suffix untuk SHA-3
        output_buffer,  # tempat menaruh hasil
        32              # panjang output yang diminta
    )
    
    # 4. Ubah array C yang sudah terisi kembali menjadi string Hex Python
    return bytes(output_buffer).hex()

if __name__ == "__main__":
    teks = "FufuFafa"
    hasil_hash = hitung_SHA3_256_via_C(teks)
    
    print(f"Input   : {teks}")
    print(f"SHA3-256: {hasil_hash}")
