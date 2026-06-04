import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/drive']
DOCUMENT_ID = '1qglhoi2rKr1MP8wcj3ZzpNqull4ShV9RJjt6KldjZ6s'

def authenticate():
    creds = None
    token_file = 'token.pickle'
    if os.path.exists(token_file):
        with open(token_file, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file, 'wb') as f:
            pickle.dump(creds, f)
    return creds

def get_doc_end(docs_service):
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    content = doc.get('body', {}).get('content', [])
    last_idx = 1
    for el in content:
        if 'endIndex' in el:
            last_idx = max(last_idx, el['endIndex'] - 1)
    return last_idx

def insert_text(requests_list, idx, text):
    requests_list.append({
        'insertText': {
            'location': {'index': idx},
            'text': text
        }
    })

def update_style(requests_list, idx, length, bold=False, font_size=11, heading=False):
    requests_list.append({
        'updateParagraphStyle': {
            'range': {'startIndex': idx, 'endIndex': idx + length},
            'paragraphStyle': {
                'namedStyleType': 'NORMAL_TEXT',
                'spaceAbove': {'magnitude': 6, 'unit': 'PT'},
                'spaceBelow': {'magnitude': 6, 'unit': 'PT'},
            },
            'fields': 'namedStyleType,spaceAbove,spaceBelow'
        }
    })
    if bold or heading:
        if heading:
            requests_list.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': idx, 'endIndex': idx + length},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType'
                }
            })
        requests_list.append({
            'updateTextStyle': {
                'range': {'startIndex': idx, 'endIndex': idx + length},
                'textStyle': {'bold': True, 'fontSize': {'magnitude': 14 if heading else 11, 'unit': 'PT'}},
                'fields': 'bold,fontSize'
            }
        })

def add_table(requests_list, insert_idx, rows, cols, data):
    requests_list.append({
        'insertTable': {
            'location': {'index': insert_idx},
            'rows': rows,
            'columns': cols
        }
    })
    table_start = insert_idx + 1
    for r in range(rows):
        for c in range(cols):
            cell_start = table_start + (r * cols + c) * 2
            text = data[r][c] if r < len(data) and c < len(data[r]) else ''
            requests_list.append({
                'insertText': {
                    'location': {'index': cell_start},
                    'text': text
                }
            })
            requests_list.append({
                'updateTextStyle': {
                    'range': {'startIndex': cell_start, 'endIndex': cell_start + len(text)},
                    'textStyle': {'bold': r == 0, 'fontSize': {'magnitude': 9, 'unit': 'PT'}},
                    'fields': 'bold,fontSize'
                }
            })

