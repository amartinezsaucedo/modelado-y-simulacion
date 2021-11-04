import sympy as sym
from scipy.integrate import odeint
import numpy as np


def calculate(expression, x0, h ,method):
    x, t = sym.symbols('x t')
    f = sym.lambdify([x, t], expression) 
    if method == "euler":
        x, t = euler(f, x0, h)
    y_true = odeint(f, x0, t)
    return f, x, t, y_true

def calculate_h(tf, t0, n):
    return (tf - t0) / n

def euler(f,x0, h):
    t = np.arange(0, 1 + h, h)  
    x = np.zeros(len(t))
    x[0] = x0
    for k in range(0, len(t)- 1):
        x[k + 1] = x[k] + h*f(x[k] ,t[k])
    return x, t