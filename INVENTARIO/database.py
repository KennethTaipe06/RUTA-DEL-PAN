import mysql.connector
from config import DB_CONFIG

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


# Ejemplo para probar la conexión
if __name__ == "__main__":
    try:
        connection = get_db_connection()
        print("Conexión exitosa a la base de datos.")
        connection.close()
    except mysql.connector.Error as err:
        print(f"Error al conectar: {err}")