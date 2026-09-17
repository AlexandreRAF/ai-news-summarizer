from pathlib import Path
from functools import partial
import socketserver
import http.server
from threading import Thread

from playwright.sync_api import sync_playwright

class httpServer():
    def __init__(self):
        self.defaultPort = 8000

        script_dir = Path(__file__).resolve().parent

        # partial sets the directory now; TCPServer supplies request arguments later.
        self.Handler = partial(http.server.SimpleHTTPRequestHandler, directory=str(script_dir))

        self.httpd = None
        self.server_thread = None
        self.availablePort = self.findAvailablePort(10)
        if self.availablePort:
            self.server_thread = Thread(target=self.serveHTTP, args=[self.availablePort])
            self.server_thread.start()

    def returnServerURL(self):
        return 'http://127.0.0.1:' + str(self.availablePort)

    def findAvailablePort(self, maxRetries):
        port = self.defaultPort
        tryCount = 0
        while True:
            try:
                tryCount += 1
                if tryCount > maxRetries:
                    return False
                with socketserver.TCPServer(("127.0.0.1", port), self.Handler):
                    return port
            except OSError:
                port += 1
                
    def serveHTTP(self, port):
        with socketserver.TCPServer(("127.0.0.1", port), self.Handler) as httpd:
            self.httpd = httpd
            print(f"Serving at http://127.0.0.1:{port}")
            httpd.serve_forever()

    def stopHTTP(self):
        if self.server_thread is not None:
            while self.httpd is None and self.server_thread.is_alive():
                self.server_thread.join(timeout=0.2)
            if self.server_thread.is_alive():
                self.httpd.shutdown()
            self.server_thread.join()
            
class downloadPDF():
    def __init__(self):
        pass

    @staticmethod
    def downloadPDF(address, file_path):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.emulate_media(media='print')
                page.goto(address)
                page.wait_for_load_state('networkidle')
                page.pdf(path=file_path)
                print(page.title())
                browser.close()
                return True
        except Exception as e:
            print('[ERROR GENERATING PDF - PLAYWRIGHT]', e)
            return False

def run(file_path):
    server = httpServer()
    try:
        while server.server_thread is not None and server.server_thread.is_alive():
            server.server_thread.join(timeout=0.2)
            if downloadPDF().downloadPDF(server.returnServerURL(), file_path):
                print("[PDF GENERATED]")
                server.stopHTTP()
                return True

    except KeyboardInterrupt:
        print('Stopping server...')
        server.stopHTTP()
        return False

    except Exception as e:
        print('[ERROR GENERATING PDF]', e)
        server.stopHTTP()
        return False