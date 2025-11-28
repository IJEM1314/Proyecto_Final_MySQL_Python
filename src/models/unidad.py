from db.db_connection import get_conn

class Unidad:
    def __init__(self, id, tipo, placas, chofer_id):
        self.id = id
        self.tipo = tipo
        self.placas = placas
        self.chofer_id = chofer_id

    @classmethod
    def crear(cls, tipo, placas, chofer_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""INSERT INTO unidades (tipo, placas, chofer_id)VALUES (%s, %s, %s)""", 
            (tipo, placas, chofer_id))
        conn.commit()
        uid = cur.lastrowid
        cur.close()
        conn.close()
        return cls(uid, tipo, placas, chofer_id)
