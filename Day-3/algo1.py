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
 
if __name__ == "__main__":
    # Gunakan bilangan prima kecil untuk belajar
    # Jangan gunakan angka yang sama!
    p = 61
    q = 53
    bangkitkan_kunci(p, q)

