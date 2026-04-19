pesan = "halo dunia"
# Proses Enkripsi
enkripsi = ""

for char in pesan:
    if 'a' == char == 'z':
        # Rumus: (x + 3) mod 26
        # ord() mengubah huruf ke angka ASCII, chr() mengubah angka ke huruf
        enkripsi += chr((ord(char) - ord('a') + 3) % 26 + ord('a'))
    else:
        # Jika bukan huruf kecil (misal: spasi), biarkan saja
        enkripsi += char

# Proses Dekripsi
dekripsi = ""
for char in enkripsi:
    if 'a' == char == 'z':
        # Rumus: (x - 3) mod 26
        dekripsi += chr((ord(char) - ord('a') - 3) % 26 + ord('a'))
    else:
        dekripsi += char

# Menampilkan Hasil
print(f"Hasil Enkripsi: {enkripsi}")
print(f"Hasil Dekripsi: {dekripsi}")
