from db.db_connection import get_conn
from logs.registro import Bitacora

class Cliente:
    def __init__(self, id, nombre, codigo_cliente, direccion):
        self.id = id
        self.nombre = nombre
        self.codigo_cliente = codigo_cliente
        self.direccion = direccion

    @classmethod
    def crear(cls, nombre, codigo_cliente, direccion):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""INSERT INTO clientes (nombre, codigo_cliente, direccion) VALUES (%s, %s, %s)""",
            (nombre, codigo_cliente, direccion))
        conn.commit()
        cid = cur.lastrowid
        cur.close()
        conn.close()
        Bitacora.registrar(None, "CREAR_CLIENTE", f"Cliente creado: {nombre}")
        return cls(cid, nombre, codigo_cliente, direccion)

    @classmethod
    def listar(cls):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, codigo_cliente, direccion FROM clientes")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(*r) for r in rows]
