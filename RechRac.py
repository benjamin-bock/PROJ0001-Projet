# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 11:23:23 2025

@author: b3nja
"""

def bissection2(f, x0, x1, tol):
    """
    Recherche la racine de la fonction f dans l'intervalle [x0, x1] en utilisant la méthode de la bissection.

    :param f: La fonction pour laquelle on cherche la racine.
    :param x0: Borne inférieure de l'intervalle initial.
    :param x1: Borne supérieure de l'intervalle initial.
    :param tol: Tolérance pour la convergence.
    :return: Une liste [x, statut], où x est la racine approximative et statut est un code de statut.
             statut = 0 si la méthode a convergé, 1 si les hypothèses ne sont pas satisfaites, -1 si la méthode ne converge pas.
    """
    # Vérifier les hypothèses de la méthode de bissection
    f_x0 = f(x0)
    f_x1 = f(x1)
    if f_x0 * f_x1 >= 0:
        print("Erreur : f(x0) et f(x1) doivent avoir des signes opposés.")
        return [None, 1]  # Statut 1 : hypothèses non satisfaites

    a, b = x0, x1
    f_a = f_x0
    iteration = 0
    max_iter = 1000  # Nombre maximal d'itérations pour éviter une boucle infinie

    while abs((b - a) / 2.0) > tol:
        iteration += 1
        if iteration > max_iter:
            print("Erreur : La méthode de bissection n'a pas convergé.")
            return [None, -1]  # Statut -1 : non-convergence

        c = (a + b) / 2.0  # Point milieu
        f_c = f(c)  # Évaluer f(c) une seule fois

        if f_c == 0.0:  # Solution exacte trouvée
            return [c, 0]

        # Mettre à jour l'intervalle
        if f_c * f_a < 0:
            b = c
        else:
            a = c
            f_a = f_c  # Réutiliser f_c pour la prochaine itération

    return [(a + b) / 2.0, 0]  # Statut 0 : convergence réussie