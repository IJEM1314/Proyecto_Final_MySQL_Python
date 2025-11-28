import tkinter as tk
from tkinter import ttk, messagebox
from models.pedido import Pedido
from db.db_connection import get_conn

class EstatusWindow:
    def __init__(self, usuario):
        self.usuario = usuario
        self.win = tk.Toplevel()
        self.win.title("Cambiar estatus")
        self.win.geometry("450x400")
        self.lista = tk.Listbox(self.win, height=12)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        if usuario.departamento == "embarques":
            opciones = ["Recibido", "En Ruta", "En Puerta"]
        else:
            opciones = ["Entregado", "Revisado"]
        self.estatus = tk.StringVar()
        ttk.OptionMenu(self.win, self.estatus, opciones[0], *opciones).pack()
        ttk.Button(self.win, text="Actualizar", command=self.cambiar).pack(pady=10)
        self.cargar()

    def cargar(self):
        self.lista.delete(0, tk.END)
        for p in Pedido.listar():
            self.lista.insert(tk.END, f"{p.id} | {p.tipo} | {p.estatus}")

    def cambiar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        pid = int(self.lista.get(sel[0]).split("|")[0].strip())
        nuevo = self.estatus.get()
        Pedido.cambiar_estatus(pid, nuevo)
        self.cargar()
        messagebox.showinfo("OK", "Estatus actualizado")
