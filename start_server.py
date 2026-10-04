#!/usr/bin/env python3
"""
GeoFibra Collesalvetti - Server Web Locale
Avvia un server HTTP locale per la visualizzazione della mappa GIS e della Wiki.
Compatibile con percorsi relativi e assoluti su qualsiasi sistema operativo.
"""

import os
import sys
import socket
import http.server
import socketserver
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_FILE = os.path.join(BASE_DIR, "index.html")

def find_available_port(start_port=8080, max_attempts=20):
    """Trova una porta TCP libera a partire da start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    return start_port

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def log_message(self, format, *args):
        try:
            message = format % args
        except Exception:
            message = " ".join(str(a) for a in args)
        sys.stdout.write(f"[{self.log_date_time_string()}] {message}\n")
        sys.stdout.flush()

def run_server():
    if not os.path.exists(INDEX_FILE):
        print(f"ERRORE CRITICO: File index.html non trovato nel percorso:\n  {INDEX_FILE}")
        sys.exit(1)

    port = find_available_port(8080)
    url = f"http://localhost:{port}"

    print("=" * 68)
    print("  GEOFIBRA COLLESALVETTI // OSSERVATORIO CIVICO BANDA ULTRALARGA")
    print("=" * 68)
    print(f"  Cartella root:         {BASE_DIR}")
    print(f"  File di avvio:         {INDEX_FILE}")
    print(f"  Indirizzo Web Locale:  {url}")
    print("=" * 68)
    print("  Premi Ctrl + C per arrestare il server.\n")

    handler = CustomHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    try:
        with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
            try:
                webbrowser.open(url)
            except Exception:
                pass
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nArresto del server completato. A presto!")
        sys.exit(0)
    except Exception as e:
        print(f"\nErrore durante l'avvio del server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_server()
