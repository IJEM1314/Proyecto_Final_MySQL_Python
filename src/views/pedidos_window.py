import tkinter as tk
from tkinter import ttk, messagebox
from models.pedido import Pedido
from models.cliente import Cliente
from models.etiqueta import Etiqueta
from db.db_connection import get_conn

class PedidosWindow:
    def __init__(self, usuario):
        self.usuario = usuario
        self.win = tk.Toplevel()
        self.win.title("Pedidos")
        self.win.geometry("800x500")
        self.lista = tk.Listbox(self.win, height=18)
        self.lista.pack(fill="both", expand=True, padx=10, pady=10)
        frame = ttk.Frame(self.win)
        frame.pack(pady=10)

        ttk.Button(frame, text="Actualizar", command=self.cargar).grid(row=0, column=0, padx=5)
        if self.usuario.departamento == "ventas" or self.usuario.role == "admin":
             ttk.Button(frame, text="Crear pedido", command=self.crear).grid(row=0, column=1, padx=5)
        ttk.Button(frame, text="Etiquetas", command=self.etiquetas).grid(row=0, column=2, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=3, padx=5)

        self.cargar()

    def cargar(self):
        self.lista.delete(0, tk.END)
        for p in Pedido.listar():
            unidad = p.unidad_id if p.unidad_id else "Sin unidad"
            self.lista.insert(tk.END, f"{p.id} | Cliente {p.cliente_id} | {p.tipo} | {p.estatus} | Unidad: {unidad}")


    def crear(self):
        win = tk.Toplevel(self.win)
        win.title("Crear pedido")
        win.geometry("350x400")
        clientes = Cliente.listar()
        clientes_op = [f"{c.id} - {c.nombre}" for c in clientes]
        cliente_var = tk.StringVar()
        tipo_var = tk.StringVar()
        direccion_var = tk.StringVar()

        ttk.Label(win, text="Cliente").pack()
        ttk.OptionMenu(win, cliente_var, clientes_op[0], *clientes_op).pack()
        ttk.Label(win, text="Tipo").pack()
        ttk.OptionMenu(win, tipo_var, "Requisición", "Requisición", "Factura", "Cotización").pack()
        ttk.Label(win, text="Dirección").pack()
        ttk.Entry(win, textvariable=direccion_var).pack()

        def guardar():
            cid = cliente_var.get().split("-")[0].strip()
            Pedido.crear(cid, tipo_var.get(), direccion_var.get())
            win.destroy()
            self.cargar()
        ttk.Button(win, text="Guardar", command=guardar).pack(pady=15)

    def etiquetas(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showerror("Error", "Selecciona un pedido")
            return
        pid = int(self.lista.get(sel[0]).split("|")[0].strip())
        EtiquetaAplicacion(pid)

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        pid = int(self.lista.get(sel[0]).split("|")[0].strip())
        Pedido(pid, None, None, None, None, None).eliminar()
        self.cargar()


class EtiquetaAplicacion:
    def __init__(self, pid):
        self.pid = pid
        self.win = tk.Toplevel()
        self.win.title("Etiquetas")
        self.win.geometry("350x350")
        self.lista = tk.Listbox(self.win, height=15)
        self.lista.pack(fill="both", padx=10, pady=10)
        for e in Etiqueta.listar():
            self.lista.insert(tk.END, f"{e.id} | {e.nombre}")
        ttk.Button(self.win, text="Aplicar", command=self.aplicar).pack(pady=5)
        ttk.Button(self.win, text="Quitar", command=self.quitar).pack(pady=5)

    def aplicar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        eid = int(self.lista.get(sel[0]).split("|")[0].strip())
        Pedido.aplicar_etiqueta(self.pid, eid)
        messagebox.showinfo("OK", "Etiqueta aplicada")

    def quitar(self):
        sel = self.lista.curselection()
        if not sel:
            return
        eid = int(self.lista.get(sel[0]).split("|")[0].strip())
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM pedido_etiqueta WHERE pedido_id=%s AND etiqueta_id=%s",
            (self.pid, eid))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("OK", "Etiqueta quitada")
