import json
import csv
import os
import psycopg
import math
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/salmon_etl.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def extraer_datos():
    with open("data/raw/salmon_production.json", "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos


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
    if toneladas < 0:
        return None, "toneladas negativas"

    if not math.isfinite(toneladas):
        return None, "toneladas no finitas"

    
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
            logging.warning(
                "Registro rechazado: %s | Motivo: %s",
                registro,
                error
            )

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

def guardar_salmon_postgres(datos):
    password = os.getenv("DB_PASSWORD")

    if not password:
        logging.error("No se ha configurado DB_PASSWORD")
        raise ValueError("Falta la contraseña de PostgreSQL")

    # 1. Abrimos la conexión
    conexion = psycopg.connect(
        host="localhost",
        dbname="salmon_data",
        user="postgres",
        password=password
    )

    try:
        # 2. Creamos el cursor
        cursor = conexion.cursor()

        # 3. Recorremos los registros
        for registro in datos:

            # Buscamos el ID de la planta
            cursor.execute(
                "SELECT id FROM plantas WHERE nombre = %s;",
                (registro["planta"],)
            )

            planta = cursor.fetchone()

            if planta is None:
                logging.warning(
                    "Planta desconocida: %s",
                    registro["planta"]
                )
                continue

            planta_id = planta[0]

            # Guardamos o actualizamos la producción
            cursor.execute(
                """
                INSERT INTO salmon_production
                    (planta, fecha, toneladas, calidad, planta_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (planta, fecha)
                DO UPDATE SET
                    toneladas = EXCLUDED.toneladas,
                    calidad = EXCLUDED.calidad,
                    planta_id = EXCLUDED.planta_id;
                """,
                (
                    registro["planta"],
                    registro["fecha"],
                    registro["toneladas"],
                    registro["calidad"],
                    planta_id
                )
            )

        conexion.commit()
        logging.info("Datos guardados correctamente en PostgreSQL")

    except psycopg.Error:
        conexion.rollback()
        logging.exception("Error durante la operación con PostgreSQL")
        raise

    finally:
        conexion.close()

def main():
    datos = extraer_datos()

    datos_limpios, datos_rechazados = transformar_datos(datos)

    guardar_salmon_csv(datos_limpios)
    guardar_salmon_rechazados(datos_rechazados)

    guardar_salmon_postgres(datos_limpios)

    logging.info("ETL ejecutado correctamente")
    print(f"Registros válidos: {len(datos_limpios)}")
    print(f"Registros rechazados: {len(datos_rechazados)}")
    


if __name__ == "__main__":
    main()
    