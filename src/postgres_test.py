import os
import psycopg
from psycopg.rows import dict_row

def buscar_planta(cursor, nombre):
    cursor.execute(
        "SELECT * FROM plantas WHERE nombre = %s;",
        (nombre,)
    )

    planta = cursor.fetchone()
    return planta

def conectar_db():
    password = os.getenv("DB_PASSWORD")

    conexion = psycopg.connect(
        host="localhost",
        dbname="salmon_data",
        user="postgres",
        password=password
    )
    return conexion

def guardar_planta(conexion, id, nombre, pais, capacidad):
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO plantas (id, nombre, pais, capacidad)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE
        SET capacidad = EXCLUDED.capacidad;
        """,
        (id, nombre, pais, capacidad)
    )

conexion = conectar_db()

guardar_planta(conexion, 5, "BERGEN", "NORWAY", 250)

print("Conexión realizada correctamente")
cursor = conexion.cursor(row_factory=dict_row)
nombre = "FROYA"
planta = buscar_planta(cursor, nombre)

if planta is None:
    print("La planta no existe")
else:
    print(f"Planta: {planta['nombre']} - Pais: {planta['pais']}")


# NUEVO EJERCICIO: INSERTAR UNA PLANTA

nombre = "TRONDHEIM"
pais = "NORWAY"
capacidad = 250

cursor.execute(
    """
    INSERT INTO plantas (id, nombre, pais, capacidad)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE
    SET capacidad = EXCLUDED.capacidad;
    """,
    (4, nombre, pais, capacidad)
)
conexion.commit()

cursor.execute(
    "SELECT * FROM plantas WHERE id = %s;",
    (4,)
)

planta = cursor.fetchone()

print(f"Planta: {planta['nombre']} - Capacidad: {planta['capacidad']}")

