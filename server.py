import http.server
import socketserver
import os

PORT = 3000
FILENAME = "Thebe.html"

# 確保當前目錄中存在 abc.html
if not os.path.exists(FILENAME):
    raise FileNotFoundError(f"{FILENAME} 不存在於當前目錄。")

# 切換到該 HTML 文件的目錄
os.chdir(os.path.dirname(os.path.abspath(FILENAME)))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 自定義首頁為 Thebe.html
        if self.path == "/" or self.path == f"/{FILENAME}":
            self.path = f"/{FILENAME}"
        return super().do_GET()

# 啟動伺服器
with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print(f"Serving {FILENAME} at http://localhost:{PORT}")
    httpd.serve_forever()
