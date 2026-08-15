# Ez a fájl definiálja, hogyan néz ki egy "adat" az alkalmazásunkban.
# Egyelőre csak egy egyszerű Python osztály, adatbázis nélkül.

class Feladat:
    """Egy egyszerű feladat-objektum (pl. egy teendő lista eleme)."""
    def __init__(self, id, cim, kesz=False):
        self.id = id
        self.cim = cim
        self.kesz = kesz

    def to_dict(self):
        # Ez alakítja át az objektumot olyan formára, amit a webes válaszban
        # (JSON-ként) vissza tudunk küldeni.
        return {"id": self.id, "cim": self.cim, "kesz": self.kesz}
