def proses_dengan_bitset(teks):
    for c in teks:
        # Mengubah 1 byte (char) menjadi representasi biner 8-bit
        b = format(ord(c), '08b')
        print(f"Karakter [{c}] biner: {b}")

        # Kamu bisa akses bit spesifik seperti string
        # b[7] adalah bit paling kanan (LSB)
        # b[0] adalah bit paling kiri (MSB)
        if b[7] == '1':
            # Sama dengan mengecek apakah bit ke-0 adalah 1
            pass
