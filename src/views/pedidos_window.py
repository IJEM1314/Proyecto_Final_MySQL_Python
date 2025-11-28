import tkinter as tk
from tkinter import ttk, messagebox
from controllers.pedidos_controller import PedidosController

class PedidosWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Pedidos")
        self.win.geometry("600x400")
        ttk.Label(self.win, text="Pedidos registrados:",
                  font=("Arial", 12)).pack(pady=5)
        self.lista = tk.Listbox(self.win, height=15)
        self.lista.pack(fill="both", expand=True, padx=10)
        self.cargar_pedidos()
        frame = ttk.Frame(self.win)
        frame.pack(pady=10)
        ttk.Button(frame, text="Actualizar", command=self.cargar_pedidos).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=1, padx=5)

    def cargar_pedidos(self):
        self.lista.delete(0, tk.END)
        pedidos = PedidosController.listar_pedidos()
        if not pedidos:
            self.lista.insert(tk.END, "No hay pedidos")
            return
        for p in pedidos:
            self.lista.insert(tk.END, f"[{p.id}] Cliente ID: {p.cliente_id} | {p.tipo} | {p.estatus}")

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un pedido")
            return
        item = self.lista.get(sel[0])
        pid = int(item.split("]")[0].replace("[", ""))
        if PedidosController.eliminar_pedido(pid):
            messagebox.showinfo("OK", "Pedido eliminado")
            self.cargar_pedidos()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")
