import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Toggle Button Couleur")

# Créer un style
style = ttk.Style()
style.configure("Red.TButton", foreground="red", background="red")
style.configure("Green.TButton", foreground="green", background="green")

toggle_state = False

def toggle():
    global toggle_state
    toggle_state = not toggle_state
    if toggle_state:
        btn.config(text="ON", style="Green.TButton")
    else:
        btn.config(text="OFF", style="Red.TButton")

# Bouton initial
btn = ttk.Button(root, text="OFF", style="Red.TButton", command=toggle)
btn.pack(pady=20, padx=20)

root.mainloop()
