import tkinter as tk

root = tk.Tk()

# Création d'une Frame positionnée à (50, 50) par .place() (par exemple)
frame = tk.Frame(root, width=200, height=100, bg="lightblue")
frame.place(x=50, y=50)

# Un bouton dans la frame, positionné par .grid() RELATIVEMENT À la frame
btn = tk.Button(frame, text="Bouton dans frame")
btn.grid(row=0, column=0)

root.mainloop()
