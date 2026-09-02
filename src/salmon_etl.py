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
def transformar_datos(datos):
    datos_limpios = []
    datos_rechazados = []
    for registro in datos:
        limpio, error = limpiar_registro(registro)

        if limpio is None:
            print("Registro rechazado:", registro)
            print("Motivo:", error)

            rechazo = {
                "plant": registro.get("plant"),
                "date": registro.get("date"),
                "tons": registro.get("tons"),
                "quality": registro.get("quality"),
                "error": error
            }
            datos_rechazados.append(rechazo)
            continue
        datos_limpios.append(limpio)
    return datos_limpios, datos_rechazados

def guardar_salmon_csv(datos):

    columnas = ["planta", "fecha", "toneladas", "calidad"]
    with open("data/processed/salmon_clean.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos)

def guardar_salmon_rechazados(datos):
    columnas = ["plant", "date", "tons", "quality", "error"]
    with open("data/processed/salmon_rejected.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos)

datos = extraer_datos()
datos_limpios, datos_rechazados = transformar_datos(datos)
print(datos_limpios)
print(datos_rechazados)
guardar_salmon_csv(datos_limpios)
guardar_salmon_rechazados(datos_rechazados)