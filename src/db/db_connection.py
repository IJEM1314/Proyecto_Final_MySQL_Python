import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_conn():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            username=os.getenv("DB_USERNAME"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return conn
    except mysql.connector.Error as e:
        print("Error de conexión a la base de datos:", e)
        return None
