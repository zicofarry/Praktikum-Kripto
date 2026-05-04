import hashlib
pesan = b"FuFuFaFa"
hasil_hash = hashlib.sha3_256(pesan).hexdigest()
print(hasil_hash)
