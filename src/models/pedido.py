from db.db_connection import get_conn
from logs.registro import Bitacora

class Pedido:
    def __init__(self, id, cliente_id, tipo, estatus, fecha, direccion, unidad_id=None):
        self.id = id
        self.cliente_id = cliente_id
        self.tipo = tipo
        self.estatus = estatus
        self.fecha = fecha
        self.direccion = direccion
        self.unidad_id = unidad_id

    @staticmethod
    def asignar_unidad(pedido_id, unidad_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""UPDATE pedidos SET unidad_id=%s, estatus='En Ruta' WHERE id=%s""",
            (unidad_id, pedido_id))
        conn.commit()
        cur.close()
        conn.close()
        
    @classmethod
    def crear(cls, cliente_id, tipo, direccion_envio):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pedidos (cliente_id, tipo, estatus, direccion_envio) VALUES (%s, %s, 'Generado', %s)",
            (cliente_id, tipo, direccion_envio)
        )
        conn.commit()
        pid = cur.lastrowid
        cur.close()
        conn.close()
        Bitacora.registrar(None, "CREAR_PEDIDO", f"Pedido {pid}")
        return cls(pid, cliente_id, tipo, "Generado", None, direccion_envio)

    @classmethod
    def listar(cls):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, cliente_id, tipo, estatus, fecha_creacion, direccion_envio FROM pedidos"
        )
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
        Bitacora.registrar(None, "ELIMINAR_PEDIDO", f"Pedido {self.id}")

    @classmethod
    def cambiar_estatus(cls, pedido_id, nuevo):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE pedidos SET estatus=%s WHERE id=%s", (nuevo, pedido_id))
        conn.commit()
        cur.close()
        conn.close()

    @classmethod
    def aplicar_etiqueta(cls, pedido_id, etiqueta_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pedido_etiqueta (pedido_id, etiqueta_id) VALUES (%s, %s)",
            (pedido_id, etiqueta_id)
        )
        conn.commit()
        cur.close()
        conn.close()
