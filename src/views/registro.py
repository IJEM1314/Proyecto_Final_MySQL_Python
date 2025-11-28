import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models.usuario import Usuario

class RegistroWindow:
    def __init__(self, root):
        self.root = tk.Toplevel(root)
        self.root.title("Registro")
        self.root.geometry("350x380")
        ttk.Label(self.root, text="Nombre:").pack(pady=5)
        self.entry_nombre = ttk.Entry(self.root)
        self.entry_nombre.pack()
        ttk.Label(self.root, text="Correo:").pack(pady=5)
        self.entry_correo = ttk.Entry(self.root)
        self.entry_correo.pack()
        ttk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.entry_password = ttk.Entry(self.root, show="*")
        self.entry_password.pack()
        ttk.Label(self.root, text="Departamento:").pack(pady=5)
        self.dep = tk.StringVar()
        deps = ["ventas", "embarques", "auditoria", "flotilla", "administracion"]
        ttk.OptionMenu(self.root, self.dep, deps[0], *deps).pack()
        ttk.Label(self.root, text="Rol:").pack(pady=5)
        self.role = tk.StringVar()
        roles = ["empleado", "admin"]
        ttk.OptionMenu(self.root, self.role, roles[0], *roles).pack()
        ttk.Button(self.root, text="Crear cuenta", command=self.crear).pack(pady=15)
        ttk.Button(self.root, text="Cancelar", command=self.root.destroy).pack()
        self.usuario_creado = None

    def crear(self):
        nombre = self.entry_nombre.get()
        correo = self.entry_correo.get()
        password = self.entry_password.get()
        departamento = self.dep.get()
        rol = self.role.get()
        if rol == "admin":
            codigo = simpledialog.askstring("Código admin", "Ingresa el código:")
            if codigo != "1314":
                messagebox.showerror("Error", "Código incorrecto")
                return
        u = Usuario.crear(nombre, correo, rol, departamento, password)
        self.usuario_creado = u
        messagebox.showinfo("OK", "Cuenta creada")
        self.root.destroy()
