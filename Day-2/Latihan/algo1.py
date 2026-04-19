def baca_bit(teks):
    for c in teks:
        # Kita tahu 1 char = 8 bit
        # Kita gunakan loop dari bit paling signifikan (MSB) ke paling rendah (LSB)
        for i in range(7, -1, -1):
            # Operasi Bitwise:
            # 1. (ord(c) >> i) menggeser bit ke posisi paling kanan
            # 2. & 1 membandingkan bit tersebut dengan 1 (masking)
            bit = (ord(c) >> i) & 1
            print(bit, end='')
        print(' ', end='')  # Spasi antar karakter agar mudah dibaca
    print()

if __name__ == "__main__":
    input_text = "saya"
    print(f"Teks: {input_text}")
    print("Bit : ", end='')
    baca_bit(input_text)
