import hashlib
import itertools

# ── Konfigurasi target ──
SSID = "HotspotPraktikum"
TARGET_PSK = "praktikum2026"  # passphrase yang ingin ditemukan


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


# Generate target hash (yang mau dicocokkan)
target_hash = derive_psk(TARGET_PSK, SSID)


# ── Dictionary Attack ──────────────────────────────────────────
print("[*] Memulai Dictionary Attack...")

wordlist = [
    "password",
    "12345678",
    "praktikum",
    "praktikum2026",
    "wifi1234",
    "abcdefgh",
    "qwerty123"
]

found = False

for word in wordlist:
    candidate_hash = derive_psk(word, SSID)
    print(f"    Mencoba: {word}")

    if candidate_hash == target_hash:
        print(f"[+] PASSWORD DITEMUKAN (Dictionary): {word}")
        found = True
        break

if not found:
    print(f"\n[*] {TARGET_PSK} Tidak ditemukan di dictionary.")

