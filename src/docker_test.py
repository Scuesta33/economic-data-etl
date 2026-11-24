import os
import psycopg

conexion = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="salmon_data",
    user="postgres",
    password=os.getenv("DB_PASSWORD")
)

with conexion.cursor() as cursor:
    cursor.execute("SELECT nombre FROM plantas ORDER BY id;")
    plantas = cursor.fetchall()

    for planta in plantas:
        print(planta[0])

conexion.close()