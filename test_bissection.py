import numpy as np
from RechercheRacine import bissection, secante


# Définir une fonction
def f(x):
    return x**3 - x - 2

# Utiliser la méthode de bissection
resultat_bissection = bissection(f, -50, 100, 1e-15)
print("Bissection :", resultat_bissection)

# Utiliser la méthode de sécante
resultat_secante = secante(f, -50, 100, 1e-6)
print("Sécante :", resultat_secante)

