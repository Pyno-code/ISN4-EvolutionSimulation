import collections
import tkinter as tk

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import font as tkFont
import numpy as np

# code récupéré à l'origine sur https://es.stackoverflow.com/questions/348847/gr%C3%A1ficos-en-tiempo-real-con-matplotlib-y-tkinter


import collections
import tkinter as tk

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import font as tkFont
import numpy as np

# récupéré sur https://es.stackoverflow.com/questions/348847/gr%C3%A1ficos-en-tiempo-real-con-matplotlib-y-tkinter

class Graphique (tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        plt.style.use('dark_background')
        self.frame_graficas = tk.Frame(self, bg="#6E6E6E")
        self._figure_1, self._ax1 = plt.subplots()
        self._figure_1_canvas = FigureCanvasTkAgg(
            self._figure_1, master=self.frame_graficas
            )
        self._figure_2, self._ax2 = plt.subplots()
        self._figure_2_canvas = FigureCanvasTkAgg(
            self._figure_2, master=self.frame_graficas
            )
        self._figure_3, self._ax3 = plt.subplots()
        self._figure_3_canvas = FigureCanvasTkAgg(
            self._figure_3, master=self.frame_graficas
            )

        self.frame_graficas.grid_columnconfigure(0, weight=1, uniform="fig")
        self.frame_graficas.grid_columnconfigure(1, weight=1, uniform="fig")
        self.frame_graficas.grid_columnconfigure(2, weight=1, uniform="fig")

        self._figure_1_canvas.get_tk_widget().place(x=50, y=0, width=300, height=250)

        self._figure_2_canvas.get_tk_widget().place(x=50, y=500, width=500, height=500)

        self._figure_3_canvas.get_tk_widget().place(x=50, y=500, width=500, height=500)


        self.frame_botones = tk.Frame(self, bg="#151515")
        self.btn_iniciar = tk.Button(
            self.frame_botones, bg="#7401DF", fg="#FFBF00",
            activebackground="#8258FA", font=('Courier', 16),
            text="Iniciar", command=self.iniciar_animación
            )
        self.btn_pausar = tk.Button(
            self.frame_botones, bg="#7401DF", fg="#FFBF00",
            activebackground="#8258FA", font=('Courier', 16),
            text="  Pausa  ", command=self.pausar_animación, state=tk.DISABLED
            )
        self.btn_iniciar.pack(
            side="left", padx=(100, 100), pady=(100, 100),
            fill="y", expand=True
            )
        self.btn_pausar.pack(
            side="left", padx=(100, 100), pady=(100, 100),
            fill="y", expand=True
            )

        self._anim1 = None
        self._anim2 = None
        self._anim3 = None

        self.frame_graficas.pack(fill="both", expand=True)
        self.frame_botones.pack(fill="x")
        self._init_axes()

    def _init_axes(self):

        self._ax1.set_title('Individus')
        self._ax1.set_xlabel("Time")
        self._ax1.set_ylabel("Amplitude")
        self._ax1.set_xlim(0, 100)
        self._ax1.set_ylim(0, 100)

        self._ax2.set_title('Vitesse totale moyenne')
        self._ax2.set_xlabel("Time")
        self._ax2.set_ylabel("Amplitude")
        self._ax2.set_xlim(0, 100)
        self._ax2.set_ylim(0, 100)

        self._ax3.set_title('Energie')
        self._ax3.set_xlabel("Time")
        self._ax3.set_ylabel("Energie totale")
        self._ax3.set_xlim(0, 100)
        self._ax3.set_ylim(0, 100)


    def iniciar_animación(self):

        def animate(values):
            value=values
            data.append(value)
            lines.set_data(range(0, 100), data)
            return lines

        def animate2(values):
            value=values
            data2.append(value)
            lines2.set_data(range(0, 100), data2)
            return lines2

        def animate3(values):
            value=values
            data3.append(value)
            lines3.set_data(range(0, 100), data3)
            return lines3

        def data_gen():
            for k in range(100):
                t = k / 100
                yield 0.5 * np.sin(40 * t) * np.exp(-2 * t)

        def data_gen2():
            for k in range(100):
                t = k / 100
                yield 0.5 * np.sin(60 * t)

        def data_gen3():
            for k in range(100):
                t = k / 100
                yield 0.5 * np.cos(60 * t)

        if self._anim1 is None:
            lines = self._ax1.plot([], [], color='#80FF00')[0]
            lines2 = self._ax2.plot([], [], color='#80FF00')[0]
            lines3 = self._ax3.plot([], [], color='#80FF00')[0]

            data = collections.deque([0] * 100, maxlen=100)
            data2 = collections.deque([0] * 100, maxlen=100)
            data3 = collections.deque([0] * 100, maxlen=100)

            self._anim1 = animation.FuncAnimation(
                self._figure_1, animate, data_gen, interval=5
                )
            self._anim2 = animation.FuncAnimation(
                self._figure_2, animate2, data_gen2, interval=5
                )
            self._anim3 = animation.FuncAnimation(
                self._figure_3, animate3, data_gen3, interval=5
                )

            self._figure_1_canvas.draw()
            self._figure_2_canvas.draw()
            self._figure_3_canvas.draw()

            self.btn_pausar.configure(state=tk.NORMAL)
            self.btn_iniciar.configure(text="Detener")
        else:
            self._ax1.lines = []  
            self._ax2.lines = []
            self._ax3.lines = []
            self.btn_pausar.configure(state=tk.DISABLED, text="  Pausa  ")
            self.btn_iniciar.configure(text="Iniciar")
            self._anim1 = self._anim2 = self._anim3 = None


    def pausar_animación(self):
        if self.btn_pausar["text"] == "  Pausa  ":
            self._anim1.event_source.stop()
            self._anim2.event_source.stop()
            self._anim3.event_source.stop()
            self.btn_pausar.configure(text="Continuar")

        else:
            self._anim1.event_source.start()
            self._anim2.event_source.start()
            self._anim3.event_source.start()
            self.btn_pausar.configure(text="  Pausa  ")



if __name__ == "__main__":
    root = tk.Tk()
    Graphique(root).pack(side="top", fill="both", expand=True)
    root.mainloop()