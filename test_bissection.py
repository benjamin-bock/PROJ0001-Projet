# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:09:09 2025

@author: b3nja
"""
import numpy as np
from RechercheRacine import bissection


# Définir une fonction
def f(x):
    return x**5 -x**4 + 4*x**3 -18*x**2 +(np.pi)*x - 15*(np.log(3*x))

# Utiliser la méthode de bissection
resultat_bissection = bissection(f, 100, 1, 1e-15)
print("Bissection :", resultat_bissection)

