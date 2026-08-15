# Ez a fájl indítja el ténylegesen a webszervert.
# Ide importáljuk be a többi fájlban definiált részeket.

from flask import Flask
from routes import bp as routes_blueprint

def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes_blueprint)  # az útvonalak becsatlakoztatása
    return app

app = create_app()

if __name__ == "__main__":
    # debug=True: fejlesztés közben hasznos, éles környezetben nem ajánlott
    app.run(debug=True, host="0.0.0.0", port=5000)
