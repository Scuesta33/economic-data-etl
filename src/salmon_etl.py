import json
import csv

def extraer_datos():
    with open("data/raw/salmon_production.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos

datos = extraer_datos()
print(datos)

def limpiar_registro(registro):
    plant = registro.get("plant")
    date = registro.get("date")
    tons = registro.get("tons")
    quality = registro.get("quality")

    if plant is None:
        return None, "falta plant"
    if date is None:
        return None, "falta date"
    if tons is None:
        return None, "falta tons"
    if quality is None:
        return None, "falta quality"


    try:
        toneladas = float(tons)
    except ValueError:
        return None, "tons no tiene formato valido"

    
    resultado = {
        "planta": plant.upper(),
        "fecha": str(date),
        "toneladas": toneladas,
        "calidad": str(quality)
    }
    return resultado, None