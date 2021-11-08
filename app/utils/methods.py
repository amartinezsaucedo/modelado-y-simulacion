import sympy as sym
from scipy.integrate import solve_ivp
import numpy as np


def calculate(expression, t0, tf, x0, h):
    x, t = sym.symbols("x t")
    f = sym.lambdify([t, x], expression)
    t_input = np.arange(t0, tf, h)
    x_euler = euler(f, t_input, x0, h)
    x_improved_euler = improved_euler(f, t_input, x0, h)
    x_runge_kutta = runge_kutta(f, t_input, x0, h)
    exact = solve_ivp(f, [t0, np.max(t_input)],[x0], t_eval=t_input,method= "DOP853")
    return t_input, x_euler, x_improved_euler, x_runge_kutta, exact.y[0]


def calculate_h(tf, t0, n):
    return (tf - t0) / n


def euler(f, t, x0, h):
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t) - 1):
        x[k + 1] = x[k] + h * f(t[k], x[k])
    return x


def improved_euler(f, t, x0, h):
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t) - 1):
        predictor = x[k] + h * f(t[k], x[k])
        x[k + 1] = x[k] + (h / 2) * (f(t[k], x[k]) + f(t[k + 1], predictor))
    return x


def runge_kutta(f, t, x0, h):
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t) - 1):
        k1 = h * (f(t[k], x[k]))
        k2 = h * (f(t[k] + h * 0.5, x[k] + 0.5 * k1))
        k3 = h * (f(t[k] + h * 0.5, x[k] + 0.5 * k2))
        k4 = h * (f(t[k] + h, x[k] + k3))
        x[k + 1] = x[k] + (k1 + 2 * (k2 + k3) + k4) / 6.0
    return x
