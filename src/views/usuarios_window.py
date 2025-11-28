import tkinter as tk
from tkinter import ttk, messagebox
from models.usuario import Usuario

class UsuariosWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Usuarios")
        self.win.geometry("650x450")
        self.lista = tk.Listbox(self.win, height=15)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        frame = ttk.Frame(self.win)
        frame.pack(pady=10)
        ttk.Button(frame, text="Actualizar", command=self.cargar).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Crear", command=self.crear).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Editar", command=self.editar).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=3, padx=5)
        self.cargar()

    def cargar(self):
        self.lista.delete(0, tk.END)
        for u in Usuario.listar():
            self.lista.insert(tk.END, f"{u.id} | {u.nombre} | {u.role} | {u.departamento}")

    def crear(self):
        from views.registro import RegistroWindow
        r = RegistroWindow(self.win)
        self.win.wait_window(r.root)
        self.cargar()

    def editar(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un usuario")
            return
        raw = self.lista.get(sel[0])
        uid = int(raw.split("|")[0].strip())
        u = Usuario.buscar_por_id(uid)
        win = tk.Toplevel(self.win)
        win.title("Editar usuario")
        win.geometry("300x300")
        nombre = tk.StringVar(value=u.nombre)
        correo = tk.StringVar(value=u.correo)
        rol = tk.StringVar(value=u.role)
        dep = tk.StringVar(value=u.departamento)

        ttk.Label(win, text="Nombre").pack()
        ttk.Entry(win, textvariable=nombre).pack()
        ttk.Label(win, text="Correo").pack()
        ttk.Entry(win, textvariable=correo).pack()
        ttk.Label(win, text="Rol").pack()
        ttk.OptionMenu(win, rol, rol.get(), "empleado", "admin").pack()

        deps = ["ventas", "embarques", "auditoria", "flotilla", "administracion"]
        ttk.Label(win, text="Departamento").pack()
        ttk.OptionMenu(win, dep, dep.get(), *deps).pack()

        def guardar():
            from db.db_connection import get_conn
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE usuarios SET nombre=%s, correo=%s, role=%s, departamento=%s WHERE id=%s",
                (nombre.get(), correo.get(), rol.get(), dep.get(), uid))
            conn.commit()
            cur.close()
            conn.close()
            win.destroy()
            self.cargar()

        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un usuario")
            return
        raw = self.lista.get(sel[0])
        uid = int(raw.split("|")[0].strip())
        u = Usuario.buscar_por_id(uid)
        u.eliminar()
        self.cargar()
