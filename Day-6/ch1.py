import base64

ciphertext = base64.b64decode("yRvuVex/1U/YeNJUwyLdcf5/w0r4FJZNpS6fT+E=")

def xor_decrypt(data, key):
    key_bytes = key if isinstance(key, bytes) else key.encode()
    return bytes([data[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(data))])

# Coba flag format UPI{ untuk tebak key
print("=== Known plaintext attack (assuming starts with UPI{) ===")
known = b"UPI{"
for i in range(len(known)):
    print(f"  key[{i}] = 0x{ciphertext[i] ^ known[i]:02x} = {chr(ciphertext[i] ^ known[i])}")

# Reconstruct key dari known plaintext
key_partial = bytes([ciphertext[i] ^ known[i] for i in range(len(known))])
print(f"  Partial key: {key_partial} = {key_partial.hex()}")

# Coba extend key asumsi key adalah kata
for keylen in range(1, 20):
    key_candidate = bytes([ciphertext[i % keylen] ^ 0x00 for i in range(keylen)])  # placeholder
    # Known plaintext attack properly
    if keylen >= 4:
        # key derived from known plaintext
        key_from_kpa = bytes([ciphertext[i] ^ known[i % len(known)] for i in range(keylen)])
        result = xor_decrypt(ciphertext, key_from_kpa)
        try:
            decoded = result.decode('utf-8')
            if decoded.isprintable():
                print(f"  keylen={keylen}, key={key_from_kpa}: {decoded}")
        except:
            pass