import tkinter as tk
from tkinter import ttk
from views.usuarios_window import UsuariosWindow
from views.clientes_window import ClientesWindow
from views.pedidos_window import PedidosWindow
from views.unidades_window import UnidadesWindow
from views.etiquetas_window import EtiquetasWindow
from views.estatus_window import EstatusWindow
from views.unidad_pedido_window import AsignarUnidadWindow

class MainWindow:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = tk.Tk()
        self.root.title("Sistema de Pedidos")
        self.root.geometry("900x550")

        menubar = tk.Menu(self.root)

        menu_pedidos = tk.Menu(menubar, tearoff=0)
        menu_pedidos.add_command(label="Ver pedidos", command=self.abrir_pedidos)

        if usuario.departamento == "ventas" or usuario.role == "admin":
            menu_pedidos.add_command(label="Crear pedido", command=self.abrir_pedidos)

        if usuario.departamento == "embarques" or usuario.role == "admin":
            menu_pedidos.add_command(label="Asignar unidad", command=self.abrir_asignar_unidad)

        if usuario.departamento in ["embarques", "auditoria"] or usuario.role == "admin":
            menu_pedidos.add_command(label="Cambiar estatus", command=self.abrir_estatus)

        menubar.add_cascade(label="Pedidos", menu=menu_pedidos)

        if usuario.departamento in ["ventas", "administracion"] or usuario.role == "admin":
            menu_clientes = tk.Menu(menubar, tearoff=0)
            menu_clientes.add_command(label="Administrar clientes", command=self.abrir_clientes)
            menubar.add_cascade(label="Clientes", menu=menu_clientes)

        if usuario.departamento in ["flotilla", "administracion"] or usuario.role == "admin":
            menu_unidades = tk.Menu(menubar, tearoff=0)
            menu_unidades.add_command(label="Administrar unidades", command=self.abrir_unidades)
            menubar.add_cascade(label="Unidades", menu=menu_unidades)

        if usuario.role == "admin":
            menu_usuarios = tk.Menu(menubar, tearoff=0)
            menu_usuarios.add_command(label="Administrar usuarios", command=self.abrir_usuarios)
            menubar.add_cascade(label="Usuarios", menu=menu_usuarios)

        if usuario.role == "admin":
            menu_etiquetas = tk.Menu(menubar, tearoff=0)
            menu_etiquetas.add_command(label="Administrar etiquetas", command=self.abrir_etiquetas)
            menubar.add_cascade(label="Etiquetas", menu=menu_etiquetas)

        self.root.config(menu=menubar)

        ttk.Label(self.root, text=f"Bienvenido, {usuario.nombre}", font=("Arial", 16)).pack(pady=20)
        ttk.Label(self.root, text=f"Rol: {usuario.role} | Depto: {usuario.departamento}",
                  font=("Arial", 12)).pack()

        self.root.mainloop()

    def abrir_usuarios(self):
        UsuariosWindow()

    def abrir_clientes(self):
        ClientesWindow(self.usuario)

    def abrir_pedidos(self):
        PedidosWindow(self.usuario)

    def abrir_unidades(self):
        UnidadesWindow(self.usuario)

    def abrir_etiquetas(self):
        EtiquetasWindow(self.usuario)

    def abrir_estatus(self):
        EstatusWindow(self.usuario)

    def abrir_asignar_unidad(self):
        AsignarUnidadWindow(self.usuario)
