import tkinter as tk
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self,canvas_,parent_):
        self.toolitems = (
            ('Home', 'Reestablecer gráfico', 'home', 'home'),
            ('Back', 'Mostrar gráfico anterior', 'back', 'back'),
            ('Forward', 'Mostrar siguiente gráfico', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'Mover gráfico', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'Zoom en área', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'putamus parum claram', 'Configurar gráfico', 'configure_subplots'),
            ('Save', 'sollemnes in futurum', 'Guardar gráfico', 'save_figure'),
            )
        NavigationToolbar2Tk.__init__(self,canvas_,parent_)

class App:
    def __init__(self, window):
        self.window = window
        self._init_app()

    def _init_app(self):
        self.figure = mpl.figure.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure,self.window )
        self.toolbar = CustomToolbar(self.canvas,self.window )
        self.toolbar.update()
        self.plot_widget = self.canvas.get_tk_widget()
        self.plot_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.draw()

    # plot something random
    def plot(self):
        self.ax.imshow(np.random.normal(0.,1.,size=[100,100]),cmap="hot",aspect="auto")
        self.figure.canvas.draw()

def main():
    root = tk.Tk()
    app = App(root)
    app.plot()
    root.mainloop()

if __name__ == "__main__":
    main()
