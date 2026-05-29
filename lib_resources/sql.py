import pg8000
import json
class DBManager:
    def __init__(self):
        with open ("credentials/credentials_sql.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        self.config = {
            "host": datos["host"],
            "database": datos["database"],
            "user": datos["user"],
            "password": datos["password"]
        }

    def registrar_log(self, bot, evento, estado, anio=None, bytes=None, error=None):
        try:
            conn = pg8000.connect(**self.config)
            cursor = conn.cursor()
            query = """
                INSERT INTO rpa_logs (bot_nombre, evento, estado, anio_reporte, tamanio_bytes, mensaje_error)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (bot, evento, estado, anio, bytes, error))
            conn.commit()
            cursor.close()
        except Exception as e:
            print(f"Error real en la conexión: {e}")
        finally:
            if conn is not None:
                conn.close()
               