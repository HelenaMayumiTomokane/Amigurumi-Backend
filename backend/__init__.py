import threading
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
from app import app, UPLOAD_FOLDER

class CustomHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        return os.path.join(UPLOAD_FOLDER, os.path.relpath(path, "/"))

def run_http_server():
    with TCPServer(("0.0.0.0", 8000), CustomHandler) as httpd:
        print(f"Servidor HTTP rodando na porta 8000, servindo imagens de {UPLOAD_FOLDER}")
        httpd.serve_forever()

thread = threading.Thread(target=run_http_server)
thread.daemon = True
thread.start()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=False)
