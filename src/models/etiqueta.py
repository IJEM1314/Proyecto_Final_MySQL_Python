from db.db_connection import get_conn

class Etiqueta:
    def __init__(self, id, nombre, color):
        self.id = id
        self.nombre = nombre
        self.color = color

    @classmethod
    def crear(cls, nombre, color):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""INSERT INTO etiquetas (nombre, color) VALUES (%s, %s)""",
            (nombre, color))
        conn.commit()
        eid = cur.lastrowid
        cur.close()
        conn.close()
        return cls(eid, nombre, color)
