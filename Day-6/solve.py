import base64

ciphertext = base64.b64decode("yRvuVex/1U/YeNJUwyLdcf5/w0r4FJZNpS6fT+E=")
known = b"UPI{"

key = [ciphertext[i] ^ known[i] for i in range(4)]
print("Partial key:", bytes(key))

def xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

print("Trying with repeating 4-byte key:")
print(xor(ciphertext, key))

print("Trying with William related keys:")
keys = [b"William", b"Hater", b"Frankfurt", b"Odessa", b"Paradeus", b"WilliamHater"]
for k in keys:
    res = xor(ciphertext, k)
    if b"UPI{" in res:
        print(f"Key {k}: {res}")
