import tkinter as tk
from tkinter import ttk


class Application(ttk.Frame):

    def __init__(self, main_window):
        super().__init__(main_window)
        # Establecer un título.
        main_window.title("Vista de árbol en Tkinter")
        # Creación de la vista de árbol.
        self.treeview = ttk.Treeview(self)
        self.treeview.insert("", tk.END, text="Elemento 1")
        self.treeview.insert("", tk.END, text="Elemento 2")
        self.treeview.insert("", tk.END, text="Elemento 3")
        self.treeview.insert("", tk.END, text="Elemento 4")
        self.treeview.insert("Elemento 1", tk.END, text="Subelemento 1")
        self.treeview.pack()
        self.pack()


# Creación de la ventana principal.
main_window = tk.Tk()
app = Application(main_window)
app.mainloop()