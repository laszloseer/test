# Ez a fájl mondja meg, hogy egy adott webcímre (URL) érkező kérésre
# hogyan reagáljon az app: milyen adatot fogadjon be, mit adjon vissza.

from flask import Blueprint, request, jsonify
from models import Feladat
from utils import validald_cimet

# Blueprint = a Flask egyik eszköze arra, hogy az útvonalakat
# külön fájlba lehessen szervezni, ne az app.py-ban legyen minden.
bp = Blueprint("routes", __name__)

# Ideiglenes "adatbázis" memóriában (valós appban ez egy tényleges
# adatbázis lenne, pl. PostgreSQL vagy SQLite).
feladatok = []
kovetkezo_id = 1


@bp.route("/feladatok", methods=["GET"])
def feladatok_listazasa():
    """Adatok KIADÁSA: visszaadja az összes eddig eltárolt feladatot."""
    return jsonify([f.to_dict() for f in feladatok])


@bp.route("/feladatok", methods=["POST"])
def feladat_letrehozasa():
    """Adatok BEKÉRÉSE: fogad egy új feladatot a webes felületről/kliensről."""
    global kovetkezo_id
    adat = request.get_json()

    cim = adat.get("cim") if adat else None
    if not validald_cimet(cim):
        # Ha az adat hibás, hibaüzenetet küldünk vissza 400-as státusszal.
        return jsonify({"hiba": "Érvénytelen cím mező"}), 400

    uj_feladat = Feladat(id=kovetkezo_id, cim=cim)
    feladatok.append(uj_feladat)
    kovetkezo_id += 1

    # A frissen létrehozott adatot visszaküldjük, 201 (Created) státusszal.
    return jsonify(uj_feladat.to_dict()), 201
