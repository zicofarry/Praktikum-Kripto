import hashlib

# ── Konfigurasi target ──
SSID = "HotspotPraktikum"

def derive_psk(passphrase, ssid):
    """
    Simulasi PBKDF2-SHA1:
    passphrase + SSID -> PSK 256-bit
    """
    return hashlib.pbkdf2_hmac(
        'sha1',
        passphrase.encode('utf-8'),
        ssid.encode('utf-8'),
        iterations=4096,
        dklen=32
    ).hex()

# ── Dictionary Attack ──────────────────────────────────────────
wordlist = [
    "password",
    "12345678",
    "praktikum",
    "praktikum2026",
    "wifi1234",
    "abcdefgh",
    "qwerty123",
    # 10 Kandidat password baru
    "kriptografi",
    "kripto123",
    "rahasia123",
    "admin123",
    "jarkom2026",
    "ilkom2026",
    "mahasiswa",
    "semangka",
    "password123",
    "bismillah"
]

def run_simulation(scenario_name, target_psk):
    print(f"=== {scenario_name} ===")
    print(f"Target Password: {target_psk}")
    print("[*] Memulai Dictionary Attack...")
    
    target_hash = derive_psk(target_psk, SSID)
    found = False

    for word in wordlist:
        candidate_hash = derive_psk(word, SSID)
        print(f"    Mencoba: {word}")

        if candidate_hash == target_hash:
            print(f"[+] PASSWORD DITEMUKAN (Dictionary): {word}")
            found = True
            break

    if not found:
        print(f"[-] PASSWORD TIDAK DITEMUKAN di dictionary.")
    print("-" * 50 + "\n")

if __name__ == "__main__":
    # Skenario 1: Cracking salah satu password baru yang ada di dictionary
    run_simulation("Skenario 1: Password Ditemukan", "rahasia123")
    
    # Skenario 2: Cracking password yang tidak ada di dictionary
    run_simulation("Skenario 2: Password Tidak Ditemukan", "supersecret999")
