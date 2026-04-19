def cari_fpb(a, b):
    """Mencari FPB (Faktor Persekutuan Terbesar)"""
    while b != 0:
        a, b = b, a % b
    return a
 
def cari_mod_inverse(e, phi):
    """Mencari Modular Multiplicative Inverse untuk Private Key (d)"""
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return 1
 
def bangkitkan_kunci(p, q):
    # 1. Menghitung Modulus (n)
    n = p * q
 
    # 2. Menghitung Totient / Euler Phi
    phi = (p - 1) * (q - 1)
 
    # 3. Mencari Eksponen Publik (e)
    e = 2
    while e < phi:
        if cari_fpb(e, phi) == 1:
            break
        e += 1
 
    # 4. Mencari Eksponen Privat (d)
    d = cari_mod_inverse(e, phi)
 
    print("=" * 40)
    print("      PROSES PEMBANGKITAN KUNCI        ")
    print("=" * 40)
    print(f"Bilangan Prima p    : {p}")
    print(f"Bilangan Prima q    : {q}")
    print(f"Modulus (n = p*q)   : {n}")
    print(f"Euler Phi (p-1)(q-1): {phi}")
    print("-" * 40)
    print(f"PUBLIC KEY (e, n)   : ({e}, {n})")
    print(f"PRIVATE KEY (d, n)  : ({d}, {n})")
    print("=" * 40)
 
    return {"n": n, "e": e, "d": d}

def enkripsi(basis, eksponen, n):
    """Modular exponentiation: (basis ^ eksponen) mod n"""
    hasil = 1
    basis = basis % n
    while eksponen > 0:
        if eksponen % 2 == 1:
            hasil = (hasil * basis) % n
        basis = (basis * basis) % n
        eksponen = eksponen // 2
    return hasil
 
if __name__ == "__main__":
    # Bangkitkan kunci
    kunci = bangkitkan_kunci(61, 53)
    print(f"Kunci E yang didapat: {kunci['e']}")
 
    pesan = 65
 
    # Enkripsi dengan kunci publik
    encrypted = enkripsi(pesan, kunci["e"], kunci["n"])
    print(f"Pesan asli    : {pesan}")
    print(f"Hasil Enkripsi: {encrypted}")
