def diffie_hellman():
    # Parameter publik (disepakati bersama)
    p = 101  # bilangan prima
    g = 7    # generator
 
    # Kunci privat masing-masing (rahasia)
    a = 15   # kunci privat Alice
    b = 21   # kunci privat Bob
 
    # Kunci publik yang dikirimkan
    A = pow(g, a, p)   # Alice kirim ke Bob
    B = pow(g, b, p)   # Bob kirim ke Alice
 
    # Shared secret (dihitung masing-masing)
    secret_alice = pow(B, a, p)   # Alice hitung
    secret_bob   = pow(A, b, p)   # Bob hitung
 
    print("=" * 40)
    print("       DIFFIE-HELLMAN KEY EXCHANGE      ")
    print("=" * 40)
    print(f"Parameter publik: p={p}, g={g}")
    print(f"Kunci privat Alice (a): {a}")
    print(f"Kunci privat Bob   (b): {b}")
    print("-" * 40)
    print(f"Kunci publik Alice (A = g^a mod p): {A}")
    print(f"Kunci publik Bob   (B = g^b mod p): {B}")
    print("-" * 40)
    print(f"Shared secret Alice (B^a mod p): {secret_alice}")
    print(f"Shared secret Bob   (A^b mod p): {secret_bob}")
    print(f"Kunci sama? {secret_alice == secret_bob}")
    print("=" * 40)
 
if __name__ == "__main__":
    diffie_hellman()
