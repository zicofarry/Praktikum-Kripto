import pyaes

def print_hex(label, data):
    hex_str = ' '.join(f'{b:02x}' for b in data)
    print(f"{label}: {hex_str}")

if __name__ == "__main__":
    # 1. Kunci 128-bit (16 Karakter)
    key = b'mykuncirahasia36'

    # 2. Data yang mau dienkripsi (Wajib 16 byte untuk 1 blok ECB)
    plaintext = b'Halo Z1c0f4rry!\x00'

    print("=== PROSES AES-128 ECB ===")
    print(f"Data Asli : {plaintext.decode(errors='replace')}")

    # 3. ENKRIPSI
    # Inisialisasi AES ECB encryptor
    aes_enc = pyaes.AESModeOfOperationECB(key)
    ciphertext = aes_enc.encrypt(plaintext)

    print_hex("Terenskripsi", ciphertext)

    # 4. DEKRIPSI
    aes_dec = pyaes.AESModeOfOperationECB(key)
    decrypted = aes_dec.decrypt(ciphertext)

    print(f"Hasil Kembali: {decrypted.decode(errors='replace')}")
    print("==========================")
