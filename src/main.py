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

    if country is None or year is None or gdp is None:
        return None

    try:
        anio = int(year)
        pib = float(gdp)
    except ValueError:
        return None

    resultado = {
        "pais": country.upper(),
        "anio": anio,
        "pib_per_capita": pib
    }

    return resultado

def transformar_datos(datos):
    datos_limpios = []

    for registro in datos:
        limpio = limpiar_registro(registro)

        if limpio is None:
            continue

        datos_limpios.append(limpio)

    return datos_limpios


def guardar_csv(datos):

    columnas = ["pais", "anio", "pib_per_capita"]
    with open("data/processed/economy_clean.csv", "w", newline="", encoding="utf-8") as archivo:
            writer = csv.DictWriter(archivo, fieldnames=columnas)
            writer.writeheader()
            writer.writerows(datos)

datos = extraer_datos()
datos_limpios = transformar_datos(datos)
print(datos_limpios)
guardar_csv(datos_limpios)