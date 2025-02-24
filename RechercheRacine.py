
def bissection(f, x0, x1, tol):
    
    # Vérifier les hypothèses de la méthode de la bissection
    f_x0 = f(x0)
    f_x1 = f(x1)
    if f_x0 * f_x1 >= 0.0:
        print("Erreur : f(x0) et f(x1) doivent avoir des signes opposés.")
        return [None, 1]  # statut = 1 -> hypothèses non satisfaites

    a, b = x0, x1
    f_a = f_x0
    iteration = 0
    max_iter = 1000000  # Nb max d'itérations pour éviter une boucle infinie

    while abs((b - a) / 2.0) >= tol:
        
        # Éviter une boucle infinie
        iteration += 1
        if iteration > max_iter:
            print("Erreur : La méthode de bissection n'a pas convergé.")
            return [None, -1]  # statut = -1 -> non-convergence

        x = (a + b) / 2.0  # Milieu d'intervalle
        f_x = f(x)  # Évaluer f(x) une seule fois

        if f_x == 0.0:  # Solution exacte trouvée
            return [x, 0]

        # Mettre à jour l'intervalle
        if f_x * f_a < 0:
            b = x
        else:
            a = x
            f_a = f_x  # Réutiliser f_x pour la prochaine itération

    return [(a + b) / 2.0, 0]  # statut = 0 -> convergence réussie
