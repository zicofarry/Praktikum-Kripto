ciphertext = "QBYXH ZXOX JBOBQXP QXKMX HRKZF"
print(f"Ciphertext: {ciphertext}")
print("Hasil Brute Force:")

for key in range(26):
    plaintext = ""
    for c in ciphertext:
        if 'A' <= c <= 'Z':
            # Rumus dekripsi: geser mundur sebanyak key
            p = chr((ord(c) - ord('A') - key) % 26 + ord('A'))
            plaintext += p
        else:
            # Karakter non-huruf (spasi, tanda baca) dibiarkan
            plaintext += c
    print(f"Kunci {key:2d}: {plaintext}")
