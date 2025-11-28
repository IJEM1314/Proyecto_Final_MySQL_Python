import unittest
from models.etiqueta import Etiqueta
from db.db_connection import get_conn

class TestEtiquetas(unittest.TestCase):

    def setUp(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM etiquetas")
        conn.commit()
        cur.close()
        conn.close()

    def test_crear_listar(self):
        Etiqueta.crear("Urgente", "Rojo")
        lista = Etiqueta.listar()
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].nombre, "Urgente")

if __name__ == "__main__":
    unittest.main()
