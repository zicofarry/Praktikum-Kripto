def xor_file_128bit(input_file, output_file, key_16bytes):
    try:
        with open(input_file, 'rb') as fin:
            data = fin.read()
    except FileNotFoundError:
        print("Gagal membuka file!")
        return

    # 128 bits = 16 bytes
    block_size = 16
    result = bytearray()

    for i in range(0, len(data), block_size):
        block = data[i:i+block_size]
        # Proses XOR blok 128-bit dengan kunci 128-bit
        xor_block = bytes([
            b ^ key_16bytes[j % len(key_16bytes)]
            for j, b in enumerate(block)
        ])
        result.extend(xor_block)

    with open(output_file, 'wb') as fout:
        fout.write(result)

    print("Proses blok 128-bit selesai!")

if __name__ == "__main__":
    # Kunci 128-bit (16 karakter/byte)
    key_str = "HIDUPJOKOWI12345"
    key = key_str.encode('utf-8')

    xor_file_128bit("gambar.jpg", "gambar_aman.dat", key)
