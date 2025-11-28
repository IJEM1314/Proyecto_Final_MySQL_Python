from models.pedido import Pedido
from db.db_connection import get_conn
from models.usuario import Usuario

class Empleado(Usuario):
    def __init__(self, id, nombre, correo, departamento, password_hash):
        super().__init__(id, nombre, correo, "empleado", departamento, password_hash)

    def registrar_pedido(self, cliente_id, tipo, direccion_envio):
        return Pedido.crear(cliente_id, tipo, direccion_envio)

    def actualizar_estatus(self, pedido_id, nuevo_estatus):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE pedidos SET estatus=%s WHERE id=%s", (nuevo_estatus, pedido_id))
        conn.commit()
        cur.close()
        conn.close()

    def validar_entrega(self, pedido_id):
        self.actualizar_estatus(pedido_id, "Entregado")
