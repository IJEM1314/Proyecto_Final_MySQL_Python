import tkinter as tk
from tkinter import ttk, messagebox
from models.cliente import Cliente
from db.db_connection import get_conn

class ClientesWindow:
    def __init__(self, usuario):
        self.usuario = usuario
        self.win = tk.Toplevel()
        self.win.title("Clientes")
        self.win.geometry("700x450")
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
        for c in Cliente.listar():
            self.lista.insert(tk.END, f"{c.id} | {c.nombre} | {c.codigo_cliente} | {c.direccion}")

    def crear(self):
        win = tk.Toplevel(self.win)
        win.title("Crear cliente")
        win.geometry("300x300")

        nombre = tk.StringVar()
        codigo = tk.StringVar()
        direccion = tk.StringVar()

        ttk.Label(win, text="Nombre").pack()
        ttk.Entry(win, textvariable=nombre).pack()

        ttk.Label(win, text="Código cliente").pack()
        ttk.Entry(win, textvariable=codigo).pack()

        ttk.Label(win, text="Dirección").pack()
        ttk.Entry(win, textvariable=direccion).pack()

        def guardar():
            Cliente.crear(nombre.get(), codigo.get(), direccion.get())
            win.destroy()
            self.cargar()

        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def editar(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un cliente")
            return
        raw = self.lista.get(sel[0])
        cid = int(raw.split("|")[0].strip())
        clientes = Cliente.listar()
        cliente = next(c for c in clientes if c.id == cid)
        win = tk.Toplevel(self.win)
        win.title("Editar cliente")
        win.geometry("300x300")
        nombre = tk.StringVar(value=cliente.nombre)
        codigo = tk.StringVar(value=cliente.codigo_cliente)
        direccion = tk.StringVar(value=cliente.direccion)

        ttk.Label(win, text="Nombre").pack()
        ttk.Entry(win, textvariable=nombre).pack()
        ttk.Label(win, text="Código").pack()
        ttk.Entry(win, textvariable=codigo).pack()
        ttk.Label(win, text="Dirección").pack()
        ttk.Entry(win, textvariable=direccion).pack()

        def guardar():
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE clientes SET nombre=%s, codigo_cliente=%s, direccion=%s WHERE id=%s",
                (nombre.get(), codigo.get(), direccion.get(), cid))
            conn.commit()
            cur.close()
            conn.close()
            win.destroy()
            self.cargar()
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un cliente")
            return
        cid = int(self.lista.get(sel[0]).split("|")[0].strip())

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM clientes WHERE id=%s", (cid,))
        conn.commit()
        cur.close()
        conn.close()

        self.cargar()
