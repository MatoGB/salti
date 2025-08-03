import json
import os

DATA_PATH = "data/save.json"

def cargar_datos():
    if not os.path.exists(DATA_PATH):
        # Crear carpeta si no existe
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

        # Datos por defecto
        datos = {
            "highscore": 0,
            "monedas": 0,
            "skins": ["skin1.png"],
            "skin_equipada": "skin1.png"
        }

        # Guardar datos
        with open(DATA_PATH, "w") as f:
            json.dump(datos, f)

        return datos

    # Si ya existe, cargar
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def guardar_datos(datos):
    with open(DATA_PATH, "w") as f:
        json.dump(datos, f)
