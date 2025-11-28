import unittest
from models.cliente import Cliente
from db.db_connection import get_conn

class TestClientes(unittest.TestCase):

    def setUp(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes")
        conn.commit()
        cur.close()
        conn.close()

    def test_crear_listar(self):
        c = Cliente.crear("Cliente A", "C001", "Direccion 123")
        lista = Cliente.listar()
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].nombre, "Cliente A")

if __name__ == "__main__":
    unittest.main()
