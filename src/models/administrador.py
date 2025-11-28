from models.usuario import Usuario
from models.etiqueta import Etiqueta
from db.db_connection import get_conn

class Administrador(Usuario):
    def __init__(self, id, nombre, correo, departamento, password_hash):
        super().__init__(id, nombre, correo, "admin", departamento, password_hash)

    def crear_usuario(self, nombre, correo, role, departamento, password):
        return Usuario.crear(nombre, correo, role, departamento, password)

    def eliminar_usuario(self, user_id):
        u = Usuario.buscar_por_id(user_id)
        if u:
            u.eliminar()

    def crear_etiqueta(self, nombre, color):
        return Etiqueta.crear(nombre, color)
