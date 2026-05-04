def ROTL(bits, word):
    return ((word << bits) | (word >> (32 - bits))) & 0xFFFFFFFF

def prosesBlok(H, blok):
    w = [0] * 80
    
    # 1. Bangun 16 Word pertama (dari kepingan 8-bit menjadi 32-bit Big-Endian)
    for i in range(16):
        w[i] = (blok[i*4] << 24) | (blok[i*4+1] << 16) | (blok[i*4+2] << 8) | blok[i*4+3]

    # 2. Ekspansi menjadi 80 Word
    for i in range(16, 80):
        w[i] = ROTL(1, w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16])

    # 3. Inisialisasi variabel sementara
    a, b, c, d, e = H[0], H[1], H[2], H[3], H[4]

    # 4. Siklus 80 Putaran
    for i in range(80):
        if i < 20:
            f = (b & c) | ((~b & 0xFFFFFFFF) & d)
            k = 0x5A827999
        elif i < 40:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif i < 60:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6

        # Hitung TEMP dan gunakan & 0xFFFFFFFF untuk meniru Modulo 2^32
        temp = (ROTL(5, a) + f + e + k + w[i]) & 0xFFFFFFFF
        
        # Geser posisi Register
        e = d
        d = c
        c = ROTL(30, b)
        b = a
        a = temp

    # 5. Update Nilai Hash Utama (selalu pastikan terpotong di 32-bit)
    H[0] = (H[0] + a) & 0xFFFFFFFF
    H[1] = (H[1] + b) & 0xFFFFFFFF
    H[2] = (H[2] + c) & 0xFFFFFFFF
    H[3] = (H[3] + d) & 0xFFFFFFFF
    H[4] = (H[4] + e) & 0xFFFFFFFF

def hitungSHA1(pesan):
    # LANGKAH 3: Inisialisasi MD Buffer (Menggunakan List/Array biasa)
    H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    # Persiapan data: bytearray mirip dengan vector<uint8_t> di C++
    data = bytearray(pesan.encode('utf-8'))
    bitLength = len(data) * 8

    # LANGKAH 1: Penambahan Padding Bits
    data.append(0x80)
    while (len(data) % 64) != 56:
        data.append(0x00)

    # LANGKAH 2: Penambahan Nilai Panjang Pesan Semula (64-bit Big Endian)
    for i in range(7, -1, -1):
        # & 0xFF memastikan kita hanya mengambil 8-bit paling kanan (meniru uint8_t)
        data.append((bitLength >> (i * 8)) & 0xFF)

    # LANGKAH 4 (Lanjutan): Pengolahan pesan per blok 512 bit (64 Byte)
    for i in range(0, len(data), 64):
        prosesBlok(H, data[i : i+64])

    # Konversi array H menjadi format string Hexadesimal bersambung
    return ''.join(f'{x:08x}' for x in H)

if __name__ == "__main__":
    input_text = "abc"
    print(f"Input  : {input_text}")
    print(f"SHA-1  : {hitungSHA1(input_text)}")
