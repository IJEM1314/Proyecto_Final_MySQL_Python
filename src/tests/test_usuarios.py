import unittest
from models.usuario import Usuario
from db.db_connection import get_conn

class TestUsuarios(unittest.TestCase):

    def setUp(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios")
        conn.commit()
        cur.close()
        conn.close()

    def test_crear_y_login(self):
        u = Usuario.crear("isai", "isa@mail.com", "empleado", "ventas", "1234")
        self.assertIsNotNone(u)
        login_ok = Usuario.login("isai", "1234")
        self.assertIsNotNone(login_ok)

    def test_eliminar(self):
        u = Usuario.crear("juan", "j@mail.com", "empleado", "ventas", "pass")
        uid = u.id
        u.eliminar()
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id=%s", (uid,))
        self.assertIsNone(cur.fetchone())
        cur.close()
        conn.close()

if __name__ == "__main__":
    unittest.main()
