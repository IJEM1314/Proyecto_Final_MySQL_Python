import tkinter as tk
from tkinter import ttk, messagebox
from controllers.usuarios_controller import UsuariosController

class UsuariosWindow:
    def __init__(self):
        self.win = tk.Toplevel()
        self.win.title("Usuarios del Sistema")
        self.win.geometry("600x400")
        ttk.Label(self.win, text="Usuarios registrados:",
                  font=("Arial", 12)).pack(pady=5)
        self.lista = tk.Listbox(self.win, height=15)
        self.lista.pack(fill="both", expand=True, padx=10)
        self.cargar_usuarios()
        frame = ttk.Frame(self.win)
        frame.pack(pady=10)
        ttk.Button(frame, text="Actualizar", command=self.cargar_usuarios).grid(row=0, column=0, padx=5)
        ttk.Button(frame, text="Eliminar", command=self.eliminar).grid(row=0, column=1, padx=5)

    def cargar_usuarios(self):
        self.lista.delete(0, tk.END)
        usuarios = UsuariosController.listar_usuarios()
        if not usuarios:
            self.lista.insert(tk.END, "No hay usuarios registrados")
            return
        for u in usuarios:
            self.lista.insert(tk.END, f"[{u.id}] {u.nombre} - {u.role}")

    def eliminar(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecciona un usuario")
            return
        item = self.lista.get(sel[0])
        uid = int(item.split("]")[0].replace("[", ""))
        if UsuariosController.eliminar_usuario(uid):
            messagebox.showinfo("OK", "Usuario eliminado")
            self.cargar_usuarios()
        else:
            messagebox.showerror("Error", "No se pudo eliminar")
