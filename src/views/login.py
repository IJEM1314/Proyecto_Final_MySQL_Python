import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario
from views.registro import RegistroWindow

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x230")

        ttk.Label(root, text="Usuario:").pack(pady=5)
        self.entry_nombre = ttk.Entry(root)
        self.entry_nombre.pack()

        ttk.Label(root, text="Contraseña:").pack(pady=5)
        self.entry_password = ttk.Entry(root, show="*")
        self.entry_password.pack()

        ttk.Button(root, text="Iniciar sesión", command=self.login).pack(pady=10)
        ttk.Button(root, text="Crear cuenta", command=self.registro).pack()
        ttk.Button(root, text="Salir", command=root.quit).pack(pady=5)

        self.usuario_logeado = None

    def registro(self):
        r = RegistroWindow(self.root)
        self.root.wait_window(r.root)
        if r.usuario_creado:
            self.usuario_logeado = r.usuario_creado
            self.root.destroy()

    def login(self):
        nombre = self.entry_nombre.get()
        password = self.entry_password.get()
        usuario = Usuario.login(nombre, password)
        if usuario:
            self.usuario_logeado = usuario
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
