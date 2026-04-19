def xor_file(input_file, output_file, key):
    # Membuka file input dalam mode biner
    try:
        with open(input_file, 'rb') as fin:
            data = fin.read()
    except FileNotFoundError:
        print("Gagal membuka file!")
        return

    # Operasi XOR pada setiap byte
    result = bytes([b ^ key for b in data])

    # Menulis byte hasil XOR ke file tujuan
    with open(output_file, 'wb') as fout:
        fout.write(result)

    print(f"Proses selesai. File disimpan di: {output_file}")

if __name__ == "__main__":
    file_asal = "pesan.txt"
    file_hasil = "pesan_enkripsi.dat"
    kunci = 0x42  # Kunci bebas (1 byte)
    xor_file(file_asal, file_hasil, kunci)
