import tkinter as tk
from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.constants import BOTTOM, CENTER, RIGHT
from tkinter.ttk import Frame, Label, Entry, Button
from ttkbootstrap import Style
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from utils.methods import calculate, calculate_h

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self,canvas_,parent_):
        '''self.toolitems = (
            ('Home', 'Reestablecer gráfico', 'home', 'home'),
            ('Back', 'Mostrar gráfico anterior', 'back', 'back'),
            ('Forward', 'Mostrar siguiente gráfico', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Mover gráfico', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'Zoom en área', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'putamus parum claram', 'Configurar gráfico', 'configure_subplots'),
            ('Save', 'sollemnes in futurum', 'Guardar gráfico', 'save_figure'),
            )'''
        NavigationToolbar2Tk.__init__(self,canvas_,parent_, pack_toolbar=False)

class App:
    def __init__(self, window):
        self.window = window
        self.place_ui_components()
        self.draw_graph()
     

    def place_ui_components(self):
        self.window.title("Modelado y Simulación - TPO")
        self.frame = Frame(self.window)
        self.frame.pack(fill= BOTH, expand= True, padx= 20, pady=20)
        self.frame.columnconfigure(2, weight=1)
        Label(self.frame, text="Modelado y Simulación - TPO", font=('Helvetica', 16, 'bold')).grid(row=0, column=0, columnspan=2)
        Label(self.frame, text="f(x,t)",style="primary.TLabel").grid(row=1, column=0 ,sticky="nsew")
        self.function_input = Entry(self.frame, width=50)
        self.function_input.grid(pady=2, row=1, column=1)
        Label(self.frame, text="t0",style="primary.TLabel").grid( row=2, column=0)
        self.t0_input = Entry(self.frame, width=50)
        self.t0_input.grid(pady=2, row=2, column=1)
        Label(self.frame, text="x0",style="primary.TLabel").grid( row=3, column=0, sticky="nsew")
        self.x0_input = Entry(self.frame, width=50)
        self.x0_input.grid(pady=3, row=3, column=1)
        Label(self.frame, text="tf",style="primary.TLabel").grid( row=4, column=0, sticky="nsew")
        self.tf_input = Entry(self.frame, width=50)
        self.tf_input.grid(pady=2, row=4, column=1)
        Label(self.frame, text="h",style="primary.TLabel").grid( row=5, column=0, sticky="nsew")
        self.h_input = Entry(self.frame, width=50)
        self.h_input.grid(pady=2, row=5, column=1)
        Label(self.frame, text="N",style="primary.TLabel").grid( row=6, column=0, sticky="nsew")
        self.n_input = Entry(self.frame, width=50)
        self.n_input.grid(pady=2, row=6, column=1)
        Button(self.frame, text="Calcular", command=self.calculate, width=50).grid(pady=2, padx=5, row=7, column=0, columnspan=2)
        
    def calculate(self):
        f = self.function_input.get()
        t0 = float(self.t0_input.get())
        x0 = float(self.x0_input.get())
        tf = float(self.tf_input.get())
        n = float(self.n_input.get())
        h = self.h_input.get()
        if not h:
            h = calculate_h(tf, t0, n)
        else:
            h = float(h)
        f, x, t, y_true = calculate(f, x0, h , "euler")
        self.plot(t, x, y_true)

    def draw_graph(self):
        graph_frame = Frame(self.frame)
        graph_frame.grid(row=1, column=2, rowspan=7)
        graph_frame.columnconfigure(0, weight=1)
        self.figure = mpl.figure.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure,graph_frame )
        self.toolbar = CustomToolbar(self.canvas,graph_frame)
        self.toolbar.update()
        self.plot_widget = self.canvas.get_tk_widget().grid(row=1,column=0, sticky="nsew")
        self.toolbar.grid(row=0, column=0)
        self.canvas.draw()

    # plot something random
    def plot(self, t, x, y_true):
        self.ax.clear()
        self.ax.plot(t, x, 'bo--', label='Approximate')
        self.ax.plot(t, y_true, 'g', label='Exact')
        '''self.ax.plot(t, f(t ), 'g', label='Exact')
        self.ax.title('Approximate and Exact Solution for Simple ODE')
        self.ax.xlabel('t')
        self.ax.ylabel('f(t)')
        self.ax.grid()
        self.ax.legend(loc='lower right')
        self.ax.show()'''
        self.figure.canvas.draw()

def main():
    style = Style(theme="minty")
    style.configure('TLabel', font=('Helvetica', 12))
    root = style.master
    App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
