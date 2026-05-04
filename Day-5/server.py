import http.server
import socketserver
import logging
from datetime import datetime

PORT = 8080

# Setup basic logging to file and console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler("server_log.txt"),
        logging.StreamHandler()
    ]
)

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"Received GET request from {self.client_address[0]}")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Test Server</title></head>")
        self.wfile.write(b"<body><p>Hello, World!</p></body></html>")

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server stopped.")
