import os
import psycopg
from psycopg.rows import dict_row

password = os.getenv("DB_PASSWORD")

conexion = psycopg.connect(
    host="localhost",
    dbname="salmon_data",
    user="postgres",
    password=password
)

print("Conexión realizada correctamente")
cursor = conexion.cursor(row_factory=dict_row)

cursor.execute("SELECT * FROM plantas;")

resultados = cursor.fetchall()

for planta in resultados:
    print(f"Planta: {planta['nombre']} - Capacidad: {planta['capacidad']}")