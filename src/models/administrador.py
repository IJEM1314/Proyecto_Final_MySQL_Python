from models.usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id, nombre, correo, departamento, password_hash):
        super().__init__(id, nombre, correo, "admin", departamento, password_hash)

    def crear_usuario(self):
        pass

    def eliminar_usuario(self):
        pass

    def generar_reporte(self):
        pass

    def crear_etiqueta(self):
        pass
