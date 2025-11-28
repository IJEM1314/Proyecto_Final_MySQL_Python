import unittest
from models.pedido import Pedido
from models.cliente import Cliente
from db.db_connection import get_conn

class TestPedidos(unittest.TestCase):

    def setUp(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM pedidos")
        cur.execute("DELETE FROM clientes")
        conn.commit()
        cur.close()
        conn.close()

    def test_crear_cambiar_estatus(self):
        c = Cliente.crear("Cliente Test", "C002", "Dir")
        p = Pedido.crear(c.id, "Requisición", "Dir X")
        Pedido.cambiar_estatus(p.id, "En Ruta")
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT estatus FROM pedidos WHERE id=%s", (p.id,))
        est = cur.fetchone()[0]
        cur.close()
        conn.close()
        self.assertEqual(est, "En Ruta")

if __name__ == "__main__":
    unittest.main()
