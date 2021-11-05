import sympy as sym
from scipy.integrate import odeint
import numpy as np


def calculate(expression, t0, tf, x0, h):
    x, t = sym.symbols("x t")
    f = sym.lambdify([x, t], expression)
    t_input = np.arange(t0, tf, h)
    x_euler = euler(f, t_input, x0, h)
    x_improved_euler = improved_euler(f, t_input, x0, h)
    x_runge_kutta = runge_kutta(f, t_input, x0, h)
    exact = odeint(f, x0, t_input)
    return t_input, x_euler, x_improved_euler, x_runge_kutta, exact


def calculate_h(tf, t0, n):
    return (tf - t0) / n


def euler(f, t, x0, h):
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t) - 1):
        x[k + 1] = x[k] + h * f(x[k], t[k])
    return x


def improved_euler(f, t, x0, h):
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t) - 1):
        predictor = x[k] + h * f(x[k], t[k])
        x[k + 1] = x[k] + (h / 2) * (f(x[k], t[k]) + f(predictor, t[k + 1]))
    return x


def runge_kutta(f, t, x0, h):
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t) - 1):
        k1 = h * (f(x[k], t[k]))
        k2 = h * (f(x[k] + 0.5 * k1, t[k] + h * 0.5))
        k3 = h * (f(x[k] + 0.5 * k2, t[k] + h * 0.5))
        k4 = h * (f(x[k] + k3, t[k] + h))
        x[k + 1] = x[k] + (k1 + 2 * (k2 + k3) + k4) / 6.0
    return x
