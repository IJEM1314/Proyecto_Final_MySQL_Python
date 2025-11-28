from views.login import LoginWindow
from views.main import MainWindow
import tkinter as tk

def iniciar_app():
    login_root = tk.Tk()
    login_win = LoginWindow(login_root)
    login_root.mainloop()
    usuario = login_win.usuario_logeado
    if not usuario:
        return

    MainWindow(usuario)

if __name__ == "__main__":
    iniciar_app()
