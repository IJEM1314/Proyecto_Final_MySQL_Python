import unittest
from models.unidad import Unidad
from db.db_connection import get_conn

class TestUnidades(unittest.TestCase):

    def setUp(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM unidades")
        conn.commit()
        cur.close()
        conn.close()

    def test_crear_listar(self):
        u = Unidad.crear("Camión", "ABC123", None)
        unidades = Unidad.listar()
        self.assertEqual(len(unidades), 1)
        self.assertEqual(unidades[0].tipo, "Camión")

if __name__ == "__main__":
    unittest.main()
