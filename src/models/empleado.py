from models.usuario import Usuario

class Empleado(Usuario):
    def __init__(self, id, nombre, correo, departamento, password_hash):
        super().__init__(id, nombre, correo, "empleado", departamento, password_hash)

    def registrar_pedido(self):
        pass

    def actualizar_estatus(self):
        pass

    def validar_entrega(self):
        pass
