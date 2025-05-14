import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = "ISN4-evolution"
        self.height = 1080
        self.width = 1920
        self.geometry = f"{self.width}x{self.height}"

    def run(self):
        self.mainloop()
