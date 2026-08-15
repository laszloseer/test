# Ugyanaz a demó, mint app.py + routes.py, de KIZÁRÓLAG a Python
# beépített könyvtárával (http.server), hogy internet/csomagtelepítés
# nélkül is ki lehessen próbálni.
#
# Ez jól mutatja, mit csinál "a háttérben" egy olyan keretrendszer, mint a Flask:
# fogadja a HTTP kérést, eldönti melyik útvonalról van szó, adatot olvas/ír.

import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from models import Feladat
from utils import validald_cimet

feladatok = []
kovetkezo_id = 1


class Handler(BaseHTTPRequestHandler):

    def _json_valasz(self, status, adat):
        body = json.dumps(adat, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        # Adatok KIADÁSA
        if self.path == "/feladatok":
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
