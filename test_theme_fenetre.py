import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def changer_theme(nouveau_theme):
    root.style.theme_use(nouveau_theme)
    label.config(text=f"Thème actuel : {nouveau_theme}")

# Création de la fenêtre avec un thème initial (ex: 'darkly')
root = ttk.Window(themename="darkly")
root.title("Demo des thèmes ttkbootstrap")
root.geometry("300x220")

# Récupère les styles disponibles
themes = root.style.theme_names()

label = ttk.Label(root, text="Thème actuel :", font=("Segoe UI", 10))
label.pack(pady=10)

combo = ttk.Combobox(root, values=themes, state="readonly")
combo.set(root.style.theme_use())
combo.pack(pady=5)
combo.bind("<<ComboboxSelected>>", lambda e: changer_theme(combo.get()))

btn = ttk.Button(root, text="Bouton test", bootstyle="success")
btn.pack(pady=10)

entry = ttk.Entry(root)
entry.insert(0, "Champ texte")
entry.pack(pady=5)

chk = ttk.Checkbutton(root, text="Case à cocher", bootstyle="info")
chk.pack(pady=5)

root.mainloop()
