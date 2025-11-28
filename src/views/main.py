import tkinter as tk
from tkinter import ttk
from views.pedidos_window import PedidosWindow
from views.usuarios_window import UsuariosWindow

class MainWindow:
    def __init__(self, usuario):
        self.usuario = usuario

        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Pedidos")
        self.root.geometry("800x500")

        menubar = tk.Menu(self.root)

        menu_pedidos = tk.Menu(menubar, tearoff=0)
        menu_pedidos.add_command(label="Ver pedidos", command=self.abrir_pedidos)
        menubar.add_cascade(label="Pedidos", menu=menu_pedidos)


        if self.usuario.role == "admin":
            menu_usuarios = tk.Menu(menubar, tearoff=0)
            menu_usuarios.add_command(label="Ver usuarios", command=self.abrir_usuarios)
            menubar.add_cascade(label="Usuarios", menu=menu_usuarios)

        self.root.config(menu=menubar)

        ttk.Label(self.root, text=f"Bienvenido, {self.usuario.nombre}",
                  font=("Arial", 14)).pack(pady=10)

        ttk.Label(self.root,
                  text="Usa el menú superior para navegar.",
                  font=("Arial", 10)).pack()

        self.root.mainloop()


    def abrir_pedidos(self):
        PedidosWindow()

    def abrir_usuarios(self):
        UsuariosWindow()
