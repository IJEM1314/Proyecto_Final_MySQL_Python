from db.db_connection import get_conn

class Bitacora:
    @staticmethod
    def registrar(usuario_id, accion, detalles=""):
        try:
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(""" INSERT INTO logs (usuario_id, accion, detalles) VALUES (%s, %s, %s)""",
                (usuario_id, accion, detalles))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print("Error registrando log:", e)
