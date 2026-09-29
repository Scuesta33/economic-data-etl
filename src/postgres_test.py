import os
import psycopg

password = os.getenv("DB_PASSWORD")

conexion = psycopg.connect(
    host="localhost",
    dbname="salmon_data",
    user="postgres",
    password=password
)

print("Conexión realizada correctamente")
cursor = conexion.cursor()

cursor.execute("SELECT * FROM plantas;")

resultados = cursor.fetchall()

for planta in resultados:
    print(f"Planta: {planta[1]} - Capacidad: {planta[3]}")