# Ugyanaz a demó, mint app.py + routes.py, de KIZÁRÓLAG a Python
# beépített könyvtárával (http.server), hogy internet/csomagtelepítés
# nélkül is ki lehessen próbálni.
#
# Ez jól mutatja, mit csinál "a háttérben" egy olyan keretrendszer, mint a Flask:
# fogadja a HTTP kérést, eldönti melyik útvonalról van szó, adatot olvas/ír.

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from models import Feladat
from utils import validald_cimet

feladatok = []
kovetkezo_id = 1

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")


class Handler(BaseHTTPRequestHandler):

    def _json_valasz(self, status, adat):
        body = json.dumps(adat, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _html_valasz(self, fajlnev):
        # A böngészőnek szánt HTML felületet szolgáljuk ki a static/ mappából.
        with open(os.path.join(STATIC_DIR, fajlnev), "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self._html_valasz("index.html")
        elif self.path == "/feladatok":
            # Adatok KIADÁSA
            self._json_valasz(200, [f.to_dict() for f in feladatok])
        else:
            self._json_valasz(404, {"hiba": "Nincs ilyen útvonal"})

    def do_POST(self):
        # Adatok BEKÉRÉSE
        global kovetkezo_id
        if self.path == "/feladatok":
            length = int(self.headers.get("Content-Length", 0))
            nyers = self.rfile.read(length)
            try:
                adat = json.loads(nyers)
            except json.JSONDecodeError:
                adat = None

            cim = adat.get("cim") if adat else None
            if not validald_cimet(cim):
                self._json_valasz(400, {"hiba": "Érvénytelen cím mező"})
                return

            uj_feladat = Feladat(id=kovetkezo_id, cim=cim)
            feladatok.append(uj_feladat)
            kovetkezo_id += 1
            self._json_valasz(201, uj_feladat.to_dict())
        else:
            self._json_valasz(404, {"hiba": "Nincs ilyen útvonal"})

    def log_message(self, format, *args):
        # Elnémítjuk az alapértelmezett konzol-logot, hogy tisztább legyen a kimenet.
        pass


if __name__ == "__main__":
    szerver = HTTPServer(("0.0.0.0", 5000), Handler)
    print("Szerver fut: http://localhost:5000")
    szerver.serve_forever()
