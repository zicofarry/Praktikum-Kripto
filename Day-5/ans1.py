def solve_caesar_bruteforce(ciphertext):
    print(f"Ciphertext: {ciphertext}")
    for key in range(26):
        plaintext = ""
        for c in ciphertext:
            if 'A' <= c <= 'Z':
                # Rumus dekripsi: geser mundur sebanyak key
                p = chr((ord(c) - ord('A') - key) % 26 + ord('A'))
                plaintext += p
            else:
                # Karakter non-huruf dibiarkan (seperti spasi)
                plaintext += c
        print(f"Kunci {key:2d}: {plaintext}")

if __name__ == "__main__":
    print("=== SOAL 1 ===")
    solve_caesar_bruteforce("HTZPX ST XRWXQPC DWXBTHPBP")
    
    print("\n=== SOAL 2 ===")
    solve_caesar_bruteforce("RMTIASIV LMVOIV SITQUIB UC AMVLQZQ IXI QBC JZCBMNWZKM IBBIKS")
