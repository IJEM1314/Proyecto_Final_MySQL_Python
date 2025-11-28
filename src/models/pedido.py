from db.db_connection import get_conn
from logs.registro import Bitacora

class Pedido:
    def __init__(self, id, cliente_id, tipo, estatus, fecha_creacion, direccion_envio):
        self.id = id
        self.cliente_id = cliente_id
        self.tipo = tipo
        self.estatus = estatus
        self.fecha_creacion = fecha_creacion
        self.direccion_envio = direccion_envio

    # CRUD
    @classmethod
    def crear(cls, cliente_id, tipo, direccion_envio):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""INSERT INTO pedidos (cliente_id, tipo, estatus, direccion_envio) VALUES (%s, %s, 'Generado', %s)""",
            (cliente_id, tipo, direccion_envio))
        conn.commit()
        pid = cur.lastrowid
        cur.close()
        conn.close()

        Bitacora.registrar(None, "CREAR_PEDIDO", f"Pedido {pid} para cliente {cliente_id}")

        return cls(pid, cliente_id, tipo, "Generado", None, direccion_envio)

    @classmethod
    def listar(cls):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""SELECT id, cliente_id, tipo, estatus, fecha_creacion, direccion_envio FROM pedidos""")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(*r) for r in rows]

    def eliminar(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM pedidos WHERE id=%s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()

        Bitacora.registrar(None, "ELIMINAR_PEDIDO", f"Pedido eliminado: {self.id}")