def main():
    creds = authenticate()
    docs_service = build('docs', 'v1', credentials=creds)
    
    end = get_doc_end(docs_service)
    idx = end
    requests = []
    
    insert_text(requests, idx, '\n\n')
    idx += 2
    
    # ==================== TUGAS 1 ====================
    insert_text(requests, idx, 'TUGAS 1: Analisis Risiko Web Pembayaran Dummy\n\n')
    update_style(requests, idx, 48, heading=True)
    idx += 48
    
    insert_text(requests, idx, '1.1 Threat Model\n\n')
    update_style(requests, idx, 17, bold=True)
    idx += 17
    
    add_table(requests, idx, 7, 5, [
        ['Aset', 'Klasifikasi', 'Threat Actor', 'Threat', 'Dampak Potensial'],
        ['Data Pembayaran', 'Confidential', 'External Attacker', 'SQL Injection pada endpoint transaksi', 'Kebocoran data finansial nasabah secara massal'],
        ['Password User', 'Private', 'External Attacker', 'Password hash terekspos di API response', 'Hash dapat di-crack menggunakan lookup table'],
        ['Session Token', 'Private', 'External Attacker', 'JWT algorithm manipulation', 'Privilege escalation ke role admin'],
        ['Data Transaksi', 'Private', 'External Attacker', 'IDOR pada endpoint transaksi', 'Akses tidak sah ke data transaksi pengguna lain'],
        ['Kredensial Login', 'Private', 'External Attacker', 'Brute force pada endpoint login', 'Akun pengguna dapat diambil alih'],
        ['Data Profil Pengguna', 'Private', 'Internal Attacker', 'Stored XSS pada form profil', 'Eksekusi script berbahaya di browser pengguna lain'],
    ])
    idx += 100  # rough estimate
    
    insert_text(requests, idx, '\n\n1.2 Analisis Kuantitatif\n\n')
    update_style(requests, idx - 0, 24, bold=True)
    idx += 24
    
    add_table(requests, idx, 7, 6, [
        ['Threat', 'AV (Rp)', 'EF', 'SLE (Rp)', 'ARO', 'ALE (Rp)'],
        ['SQL Injection', '800.000.000', '60%', '480.000.000', '1', '480.000.000'],
        ['Exposed Hash', '200.000.000', '40%', '80.000.000', '2', '160.000.000'],
        ['JWT Manipulation', '500.000.000', '70%', '350.000.000', '0,5', '175.000.000'],
        ['IDOR', '300.000.000', '30%', '90.000.000', '1', '90.000.000'],
        ['Brute Force', '150.000.000', '50%', '75.000.000', '3', '225.000.000'],
        ['Stored XSS', '250.000.000', '35%', '87.500.000', '0,5', '43.750.000'],
    ])
    idx += 100
    
    insert_text(requests, idx, '\n\nJustifikasi Nilai:\n\n')
    update_style(requests, idx - 0, 18, bold=True)
    idx += 18
    
    add_table(requests, idx, 7, 4, [
        ['Threat', 'Justifikasi AV', 'Justifikasi EF', 'Justifikasi ARO'],
        ['SQL Injection', 'Database finansial nasabah + sanksi regulasi', '60% — satu serangan ekspos mayoritas data', '1 — serangan SQLi masih umum pada web finansial'],
        ['Exposed Hash', 'Database kredensial pengguna', '40% — hanya hash, perlu di-crack', '2 — human error serialisasi API cukup sering'],
        ['JWT Manipulation', 'Akses administratif sistem', '70% — privilege escalation = kendali penuh', '0,5 — butuh pengetahuan teknis JWT'],
        ['IDOR', 'Data transaksi pengguna', '30% — terbatas pada endpoint spesifik', '1 — mudah ditemukan dengan enumerasi'],
        ['Brute Force', 'Rata-rata nilai akun pengguna', '50% — tergantung kekuatan password', '3 — automated tools mudah dijalankan'],
        ['Stored XSS', 'Data profil & cookie session', '35% — terbatas pengguna buka halaman profil', '0,5 — butuh entry point lolos validasi'],
    ])
    idx += 100
    
    insert_text(requests, idx, '\n\n1.3 Risk Matrix (Kualitatif)\n\n')
    update_style(requests, idx - 0, 29, bold=True)
    idx += 29
    
    add_table(requests, idx, 7, 4, [
        ['Threat', 'Likelihood', 'Impact', 'Risk Level'],
        ['SQL Injection', 'High', 'Critical', 'Critical'],
        ['Exposed Hash', 'High', 'Medium', 'High'],
        ['JWT Manipulation', 'Medium', 'High', 'High'],
        ['IDOR', 'Medium', 'High', 'High'],
        ['Brute Force', 'High', 'Medium', 'High'],
        ['Stored XSS', 'Low', 'High', 'Medium'],
    ])
    idx += 100
    
    insert_text(requests, idx, '\n\n1.4 Risk Treatment Plan\n\n')
    update_style(requests, idx - 0, 24, bold=True)
    idx += 24
    
    add_table(requests, idx, 7, 4, [
        ['Threat', 'Risk Level', 'Label', 'Strategi/Alasan'],
        ['SQL Injection', 'Critical', 'M', 'Parameterized query / prepared statement + WAF. Biaya ~Rp15jt, ALE Rp480jt -> ROI jelas.'],
        ['Exposed Hash', 'High', 'M', 'DTO/serializer eksplisit, field sensitif tidak pernah di response. Biaya minimal, dampak signifikan.'],
        ['JWT Manipulation', 'High', 'M', 'Whitelist algoritma JWT, library terpercaya, verifikasi signature tiap request. Biaya rendah.'],
        ['IDOR', 'High', 'M', 'Ownership check tiap endpoint, UUID instead of incremental ID. Biaya rendah, dampak tinggi.'],
        ['Brute Force', 'High', 'M', 'Rate limiting, account lockout 5x gagal, CAPTCHA. Biaya sangat rendah, efektif.'],
        ['Stored XSS', 'Medium', 'M', 'Output encoding, CSP headers, sanitasi input HTML. Biaya rendah, standar web modern.'],
    ])
    idx += 100
    
    # ==================== TUGAS 2 ====================
    insert_text(requests, idx, '\n\nTUGAS 2: Risk Management Report - Karlan Trading Company\n\n')
    update_style(requests, idx - 0, 54, heading=True)
    idx += 54
    
    insert_text(requests, idx, '2.1 Deskripsi Sistem\n\n')
    update_style(requests, idx - 0, 21, bold=True)
    idx += 21
    
    desc = (
        'Kjerag Logistics & Trading Management System (KLTMS) adalah sistem informasi terpadu milik Karlan Trading Company '
        'untuk mengelola operasi logistik dan perdagangan di wilayah pegunungan Kjerag. Sistem menghubungkan kantor pusat, '
        'gudang penyimpanan, mitra bisnis, dan tim logistik lapangan. KLTMS menangani manajemen inventaris gudang berbasis IoT, '
        'pelacakan pengiriman real-time, kontrak dagang dengan mitra, serta pelaporan keuangan dan audit dalam satu platform '
        'terintegrasi dengan arsitektur yang resilient terhadap keterbatasan infrastruktur jaringan Kjerag.\n\n'
    )
    insert_text(requests, idx, desc)
    idx += len(desc)
    
    insert_text(requests, idx, '2.2 Komponen Sistem\n\n')
    update_style(requests, idx - 0, 21, bold=True)
    idx += 21
    
    komponen = (
        '1. Frontend Web App - Portal akses berbasis browser (React.js)\n'
        '2. Backend API Server - RESTful API (Node.js/Express)\n'
        '3. Database Server - Penyimpanan data utama (PostgreSQL)\n'
        '4. Warehouse IoT Gateway - Perangkat IoT gudang (barcode scanner, sensor stok)\n\n'
    )
    insert_text(requests, idx, komponen)
    idx += len(komponen)
    
    insert_text(requests, idx, '2.3 Tipe Pengguna\n\n')
    update_style(requests, idx - 0, 18, bold=True)
    idx += 18
    
    users = (
        '1. Admin Sistem - Manajemen user, konfigurasi, audit log\n'
        '2. Staff Logistik - Manajemen inventaris, pemrosesan pengiriman\n'
        '3. Client/Mitra Bisnis - Lacak kiriman, akses kontrak, buat permintaan\n'
        '4. Auditor - Akses read-only untuk kepatuhan & review\n\n'
    )
    insert_text(requests, idx, users)
    idx += len(users)
    
    insert_text(requests, idx, '2.4 Data Asset & Klasifikasi\n\n')
    update_style(requests, idx - 0, 28, bold=True)
    idx += 28
    
    add_table(requests, idx, 6, 3, [
        ['Data Asset', 'Klasifikasi', 'Deskripsi'],
        ['Kontrak Dagang & Harga', 'Confidential', 'Perjanjian bisnis, harga khusus mitra, strategi dagang'],
        ['Data Personal Karyawan', 'Private', 'Gaji, alamat, dokumen identitas'],
        ['Data Pelacakan Pengiriman', 'Public', 'Status & lokasi pengiriman, estimasi waktu tiba'],
        ['Laporan Keuangan Internal', 'Restricted', 'P&L, revenue, metrik finansial internal'],
        ['Data Inventaris Gudang', 'Internal', 'Stok barang, kapasitas gudang, riwayat masuk/keluar'],
    ])
    idx += 100
    
    insert_text(requests, idx, '\n\n2.5 DFD Level 0 (Context Diagram)\n\n')
    update_style(requests, idx - 0, 35, bold=True)
    idx += 35
    
    dfd0 = (
        '[Client/Mitra] <--> [KLTMS System] <--> [Staff Logistik]\n'
        '     ^                            ^\n'
        '     |                            |\n'
        '     v                            v\n'
        '[Admin Sistem] <--> [KLTMS System] <--> [Auditor]\n'
        '                          |\n'
        '                          v\n'
        '              [Database Server]\n'
        '                          |\n'
        '                          v\n'
        '              [Warehouse IoT Gateway]\n\n'
        'External Entities: Admin Sistem, Staff Logistik, Client/Mitra, Auditor\n'
        'Main Process: KLTMS\n'
        'Data Stores: Database Server, Warehouse IoT Gateway\n\n'
    )
    insert_text(requests, idx, dfd0)
    idx += len(dfd0)
    
    insert_text(requests, idx, '2.6 DFD Level 1\n\n')
    update_style(requests, idx - 0, 15, bold=True)
    idx += 15
    
    dfd1 = (
        'Proses dalam KLTMS System:\n'
        '1.0 Manajemen Inventaris - Mengelola stok gudang, input dari Staff & IoT Gateway\n'
        '2.0 Manajemen Kontrak Dagang - Mengelola kontrak mitra\n'
        '3.0 Pelacakan Pengiriman - Update & lacak status kiriman\n'
        '4.0 Laporan & Audit - Generate laporan keuangan & audit\n'
        '5.0 Manajemen User & Auth - Kelola user, role, otentikasi & otorisasi\n\n'
        'Data Stores:\n'
        'D1 Inventory DB - Data stok & inventaris\n'
        'D2 Contracts DB - Data kontrak dagang\n'
        'D3 Tracking DB - Data pelacakan pengiriman\n'
        'D4 Financial DB - Data laporan keuangan\n'
        'D5 Users DB - Data user & role\n\n'
        'Data Flows:\n'
        '- Admin -> 5.0: Kelola user & peran\n'
        '- Staff -> 1.0: Update stok gudang\n'
        '- Staff -> 2.0: Input kontrak baru\n'
        '- Staff -> 3.0: Update status pengiriman\n'
        '- Client -> 2.0: Lihat kontrak\n'
        '- Client -> 3.0: Lacak pengiriman\n'
        '- Auditor -> 4.0: Generate laporan\n'
        '- IoT Gateway -> 1.0: Data sensor stok\n\n'
    )
    insert_text(requests, idx, dfd1)
    idx += len(dfd1)
    
    insert_text(requests, idx, '2.7 Threat Model\n\n')
    update_style(requests, idx - 0, 16, bold=True)
    idx += 16
    
    add_table(requests, idx, 8, 5, [
        ['Aset', 'Klasifikasi', 'Threat Actor', 'Threat', 'Dampak Potensial'],
        ['Kontrak Dagang & Harga', 'Confidential', 'External Attacker', 'SQL Injection pd endpoint API kontrak', 'Kebocoran data harga & strategi ke kompetitor'],
        ['Data Personal Karyawan', 'Private', 'Malicious Insider', 'Privilege escalation Staff -> data HR', 'Eksposur data pribadi seluruh karyawan'],
        ['Data Pelacakan', 'Public', 'External Attacker', 'MITM pd komunikasi IoT Gateway', 'Pemalsuan data lokasi & status kiriman'],
        ['Session Token Admin', 'Restricted', 'External Attacker', 'XSS pada portal admin', 'Pengambilalihan sesi admin = akses penuh'],
        ['Data Inventaris Gudang', 'Internal', 'Competitor', 'API scraping endpoint inventaris', 'Analisis kompetitor stok & kapasitas gudang'],
        ['Laporan Keuangan', 'Restricted', 'External Attacker', 'SSRF pd fitur export laporan', 'Eksfiltrasi data keuangan internal'],
        ['Data Transaksi (semua)', 'Confidential', 'External Attacker', 'Weak JWT secret -> token forgery', 'Token palsu untuk akses tak sah'],
    ])
    idx += 120
    
    insert_text(requests, idx, '\n\n2.8 Risk Measurement Kuantitatif\n\n')
    update_style(requests, idx - 0, 33, bold=True)
    idx += 33
    
    add_table(requests, idx, 8, 6, [
        ['Threat', 'AV (Rp)', 'EF', 'SLE (Rp)', 'ARO', 'ALE (Rp)'],
        ['SQL Injection (Kontrak)', '2.500.000.000', '70%', '1.750.000.000', '0,5', '875.000.000'],
        ['Privilege Escalation', '1.000.000.000', '40%', '400.000.000', '1', '400.000.000'],
        ['MITM IoT Gateway', '750.000.000', '25%', '187.500.000', '2', '375.000.000'],
        ['XSS (Session Admin)', '3.000.000.000', '80%', '2.400.000.000', '0,3', '720.000.000'],
        ['API Scraping Inventaris', '500.000.000', '30%', '150.000.000', '4', '600.000.000'],
        ['SSRF (Laporan Keuangan)', '2.000.000.000', '60%', '1.200.000.000', '0,2', '240.000.000'],
        ['JWT Forgery', '1.500.000.000', '65%', '975.000.000', '0,3', '292.500.000'],
    ])
    idx += 120
    
    insert_text(requests, idx, '\n\nJustifikasi Asset Value & ARO:\n\n')
    update_style(requests, idx - 0, 31, bold=True)
    idx += 31
    
    add_table(requests, idx, 8, 3, [
        ['Threat', 'Justifikasi AV', 'Justifikasi ARO'],
        ['SQL Injection (Kontrak)', 'Kerugian jika kontrak & harga bocor: hilang keunggulan kompetitif + NDA', '0,5 - SQLi masih umum tapi ada mitigasi standar'],
        ['Privilege Escalation', 'Denda regulasi + kompensasi + reputasi', '1 - insider threat umum di organisasi menengah'],
        ['MITM IoT Gateway', 'Gangguan operasional akibat kiriman salah di pegunungan', '2 - jaringan pegunungan tidak selalu terenkripsi'],
        ['XSS (Session Admin)', 'Kerugian maksimal karena akses penuh ke seluruh sistem', '0,3 - XSS diketahui, ada CSP'],
        ['API Scraping', 'Informasi stok & kapasitas untuk kompetitor', '4 - scraping mudah otomatis'],
        ['SSRF (Keuangan)', 'Laporan keuangan internal bocor publik', '0,2 - butuh konfigurasi spesifik'],
        ['JWT Forgery', 'Akses tak sah ke transaksi & kontrak', '0,3 - butuh pengetahuan teknis JWT'],
    ])
    idx += 120
    
    insert_text(requests, idx, '\n\n2.9 Risk Measurement Kualitatif\n\n')
    update_style(requests, idx - 0, 31, bold=True)
    idx += 31
    
    add_table(requests, idx, 8, 4, [
        ['Threat', 'Likelihood', 'Impact', 'Risk Level'],
        ['SQL Injection (Kontrak)', 'Medium', 'Critical', 'Critical'],
        ['Privilege Escalation', 'High', 'High', 'High'],
        ['MITM IoT Gateway', 'High', 'Medium', 'High'],
        ['XSS (Session Admin)', 'Low', 'Critical', 'High'],
        ['API Scraping Inventaris', 'High', 'Low', 'Medium'],
        ['SSRF (Keuangan)', 'Low', 'Critical', 'High'],
        ['JWT Forgery', 'Low', 'High', 'Medium'],
    ])
    idx += 120
    
    insert_text(requests, idx, '\n\nRisk Matrix:\n\n')
    update_style(requests, idx - 0, 13, bold=True)
    idx += 13
    
    risk_matrix = (
        '                      | Low Impact  | Medium Impact | High Impact  | Critical Impact |\n'
        'High Likelihood       | API Scraping | MITM IoT      | Priv.Escal.  | -               |\n'
        'Medium Likelihood     | -            | -             | -            | SQL Injection   |\n'
        'Low Likelihood        | -            | -             | JWT Forgery  | XSS, SSRF       |\n\n'
    )
    insert_text(requests, idx, risk_matrix)
    idx += len(risk_matrix)
    
    insert_text(requests, idx, '2.10 Risk Treatment Plan\n\n')
    update_style(requests, idx - 0, 24, bold=True)
    idx += 24
    
    add_table(requests, idx, 8, 4, [
        ['Threat', 'Risk Level', 'Label', 'Strategi/Alasan'],
        ['SQL Injection (Kontrak)', 'Critical', 'M', 'Parameterized query/ORM + WAF. Biaya Rp20jt, ALE Rp875jt -> ROI jelas.'],
        ['Privilege Escalation', 'High', 'M', 'RBAC ketat + least privilege. Review mapping tiap kuartal. Biaya Rp10jt.'],
        ['MITM IoT Gateway', 'High', 'M', 'TLS 1.3 + mTLS utk autentikasi perangkat. Biaya Rp25jt, ALE Rp375jt.'],
        ['XSS (Session Admin)', 'High', 'M', 'CSP headers, output encoding, HttpOnly+Secure cookies. Biaya rendah.'],
        ['API Scraping', 'Medium', 'T', 'Transfer risiko ke CDN dgn rate limiting via SLA. Rate limiting tetap di API.'],
        ['SSRF (Keuangan)', 'High', 'M', 'Whitelist URL, network segmentation, firewall. Biaya Rp5-15jt.'],
        ['JWT Forgery', 'Medium', 'M', 'JWT secret kuat (256-bit), rotasi berkala, nonaktifkan algoritma lemah.'],
    ])
    idx += 120
    
    insert_text(requests, idx, '\n\nKeterangan Label Treatment (ISO/IEC 27005):\n'
                'M = Mitigation - implementasi kontrol keamanan\n'
                'A = Accept - terima risiko (ALE < biaya treatment)\n'
                'T = Transfer - transfer risiko ke entitas lain\n'
                'Av = Avoid - hindari dengan tidak implementasi fitur\n')
    
    # Execute all requests in batches
    batch_size = 50
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i+batch_size]
        try:
            docs_service.documents().batchUpdate(
                documentId=DOCUMENT_ID,
                body={'requests': batch}
            ).execute()
            print(f'Batch {i//batch_size + 1}/{(len(requests)-1)//batch_size + 1} berhasil!')
        except HttpError as e:
            print(f'Error di batch {i//batch_size + 1}: {e}')
            # Retry one by one
            for j, req in enumerate(batch):
                try:
                    docs_service.documents().batchUpdate(
                        documentId=DOCUMENT_ID,
                        body={'requests': [req]}
                    ).execute()
                except HttpError as e2:
                    print(f'  Request {j} gagal: {e2}')
    
    print('\nSelesai! Semua konten berhasil ditulis ke Google Docs.')

if __name__ == '__main__':
    main()
