import tkinter as tk
from tkinter import ttk, messagebox
from models.unidad import Unidad
from models.usuario import Usuario
from db.db_connection import get_conn

class UnidadesWindow:
    def __init__(self, usuario):
        self.usuario = usuario
        self.win = tk.Toplevel()
        self.win.title("Unidades")
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
        for u in Unidad.listar():
            self.lista.insert(tk.END, f"{u.id} | {u.tipo} | {u.placas} | Chofer {u.chofer_id}")

    def crear(self):
        win = tk.Toplevel(self.win)
        win.title("Crear unidad")
        win.geometry("300x300")
        tipo = tk.StringVar()
        placas = tk.StringVar()
        choferes = [u for u in Usuario.listar() if u.departamento == "flotilla"]
        opciones = [f"{u.id} - {u.nombre}" for u in choferes]
        chofer_var = tk.StringVar(value=opciones[0] if opciones else "")

        ttk.Label(win, text="Tipo").pack()
        ttk.Entry(win, textvariable=tipo).pack()
        ttk.Label(win, text="Placas").pack()
        ttk.Entry(win, textvariable=placas).pack()
        ttk.Label(win, text="Chofer").pack()
        ttk.OptionMenu(win, chofer_var, chofer_var.get(), *opciones).pack()

        def guardar():
            elegido = chofer_var.get().split("-")[0].strip()
            Unidad.crear(tipo.get(), placas.get(), elegido)
            win.destroy()
            self.cargar()

        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def editar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        uid = int(self.lista.get(sel[0]).split("|")[0].strip())
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT tipo, placas, chofer_id FROM unidades WHERE id=%s", (uid,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        win = tk.Toplevel(self.win)
        win.title("Editar unidad")
        win.geometry("300x300")
        tipo = tk.StringVar(value=row[0])
        placas = tk.StringVar(value=row[1])
        choferes = [u for u in Usuario.listar() if u.departamento == "flotilla"]
        opciones = [f"{u.id} - {u.nombre}" for u in choferes]
        inicial = next((o for o in opciones if o.startswith(str(row[2]))), opciones[0])
        chofer_var = tk.StringVar(value=inicial)

        ttk.Label(win, text="Tipo").pack()
        ttk.Entry(win, textvariable=tipo).pack()
        ttk.Label(win, text="Placas").pack()
        ttk.Entry(win, textvariable=placas).pack()
        ttk.Label(win, text="Chofer").pack()
        ttk.OptionMenu(win, chofer_var, inicial, *opciones).pack()

        def guardar():
            elegido = chofer_var.get().split("-")[0].strip()
            conn = get_conn()
            cur = conn.cursor()
            cur.execute(
                "UPDATE unidades SET tipo=%s, placas=%s, chofer_id=%s WHERE id=%s",
                (tipo.get(), placas.get(), elegido, uid)
            )
            conn.commit()
            cur.close()
            conn.close()
            win.destroy()
            self.cargar()

        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        uid = int(self.lista.get(sel[0]).split("|")[0].strip())

        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM unidades WHERE id=%s", (uid,))
        conn.commit()
        cur.close()
        conn.close()
        self.cargar()
