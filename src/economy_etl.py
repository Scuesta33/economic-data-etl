import json
import csv

def extraer_datos():
    with open("data/raw/economy.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos


def limpiar_registro(registro):
    country = registro.get("country")
    year = registro.get("year")
    gdp = registro.get("gdp")

    if country is None:
        return None, "falta country"
    if year is None:
        return None, "falta year"
    if gdp is None:
        return None, "falta gdp"
     

    try:
        anio = int(year)
        pib = float(gdp)
    except ValueError:
        return None, "year o gdp no tienen un formato válido"

    resultado = {
        "pais": country.upper(),
        "anio": anio,
        "pib_per_capita": pib
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
                "country": registro.get("country"),
                "year": registro.get("year"),
                "gdp": registro.get("gdp"),
                "error": error
            }
            datos_rechazados.append(rechazo)
            continue

        datos_limpios.append(limpio)

    return datos_limpios, datos_rechazados


def guardar_csv(datos):

    columnas = ["pais", "anio", "pib_per_capita"]
    with open("data/processed/economy_clean.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos)

def guardar_rechazados(datos):
    columnas = ["country", "year", "gdp", "error"]
    with open("data/processed/economy_rejected.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos)

datos = extraer_datos()
datos_limpios, datos_rechazados = transformar_datos(datos)
print(datos_limpios)
print(datos_rechazados)
guardar_csv(datos_limpios)
guardar_rechazados(datos_rechazados)