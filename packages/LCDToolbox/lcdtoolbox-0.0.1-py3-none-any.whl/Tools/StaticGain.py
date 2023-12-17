import sympy as sym
from sympy import Symbol, symbols

def calculate_static_loop_gain(G_ol, laplace_variable=Symbol('s')):
    G = G_ol
    K0 = G.subs(laplace_variable, 0)

    while sym.zoo in K0.atoms():
        G *= laplace_variable
        K0 = G.subs(laplace_variable, 0)
    
    return K0

