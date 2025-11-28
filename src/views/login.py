import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuarios_controller import UsuariosController

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistema de Pedidos")
        self.root.geometry("300x200")

        ttk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_nombre = ttk.Entry(root)
        self.entry_nombre.pack()

        ttk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_password = ttk.Entry(root, show="*")
        self.entry_password.pack()

        ttk.Button(root, text="Iniciar Sesión", command=self.login).pack(pady=10)
        ttk.Button(root, text="Cancelar", command=root.quit).pack()
        self.usuario_logeado = None

    def login(self):
        nombre = self.entry_nombre.get()
        password = self.entry_password.get()
        usuario = UsuariosController.login(nombre, password)
        if usuario:
            self.usuario_logeado = usuario
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
