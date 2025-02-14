import mysql.connector
from config import DB_CONFIG

try:
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    cursor.execute("SELECT DATABASE();")
    database_name = cursor.fetchone()[0]
    print(f"✅ Conexión exitosa a MySQL. Base de datos en uso: {database_name}")
    cursor.close()
    db.close()
except mysql.connector.Error as err:
    print(f"❌ Error al conectar a MySQL: {err}")
