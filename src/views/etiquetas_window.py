import tkinter as tk
from tkinter import ttk, messagebox
from models.etiqueta import Etiqueta
from db.db_connection import get_conn

class EtiquetasWindow:
    def __init__(self, usuario):
        self.win = tk.Toplevel()
        self.win.title("Etiquetas")
        self.win.geometry("500x400")
        self.lista = tk.Listbox(self.win, height=15)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        frame = ttk.Frame(self.win)
        frame.pack()

        ttk.Button(frame, text="Actualizar", command=self.cargar).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Crear", command=self.crear).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Editar", command=self.editar).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=3, padx=5)

        self.cargar()

    def cargar(self):
        self.lista.delete(0, tk.END)
        for e in Etiqueta.listar():
            self.lista.insert(tk.END, f"{e.id} | {e.nombre} | {e.color}")

    def crear(self):
        win = tk.Toplevel(self.win)
        win.title("Crear etiqueta")
        win.geometry("300x250")
        nombre = tk.StringVar()
        color = tk.StringVar()

        ttk.Label(win, text="Nombre").pack()
        ttk.Entry(win, textvariable=nombre).pack()
        ttk.Label(win, text="Color").pack()
        ttk.Entry(win, textvariable=color).pack()

        def guardar():
            Etiqueta.crear(nombre.get(), color.get())
            win.destroy()
            self.cargar()

        ttk.Button(win, text="Guardar", command=guardar).pack(pady=10)

    def editar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        eid = int(self.lista.get(sel[0]).split("|")[0].strip())
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT nombre, color FROM etiquetas WHERE id=%s", (eid,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        win = tk.Toplevel(self.win)
        win.title("Editar etiqueta")
        win.geometry("300x250")
        nombre = tk.StringVar(value=row[0])
        color = tk.StringVar(value=row[1])

        ttk.Label(win, text="Nombre").pack()
        ttk.Entry(win, textvariable=nombre).pack()
        ttk.Label(win, text="Color").pack()
        ttk.Entry(win, textvariable=color).pack()

        def guardar():
            conn = get_conn()
            cur = conn.cursor()
            cur.execute("UPDATE etiquetas SET nombre=%s, color=%s WHERE id=%s",
                (nombre.get(), color.get(), eid))
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
        eid = int(self.lista.get(sel[0]).split("|")[0].strip())
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM etiquetas WHERE id=%s", (eid,))
        conn.commit()
        cur.close()
        conn.close()
        self.cargar()
