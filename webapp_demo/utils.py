# Ide kerülnek az olyan apró, általános funkciók, amik nem tartoznak
# szorosan sem a modellekhez, sem az útvonalakhoz.

def validald_cimet(cim):
    """Ellenőrzi, hogy a beküldött 'cim' mező érvényes-e."""
    if not cim or not isinstance(cim, str):
        return False
    if len(cim.strip()) == 0:
        return False
    return True
