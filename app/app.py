from tkinter import BOTH, TOP
from tkinter.ttk import Frame, Label, Entry, Button
from ttkbootstrap import Style
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from utils.methods import calculate, calculate_h

mpl.use("TkAgg")


class CustomToolbar(NavigationToolbar2Tk):
    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ("Home", "Reestablecer gráfico", "home", "home"),
            (None, None, None, None),
            ("Pan", "Mover gráfico", "move", "pan"),
            (None, None, None, None),
            ("Zoom", "Zoom en área", "zoom_to_rect", "zoom"),
            (None, None, None, None),
            ("Subplots", "Configurar gráfico", "subplots", "configure_subplots"),
            (None, None, None, None),
            ("Save", "Guardar gráfico", "filesave", "save_figure"),
        )
        NavigationToolbar2Tk.__init__(self, canvas_, parent_, pack_toolbar=False)


class App:
    def __init__(self, window):
        self.window = window
        self.place_ui_components()
        self.draw_graph()

    def place_ui_components(self):
        self.window.title("Modelado y Simulación - TPO")
        self.frame = Frame(self.window)
        self.frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
        self.frame.columnconfigure(2, weight=1)
        Label(
            self.frame,
            text="Modelado y Simulación - TPO",
            font=("Helvetica", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2)
        Label(self.frame, text="f(x,t)", style="primary.TLabel").grid(
            row=1, column=0, sticky="nsew"
        )
        self.function_input = Entry(self.frame, width=50)
        self.function_input.grid(pady=2, row=1, column=1)
        Label(self.frame, text="t0", style="primary.TLabel").grid(row=2, column=0)
        self.t0_input = Entry(self.frame, width=50)
        self.t0_input.grid(pady=2, row=2, column=1)
        Label(self.frame, text="x0", style="primary.TLabel").grid(
            row=3, column=0, sticky="nsew"
        )
        self.x0_input = Entry(self.frame, width=50)
        self.x0_input.grid(pady=3, row=3, column=1)
        Label(self.frame, text="tf", style="primary.TLabel").grid(
            row=4, column=0, sticky="nsew"
        )
        self.tf_input = Entry(self.frame, width=50)
        self.tf_input.grid(pady=2, row=4, column=1)
        Label(self.frame, text="N", style="primary.TLabel").grid(
            row=5, column=0, sticky="nsew"
        )
        self.n_input = Entry(self.frame, width=50)
        self.n_input.grid(pady=2, row=5, column=1)
        Button(self.frame, text="Calcular", command=self.calculate, width=50).grid(
            pady=2, padx=5, row=6, column=0, columnspan=2
        )

    def calculate(self):
        f = self.function_input.get()
        t0 = float(self.t0_input.get())
        x0 = float(self.x0_input.get())
        tf = float(self.tf_input.get())
        n = float(self.n_input.get())
        h = calculate_h(tf, t0, n)
        t, x_euler, x_improved_euler, x_runge_kutta, exact = calculate(f, t0, tf, x0, h)
        self.plot(t, x_euler, x_improved_euler, x_runge_kutta, exact)
        self.reset_buttons()

    def draw_graph(self):
        graph_frame = Frame(self.frame)
        graph_frame.grid(row=1, column=2, rowspan=6)
        graph_frame.rowconfigure(2, weight=1)
        self.figure = mpl.figure.Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, graph_frame)
        self.toolbar = CustomToolbar(self.canvas, graph_frame)
        self.toolbar._message_label.config(font=("Helvetica", 16), fg="#5a5a5a")
        for button in self.toolbar.winfo_children():
            button.config(background="white")
        self.toolbar.update()
        self.euler_button = Button(
            graph_frame,
            style="secondary.TButton",
            text="Euler",
            command=lambda: self.change_line_status("euler"),
            width=10,
        )
        self.euler_button.grid(pady=5, padx=5, row=1, column=0, sticky="nsew")
        self.improved_euler_button = Button(
            graph_frame,
            style="info.TButton",
            text="Euler mejorado",
            command=lambda: self.change_line_status("improved_euler"),
            width=10,
        )
        self.improved_euler_button.grid(pady=5, padx=5, row=1, column=1, sticky="nsew")
        self.runge_kutta_button = Button(
            graph_frame,
            text="Runge Kutta",
            style="danger.TButton",
            command=lambda: self.change_line_status("runge_kutta"),
            width=10,
        )
        self.runge_kutta_button.grid(pady=5, padx=5, row=1, column=2, sticky="nsew")
        self.exact_button = Button(
            graph_frame,
            text="Exacta",
            style="success.TButton",
            command=lambda: self.change_line_status("exact"),
            width=10,
        )
        self.exact_button.grid(pady=5, padx=5, row=1, column=3, sticky="nsew")
        self.plot_widget = self.canvas.get_tk_widget().grid(
            row=2, column=0, sticky="nsew", columnspan=4
        )
        self.toolbar.grid(row=0, column=0, sticky="nsew", columnspan=4)
        self.configure_plot()
        self.canvas.draw()

    def change_line_status(self, method):
        line = getattr(self, method + "_line", None)
        button = getattr(self, method + "_button", None)
        if line:
            linestyle = line[0]._linestyle
            button_style = button.cget("style")
            if linestyle != "None":
                line[0]._linestyle = "None"
                index = button_style.find(".")
                style = button_style[:index] + ".Outline" + button_style[index:]
                button.configure(style=style)
            else:
                style = (
                    button_style[: button_style.find(".")]
                    + button_style[button_style.rfind(".") :]
                )
                button.configure(style=style)
                line[0]._linestyle = "--" if not method == "exacta" else "-"
        self.figure.canvas.draw()

    def reset_buttons(self):
        self.euler_button.configure(style="secondary.TButton")
        self.improved_euler_button.configure(style="info.TButton")
        self.runge_kutta_button.configure(style="danger.TButton")
        self.exact_button.configure(style="success.TButton")

    def configure_plot(self):
        self.ax.grid(alpha=0.01)
        self.ax.set_xlabel("t")
        self.ax.set_ylabel("f(x, t)")
        self.ax.xaxis.label.set_color("#5a5a5a")
        self.ax.yaxis.label.set_color("#5a5a5a")
        [t.set_color("#5a5a5a") for t in self.ax.xaxis.get_ticklines()]
        [t.set_color("#5a5a5a") for t in self.ax.xaxis.get_ticklabels()]
        [t.set_color("#5a5a5a") for t in self.ax.yaxis.get_ticklines()]
        [t.set_color("#5a5a5a") for t in self.ax.yaxis.get_ticklabels()]

    def plot(self, t, x_euler, x_improved_euler, x_runge_kutta, exact):
        self.ax.clear()
        self.configure_plot()
        self.euler_line = self.ax.plot(
            t, x_euler, color="#f3969a", linestyle="--", label="Euler (O(h))"
        )
        self.improved_euler_line = self.ax.plot(
            t,
            x_improved_euler,
            "#6cc3d5",
            linestyle="--",
            label="Euler mejorado (O(h^2))",
        )
        self.runge_kutta_line = self.ax.plot(
            t, x_runge_kutta, "#ff7851", linestyle="--", label="Runge-Kutta (O(h^4))"
        )
        self.exact_line = self.ax.plot(t, exact, "#56cc9d", label="Exacta")
        self.ax.legend(loc="best")
        self.figure.canvas.draw()


def main():
    style = Style(theme="minty")
    style.configure("TLabel", font=("Helvetica", 12))
    plt.rc("font", size=10)
    plt.style.use("seaborn")
    root = style.master
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
