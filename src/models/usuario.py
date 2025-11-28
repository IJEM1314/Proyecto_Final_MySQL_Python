from db.db_connection import get_conn
from logs.registro import Bitacora
import hashlib

class Usuario:
    def __init__(self, id, nombre, correo, role, departamento, password_hash=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
        self.role = role
        self.departamento = departamento
        self.password_hash = password_hash

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @classmethod
    def crear(cls, nombre, correo, role, departamento, password):
        password_hash = cls.hash_password(password)
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuarios (nombre, correo, role, departamento, password_hash) VALUES (%s, %s, %s, %s, %s)",
            (nombre, correo, role, departamento, password_hash)
        )
        conn.commit()
        uid = cur.lastrowid
        cur.close()
        conn.close()
        Bitacora.registrar(uid, "CREAR_USUARIO", f"Usuario creado: {nombre}")
        return cls(uid, nombre, correo, role, departamento, password_hash)

    @classmethod
    def listar(cls):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, correo, role, departamento, password_hash FROM usuarios")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [cls(*r) for r in rows]

    @classmethod
    def buscar_por_id(cls, user_id):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, correo, role, departamento, password_hash FROM usuarios WHERE id=%s",
                    (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def login(cls, nombre, password):
        hashed = cls.hash_password(password)
        for u in cls.listar():
            if u.nombre == nombre and u.password_hash == hashed:
                Bitacora.registrar(u.id, "LOGIN", "Inicio de sesión")
                return u
        return None

    def eliminar(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=%s", (self.id,))
        conn.commit()
        cur.close()
        conn.close()
        Bitacora.registrar(self.id, "ELIMINAR_USUARIO", f"Usuario eliminado: {self.nombre}")
