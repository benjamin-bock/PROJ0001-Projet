
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
        elif f_x * f_a < 0:
            b = x
        else:
            a = x
            f_a = f_x  # Réutiliser f_x pour la prochaine itération

    return [(a + b) / 2.0, 0]  # statut = 0 -> convergence réussie

def secante(f, x0, x1, tol):
    
    # Vérifier les hypothèses de la méthode de la bissection
    f_x0 = f(x0)
    f_x1 = f(x1)
    if f_x0 * f_x1 >= 0.0:
        print("Erreur : f(x0) et f(x1) doivent avoir des signes opposés.")
        return [None, 1]  # statut = 1 -> hypothèses non satisfaites

    iteration = 0
    max_iter = 100000  # Nb max d'itérations pour éviter une boucle infinie
    f_x2 = 100 # On initialise un grand nombre pour ne pas sortir de la boucle
    
    while iteration < max_iter :
              
        iteration += 1 
        
        # Éviter la division par zéro
        if f_x1 - f_x0 == 0.0 :
            print("Erreur : Division par zéro")
            return [None, 1] # statut = 1 -> Processus interrompu

        # Calculer la nouvelle itérée
        x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)

        # On appelle une seule fois f
        f_x2 = f(x2)
        
        # Critère d'arrêt
        if abs(f_x2) < tol :
            print("La méthode a convergé")
            return [x2, 0]
        
        # Mise à jour des paramètres
        
        # y devient x0
        if f_x1 * f_x2 < 0.0 :
            x0 = x1
            f_x0 = f_x1
            
        # x2 devient x1
        
        x1 = x2
        f_x1 = f_x2
        

    print("Erreur : La méthode n'a pas convergé")
    return [None, -1] # statut = -1 -> non-convergence
            
            





























