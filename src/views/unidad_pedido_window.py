import tkinter as tk
from tkinter import ttk, messagebox
from models.pedido import Pedido
from models.unidad import Unidad

class AsignarUnidadWindow:
    def __init__(self, usuario):
        self.usuario = usuario
        self.win = tk.Toplevel()
        self.win.title("Asignar unidad")
        self.win.geometry("450x400")

        self.lista_pedidos = tk.Listbox(self.win, height=10, exportselection=False)
        self.lista_pedidos.pack(fill="x", padx=10, pady=5)

        self.lista_unidades = tk.Listbox(self.win, height=10, exportselection=False)
        self.lista_unidades.pack(fill="x", padx=10, pady=5)

        ttk.Button(self.win, text="Asignar", command=self.asignar).pack(pady=10)

        self.cargar()

    def cargar(self):
        self.lista_pedidos.delete(0, tk.END)
        for p in Pedido.listar():
            if p.estatus in ["Generado", "Recibido"]:
                self.lista_pedidos.insert(tk.END, f"{p.id} | {p.tipo} | {p.estatus}")

        self.lista_unidades.delete(0, tk.END)
        for u in Unidad.listar():
            self.lista_unidades.insert(tk.END, f"{u.id} | {u.tipo} | {u.placas}")

    def asignar(self):
        sp = self.lista_pedidos.curselection()
        su = self.lista_unidades.curselection()

        if not sp or not su:
            messagebox.showerror("Error", "Selecciona un pedido y una unidad")
            return

        pid = int(self.lista_pedidos.get(sp[0]).split("|")[0].strip())
        uid = int(self.lista_unidades.get(su[0]).split("|")[0].strip())

        Pedido.asignar_unidad(pid, uid)

        messagebox.showinfo("OK", "Unidad asignada correctamente")
        self.cargar()
